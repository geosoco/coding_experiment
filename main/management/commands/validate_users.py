from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from main.models import *
import simplejson as json
import codecs
from boto.mturk.connection import MTurkConnection
from boto.mturk.price import Price
import pprint
import readline

class Command(BaseCommand):
    help = "validate users' answers"

    def add_arguments(self, parser):
        pass

    def make_dict_of_answers(self):
        answers = self.query_answers()
        
        ans_dict = {}


        for a in answers:
            cnd = a.condition.id
            tweet = a.tweet.id
            code = a.code.id if a.code is not None else None

            if cnd not in ans_dict:
                ans_dict[cnd] = {} 

            if tweet not in ans_dict[cnd]:
                ans_dict[cnd][tweet] = set()

            if code is not None:
                ans_dict[cnd][tweet].add(code)

        # set it on our class
        self.answers = ans_dict

    def query_attention_checks(self):
        return Tweet.objects.filter(attention_check=True)

    def query_answers(self):
        return Answer.objects.all()


    def fold_codes(self, codes):
        ret = {}

        for code in codes:
            if code.deleted == True:
                continue

            tweet_id = code.tweet_id

            if tweet_id not in ret:
                ret[tweet_id] = set()

            ret[tweet_id].add(code.code_id)

        return ret



    def build_user_details(self):
        self.users = {}
        users = self.query_users()

        for user in users:
            #pprint.pprint(user)
            #pprint.pprint(user.__dict__)
            uid = user.user.id
            completion_code = user.completion_code

            assignment = Assignment.objects.get(user_id=uid)
            codes = CodeInstance.objects.filter(assignment=assignment)

            prepared_instances = self.fold_codes(codes)

            u = { 
                "turkuser": user,
                "assignment": assignment,
                "instances": prepared_instances
            }

            # add our user to the dictionary
            self.users[completion_code] = u

        
    def get_user_statistics(self):
        for comp_code, u in self.users.iteritems():
            cnd = u["assignment"].condition_id
            cnd_answers = self.answers[cnd]

            # lazy count of the number of datasets
            min_tweet_id = min(u["instances"].keys())
            max_tweet_id = max(u["instances"].keys())
            tweet_diff = max_tweet_id - min_tweet_id
            
            datasets = 1
            if tweet_diff > 45:
                datasets = 2

            u["datasets"] = datasets 
           
            # calculate attention checks
            misses = {}
            hits = {}
            cnt_correct_attention_checks = 0
            for tweet_id, codes in cnd_answers.iteritems():
                if tweet_id not in u["instances"]:
                    if len(codes) == 0:
                        hits[tweet_id] = codes
                        cnt_correct_attention_checks += 1
                    else:
                        misses[tweet_id] = {
                            "expected": codes,
                            "user_codes": set()
                        }
                else:
                    if u["instances"][tweet_id] == codes:
                        cnt_correct_attention_checks += 1
                        hits[tweet_id] = codes
                    else:
                        misses[tweet_id] = {
                            "expected": codes,
                            "user_codes": u["instances"][tweet_id]
                        }

            u["cnt_correct_attention"] = cnt_correct_attention_checks
            u["hits"] = hits
            u["misses"] = misses


    def query_users(self):
        return TurkUser.objects.filter(finish_time__isnull=False)


    def get_all_reviewable_hits(self,mtc):
        page_size = 50
        hits = mtc.get_reviewable_hits(page_size=page_size)
        print "Total results to fetch %s " % hits.TotalNumResults
        print "Request hits page %i" % 1
        total_pages = float(hits.TotalNumResults)/page_size
        int_total= int(total_pages)
        if(total_pages - int_total > 0):
            total_pages = int_total + 1
        else:
            total_pages = int_total
        pn = 1
        while pn < total_pages:
            pn = pn + 1
            print "Request hits page %i" % pn
            temp_hits = mtc.get_reviewable_hits(
                page_size=page_size,
                page_number=pn)
            hits.extend(temp_hits)
        return hits


    def handle(self, *args, **options):
        """handle the command."""

        print "querying local database..."
        self.make_dict_of_answers()
        pprint.pprint(self.answers)

        self.build_user_details()
        self.get_user_statistics()

        print "getting reviewable hits"
        mtc = MTurkConnection(debug=1)
        hits = self.get_all_reviewable_hits(mtc)

        for hit in hits:
            print "getting assignments for hit (", hit.HITId, ")"
            assignments = mtc.get_assignments(hit.HITId, status="Submitted")
#            if len(assignments) == 0:
#                mtc.
            for assignment in assignments:
                print "\n##################\n"
                print assignment.__dict__
                pprint.pprint(assignment)
                worker_id = assignment.WorkerId
                assign_id = assignment.AssignmentId
                survey_code = assignment.answers[0][0].fields[0]
                assignment_status = assignment.AssignmentStatus


                # fix survey code
                survey_code = survey_code.strip()

                print "worker:", worker_id
                print "assignment:", assign_id

                if survey_code not in self.users:
                    print "!"*20
                    print "invalid survey code",survey_code 
                    print "!"*20

                u = self.users[survey_code]    
                turkuser = u["turkuser"]            
                u_id = turkuser.user_id            
               
                # add turker id
                if turkuser.turker_id is None: 
                    turkuser.turker_id = worker_id                
                    turkuser.save()
 
                ic = InstructionCheck.objects.get(user_id=u_id)
                print survey_code, u["datasets"], u["cnt_correct_attention"]
                if len(u["misses"]) > 0:
                    print "MISSES: "
                    for tid, miss in u["misses"].iteritems():
                        print "%s| expected: %s, got: %s"%(
                            tid,
                            repr(miss["expected"]),
                            repr(miss["user_codes"]))
                            
                print "description: ", ic.rumor_description
                print "which codes: ", ic.which_codes 
                print ""
                handle = raw_input("approve? (y/n)")
                handle = handle.lower()

                if handle == 'y':
                    if assignment_status == "Rejected":
                        mtc.approve_rejected_assignment(assign_id)
                    else:
                        mtc.approve_assignment(assign_id)
                    if u["datasets"] == 2:
                        print "++ bonus"
                        mtc.grant_bonus(
                            worker_id,
                            assign_id,
                            Price(amount=3.00),
                            "completed bonus set. Congratulations!")
                    else:
                        print "++"
                elif handle == 'n':
                    print "--"
                    reason = raw_input("reason?")
                    mtc.reject_assignment(assign_id, reason)


 

             
         

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
    help = "get user results"

    def add_arguments(self, parser):
        parser.add_argument('completion_code', help="completion code of the user")

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


    def handle(self, *args, **options):
        """handle the command."""
        completion_code = options.get("completion_code")


        print "querying local database..."
        self.make_dict_of_answers()
        pprint.pprint(self.answers)

        self.build_user_details()
        self.get_user_statistics()
        
        print "\n##################\n"

        # fix survey code
        completion_code = completion_code.strip()

        if completion_code not in self.users:
            print "!"*20
            print "invalid survey code",completion_code
            print "!"*20

        u = self.users[completion_code]    
        turkuser = u["turkuser"]            
        u_id = turkuser.user_id            
       
        ic = InstructionCheck.objects.get(user_id=u_id)
        print completion_code, u["datasets"], u["cnt_correct_attention"]
        if len(u["misses"]) > 0:
            print "MISSES: "
            for tid, miss in u["misses"].iteritems():
                print "%s| expected: %s, got: %s"%(
                    tid,
                    repr(miss["expected"]),
                    repr(miss["user_codes"]))
                    
        print "description: ", ic.rumor_description
        print "which codes: ", ic.which_codes 
     
 

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from main.models import *
import simplejson as json
import sys

from pprint import pprint

class Command(BaseCommand):
    help = "import a series of oembed tweets from a json file"

    def add_arguments(self, parser):
        parser.add_argument('condition')        
        parser.add_argument('dataset')
        parser.add_argument('--condition')
        parser.add_argument('--codescheme', action="append")


    def create_code_scheme_dict(self, code_schemes):
        cs_dict = {}

        for scheme_id in code_schemes:

            try:
                cs = CodeScheme.objects.get(name=scheme_id)
            except ObjectDoesNotExist:
                cs = CodeScheme.objects.get(pk=scheme_id)


            codes = Code.objects.filter(scheme=cs)
            for code in codes:

                # check for duplicates
                if code.name in cs_dict:
                    raise CommandError("Found multiple codes with the same name (ids: %d,%d)"%(cs_dict[code.name]["id"], code.id))

                # add to dict
                cs_dict[code.name] = code

        return cs_dict


    def handle(self, *args, **options):

        # lookup the condition
        condition = None
        condition_name = options.get('condition', None)
        if condition_name:
            #print "getting condition: %s"%(condition_name)
            condition = Condition.objects.get(name=condition_name)
            #print condition.id

        # lookup the dataset
        dataset_name = options.get('dataset', None)
        try:
            dataset = condition.dataset.get(name=dataset_name)
        except ObjectDoesNotExist,e:
            print >> sys.stderr,  "Couldn't find dataset: ", dataset_name
            raise 
        except Exception,e:
            print >> sys.stderr, "Couldn't find dataset: ", dataset_name
            raise 

        # lookup codes
        code_dict = {}
        opt_codeschemes = options['codescheme']
        if len(opt_codeschemes) > 0:
            code_dict.update(self.create_code_scheme_dict(opt_codeschemes))

        export_code_ids = [c.id for c in code_dict.values()]
        #print repr(code_dict)
        #print export_code_ids


        # grab assignments
        assignments = Assignment.objects.filter(condition=condition, user__turkuser__finish_time__isnull=False, user__turkuser__exclude=False)
        #print "got %d assignments for this condition"%(assignments.count())

        assignment_user_dict = {a.id: a.user_id for a in assignments}
        assignment_ids = sorted(assignment_user_dict.keys())
        #print "assignment ids: ", repr(assignment_ids)
        codeinstances = CodeInstance.objects.filter(assignment__in=assignment_ids, deleted=False, code__in=export_code_ids).order_by('date')


        inst_dict = {a:{} for a in assignment_ids}

        for ci in codeinstances:
            as_id = ci.assignment_id
            c_id = ci.code_id
            t_id = ci.tweet_id

            #print as_id, t_id, c_id
            inst_dict[as_id][t_id] = c_id

            #pprint(inst_dict)


        tweets = Tweet.objects.filter(dataset=dataset).order_by('id')
        tw_ids = sorted([t.id for t in tweets])

        #print "inst_dict: ", repr(inst_dict)

        for a in assignment_ids:
            code_list = []
            tweet_code_dict = inst_dict[a]

            #print "assignment: ", a
            #print repr(tweet_code_dict)

            # step through tweets
            for tid in tw_ids:
                code_list.append(str(tweet_code_dict.get(tid, 0)))

            print "%d,%s"%(a, ",".join(code_list))







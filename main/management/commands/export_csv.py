from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from main.models import *
import simplejson as json
import codecs


class Command(BaseCommand):
    help = "export codes to a csv"

    def add_arguments(self, parser):
        parser.add_argument('condition')
        parser.add_argument('dataset')
        parser.add_argument('rumor')
        parser.add_argument('filename')
        parser.add_argument('--codescheme', action="append")
        parser.add_argument(
            '--only_finished',
            action="store_true",
            default=False)


    def get_code_schemes_from_names_or_ids(self, code_scheme_ids):
        """get code scheme objects from ids or names."""
        code_schemes = []

        for scheme_id in code_scheme_ids:
            try:
                cs = CodeScheme.objects.get(name=scheme_id)
            except ObjectDoesNotExist:
                cs = CodeScheme.objects.get(pk=scheme_id)

            if cs is not None:
                code_schemes.append(cs)

        return code_schemes            

    def create_code_scheme_dict(self, code_schemes):
        """create a dictionary of codes and names. """
        cs_dict = {}

        for cs in code_schemes:

            # find codes within the scheme
            codes = Code.objects.filter(scheme=cs)
            for code in codes:

                # check for duplicates
                if code.name in cs_dict:
                    raise CommandError(
                        "Found multiple codes with the same name (ids: %d,%d)"
                        % (cs_dict[code.name]["id"], code.id))

                # add to dict
                cs_dict[code.name] = code

        return cs_dict


    def handle(self, *args, **options):
        """handle the command."""

        # get rumor
        rumor = options.get('rumor')

        # lookup the condition
        condition = None
        condition_name = options.get('condition', None)
        if condition_name:
            print "getting condition: %s" % (condition_name)
            condition = Condition.objects.get(name=condition_name)
            print condition.id

        # lookup the dataset
        dataset_name = options.get('dataset', None)
        dataset = condition.dataset.get(name=dataset_name)


        # lookup codes
        code_dict = {}
        opt_codeschemes = options['codescheme']
        code_schemes = None
        if opt_codeschemes is not None and len(opt_codeschemes) > 0:
            code_schemes = self.get_code_schemes_from_names_or_ids(
                opt_codeschemes)
        else:
            code_schemes = [cs.id for cs in condition.code_schemes.all()]

        if code_schemes is None:
            raise CommandError("No code schemes found.")

        code_dict.update(self.create_code_scheme_dict(code_schemes))

        export_code_names = code_dict.keys()
        export_code_ids = [code_dict[c].id for c in export_code_names]

        print repr(code_dict)
        print export_code_ids
        print export_code_names

        # grab assignments
        assignments = None
        if options['only_finished'] is True:
            assignments = Assignment.objects.filter(
                condition=condition,
                user__turkuser__finish_time__isnull=False)
        else:
            assignments = Assignment.objects.filter(
                condition=condition)

        print "got %d assignments for this condition" % (assignments.count())

        assignment_user_dict = {a.id: a.user_id for a in assignments}
        assignment_ids = sorted(assignment_user_dict.keys())
        print "assignment ids: ", repr(assignment_ids)

        codeinstances = CodeInstance.objects.filter(
            assignment__in=assignment_ids,
            deleted=False,
            code__in=export_code_ids).order_by('date')

        # prepare our initial code instance dictionary
        inst_dict = {a: {} for a in assignment_ids}

        for ci in codeinstances:
            as_id = ci.assignment_id
            c_id = ci.code_id
            t_id = ci.tweet_id

            # print as_id, t_id, c_id
            if t_id not in inst_dict[as_id]:
                inst_dict[as_id][t_id] = set()
            inst_dict[as_id][t_id].add(c_id)

            # pprint(inst_dict)

        # find relevant tweet ids
        tweets = Tweet.objects.filter(dataset=dataset).order_by('id')
        tw_ids = sorted([t.id for t in tweets])
        tweet_map = {tweet.id: tweet for tweet in tweets}

        # print "inst_dict: ", repr(inst_dict)

        filename = options.get('filename')
        with codecs.open(filename, 'wb', encoding="utf-8") as f:

            f.write("db_id,rumor,text,%s\n" % (",".join(export_code_names)))
            for a in assignment_ids:
                code_list = []
                tweet_code_dict = inst_dict[a]

                # print "assignment: ", a
                # print repr(tweet_code_dict)
                

                # step through tweets
                for tid in tw_ids:
                    inst_set = tweet_code_dict.get(tid)
                    instances = []
                    if inst_set is not None:
                        for code in export_code_ids:
                            instances.append('x' if code in inst_set else '')
                    else:
                        instances = ['' for _ in export_code_ids]


                    row_text = "%s,%s,\"%s\",%s\n" % (
                        tweet_map[tid].tweet_id,
                        rumor,
                        tweet_map[tid].text.replace("\"", "\\\""),
                        ','.join(instances))
                    f.write(row_text)
                    #code_list.append(str(tweet_code_dict.get(tid, 0)))

                #print "%d,%s" % (a, ",".join(code_list))



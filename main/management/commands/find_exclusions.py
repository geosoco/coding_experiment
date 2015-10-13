from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from main.models import *
import simplejson as json
import sys
from datetime import datetime

from pprint import pprint



class TweetContainer(object):
    """ Tweet wrapper class. """

    def __init__(self, id, instance=None):
        self.id = id
        self.codes = {} 
        self.all_instances = []
        self.deleted_instances = []
        self.instances = []
        self.min_time = None
        self.max_time = None

        if instance is not None:
            self.append(instance)

    def total_instance_count(self):
        return len(self.all_instances)


    def append(self, instance):
        """ appends a code instance to the object. """
        code_id = instance.code_id
        if not instance.deleted:
            if code_id not in self.codes:
                self.codes[code_id] = [instance]
            else:
                self.codes[code_id].append(instance)

        # add to deleted list if necessary
        if instance.deleted:
            self.deleted_instances.append(instance)
        else:
            self.instances.append(instance)

        # check datetimes
        inst_date = instance.date

        if self.min_time is None:
            self.min_time = inst_date
        else:
            self.min_time = min(self.min_time, inst_date)

        if self.max_time is None:
            self.max_time = inst_date
        else:
            self.max_time = max(self.max_time, inst_date)


class AssignmentContainer(object):
    """ test  """

    def __init__(self, obj):
        self.obj = obj
        self.tweets = {}

    @property
    def cnd_id(self):
        """ """
        return self.obj.condition_id

    @property
    def cnd_name(self):
        """ """
        return self.obj.condition_name

    @property
    def user_id(self):
        """ return user's id """
        return self.obj.user_id

    @property
    def id(self):
        """ return id """
        return self.obj.id

    @property
    def total_task_time(self):
        turk_user = self.obj.user.turk_user
        return turk_user.start_time - turk_user.finish_time

    def add_code_instance(self, inst):
        tweet_id = inst.tweet_id

        if tweet_id not in self.tweets:
            self.tweets[tweet_id] = TweetContainer(tweet_id, inst)
        else:
            self.tweets[tweet_id].append(inst)



# ======================================
#
# Command
#
# ======================================

class Command(BaseCommand):
    help = "import a series of oembed tweets from a json file"

    def add_arguments(self, parser):
        #parser.add_argument('condition')
        #parser.add_argument('dataset')
        #parser.add_argument('--condition')
        #parser.add_argument('--codescheme', action="append")
        pass

    def find_exclusive_violations2(self, assignments):
        
        for a_id, k in assignments.iteritems():
            a = k.obj
            tweets = k.tweets

            for tweet_id, t in tweets.iteritems():
                tweet_codes = set(t.codes.keys()) & set([1,2,3])

                if len(tweet_codes) > 1:
                    codes = [str(c) for c in tweet_codes]
                    print "%s (uid %s) on tweet %s: %s"%(
                        a.id,
                        a.user_id,
                        tweet_id,
                        ",".join(codes))

            

    def find_time_exclusions(self, assignments):
        pass


    def handle(self, *args, **options):
        

        assignments = Assignment.objects.filter(user__turkuser__finish_time__isnull=False)

        assignment_user_dict = {a.id: AssignmentContainer(a) for a in assignments}

        for id, a in assignment_user_dict.iteritems():
            instances = CodeInstance.objects.filter(assignment=a.obj)
            for i in instances:
                a.add_code_instance(i)
        
        self.find_exclusive_violations2(assignment_user_dict)

        return


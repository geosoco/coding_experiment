from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template.context_processors import csrf
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound,  HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.views.generic.edit import CreateView
#from django.template.context_processors import csrf
from models import *
import string
import random
import datetime
import time
from forms import *
from pprint import pprint




# 
# conditions
# 	1 - All Codes
#	2 - First Level only
#	3 - Second level only
#	4 - (later: uncertainty yes/no)


#
# map of the conditions
#
# current_page : page # : condition : { page: template_name, next: link for next page }
#

condition_map = {
	"instructions" : { 
		"1" : {
			"1": { "page": "instructions/instructions1-1.html", "next": "/instructions/2/" },
			"2": { "page": "instructions/instructions1-1.html", "next": "/instructions/2/" },
			"3": { "page": "instructions/instructions1-1.html", "next": "/instructions/2/" },
		},
		"2" : {
			"1": { "page": "instructions/instructions2-1.html", "next": "/instructions/3/" },
			"2": { "page": "instructions/instructions2-1.html", "next": "/instructions/3/" },
			"3": { "page": "instructions/instructions2-1.html", "next": "/instructions/3/" },
		},
		"3" : {
			"1": { "page": "instructions/instructions3-1.html", "next": "/instructions/4/" },
			"2": { "page": "instructions/instructions3-2.html", "next": "/instructions/4/" },
			"3": { "page": "instructions/instructions3-3.html", "next": "/instructions/4/" },
		},
		"4" : {
			"1": { "page": "instructions/instructions4-1.html", "next": "/instructioncheck/" },
			"2": { "page": "instructions/instructions4-2.html", "next": "/instructioncheck/" },
			"3": { "page": "instructions/instructions4-3.html", "next": "/instructioncheck/" },
		}
	}, 
	"pre_survey": {
		"1": { "next": "/instructions/1/" },
		"2": { "next": "/instructions/1/" },
		"3": { "next": "/instructions/1/" },
	},
	"post_survey": {
		"1": { "next": "/thanks/" },
		"2": { "next": "/thanks/" },
		"3": { "next": "/thanks/" },
	},
	"validate": {
		"0" : {
			"1": { "positive_redirect": "/pause/", "negative_redirect": "/survey/post/" },
			"2": { "positive_redirect": "/pause/", "negative_redirect": "/survey/post/" },
			"3": { "positive_redirect": "/pause/", "negative_redirect": "/survey/post/" },
		}
	},
	"coding" : {
		"0": {
			"1": { "page": "coding.html", "next": "/validate/0/", "help": "instructions/summary1.html" },
			"2": { "page": "coding.html", "next": "/validate/0/", "help": "instructions/summary2.html" },
			"3": { "page": "coding.html", "next": "/validate/0/", "help": "instructions/summary3.html" },	
		},
		"1": {
			"1": { "page": "coding.html", "next": "/survey/post/", "help": "instructions/summary1.html" },
			"2": { "page": "coding.html", "next": "/survey/post/", "help": "instructions/summary2.html" },
			"3": { "page": "coding.html", "next": "/survey/post/", "help": "instructions/summary3.html" },	
		}

	},
	"bonus_check" : {
		"1": { "yes": "/coding/1/", "no": "/survey/post/"},
		"2": { "yes": "/coding/1/", "no": "/survey/post/"},
		"3": { "yes": "/coding/1/", "no": "/survey/post/"},
	},
}



default_password = "password!"


def random_string(num):
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(num))



def build_user_cookie(request, user_id = None, username = None, condition = None, turkuser_id = None, assignment_id = None):
	c = {}

	user_id_str = "user_id"
	username_str = "username"
	assignment_str = "assignment"
	condition_str = "condition"
	turkuser_str = "turkuser_id"

	# if none is specified, try to pull from logged in user, then session
	if user_id is None:
		if request is not None and request.user is not None and request.user.is_authenticated():
			# grab from username
			user_id = request.user.id
			username = request.user.username
			assignment = Assignment.objects.get(user=request.user)
			assignment_id = assignment.id
			condition = assignment.condition.id
			turkuser_id = request.user.turkuser.id
		else:
			# try to grab from cookie
			if user_id_str in request.session:
				user_id = request.session[user_id_str]
			if username_str in request.session:
				username = request.session[username_str]
			if condition_str in request.session:
				condition = request.session[condition_str]
			if turkuser_str in request.session:
				turkuser_id = request.session[turkuser_str]
			if assignment_str in request.session:
				assignment_id = request.session[assignment_str]


	# add to cookie
	c[user_id_str] = user_id
	c[username_str] = username
	c[condition_str] = condition
	c[turkuser_str] = turkuser_id
	c[assignment_str] = assignment_id

	# add to session, just in case
	if user_id is not None:
		request.session[user_id] = user_id
	if username is not None:
		request.session[username_str] = username
	if condition is not None:
		request.session[condition_str] = condition
	if turkuser_id is not None:
		request.session[turkuser_str] = turkuser_id
	if assignment_id is not None:
		request.session[assignment_str] = assignment_id

	print "build_user_cookie: ", repr(c)

	return c


def create_user(request, cnd=None):
	
	request.session.flush()

	c = {}

	#print "create_user"
	# first create user
	username = random_string(16)

	user = User.objects.create_user(username=username,
								password=default_password,
								email="spamaddr1@geosoco.com")
	user.is_active = True
	#user.activate()
	user.save()

	user.backend = 'django.contrib.auth.backends.ModelBackend'

	#print "saved"
	# create matching turk user
	#condition = random.randint(0,2)
	completion_code = random_string(16)
	turk_user = TurkUser.objects.create(
		user=user, 
		initial_browser_details = request.POST['browser_info'],
		completion_code = completion_code,
		start_time = datetime.datetime.now()
		)
	turk_user.save()
	#print "turk_user saved"

	# find condition
	study = Study.objects.get(id=1)
	all_conditions = Condition.objects.filter(study=study)
	print "got %d conditions"%(all_conditions.count())


	if cnd is None:
		#rnd = datetime.datetime.now().second % (all_conditions.count()+1)
		rnd = random.randint(0,10*(all_conditions.count()-1)) // 10
		print "Assinging user to ", rnd
		condition = all_conditions[rnd]
	else:
		print "Forcing user to ", cnd
		condition = all_conditions[int(cnd)]

	# assignment
	assignment = Assignment.objects.create(
		user=user,
		condition=condition)
	assignment.save()


	# log user in
	logged_in_user = authenticate(username=username, password=default_password)
	if logged_in_user is not None:
		if logged_in_user.is_active:
			login(request, logged_in_user)
		else:
			print "user not activated"
	else:
		print "could not authenticate user"

	c = build_user_cookie(request, user_id = logged_in_user.id, username=username, condition=condition.id, turkuser_id = turk_user.id, assignment_id = assignment.id )

	print "cookie built"
	print c

	return c


######################
#
# VIEWS
#
######################


# Create your views here.

def home(request):
	return render(request, "base.html")



def make_instance_struct(queryset):
	ret_dict = {}
	for instance in queryset:
		if instance.tweet_id not in ret_dict:
			ret_dict[instance.tweet_id] = set()

		ret_dict[instance.tweet_id].add(instance.code_id)	

	return ret_dict



def validate(request, page):
	"""
	This attempts to validate some of the tweets
	"""
	_start = time.time()
	c = build_user_cookie(request)
	print "validate--- (%s)"%(page)
	print request.user.id
	print request.user.turkuser.id
	print "authenticated", request.user.is_authenticated()

	assignment_id = int(c["assignment"])
	condition_id = int(c["condition"])
	condition = Condition.objects.get(pk=condition_id)
	datasets = condition.dataset.all()

	correct = set()
	all_items = set()

	# verify the page is in range
	page_num = int(page)
	if page_num < 0 or page_num >= datasets.count():
		return HttpResponseBadRequest()

	dataset = datasets[page_num]

	# find the attention checks
	attention_checks = Tweet.objects.filter(dataset = dataset, attention_check=True)
	ac_ids = [ac.id for ac in attention_checks]
	#print "ac_ids: ", repr(ac_ids)
	#print "condition id: ", condition_id
	answers = Answer.objects.filter(tweet_id__in=ac_ids, condition=condition)
	answer_dict = make_instance_struct(answers)
	#print "answer_dict: ", repr(answer_dict)

	# grab instances
	instances = CodeInstance.objects.filter(tweet_id__in=ac_ids, assignment=assignment_id)
	instance_dict = make_instance_struct(instances)
	#print "instance_dict: ", repr(instance_dict)

	# check each one of the attention checks
	for ac in ac_ids:
		# add the attention check to our items list
		all_items.add(ac)

		answer_set = answer_dict.get(ac, set())
		instance_set = instance_dict.get(ac,set())

		is_correct = (instance_set == answer_set)
		if is_correct:
			correct.add(ac)
		
		print "tweet %d: %s"%(ac, str(is_correct))




	# find duplicates
	duplicate_tweet_ids = Tweet.objects \
		.filter(dataset=dataset) \
		.values("tweet_id") \
		.annotate(num=Count("tweet_id")) \
		.order_by() \
		.filter(num__gt=1)

	#print "dupes: ", duplicate_tweet_ids
	duplicate_tweet_ids = [t["tweet_id"] for t in duplicate_tweet_ids]
	#print "dupes: ", duplicate_tweet_ids

	duplicate_tweets = Tweet.objects.filter(dataset=dataset, tweet_id__in=duplicate_tweet_ids)
	duplicate_ids = [t.id for t in duplicate_tweets]

	dup_instances = CodeInstance.objects.filter(tweet_id__in=duplicate_ids, assignment=assignment_id)

	dup_dict = {}
	for dt in duplicate_tweets:
		if dt.tweet_id not in dup_dict:
			dup_dict[dt.tweet_id] = set()
		dup_dict[dt.tweet_id].add(dt.id)

	#print "dup dict: ", dup_dict

	# validate the duplicates
	# this will only do forward comparisons. So each dupe's codes is compared to the last
	# it does NOT do full pairwise comparisons
	# so the total # of comparisons will be N-1 (number of dupes - 1)
	dinst_dict = make_instance_struct(dup_instances)
	for tid, dup_set in dup_dict.iteritems():
		last_instance = None
		last_id = None
		for id in dup_set:
			cur_instance = dinst_dict.get(id, set())
			if last_instance is not None:
				# add it to the entire set. do not add the first one as it isn't a check
				all_items.add(id)
				if cur_instance == last_instance:
					print "%d is consistent with %d (%s,%s)"%(
						id, last_id, 
						repr(cur_instance), repr(last_instance))
					correct.add(id)
				else:
					print "%d is INCONSISTENT with %d (%s,%s)"%(
						id, last_id, 
						repr(cur_instance), repr(last_instance))
			last_instance = cur_instance
			last_id = id


	print "%d of %d correct"%(len(correct), len(all_items))


	


	#_end = time.time()
	#_total_time = _end - _start
	#print "total_time: ", _total_time

	cnd_map_entry = condition_map["validate"][page][str(condition.id)]

	if len(correct) > (len(all_items)/2):
		return HttpResponseRedirect(cnd_map_entry["positive_redirect"])
	else:
		return HttpResponseRedirect(cnd_map_entry["negative_redirect"])


def coding(request, page):
	c = build_user_cookie(request)
	#print "coding---"
	#print request.user.id
	#print request.user.turkuser.id
	#print "authenticated", request.user.is_authenticated()
	page = int(page) if page is not None else 0
	#print "page: ", page
	c["page"] = page

	condition_id = int(c["condition"])
	condition = Condition.objects.get(pk=condition_id)
	datasets = condition.dataset.all()
	c["next"] = condition_map["coding"][str(page)][str(condition.id)]["next"]
	c["help"] = condition_map["coding"][str(page)][str(condition.id)]["help"]
	
	for index, ds in enumerate(datasets):
		#print "#%d, %s"%(index, repr(ds))
		if index == int(page):
			#print "got index: ", index
			c["dataset_id"] = ds.id
			break
	
	#print condition.name, condition.id
	#print condition_map["coding"][str(page)][str(condition.id)]["next"]
	#print condition_map["coding"][str(page)][str(condition.id)]["help"]
	return render(request, "base.html" ,c)


def landing(request, cnd=None):
	print "cnd: ", cnd
	if request.method == "POST":
		c = create_user(request, cnd=cnd)

		#print "user-created"
		#print repr(request.POST)

		#c["browser_info"] = request.POST["browser_info"]

		#return render(request, "landing.html", c)
		return HttpResponseRedirect(reverse('pre_survey'))
	else:
		c = {}
		c.update(csrf(request))

	return render(request, "landing.html", c)


def instructions(request, page = 1):

	#print "instructions!"

	# check defualt value
	if page is None:
		page = 0


	c = build_user_cookie(request)

	condition = c['condition']

	page_name = condition_map["instructions"][str(page)][str(condition)]["page"]
	c['next'] = condition_map["instructions"][str(page)][str(condition)]["next"]
	c['page'] = page


	return render(request, page_name, c)

#def start(request):


def thanks(request):
	request.user.turkuser.finish_time = datetime.datetime.now()
	request.user.turkuser.save()
	request.user.save()

	c = build_user_cookie(request)
	c['completion_code'] = request.user.turkuser.completion_code

	print repr(c)
	return render(request, "thanks.html", c)


def pre_survey(request):
	c = build_user_cookie(request)
	c.update(csrf(request))

	if request.method == "POST":
		condition = c['condition']
		ps = PreSurvey(user=request.user)
		form = PreSurveyForm(request.POST, instance=ps)
		if form.is_valid():
			ps.save()
			print "pre_survey success redirection ----"
			print "redirecting to: ", condition_map["pre_survey"][str(condition)]["next"]
			return HttpResponseRedirect( condition_map["pre_survey"][str(condition)]["next"] )
	else:
		form = PreSurveyForm()

	c['form'] = form

	return render(request, "pre_survey.html", c)

def post_survey(request):
	c = build_user_cookie(request)
	c.update(csrf(request))

	if request.method == "POST":
		condition = c['condition']
		ps = PostSurvey(user=request.user)
		form = PostSurveyForm(request.POST, instance=ps)
		if form.is_valid():
			ps.save()
			return HttpResponseRedirect( condition_map["post_survey"][str(condition)]["next"] )
	else:
		form = PostSurveyForm()

	c['form'] = form

	return render(request, "post_survey.html", c)


def req_check(request):
	return render(request, "req_check.html")


class InstructionCheck(CreateView):
	template_name = 'instruction_check.html'
	form_class = InstructionCheckForm
	success_url = '/coding/0/'

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()

		return HttpResponseRedirect(self.get_success_url())



def bonus_check(request):
	c = build_user_cookie(request)
	condition = c['condition']

	c['yes'] = condition_map["bonus_check"][str(condition)]["yes"]
	c['no'] = condition_map["bonus_check"][str(condition)]["no"]

	return render(request, "bonus_check.html", c)

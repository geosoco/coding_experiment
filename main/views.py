from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.core.urlresolvers import reverse
#from django.template.context_processors import csrf
from models import *
import string
import random
import datetime


# 
# conditions
# 	0 - All Codes
#	1 - First Level only
#	2 - Second level only
#	3 - (later: uncertainty yes/no)


#
# map of the conditions
#
# current_page : page # : condition : { page: template_name, next: link for next page }
#

condition_map = {
	"instructions" : { 
		"0" : {
			"1": { "page": "instructions.html", "next": "/coding/0/" },
			"2": { "page": "instructions_1.html", "next": "/coding/0/" },
			"3": { "page": "instructions_2.html", "next": "/coding/0/" },
		}
	}, 
	"coding" : {
		"0": {
			"1": { "page": "coding.html", "next": "/coding/1/" },
			"2": { "page": "coding.html", "next": "/coding/1/" },
			"3": { "page": "coding.html", "next": "/coding/1/" },	
		},
		"1": {
			"1": { "page": "coding.html", "next": "/thanks/" },
			"2": { "page": "coding.html", "next": "/thanks/" },
			"3": { "page": "coding.html", "next": "/thanks/" },	
		}

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
	all_conditions = Condition.objects.filter(study_id=1)
	print "got %d conditions"%(all_conditions.count())

	if cnd is None:
		rnd = datetime.datetime.now().second % (all_conditions.count()+1)
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


def coding(request, page):
	c = build_user_cookie(request)
	print "coding---"
	print request.user.id
	print request.user.turkuser.id
	print "authenticated", request.user.is_authenticated()
	page = page if page is not None else 0
	c["page"] = page
	condition_id = int(c["condition"])
	condition = Condition.objects.get(pk=condition_id)
	c["next"] = condition_map["coding"][str(page)][str(condition.id)]["next"]
	datasets = condition.dataset.all()
	for index, ds in enumerate(datasets):
		print "#%d, %s"%(index, repr(ds))
		if index == int(page):
			print "got index: ", index
			c["dataset_id"] = ds.id
			break
	
	print condition.name, condition.id
	print condition_map["coding"][str(page)][str(condition.id)]["next"]
	return render(request, "base.html" ,c)


def landing(request, cnd=None):
	print "cnd: ", cnd
	if request.method == "POST":
		c = create_user(request, cnd=cnd)

		#print "user-created"
		#print repr(request.POST)

		#c["browser_info"] = request.POST["browser_info"]

		#return render(request, "landing.html", c)
		return HttpResponseRedirect(reverse('instructions', kwargs=({"page": "0"})))
	else:
		c = {}

	return render(request, "landing.html", c)


def instructions(request, page):

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



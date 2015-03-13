from rest_framework import viewsets
from main.models import *
from serializers import *
from django.core import serializers
import simplejson as json
from rest_framework.permissions import IsAuthenticated


class TurkUserViewSet(viewsets.ModelViewSet):
	"""
	"""
	queryset = TurkUser.objects.all()
	serializer_class = TurkUserSerializer
	permission_classes = (IsAuthenticated,)

	def dispatch(self, request, *args, **kwargs):
		if kwargs.get('pk') == 'current' and request.user:
			kwargs['pk'] = request.user.turkuser.pk
			#print repr(kwargs)
			#print repr(request.user)
			#print request.user.pk
			#print request.user.turkuser.pk
			#print request.session['user_id']
			#if 'user_id' in request.session:
			#	kwargs['pk'] = request.session['user_id']
			#print json.dumps(request.user)
			#data = serializers.serialize("json", request.user)
			#print data

		return super(TurkUserViewSet, self).dispatch(request, *args, **kwargs)



#class TurkAssignmentViewSet(viewsets.ModelViewSet):
#	"""
#	"""
#	queryset = TurkAssignment.objects.all()
#	serializer_class = TurkAssignmentSerializer


class TweetViewSet(viewsets.ModelViewSet):
	"""
	"""
	queryset = Tweet.objects.all()
	serializer_class = TweetSerializer
	permission_classes = (IsAuthenticated,)


class CodeViewSet(viewsets.ModelViewSet):
	"""
	"""
	queryset = Code.objects.all()
	serializer_class = CodeSerializer
	permission_classes = (IsAuthenticated,)


class CodeInstanceViewSet(viewsets.ModelViewSet):
	"""
	"""
	#queryset = CodeInstance.objects.filter(assignment=self.request.user.turkuser)
	serializer_class = CodeInstanceSerializer
	permission_classes = (IsAuthenticated,)
	#model = CodeInstance


	def get_queryset(self):
		print "getting queryset - %d %s"%(self.request.user.turkuser.id, self.request.user.turkuser.worker_id)
		return CodeInstance.objects.filter(assignment=self.request.user.turkuser)

	def create(self, request, *args, **kwargs):
		if 'tweet' in request.data or 'tweet_str' in request.data:
			tweet = request.data['tweet'] if 'tweet' in request.data else request.data['tweet_str']
			if isinstance(tweet, str) or isinstance(tweet, unicode):
				tweet = int(tweet)
			request.data['tweet'] = tweet


		return super(CodeInstanceViewSet, self).create(request, *args, **kwargs)

	def perform_create(self, serializer):
		#print "before save"
		serializer.save()

	def dispatch(self, request, *args, **kwargs):
		#print "dispatch"
		#print repr(kwargs)
		if kwargs.get('pk') == 'current' and request.user:
			kwargs['pk'] = request.user.turkuser.pk
			

		return super(CodeInstanceViewSet, self).dispatch(request, *args, **kwargs)



#class CurrentTurkUserViewSet(viewsets.ModelViewSet):
#	queryset = TurkUser.objects.all()
#	serializer_class = TurkUserSerializer
#
#	def dispatch(self, request, *args, **kwargs):
#		if kwargs.get('pk') == 'current' and request.user:
#			kwargs['pk'] = request.user.pk
#
#		return super(TurkUserViewSet, self).dispatch(request, *args, **kwargs)


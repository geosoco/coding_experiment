from rest_framework import viewsets
from main.models import *
from serializers import *
from django.core import serializers
import simplejson as json
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
	"""
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsAuthenticated,)

	def dispatch(self, request, *args, **kwargs):
		if kwargs.get('pk') == 'current' and request.user:
			kwargs['pk'] = request.user.pk

		return super(UserViewSet, self).dispatch(request, *args, **kwargs)


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
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)

class AssignmentViewSet(viewsets.ModelViewSet):
	"""
	"""
	serializer_class = AssignmentSerializer
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)


	def get_queryset(self):
		return Assignment.objects.filter(user=self.request.user)


class CodeSchemeViewSet(viewsets.ModelViewSet):
	"""
	"""
	serializer_class = CodeSchemeSerializer
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	depth=2

	def get_queryset(self):
		assignment = Assignment.objects.get(user=self.request.user.id)
		print assignment.condition
		print assignment.condition.id
		print assignment.condition.code_schemes.all().count()
		code_scheme_ids = [cs.id for cs in assignment.condition.code_schemes.all()]

		#code_schemes = 

		return CodeScheme.objects.filter(id__in=code_scheme_ids)

class CodeViewSet(viewsets.ModelViewSet):
	"""
	"""
	serializer_class = CodeSerializer
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		assignment = Assignment.objects.get(user=self.request.user.id)
		print assignment.condition
		print assignment.condition.id
		print assignment.condition.code_schemes.all().count()
		code_scheme_ids = [cs.id for cs in assignment.condition.code_schemes.all()]

		#code_schemes = 

		return Code.objects.filter(scheme__in=code_scheme_ids)


class CodeInstanceViewSet(viewsets.ModelViewSet):
	"""
	"""
	#queryset = CodeInstance.objects.filter(assignment=self.request.user.turkuser)
	#model = CodeInstance
	serializer_class = CodeInstanceSerializer
	permission_classes = (IsAuthenticated,)
	authentication_classes = (SessionAuthentication, BasicAuthentication)



	def get_queryset(self):
		print "get_queryset"
		print "user_id", self.request.user.id
		print "--", repr(self.request.user)
		print self.request.auth
		assignment = None
		try:
			assignment = Assignment.objects.get(user=self.request.user)
			print "assignment: ", assignment
		except ObjectDoesNotExist:
			pass
		if assignment is not None:
			#print "getting queryset - %d %s"%(self.request.user.turkuser.id, self.request.user.username)
			return CodeInstance.objects.filter(assignment=assignment)
		else:
			return CodeInstance.objects.all()

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
		print "dispatch-->"
		print repr(kwargs)
		#print "user id:", request.user.turkuser.pk
		if kwargs.get('pk') == 'current' and request.user:
		#	kwargs['pk'] = request.user.turkuser.pk
			kwargs['pk'] = request.user.id
			

		return super(CodeInstanceViewSet, self).dispatch(request, *args, **kwargs)


class DatasetViewSet(viewsets.ModelViewSet):
	"""
	"""
	queryset = Dataset.objects.all()
	serializer_class = DatasetSerializer
	permission_classes = (IsAuthenticated,)
	authentication_classes = (SessionAuthentication, BasicAuthentication)

	




#class CurrentTurkUserViewSet(viewsets.ModelViewSet):
#	queryset = TurkUser.objects.all()
#	serializer_class = TurkUserSerializer
#
#	def dispatch(self, request, *args, **kwargs):
#		if kwargs.get('pk') == 'current' and request.user:
#			kwargs['pk'] = request.user.pk
#
#		return super(TurkUserViewSet, self).dispatch(request, *args, **kwargs)


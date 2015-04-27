from main.models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'email')


class TurkUserSerializer(serializers.ModelSerializer):
	#user = serializers.RelatedField(source='user.id', read_only=True)
	user = UserSerializer(partial=True, read_only=True)

	class Meta:
		model = TurkUser
		fields = ('id', 'user', 'worker_id', 'condition', 'initial_browser_details', 'final_browser_details', 'start_time', 'finish_time')
		partial=True


#class TurkAssignmentSerializer(serializers.HyperlinkedModelSerializer):
#	class Meta:
#		model = TurkAssignment
#		fields = ('id', 'assignment', 'hit', 'turksubmit', 'browser_details', 'condition', 'start_time', 'finish_time', 'turker',)

class TweetSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Tweet
		fields = ('id', 'tweet_id', 'text', 'screen_name','embed_code')
		#read_only_fields = ('codeinstances',)
		# depth = 2

class CodeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Code
		fields = ('id', 'schema', 'name', 'description',)

class CodeInstanceSerializer(serializers.ModelSerializer):
	#tweet_str = serializers.CharField(source='tweet.id', allow_blank=True, allow_null=True)

	class Meta:
		model = CodeInstance
		fields = ('id', 'date', 'deleted', 'code', 'tweet', 'assignment', 'code')
		base_name = "codeinstance"



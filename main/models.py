from django.contrib.auth.models import User
from django.db import models


class TurkUser(models.Model):
	user = models.OneToOneField(User)

	initial_browser_details = models.TextField(blank=True, null=True)
	final_browser_details = models.TextField(blank=True, null=True)

	start_time = models.DateTimeField(auto_now_add=True)
	finish_time = models.DateTimeField(blank=True, null=True)

	completion_code = models.CharField(max_length=64, blank=True, null=True)


	def __str__(self):
		return str(self.id)

	def __unicode__(self):
		return unicode(self.id)



class Dataset(models.Model):

	name = models.CharField(max_length=256)
	rumor = models.CharField(max_length=64, blank=True, null=True)
	description = models.TextField(blank=True, null=True)

	def __str__(self):
		return "%s (%d)"%(self.name, self.id)

	def __unicode__(self):
		return u"%s (%d)"%(self.name, self.id)	


class CodeScheme(models.Model):
	name = models.CharField(max_length=64)
	description = models.TextField()
	mutually_exclusive = models.BooleanField(default=False)

	def __str__(self):
		return "%s (%d)"%(self.name, self.id)

	def __unicode__(self):
		return u"%s (%d)"%(self.name, self.id)		


class Code(models.Model):
	scheme = models.ForeignKey(CodeScheme)
	name = models.CharField(max_length=64)
	description = models.TextField(null=True, blank=True)
	css_class = models.CharField(max_length=64, null=True, blank=True )
	key = models.CharField(max_length=1, null=True, blank=True)

	def __str__(self):
		return "%s (%d)"%(self.name, self.scheme_id)

	def __unicode__(self):
		return u"%s (%d)"%(self.name, self.scheme_id)



class Tweet(models.Model):
	id = models.AutoField(primary_key=True)
	original_id = models.IntegerField(default=None, blank=True, null=True)
	dataset = models.ForeignKey(Dataset)
	tweet_id = models.BigIntegerField(default=None)
	text = models.CharField(max_length=1024)
	screen_name = models.CharField(max_length=64)
	embed_code = models.TextField(null=True, blank=True, default=None)
	attention_check = models.BooleanField(null=False, blank=False, default=False)

	def __str__(self):
		return "%d - %s: %s"%(self.id, self.screen_name, self.text)

	def __unicode__(self):
		return u"%d - %s: %s"%(self.id, self.screen_name, self.text)		


class Study(models.Model):
	name = models.CharField(max_length=256)
	description = models.TextField(null=True, blank=True)
	last_condition = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return "%s (%d)"%(self.name, self.id)

	def __unicode__(self):
		return u"%s (%d)"%(self.name, self.id)		


class Condition(models.Model):
	name = models.CharField(max_length=64)
	description = models.TextField(null=True, blank=True)

	study = models.ForeignKey(Study)
	dataset = models.ManyToManyField(Dataset, blank=True)
	code_schemes = models.ManyToManyField(CodeScheme, blank=True)

	def __str__(self):
		return "%s (%d)"%(self.name, self.id)

	def __unicode__(self):
		return u"%s (%d)"%(self.name, self.id)	


class Answer(models.Model):
	condition = models.ForeignKey(Condition)
	tweet = models.ForeignKey(Tweet)
	code = models.ForeignKey(Code, null=True, blank=True)



class Assignment(models.Model):
	user = models.ForeignKey(User)
	condition = models.ForeignKey(Condition)

	def __str__(self):
		return "%d (%d - %d)"%(self.id, self.user.id, self.condition.id)

	def __unicode__(self):
		return u"%d (%d - %d)"%(self.id, self.user.id, self.condition.id)	


class CodeInstance(models.Model):
	date = models.DateTimeField(auto_now=True)
	deleted = models.BooleanField(default=False)
	
	code = models.ForeignKey(Code)
	tweet = models.ForeignKey(Tweet)
	assignment = models.ForeignKey(Assignment)

	def __str__(self):
		return "%s - %d - %s"%(self.assignment.id, self.tweet.id, self.code.name)

	def __unicode__(self):
		return u"%s - %d - %s"%(self.assignment.id, self.tweet.id, self.code.name)


class ValidatedCodeInstance(models.Model):
	"""
	Ooops this is redundant with Answer. This sounds better for some things. :\
	"""
	code = models.ForeignKey(Code)
	tweet = models.ForeignKey(Tweet)
	condition = models.ForeignKey(Condition)



class PreSurvey(models.Model):
	"""
	"""
	user = models.ForeignKey(User)
	time = models.DateTimeField(auto_now_add=True)
	age = models.TextField(blank=True, null=True)
	country = models.TextField(blank=True, null=True)
	zip_code = models.TextField(blank=True, null=True)
	rumor_familiarity = models.IntegerField(blank=True, null=True)
	twitter_usage = models.IntegerField(blank=True, null=True)
	english_reading_comfort = models.IntegerField(blank=True, null=True)
	english_sarcasm_comfort = models.IntegerField(blank=True, null=True)


class PostSurvey(models.Model):
	"""
	"""
	user = models.ForeignKey(User)
	time = models.DateTimeField(auto_now_add=True)
	task_difficulty = models.IntegerField(blank=True, null=True)
	task_clarity = models.IntegerField(blank=True, null=True)
	task_value = models.IntegerField(blank=True, null=True)
	suggestions = models.TextField(blank=True, null=True)


class InstructionCheck(models.Model):
	"""
	"""
	user = models.ForeignKey(User)
	time = models.DateTimeField(auto_now_add=True)
	rumor_description = models.TextField(blank=False, null=True)
	which_codes = models.TextField(blank=False, null=True)	


class UserValidatedInstance(models.Model):
	"""
	This is intended to hold references to all 
	"""
	ATTENTION_CHECK = 1
	DUPLICATE_CHECK = 2
	KIND_CHOICES = (
		(ATTENTION_CHECK, 'Attention Check'),
		(DUPLICATE_CHECK, 'Duplicate Check')
	)

	user = models.ForeignKey(User)
	time = models.DateTimeField(auto_now_add=True)
	kind = models.IntegerField(choices=KIND_CHOICES, default=ATTENTION_CHECK)
	correct = models.BooleanField(default=False)
	tweet_1 = models.ForeignKey(Tweet, related_name='%(class)s_tweet_1')
	tweet_2 = models.ForeignKey(Tweet, blank=True, null=True, related_name='%(class)s_tweet_2')
	tweet_1_codes = models.TextField(blank=True, null=True)
	tweet_2_codes = models.TextField(blank=True, null=True)



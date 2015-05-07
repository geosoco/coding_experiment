from django.contrib.auth.models import User
from django.db import models


class TurkUser(models.Model):
	user = models.OneToOneField(User)

	initial_browser_details = models.TextField(blank=True, null=True)
	final_browser_details = models.TextField(blank=True, null=True)

	start_time = models.DateTimeField(auto_now=True)
	finish_time = models.DateTimeField(blank=True, null=True)

	completion_code = models.CharField(max_length=64, blank=True, null=True)


	def __str__(self):
		return str(self.id)

	def __unicode__(self):
		return unicode(self.id)



class Dataset(models.Model):

	name = models.CharField(max_length=256)
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
	code = models.ForeignKey(Code)



class Assignment(models.Model):
	user = models.ForeignKey(User)
	condition = models.ForeignKey(Condition)

	def __str__(self):
		return "%s (%d)"%(self.name, self.id)

	def __unicode__(self):
		return u"%s (%d)"%(self.name, self.id)	


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
	age = models.IntegerField(blank=True, null=True)
	country = models.IntegerField(blank=True, null=True)
	zip_code = models.IntegerField(blank=True, null=True)
	twitter_familiarity = models.IntegerField(blank=True, null=True)
	english_reading_comfort = models.IntegerField(blank=True, null=True)
	english_speaking_comfort = models.IntegerField(blank=True, null=True)
	overall_english_comfort = models.IntegerField(blank=True, null=True)

class PostSurvey(models.Model):
	"""
	"""
	user = models.ForeignKey(User)
	task_difficulty = models.IntegerField(blank=True, null=True)
	task_clarity = models.IntegerField(blank=True, null=True)
	task_value = models.IntegerField(blank=True, null=True)
	suggestions = models.TextField(blank=True, null=True)



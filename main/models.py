from django.contrib.auth.models import User
from django.db import models


class TurkUser(models.Model):
	user = models.OneToOneField(User)
	worker_id = models.CharField(max_length=256, blank=True, null=True)
	condition = models.IntegerField(blank=True, null=True, default=0)

	initial_browser_details = models.TextField(blank=True, null=True)
	final_browser_details = models.TextField(blank=True, null=True)

	start_time = models.DateTimeField(auto_now=True)
	finish_time = models.DateTimeField(blank=True, null=True)

	completion_code = models.CharField(max_length=64, blank=True, null=True)

	def __str__(self):
		return self.worker_id

	def __unicode__(self):
		return self.worker_id



class Tweet(models.Model):
	id = models.AutoField(primary_key=True)
	tweet_id = models.BigIntegerField(default=None)
	text = models.CharField(max_length=1024)
	screen_name = models.CharField(max_length=64)
	embed_code = models.TextField(null=True, blank=True, default=None)

	def __str__(self):
		return "%d - %s: %s"%(self.id, self.screen_name, self.text)

	def __unicode__(self):
		return u"%d - %s: %s"%(self.id, self.screen_name, self.text)		


class Code(models.Model):
	schema = models.IntegerField()
	name = models.CharField(max_length=64)
	description = models.TextField()

	def __str__(self):
		return "%s (%d)"%(self.name, self.schema)

	def __unicode__(self):
		return u"%s (%d)"%(self.name, self.schema)


class CodeInstance(models.Model):
	date = models.DateTimeField(auto_now=True)
	deleted = models.BooleanField(default=False)
	
	code = models.ForeignKey(Code)
	tweet = models.ForeignKey(Tweet)
	assignment = models.ForeignKey(TurkUser)

	def __str__(self):
		return "%s - %d - %s"%(self.assignment.id, self.tweet.id, self.code.name)

	def __unicode__(self):
		return u"%s - %d - %s"%(self.assignment.id, self.tweet.id, self.code.name)


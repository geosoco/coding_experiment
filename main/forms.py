from django.contrib.auth.models import User
from django.forms import ModelForm
from models import *

class PreSurveyForm(ModelForm):
	"""
	Form for the pre-survey
	"""
	def __init__(self, *args, **kwargs):
		super(PreSurveyForm, self).__init__(*args, **kwargs)

		#self.fields['profession'].help_text

	class Meta:
		model = PreSurvey
		exclude = ('user',)


class PostSurveyForm(ModelForm):
	"""
	Form for the post-survey
	"""
	def __init__(self, *args, **kwargs):
		super(PostSurveyForm, self).__init__(*args, **kwargs)

	class Meta:
		model = PostSurvey
		exclude = ('user',)


class InstructionCheckForm(ModelForm):
	"""
	Form for the instructions check
	"""
	def __init__(self, *args, **kwargs):
		super(InstructionCheckForm, self).__init__(*args, **kwargs)

	class Meta:
		model = InstructionCheck
		exclude = ('user',)
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from main.models import Dataset, Tweet, Code, CodeScheme, Answer, ValidatedCodeInstance, Condition
import simplejson as json

class Command(BaseCommand):
	help = "import a series of oembed tweets from a json file"

	def add_arguments(self, parser):
		parser.add_argument('filename')
		parser.add_argument('dataset_name')
		parser.add_argument('--condition')
		parser.add_argument('--codescheme', action="append")


	def create_code_scheme_dict(self, code_schemes):
		cs_dict = {}

		for scheme_id in code_schemes:

			try:
				cs = CodeScheme.objects.get(name=scheme_id)
			except ObjectDoesNotExist:
				cs = CodeScheme.objects.get(pk=scheme_id)


			codes = Code.objects.filter(scheme=cs)
			for code in codes:

				# check for duplicates
				if code.name in cs_dict:
					raise CommandError("Found multiple codes with the same name (ids: %d,%d)"%(cs_dict[code.name]["id"], code.id))

				# add to dict
				cs_dict[code.name] = code

		return cs_dict


	def handle(self, *args, **options):
		
		# lookup the condition
		condition = None
		condition_name = options.get('condition', None)
		if condition_name:
			print "getting condition: %s"%(condition_name)
			condition = Condition.objects.get(name=condition_name)
			print condition.id

		# lookup codes
		code_dict = {}
		opt_codeschemes = options['codescheme']
		if len(opt_codeschemes) > 0:
			code_dict.update(self.create_code_scheme_dict(opt_codeschemes))

		with open(options['filename']) as f:

			# find our dataset by its name, or create it
			dataset_name = options['dataset_name']
			dataset = None
			try:
				dataset = Dataset.objects.get(name=dataset_name)
			except ObjectDoesNotExist:
				dataset = Dataset(name=dataset_name)
				dataset.save()


			for line in f:
				# load the tweet as a line
				obj = json.loads(line)

				# load data from tweet
				tweet_id = obj.get('id', None)
				ac = obj.get("attention_check", False)

				# create tweet and save it so the id becomes valid
				tweet_obj = Tweet(
					tweet_id=tweet_id, 
					text='', 
					screen_name='', 
					embed_code=obj.get('html', ''), 
					dataset=dataset,
					attention_check=ac)
				tweet_obj.save()

				# check for codes
				codes = obj.get('codes', None)
				if codes is not None and len(codes) > 0:

					# step through all the codes
					for code_name in codes:

						# get our code
						code_obj = code_dict.get(code_name, None)
						if code_obj is None:
							print "ERROR finding code (%s)"%(code_name)
							continue

						if obj.get('attention_check', ''):
							answer = Answer(
								condition=condition, 
								tweet=tweet_obj,
								code=code_obj)
							answer.save()
						else:
							val_codeinstance = ValidatedCodeInstance(
								condition=condition,
								tweet=tweet_obj,
								code=code_obj)
							val_codeinstance.save()
				else:
					if obj.get('attention_check', ''):
						answer = Answer(
								condition=condition, 
								tweet=tweet_obj,
								code=None)
						answer.save()






from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from main.models import Dataset, Tweet, Code, CodeScheme, Answer, ValidatedCodeInstance, Condition, Study, Assignment
import simplejson as json
import csv
import os
import codecs

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8

    from: https://gist.github.com/eightysteele/1174811
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeDictReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.

    from: https://gist.github.com/eightysteele/1174811
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
        self.header = self.reader.next()

    def next(self):
        row = self.reader.next()
        vals = [unicode(s, "utf-8") for s in row]
        return dict((self.header[x], vals[x]) for x in range(len(self.header)))

    def __iter__(self):
        return self



class Command(BaseCommand):
	"""

	"""

	help = "import a series of oembed tweets from a json file"
	output_transaction = True


	def add_arguments(self, parser):
		parser.add_argument('filename')
		parser.add_argument('rumor')
		parser.add_argument('username')
		parser.add_argument('--dataset_name')
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

		rumor = options.get('rumor', '')
		filename = options.get('filename', '')

		# find user
		user = None
		username = options.get('username', None)
		if username is None:
			raise CommandError("Please specify a username")
		user = User.objects.get(username=username)

		# get codeset
		cs = None
		codescheme_names = options.get('codescheme', None)
		if codescheme_names is None or len(codescheme_names) == 0:
			raise CommandError("Could not find a code scheme name")
		self.stdout.write("Codescheme: %s"%(codescheme_names))

		codeschemes = []
		for cs_name in codescheme_names:
			cs = CodeScheme.objects.get(name=cs_name)			

			codeschemes.append(cs)

		# get dataset
		dataset_name = options.get('dataset_name', None)
		if dataset_name is None:
			dataset_basename = os.path.basename(filename)
			dataset_filename = os.path.splitext(dataset_basename)[0]
			dataset_name =  "%s_%s"%(dataset_filename, username)

		ds, ds_created = Dataset.objects.get_or_create(
			name=dataset_name, 
			defaults={
				"name": dataset_name,
				"rumor": rumor,
			})

		# get or create study
		study, study_created = Study.objects.get_or_create(
			name=rumor,
			defaults={
				"name": rumor
			})

		# condition
		condition_name = options.get("condition",None)
		if condition_name is None:
			condition_name = "%s:%s"%(rumor,username)
		self.stdout.write("condition name: %s"%(condition_name))
		condition, cnd_created = Condition.objects.get_or_create(
			name=condition_name,
			defaults={
				"name": condition_name,
				"study_id": study.id
			})

		# add dataset and schemes to condition
		condition.dataset.add(ds)
		for cs in codeschemes:
			condition.code_schemes.add(cs)
		condition.save()

		# Assignment
		self.stdout.write("Creating assignment for %s (%d) with condition %s (%d)"%(
			user.username, user.id, condition.name, condition.id))
		assignment = Assignment.objects.create(
				user=user,
				condition=condition
			)



		with open(filename) as csvfile:
			reader = UnicodeDictReader(csvfile)
			for row in reader:
				tweet_id_str = row['tweet_id']
				original_id_str = row['id']
				if not tweet_id_str and not original_id_str:
					continue
				#self.stdout.write("%s,%s,%s"%(original_id_str, tweet_id_str, row['text']))

				tweet_id = int(tweet_id_str)
				original_id = int()
				text = row['text']

				#self.stdout.write("%s,%s,%s"%(tweet_id, original_))

				tweet_obj = Tweet(
					tweet_id=tweet_id, 
					original_id=original_id,
					text=text, 
					screen_name='', 
					embed_code=text, 
					dataset=ds,
					attention_check=False)
				tweet_obj.save()






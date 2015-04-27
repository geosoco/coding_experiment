from django.core.management.base import BaseCommand, CommandError
from main.models import Tweet
import simplejson as json

class Command(BaseCommand):
	help = "import a series of oembed tweets from a json file"

	def add_arguments(self, parser):
		parser.add_argument('filename')

	def handle(self, *args, **options):
		
		with open(options['filename']) as f:
			for line in f:
				obj = json.loads(line)

				tweet_id = obj['id'] if 'id' in obj else None

				tweet_obj = Tweet(tweet_id = tweet_id, text='', screen_name='', embed_code=obj['html'])
				tweet_obj.save()

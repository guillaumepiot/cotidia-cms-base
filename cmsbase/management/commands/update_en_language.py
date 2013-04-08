from django.core.management.base import BaseCommand, CommandError
from cms.models import *
from directory.models import *
from agenda.models import *

class Command(BaseCommand):
	
	"""
	Updates all the current langauge in the database to 'en' instead of 'en-gb'
	"""

	help = 'Updates CMS/Category/Listing/Event english language to en'
	
	def handle(self, *args, **options):
		
		# CMS Pages
		pages = PageTranslation.objects.filter(language_code='en-gb').update(language_code='en')

		# Listing Pages
		listing = ListingTranslation.objects.filter(language_code='en-gb').update(language_code='en')	

		# Category Pages
		category = CategoryTranslation.objects.filter(language_code='en-gb').update(language_code='en')		
		
		# Events Page
		event = EventTranslation.objects.filter(language_code='en-gb').update(language_code='en')
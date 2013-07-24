# Create the search index

import os.path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from cmsbase.models import Page
from cmsbase import settings as cms_settings

from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.index import create_in

class Command(BaseCommand):
	args = '<file>'
	help = 'Create the search index'

	def handle(self, *args, **options):
		# indexed (meaning it can be searched)
		# stored (meaning the value that gets indexed is returned with the results; this is useful for fields such as the title).
		schema = Schema(title=TEXT(stored=True), content_type=TEXT(stored=True), language=KEYWORD(stored=True), id=ID(stored=True), content=TEXT)

		index_path = cms_settings.SEARCH_INDEX_PATH

		# Check if the index path exists otherwise create the
		if not os.path.exists(index_path):
			os.mkdir(index_path)
		
		ix = create_in(index_path, schema)
		writer = ix.writer()
		
		# Now add data to the index

		# CMS data
		for page in Page.objects.get_published_live():
			content_type = ContentType.objects.get_for_model(Page)
			for translation in page.get_translations():
				writer.add_document(title=u"%s" % translation.title, content_type=u"%s" % content_type,
                    id=u"%s" % page.id, language=u"%s" % translation.language_code, content=u"%s %s" % (translation.title, translation.content))

		writer.commit()
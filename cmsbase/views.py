import json

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.cache import cache
from django.conf import settings
from django.utils import translation

from cmsbase.models import *
from cmsbase.forms import SearchForm


# Function to retrieve page object depending on previwe mode and language

def get_page(request, model_class=Page , translation_class=PageTranslation , slug=False, preview=False):

	# Deconstruct the slug to get the last element corresponding to the page we are looking for
	if slug:
		slugs = slug.split('/')

		if len(slugs) == 1:
			last_slug = slugs[len(slugs)-1]
			parent_slug = False
		elif len(slugs) > 1:
			last_slug = slugs[len(slugs)-1]
			parent_slug = slugs[len(slugs)-2]

		published = []

		if preview:
			translation = translation_class.objects.filter(slug=last_slug, parent__published_from=None)

			if translation.count() > 0:
				published.append(translation[0].parent)
		else:
			translation = translation_class.objects.filter(slug=last_slug).exclude(parent__published_from=None)

			if translation.count() > 0:
				published.append(translation[0].parent)

	else:
		if preview:
			published = model_class.objects.filter(home=True, published_from=None)
		else:
			# If no sulg provided get the page checked as home
			published = model_class.objects.filter(published=True, home=True).exclude(published_from=None)
			# If no page is checked as home, return the first one in the list
			if not published:
				published = model_class.objects.filter(published=True).exclude(published_from=None)[:1]

	if len(published)> 0:
		published = published[0]
	else:
		published = False

	return published


# Page decorator
# Cover the basic handling such as page object lookup, redirect, 404, preview mode, language switching url switching
def page_processor(model_class=Page, translation_class=PageTranslation):
	def wrap(f):
		def wrapper(request, slug=False):

			# Check if the preview variable is in the path
			preview = request.GET.get('preview', False)

			# Set preview to False by default
			is_preview = False

			# Make sure the user has the right to see the preview
			if request.user.is_authenticated() and not preview == False:
				is_preview = True

			# Is it home page or not?
			if slug:
				slugs = slug.split('/')
				page = get_page(request=request, model_class=model_class, translation_class=translation_class, slug=slug, preview=is_preview)
			else:
				slugs = []
				page = get_page(request=request, model_class=model_class, translation_class=translation_class, preview=is_preview)

			# Raise a 404 if the page can't be found
			if not page:
				raise Http404('Not Found')

			# Hard redirect if specified in page attributes
			if page.redirect_to:
				return HttpResponseRedirect(page.redirect_to.get_absolute_url())

			# When you switch language it will load the right translation but stay on the same slug
			# So we need to redirect tio the right translated slug if not on it already
			page_url = page.get_absolute_url()

			if not page_url == request.path and slug:
				return HttpResponseRedirect(page_url)

			# Assign is_preview to the request object for cleanliness
			request.is_preview = is_preview

			return f(request, page, slug)
		return wrapper
	return wrap


@page_processor(model_class=Page, translation_class=PageTranslation)
def page(request, page, slug):

	# Get the root page and then all its descendants, including self
	if page.published_from == None:
		nodes = page.get_root().get_descendants(include_self=True)
	else:
		nodes = page.published_from.get_root().get_descendants(include_self=True)

	return render_to_response(page.template, {'page':page, 'nodes':nodes}, context_instance=RequestContext(request))


def search(request, directory=False):
	from whoosh.index import open_dir
	from whoosh.qparser import QueryParser
	from whoosh.query import And, Or, Term
	from django.utils.translation import get_language
	from django.contrib.contenttypes.models import ContentType
	template = 'cms/search.html'
	results_objects = []

	query = False
	root = False
	if request.POST:
		form = SearchForm(data=request.POST)
		if form.is_valid():

			language_code = get_language()
			#print "Selected language: %s" % language_code
			query = form.cleaned_data['query']
			ix = open_dir(settings.SEARCH_INDEX_PATH)

			with ix.searcher() as s:
				parser = QueryParser("content", ix.schema)
				myquery = parser.parse(query)
				# Filter results for our current language only
				allow_q = And([Term("language", language_code) , ])

				if directory:

					location = form.cleaned_data['location']

					category = Category.objects.get(id=location)
					root = u"%s"%category.published_from.get_root()

					restrict_q = Or([Term("content_type", u"page"), Term("content_type", u"event")])
					results = s.search(myquery, filter=allow_q, mask=restrict_q,  limit=None)
					template = 'cms/search_results.html'
				else:
					results = s.search(myquery, filter=allow_q, limit=None)
				#result_count = results.filtered_count

				results_objects = []

				for r in results:

					ct = ContentType.objects.get(model=r['content_type'].lower())
					obj_class = ct.model_class()
					obj = obj_class.objects.get(id=r['id'])



					if r['content_type'].lower() == 'event':
						result = {'title':obj.translated().title, 'url':obj.get_absolute_url(), 'breadcrumbs':obj.get_breadcrumbs(), 'content': obj.translated().description, 'content_type':r['content_type']}
					else:

						if root:
							if root not in obj.get_breadcrumbs():
								continue

						result = {'title':obj.translated().title, 'url':obj.get_absolute_url(), 'breadcrumbs':obj.get_breadcrumbs(), 'content': obj.translated().content, 'content_type':r['content_type']}
					results_objects.append(result)
	else:
		form = SearchForm()

	return render_to_response(template, {'query':query, 'results':results_objects, 'form':form, }, context_instance=RequestContext(request))



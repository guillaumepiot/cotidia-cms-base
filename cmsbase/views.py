import json

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import translation

from cmsbase.models import *
from cmsbase.forms import SearchForm


def get_page(request, slug=False, preview=False):

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
			translation = PageTranslation.objects.filter(slug=last_slug, parent__published_from=None)

			if translation.count() > 0:
				published.append(translation[0].parent)
		else:
			translation = PageTranslation.objects.filter(slug=last_slug).exclude(parent__published_from=None)

			if translation.count() > 0:
				published.append(translation[0].parent)

	else:
		if preview:
			published = Page.objects.filter(home=True, published_from=None)
		else:
			# translation = PageTranslation.objects.filter()
			published = Page.objects.filter(published=True, home=True).exclude(published_from=None)

	if len(published)> 0:
		published = published[0]
	else:
		published = False

	return published


def page(request, slug=False):

	context = {}

	preview = request.GET.get('preview', False)

	is_preview = False

	if request.user.is_authenticated() and preview:
		is_preview = True

	if slug:
		slugs = slug.split('/')
		page = get_page(request=request, slug=slug, preview=is_preview)
		discover = None
	else:
		slugs = []
		page = get_page(request=request, preview=is_preview)

	if not page:
		raise Http404('Not Found')

	if page.redirect_to:
		return HttpResponseRedirect(page.redirect_to.get_absolute_url())

	context['page'] = page

	if not is_preview:
		page_original = page.published_from
	else:

		page_original = page

	# page_original.get_default_url(slug)

	# if len(slugs) == 2:
	# 	navigation =  page_original.parent.get_descendants(include_self=False)
	# elif len(slugs) == 3:
	# 	navigation =  page_original.parent.parent.get_descendants(include_self=False)
	# elif len(slugs) == 4:
	# 	navigation =  page_original.parent.parent.parent.get_descendants(include_self=False)
	# else:
	# 	navigation =  page_original.get_children()
	# navigation =  page_original.get_children()
	# print page_original

	parents = page_original.get_ancestors(ascending=False, include_self=False)


	# print page_original.get_ancestors()
	navigation = []

	if parents:
		for parent in parents:
			if parent.is_root_node() == False:
				categories = parent.get_siblings(include_self=True)

				# Loop through
				for category in categories:
					# Only get Published objects
					if category.get_published():
						navigation.append(category)

					for child in category.get_children():
						if  parent == category:
						# print child
							navigation.append(child)
	else:
		navigation =  page_original.get_children()

	context['navigation'] = navigation

	children = page_original.get_children()
	context['children'] = children

	featured_events = Event.published.filter(featured=True)[:3]
	context['featured_events'] = featured_events


	return render_to_response(page.template, context, context_instance=RequestContext(request))


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


def set_language(request):

	from urlparse import urlsplit
	from django import http
	from django.utils.translation import check_for_language
	from localeurl import utils

	from agenda.models import Event, EventTranslation
	from twitterfeed import user_timeline, twitter_search
	from pinterestfeed import pinterest_feed

	"""
	Redirect to a given url while changing the locale in the path
	The url and the locale code need to be specified in the
	request parameters.
	"""

	# Default function from django-localurl
	next = request.REQUEST.get('next', None)



	if not next:
		next = urlsplit(request.META.get('HTTP_REFERER', None))[2]
	if not next:
			next = '/'
	_, path = utils.strip_path(next)
	if request.method == 'POST':

		locale = request.POST.get('locale', None)
		if locale and check_for_language(locale):
			path = utils.locale_path(path, locale)

	# Set the language to the language selected

	slug = next = request.REQUEST.get('next', None)
	response = http.HttpResponseRedirect(next)

	if hasattr(request, 'session'):
		request.session['django_language'] = locale
	else:
		response.set_cookie(settings.LANGUAGE_COOKIE_NAME, locale)
		# translation.activate(lang)

	translation.activate(locale)

	# Split the uri to individuals to compare the languages
	slugs = slug.split('/')

	if len(slugs) == 1:
		last_slug = slugs[len(slugs)-2]
		parent_slug = False
	elif len(slugs) > 1:
		last_slug = slugs[len(slugs)-2]
		parent_slug = slugs[len(slugs)-2]

	published = []

	object_translation = request.REQUEST.get('section', None)
	# Search through the database to find the slug that matches the last part of url
	translations = False

	if object_translation == 'page':
		translations = PageTranslation.objects.filter(slug=last_slug, parent__published_from=None)
	elif object_translation == 'Category':
		translations = CategoryTranslation.objects.filter(slug=last_slug, parent__published_from=None)
	elif object_translation == 'Event':

		translations = EventTranslation.objects.filter(slug=last_slug)
		# print translations
		# url = '/%s/dont-miss'%locale
		# return http.HttpResponseRedirect(next)

	page_original = False

	if translations != False:
		if translations.count() > 0 :
			page_original = translations[0].parent

	# When the page has been found.....

	if page_original != False:
		# Loop through database to find all tranlation for the page
		page_translation = page_original.get_translations()

		# Loop through all the transation and find the match it with the language asked, then redirect to the new language
		for page in page_translation:
			if page.language_code == locale:
				print page.parent.get_absolute_url()
				return http.HttpResponseRedirect(page.parent.get_absolute_url())

		# Redirect to same page but with default language

		return http.HttpResponseRedirect(page_original.get_absolute_url())
	else:

		url = '/%s'%locale

		return http.HttpResponseRedirect(url)

	if not slug:
		slug = request.META.get('HTTP_REFERER', None)
	if not slug:
		slug = '/'

    	return http.HttpResponseRedirect(next)

from django.conf.urls.defaults import * 

urlpatterns = patterns('cms', 

	#url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
	url(r'^$', 'views.page', name="home"),
	url(r'^search/$', 'views.search', name="search"),
	url(r'^set_language/$', 'views.set_language', name="set_language"),
	url(r'^search/(?P<directory>directory)/$', 'views.search', name="search"),
	url(r'^(?P<slug>[-\w\/]+)/$', 'views.page', name="page"),
	#url(r'^tag/(?P<tag>[-\w]+)/$', 'views.blog_tag', name="blog_tag"),
	#url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 'views.article', name="blog_article"),
	#url(r'^(?P<year>\d{4})/$', 'views.year', name='blog_year'),
	#url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/$', 'views.month', name="blog_month"),

)
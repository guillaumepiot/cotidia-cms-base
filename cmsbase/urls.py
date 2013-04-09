from django.conf.urls.defaults import *

urlpatterns = patterns('cmsbase',

	url(r'^$', 'views.page', name="home"),
	url(r'^search/$', 'views.search', name="search"),
	#url(r'^set_language/$', 'views.set_language', name="set_language"),
	url(r'^(?P<slug>[-\w\/]+)/$', 'views.page', name="page"),

)
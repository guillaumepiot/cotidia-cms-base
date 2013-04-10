from django.conf.urls.defaults import *

urlpatterns = patterns('cmsbase',

	url(r'^$', 'views.page', name="home"),
	url(r'^search/$', 'views.search', name="search"),
	url(r'^(?P<slug>[-\w\/]+)/$', 'views.page', name="page"),

)
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns('cmsbase',

	url(r'^$', 'views.page', name="home"),
	url(r'^search/$', 'views.search', name="search"),
	url(r'^(?P<slug>[-\w\/]+)/$', 'views.page', name="page"),

)
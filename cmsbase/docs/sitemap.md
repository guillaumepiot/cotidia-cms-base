Sitemap
=======

Cotidia CMS Base ships with a default xml sitemap generation, using the recommend Django way.

CMSbase defines a `CMSSitemap` class in `sitemap.py`.

Setup
-----

In `urls.py`, import the sitemap classes and build a sitemap dictionary:

	from cmsbase.sitemap import CMSSitemap

	sitemaps = {
		'cms': CMSSitemap,
	}


Then, add the following line in the `urlpatterns`:

	(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
	

Custom sitemaps
---------------

You can also define your own sitemap class, in the same way as CMS Base does it, and then simply add them to the sitemap dictionary.

Example:

	from cmsbase.sitemap import CMSSitemap
	from myapp.sitemap import AppSitemap

	sitemaps = {
		'cms': CMSSitemap,
		'myapp': AppSitemap,
	}
	

Template
--------

CMS Base is using a default template to render the sitemap located in `templates/sitemap.xml`.

You can override this template on a project basis.

Templates
=========

Base
----

The base html is copied from Tim Murtaugh's html5reset.org, and is located in 'templates/base.html'

Page blocks:

- {% block meta_title %}{% endblock %}: the meta title of page
- {% block meta_description %}{% endblock %}: the meta description of the page
- {% block google_site_verification %}{% endblock %}: the google webmaster verification code

Custom page templates
---------------------

You can add you own set of page templates by using the CMS_PAGE_TEMPLATES settings.

	CMS_PAGE_TEMPLATES = (
		('cmsbase/page.html', 'Default page'), # By default and mandatory, if no templates supplied, the page will not save
		('cmsbase/home.html', 'Home page'), # Optional project specific template
	)
	
	
Translation in templates
------------------------

In order to retrieve the right translated content depending on the current site language settings, you must call the `translated` method to retrieve the translated value.

For example:

	{{page.translated.title}}
	{{page.translated.content}}
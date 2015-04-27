---
layout: page
title: CMS settings
permalink: "settings.html"
---

CMS Base settings
=================

The following settings are available and can be overridden on a project basis.


`CMS_PAGE_TEMPLATES` Default = (('cmsbase/page.html', 'Default page'),)

List all available templates for the Page model.


`CMS_PAGE_IMAGES` Default = False

Enable to management on inline images for the Page model.


`CMS_PAGE_LINKS` Default = False

Enable to management on inline links for the Page model.


`CMS_PAGE_FILES` Default = False

Enable to management on inline links for the Page model.


`CMS_PAGE_RELATED_PAGES` Default = False

Enable to management of related pages.


`CMS_HASH_FILE_NAMES` Default = True

Decide whether or not to hash filename when uploaded.


## Custom page templates

You can add you own set of page templates by using the CMS_PAGE_TEMPLATES settings.

	CMS_PAGE_TEMPLATES = (
		('cmsbase/page.html', 'Default page'), # By default and mandatory, if no templates supplied, the page will not save
		('cmsbase/home.html', 'Home page'), # Optional project specific template
	)
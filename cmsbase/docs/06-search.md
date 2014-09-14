---
layout: page
title: Search
permalink: "search.html"
---

Search
======

Install Whoosh
--------------

CMS Base is using Whoosh to handle full text search and indexing.

You will need to install Whoosh 2.4.1 to enable the search feature:

	$ pip install Whoosh==2.4.1
	
	
Create the index
----------------

First you will need to verify your index path setting:

	# The path to save the search index initial
	SEARCH_INDEX_PATH =  = getattr(settings, 'SEARCH_INDEX_PATH', 'indexes')
	
**Note: If you are using a git repository, it is advised to ignore that folder (in .gitignore), as it is representaive of the local database. A production version site will create its own index.**
	
It is defaulted to 'indexes', but it is advised to set the path depending on your current project before creating the index.

CMS Base comes with the following default command:

	$ python manage.py update_search_index
	
This command will add the live pages to the index and also sort them by languages. This was way results should only be from the same language as the one current activated by the website user.


Include the search form
-----------------------

In your template, you will need to include a search form, example as follows:

	<form action="/search" method="get">
		<input type="text" placeholder="Search the site" name="query">
		<button type="button">Search</button>
	</form>
	
In the default CMS Base search view, the GET parameter for the search query must be "query". Though, you can create you own search view by replicating the code in `views.py` and write the search handling as required.


Search view template
--------------------

The default search view is `cmsbase/search.html` which can be overriden on a project basis if required.


Search index updating automation
--------------------------------

As generating the search index can be a process hungry task, it is recommend to run it daily as a scheduled task.

Use the following cron command to run it daily in a virtualenv:

	0 0 * * * /var/www/mysite/bin/python /var/www/mysite/myproject/manage.py update_search_index --settings=myproject.settings.staging
	
This command will run at 0:00 every day.

Please note that is it calling the python command via the vitualenv python binary.

The --settings argument is optional and depends on how your project is set up. Though, it will set in this way with a default CMS Base install.


Customising the index
---------------------

You can add more data to your index by copy update_search_index.py command to your project level and add the following code:


	from blog.models import Article
	from event.models import Event

	# Blog data (from cotidia-blog app)
	for page in Article.objects.get_published_live():
		content_type = ContentType.objects.get_for_model(Article)
		for translation in page.get_translations():
			writer.add_document(title=u"%s" % translation.title, content_type=u"%s" % content_type,
                id=u"%s" % page.id, language=u"%s" % translation.language_code, content=u"%s %s" % (translation.title, translation.content))

	# Events data (from cotidia-event app)
	for page in Event.objects.get_published_live():
		content_type = ContentType.objects.get_for_model(Event)
		for translation in page.get_translations():
			writer.add_document(title=u"%s" % translation.title, content_type=u"%s" % content_type,
                id=u"%s" % page.id, language=u"%s" % translation.language_code, content=u"%s %s" % (translation.title, translation.content))
                

Because Cotidia Blog and Cotidia Event inherit from the CMS Base Page classes, it is very easy to add those app to the search index. The view and template will require no update, as it recognise content-type for each app.

If you require to include a different type of app to the index, you will need to assign the right attributes
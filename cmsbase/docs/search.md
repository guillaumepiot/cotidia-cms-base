Search
======

Install Whoosh
--------------

CMS Base is using Whoosh to handle full text search and indexing.

You will need to install Whoosh to enable the search feature:

	$ pip install whoosh
	
	
Create the index
----------------

First you will need to verify your index path setting:

	# The path to save the search index initial
	SEARCH_INDEX_PATH =  = getattr(settings, 'SEARCH_INDEX_PATH', 'indexes')
	
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
Installation
============

Create a new folder for your project
------------------------------------

	$ mkdir myproject
	$ cd myproject

Create and start a virtual environment (higly recommended)
----------------------------------------------------------

	$ virtualenv .
	$ source bin/activate
	
Install CMS Base (which will also install all depencies)
--------------------------------------------------------

	$ pip install -e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cms-base.git#egg=cmsbase
	
> Since the project is under development, we install CMS Base in edit mode (-e) from the repository to enable bug fixing and improvements if required.






TO-DO: a fab file that run basic installation


Admin tools
-----------

Follow the setup instructions for the admin tools: https://bitbucket.org/guillaumepiot/cotidia-admin-tools

In settings:

- ADMIN_TOOLS_INDEX_DASHBOARD = 'cotidiacms.dashboard.CustomIndexDashboard'
- ADMIN_TOOLS_MENU = 'cotidiacms.menu.CustomMenu'


Context processor
-----------------

Create a default context processor: https://gist.github.com/guillaumepiot/5338169

And add it to your TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS = (
	    ...
	    "cotidiacms.context_processor.website_settings"
	)



Settings
--------

In settings.py, you will need to set the following settings that relates to your project:

- AUTHOR_URL = 'http://cotidia.com'
- AUTHOR = 'Cotidia Ltd'
- GOOGLE_SITE_VERIFICATION : Google webmaster verification code (optional)


In the database, you will need to setup the site name & domain.

- site.name
- site.domain

Add the following context processors:

	TEMPLATE_CONTEXT_PROCESSORS = (
	    "django.contrib.auth.context_processors.auth",
	    "django.core.context_processors.debug",
	    "django.core.context_processors.i18n",
	    "django.core.context_processors.media",
	    "django.core.context_processors.static",
	    "django.core.context_processors.tz",
	    "django.core.context_processors.request",
	    "django.contrib.messages.context_processors.messages",
	    "cotidiacms.context_processor.website_settings"
	)
	
Please note that "django.core.context_processors.request" is necessary to pass the request to the admin tools template tags.


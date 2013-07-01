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
	
Install CMS Base (which will also install some dependencies)
-----------------------------------------------------------

	$ pip install -e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-cms-base.git#egg=cmsbase
	
> Since the project is under development, we install CMS Base in edit mode (-e) from the repository to enable bug fixing and improvements if required.

Also install the dependencies underdevelopment:

	$ pip install -e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-admin-tools.git#egg=admin_tools
    $ pip install -e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-redactor.git#egg=redactor
    $ pip install -e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-filemanager.git#egg=filemanager
    $ pip install -e git+https://github.com/dokterbob/django-multilingual-model.git#egg=multilingual_model

If you don't to install it in development mode (for example on production server), use the following commands:

	$ pip install git+https://bitbucket.org/guillaumepiot/cotidia-cms-base.git
	$ pip install git+https://bitbucket.org/guillaumepiot/cotidia-admin-tools.git
    $ pip install git+https://bitbucket.org/guillaumepiot/cotidia-redactor.git
    $ pip install git+https://bitbucket.org/guillaumepiot/cotidia-filemanager.git
    $ pip install git+https://github.com/dokterbob/django-multilingual-model.git

Create a Django project
-----------------------

	$ django-admin.py startproject myproject

Setup the settings
------------------

First we set a staging/production settings method:

	$ cd myproject/myproject
	$ mkdir settings
	$ cp settings.py settings/__init__.py
	$ rm settings.py
	$ cd settings
	$ echo "from myproject.settings import *" > staging.py
	$ echo "from myproject.settings import *" > production.py

> This way we can call the adequate settings file in the server setup depending if we are in staging or production mode, while keeping all settings organised.


Settings configuration
----------------------

To facilitate our several path settings, we set the project path variable:

	import os

	PROJECT_DIR = os.path.dirname(__file__) 

Setup the local database, we recommend to use sqlite locally but feel free to any other database type.

	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
	        'NAME': 'dev/myproject.db',                      # Or path to database file if using sqlite3.
	    }
	}

Set the folder to contain the database, and make sure your path are correct whichever one you choose.

	$ mkdir dev

New in Django 1.5, setup a list ol allowed hosts for production environment:

	ALLOWED_HOSTS = ['.mydomain.com']

	# .mydomain.com is a wildcard for mydomain.com and all its sub-domains

More info on Django's website: [https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts](https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts)

Setup the media folder and url (where all uploaded will go), if any.

	MEDIA_ROOT = os.path.join(PROJECT_DIR, '../../media/')
	MEDIA_URL = '/media/'

We comment the STATIC_ROOT as we will using STATICFILES_DIRS instead.

	# Static root will be used for collecting static files for production deployment
	# Use the command: python manage.py collectstatic
	STATIC_ROOT = os.path.join(PROJECT_DIR, '../../static/')

	STATIC_URL = '/static/'

	# Here's where we save the project static files
	# Not be served in production mode
	STATICFILES_DIRS = (
	    os.path.join(PROJECT_DIR, "../static"),
	)

We insert the localeurl at the start of our middlewares, this will automatically add url language suffix if required.

	MIDDLEWARE_CLASSES = (
    	'localeurl.middleware.LocaleURLMiddleware',
    	...
    )


Context processor
-----------------

Create a default context processor, download a sample here [https://gist.github.com/guillaumepiot/5338169](https://gist.github.com/guillaumepiot/5338169) or enter the following command in the app folder of the same name as the project:

	$ curl https://gist.github.com/guillaumepiot/5338169/raw/9a7c956166b1f87a1b15d3f634f0218c2ea3fa9b/gistfile1.txt > context_processor.py

And add it to  TEMPLATE_CONTEXT_PROCESSORS

	TEMPLATE_CONTEXT_PROCESSORS = (
	    "django.contrib.auth.context_processors.auth",
	    "django.core.context_processors.debug",
	    "django.core.context_processors.i18n",
	    "django.core.context_processors.media",
	    "django.core.context_processors.static",
	    "django.core.context_processors.tz",
	    "django.core.context_processors.request",
	    "django.contrib.messages.context_processors.messages",

	    "myproject.context_processor.website_settings"
	)

> Please note that "django.core.context_processors.request" is necessary to pass the request to the admin tools template tags.


Apps
----

Include the required apps.

	INSTALLED_APPS = (

	    'admin_tools',
	    'admin_tools.menu',
	    'admin_tools.dashboard',
	    'admin_tools.liststyle',

	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.sites',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	    'django.contrib.admin',

	    'cmsbase',
	    'reversion',
	    'mptt',
	    'south',
	    'sorl.thumbnail',
	    'redactor',
	    'filemanager'
	)

Setup the templates path
------------------------

	TEMPLATE_DIRS = (
	    os.path.join(PROJECT_DIR, '../templates/')
	)


Admin panel settings
--------------------

Is it recommended to set the following variables to create a copyright notice in the admin footer:

	AUTHOR_URL = 'http://mydomain.com'
	AUTHOR = 'My project'
	#GOOGLE_SITE_VERIFICATION : Google webmaster verification code (optional)

Then, we must hook our menu and dashboard classes to generate the custom admin tools:

	ADMIN_TOOLS_INDEX_DASHBOARD = 'myproject.dashboard.CustomIndexDashboard'
	ADMIN_TOOLS_MENU = 'myproject.menu.CustomMenu'

Pull the default files from GIST automatically:

	$ curl https://gist.github.com/guillaumepiot/5391705/raw/ec10eda52976618f6f6e0a1a6efd54c95dfe2ce8/gistfile1.py > menu.py
	$ curl https://gist.github.com/guillaumepiot/5391722/raw/21d0eba942d22c8ef880703dc5701eade2569b01/gistfile1.py > dashboard.py

> You can follow the setup instructions for the admin tools here: [https://bitbucket.org/guillaumepiot/cotidia-admin-tools](https://bitbucket.org/guillaumepiot/cotidia-admin-tools)


Multilingual settings
---------------------

Include a tuple of enabled languages.

> Please note that if you include only one language, then the multilingual features will be disabled.

	LANGUAGES = (
	    ('en', 'English'),
	    # ('nl', 'Dutch'),
	    # ('es', 'Spanish'),
	    # ('pt', 'Portuguese'),
	    # ('de', 'German'),
	)
	DEFAULT_LANGUAGE = LANGUAGES[0][0]

	# Set the django language code to the default language
	LANGUAGE_CODE = DEFAULT_LANGUAGE

Include a list of URLs that doesn't require the language prefix

	LOCALE_INDEPENDENT_PATHS = (
	    r'^/admin/',
	    r'^/uploads/',
	)

	# Define wether or not to display the url prefix
	# False if we have only one language supported
	PREFIX_DEFAULT_LOCALE = False if len(LANGUAGES) <= 1 else True

Default URLS
------------

We recommend to pull the default URLs file from this gist: [https://gist.github.com/guillaumepiot/5392008/raw/ceb40367ced138d70ff0f8fe2ad31f1b474a4152/urls.py](https://gist.github.com/guillaumepiot/5392008/raw/ceb40367ced138d70ff0f8fe2ad31f1b474a4152/urls.py)

	$ curl https://gist.github.com/guillaumepiot/5392008/raw/ceb40367ced138d70ff0f8fe2ad31f1b474a4152/urls.py > urls.py

Or copy and paste the following code:

	from django.conf.urls import patterns, include, url
	from django.conf import settings
	from django.contrib import admin
	admin.autodiscover()

	urlpatterns = patterns('',
	    # URL language management
	    (r'^localeurl/', include('localeurl.urls')),
	    # Language switcher management
	    (r'^i18n/', include('django.conf.urls.i18n')),


	    # Admin
	    url(r'^admin/', include(admin.site.urls)),
	    # Text editor file uploads
	    url(r'^uploads/', include('filemanager.urls')),

	    # CMS base
	    url(r'^', include('cmsbase.urls', namespace='cms')),
	)

	if settings.DEBUG:
	    urlpatterns = patterns('',
	        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	    ) + urlpatterns

Sync the database
-----------------

	$ python manage.py syncdb
	$ python manage.py migrate --all

Set the site name and domain once logged in the admin.

That's it, now just start the site:

	$ python manage.py runserver


Possible issues
---------------

When saving the page model instance, you may encounter the following error:

	reversion_version.object_repr may not be NULL

This will happen if the Django LANGUAGE_CODE settings is not the same as the first available LANGUAGES. For example you may have 'en-us' and 'en' which don't match and will cause the page object to lack a unicode representation.




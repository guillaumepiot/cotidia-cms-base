---
layout: page
title: Installation
permalink: "install.html"
---

Install
=======

### Create a new folder for your project

    $ mkdir myproject
    $ cd myproject

### Create a Python 3 environment

    $ pyvenv venv
    $ source venv/bin/activate
    
###Install CMS Base (which will also install some dependencies)

    $ pip install -e git+https://github.com/Cotidia/cotidia-cms-base.git#egg=cmsbase
    
> Since the project is under development, we install CMS Base in edit mode (-e) from the repository to enable bug fixing and improvements if required.


##Automated installation

Copy `fabfile.py` from the cmsbase package to your working directory (next to the virtualenv folders):

    eg:
        bin/
        include/
        lib/
        src/
        fabfile.py
        
Run the installation command

    $ fab localhost install:project_name='myproject',mode='edit'



##Manual installation


Install the dependencies underdevelopment:

    $ pip install -e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-admin-tools.git#egg=admin_tools
    $ pip install -e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-filemanager.git#egg=filemanager
    $ pip install git+https://github.com/dokterbob/django-multilingual-model.git
    $ pip install django-form-utils==1.0.2

If you don't to install it in development mode (for example on production server), use the following commands:

    $ pip install git+https://bitbucket.org/guillaumepiot/cotidia-admin-tools.git
    $ pip install git+https://bitbucket.org/guillaumepiot/cotidia-filemanager.git
    $ pip install git+https://github.com/dokterbob/django-multilingual-model.git
    $ pip install django-form-utils==1.0.2

###Create a Django project

    $ django-admin.py startproject myproject

###Setup the settings

First we set a staging/production settings method:

    $ cd myproject/myproject
    $ mkdir settings
    $ cp settings.py settings/__init__.py
    $ rm settings.py
    $ cd settings
    $ echo "from myproject.settings import *" > staging.py
    $ echo "from myproject.settings import *" > production.py

> This way we can call the adequate settings file in the server setup depending if we are in staging or production mode, while keeping all settings organised.


###Settings configuration

New in Django 1.5, setup a list ol allowed hosts for production environment:

    ALLOWED_HOSTS = ['.mydomain.com']

    # .mydomain.com is a wildcard for mydomain.com and all its sub-domains

More info on Django's website: [https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts](https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts)

Setup the media folder and url (where all uploaded will go), if any.

    MEDIA_ROOT = os.path.join(BASE_DIR, '../../media/')
    MEDIA_URL = '/media/'

We comment the STATIC_ROOT as we will using STATICFILES_DIRS instead.

    # Static root will be used for collecting static files for production deployment
    # Use the command: python manage.py collectstatic
    STATIC_ROOT = os.path.join(BASE_DIR, '../../static/')

    STATIC_URL = '/static/'

    # Here's where we save the project static files
    # Not be served in production mode
    STATICFILES_DIRS = (
        os.path.join(PROJECT_DIR, "../static"),
    )


###Context processor

Create a default context processor, download a sample here [https://gist.github.com/guillaumepiot/5338169](https://gist.github.com/guillaumepiot/5338169) or enter the following command in the app folder of the same name as the project:

    $ curl https://gist.githubusercontent.com/guillaumepiot/5338169/raw/ > context_processor.py

And add it to  TEMPLATE_CONTEXT_PROCESSORS

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',

                    'myproject.context_processor.website_settings',
                ],
            },
        },
    ]

> Please note that "django.core.context_processors.request" is necessary to pass the request to the admin tools template tags.


### Apps

Include the required apps.

    INSTALLED_APPS = (
        'admin_tools',
        'admin_tools.menu',
        'admin_tools.dashboard',
        'admin_tools.liststyle',

        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',

        'cmsbase',
        'reversion',
        'mptt',
        'filemanager',
    )

### Middleware

Add the `LocaleMiddleware` to support localised urls.

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',

        'django.middleware.locale.LocaleMiddleware',
    )

### Admin panel settings

Is it recommended to set the following variables to create a copyright notice in the admin footer:

    AUTHOR_URL = 'http://mydomain.com'
    AUTHOR = 'My project'

Then, we must hook our menu and dashboard classes to generate the custom admin tools:

    ADMIN_TOOLS_INDEX_DASHBOARD = 'myproject.dashboard.CustomIndexDashboard'
    ADMIN_TOOLS_MENU = 'myproject.menu.CustomMenu'

Pull the default files from GIST automatically:

    $ curl https://gist.githubusercontent.com/guillaumepiot/5391705/raw/ > menu.py
    $ curl https://gist.githubusercontent.com/guillaumepiot/5391722/raw/ > dashboard.py

> You can follow the setup instructions for the admin tools here: [https://bitbucket.org/guillaumepiot/cotidia-admin-tools](https://bitbucket.org/guillaumepiot/cotidia-admin-tools)


### Multilingual settings

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

### Default URLS

We recommend to pull the default URLs file from this gist: [https://gist.github.com/guillaumepiot/5392008/raw/](https://gist.github.com/guillaumepiot/5392008/raw/)

    $ curl https://gist.githubusercontent.com/guillaumepiot/5392008/raw/  > urls.py

Or copy and paste the following code:

    from django.conf.urls import patterns, include, url
    from django.conf import settings
    from django.contrib import admin
    admin.autodiscover()

    urlpatterns = patterns('',

        # Password reset features
        url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
        url(r'^admin/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
        url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name="password_reset_confirm"),
        url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name="password_reset_complete"),

        # Admin
        url(r'^admin/i18n/', include('django.conf.urls.i18n')),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^uploads/', include('filemanager.urls')),

        # Front
        url(r'^', include('cmsbase.urls', namespace='cms')),
    )

    if settings.DEBUG:
        urlpatterns = patterns('',
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ) + urlpatterns

###Sync the database

    $ python manage.py migrate

Set the site name and domain once logged in the admin.

That's it, now just start the site:

    $ python manage.py runserver


###Possible issues

When saving the page model instance, you may encounter the following error:

    reversion_version.object_repr may not be NULL

This will happen if the Django LANGUAGE_CODE settings is not the same as the first available LANGUAGES. For example you may have 'en-us' and 'en' which don't match and will cause the page object to lack a unicode representation.




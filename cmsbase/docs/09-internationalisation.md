---
layout: page
title: Internationalisation
permalink: "internationalisation.html"
---

Internationalisation
====================

We require django-localeurl to manage language in urls and redirection:

    $ pip install django-localeurl==2.0.1

Language switcher
-----------------

In your template use the following code as a Bootstrap dropdown:

{% raw %} 
    <div class="btn-group pull-right">
      <span class="btn"><img src="/static/admin/img/flags/{{LANGUAGE_CODE}}.png" alt=""></span>
      <button class="btn dropdown-toggle" data-toggle="dropdown">
        {% trans "Language" %} &nbsp; <span class="caret"></span>
      </button>
      <ul class="dropdown-menu">
        {% for lang in LANGUAGES %}
        <li class="{% ifequal lang.0 LANGUAGE_CODE %}active{% endifequal %}">
            <form class="locale_switcher" method="POST" action="{% url 'localeurl_change_locale' %}">{% csrf_token %}
                <input type="hidden" name="locale" value="{{ lang.0 }}" />
                <a href="#" onclick="$(this).parent().submit()">{{ lang.1 }}</a>
            </form>
        </li>
        {% endfor %} 
      </ul>
    </div>

Or as a simple select box:

    <form id="locale_switcher" method="POST" action="{% url 'localeurl_change_locale' %}">{% csrf_token %}
        <select name="locale" onchange="$('#locale_switcher').submit()">
            {% for lang in LANGUAGES %}
                <option value="{{ lang.0 }}" {% ifequal lang.0 LANGUAGE_CODE %}selected="selected"{% endifequal %}>{{ lang.1 }}</option>
            {% endfor %}
        </select>
        <noscript>
            <input type="submit" value="Set" />
        </noscript>
    </form>
{% endraw %}  

Settings
--------

The default settings:

    LANGUAGES = (
        ('en', 'English'),
        # ('nl', 'Dutch'),
        # ('es', 'Spanish'),
        # ('pt', 'Portuguese'),
        # ('de', 'German'),
    )
    DEFAULT_LANGUAGE = LANGUAGES[0][0]

    LOCALE_INDEPENDENT_PATHS = (
        r'^/admin/',
        r'^/uploads/',
    )
    PREFIX_DEFAULT_LOCALE = False if len(LANGUAGES) == 1 else True


The LANGUAGES define all the supported languages for the application.

If the list equals 1, there's only one language and therefore the site is not multilingual, so we set the following value automatically:

    # Define wether or not to display the url prefix
    # False if we have only one language supported
    PREFIX_DEFAULT_LOCALE = False if len(LANGUAGES) == 1 else True
    
The LOCALE_INDEPENDENT_PATHS specify the urls that doesn't require localeurl support. Useful for the admin or api call such as the ajax file upload the Redactor text editor.


Translation files
-----------------

Django support gettext to manage text translation across the site.

We usually use transaltion files to manage small pieces or recurring text, such as button names, alert messages and so on.


> Note: Your server must have gettext install in order for translation to work. Download gettext here: http://www.gnu.org/software/gettext/

Run the following command on Ubuntu to install:

    $ aptitude install gettext libgettextpo-dev 


In settings.py, add the template directory to the variable LOCAL_PATHS:

    LOCALE_PATHS = (
        os.path.join(PROJECT_DIR, 'path/to/locale/'),
    )

- Create the locale folder
- In the project directory, run a command to harvest each language

    $ django-admin.py makemessages -l en

You can use includes to specify which files to crawl for translations:

    $ django-admin.py makemessages -l en -i "templates/admin*"



cd to the uncompressed folder

Install:

    $ ./configure
    $ make
    $ make install

Compile the language files

    $ django-admin.py compilemessages


Manage translation in the Admin
-------------------------------

We use Rosetta to manage the translations.

    $ pip install django-rosetta


Add 'rosetta' to your INSTALLED_APPS

Add to urls.py:

    url(r'^admin/rosetta/', include('rosetta.urls')),

Add the menu.py (from the admin nav bar):

    items.MenuItem(_('Translations'), reverse('rosetta-pick-file')),

You can now input the translations for the each language.

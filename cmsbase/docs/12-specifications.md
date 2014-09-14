---
layout: page
title: Specifications
permalink: "specifications.html"
---

Specifications
==============

Publishing
----------

The CMS must support a publishing workflow which maintain an original version of each entry and automatically generate a clone that will be used a published version.
All related models (including inlines) should be cloned/removed accordingly.


Moderation
----------

Each model includes a "can_publish" permission, which will be used to create moderators. Any user with the "can_publish" permission will be able to publish (clone) the original version to a published version, others will only be able to edit a non-publish version, which can then be moderated accordingly.


Status
------

Above the publishing workflow, each model should be able to get un-published by setting a active boolean to False, which will un-publish the "cloned" version.


Internationalisation
--------------------

Each model should support internationalisation. Each translated content will be managed by a related object. If internationalisation is not required, then the translation should be hidden, leaving the option for a future internationalisation if required. 


Search
------

The CMS should generate a search index made of a selection of models, and a management command sould be available to update the index via a schedule task.


Media management
----------------

To manage images, we will use Sorl-Tumbnail to generate images at different sizes.

The system should support cloud files management by using django-cumulus.

-e git+https://github.com/orpo/django-cumulus.git#egg=cumulus


Text editor
-----------

All content text editor should be enabled with Redactor, the best wysiwyg I know out there.

	$ -e git+https://bitbucket.org/guillaumepiot/cotidia-redactor.git

File upload
-----------

All file upload within the wysiwyg should be handle by Filemanager which plugs nicely with Redactor
  
	$ -e git+https://bitbucket.org/guillaumepiot/cotidia-filemanager.git 
	
	

Admin UI
--------

The admin UI should be extended with Cotidia Admin Tools, though the CMS Base should work without it as a fallback


Deployment
----------

A fabfile in place should allow a complete new project generation executing the following:

- Generate a Django project
- Download and install all dependencies of CMS Base
- Create a default settings environment for staging & production, by pulling template setting files from GIST.
	- Regenerate a secret key
- Create a default URLs conf included the admin
- Create a dev folder to hold local db if sqlite3
- Sync the database as SQLlite

Options should include

- name (project name) ! Required
- db (type of db: postgresql_psycopg2, mysql, sqlite3 or oracle) Default = sqlite3
- multilingual (Boolean) Default = False

A typical fab command would look like:

	$ fab createproject:name=my_project,db=sqlite3,multilingual=False
	
	
Asset management
----------------

The deployment should use Bower to manage asset packages such as Twitter Bootstrap, jQuery
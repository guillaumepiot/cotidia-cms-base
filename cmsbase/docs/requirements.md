Requirements
============

###django==1.6
The framework.

###django-mptt==0.6
The management system for pages tree. The most efficient way I know so far.

###django-reversion==1.8
Add page history and recover old edits.

### cotidia-admin-tools
The admin UI.
	-e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-admin-tools.git#egg=admin_tools

### cotidia-redactor
The Redactor app from Cotidia (please buy your own license please for the Redactor JS source!) http://imperavi.com/redactor/
	-e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-redactor.git#egg=redactor

### cotidia-filemanager
Allow file upload for Cotidia redactor.
	-e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-filemanager.git#egg=filemanager

### django-multilingual-model	
Default model to manage multiple inline translations
	-e git+https://github.com/dokterbob/django-multilingual-model.git#egg=multilingual_model
	
### pillow
Image processing and validating.

### south
Database migration management.

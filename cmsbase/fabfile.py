# Run as local
import sys 
from fabric.api import *

def localhost():
   # Setup localhost
    env.run = local
    env.cd = lcd
    env.hosts = ['localhost'] 

def install(project_name='', mode='edit'):

    if project_name == '':
        raise Exception('Please specify a project name: fab localhost install:project_name=mysite')

    print 'Starting installation...'

    if mode=='edit':
        env.run('pip install -e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-admin-tools.git#egg=admin_tools')
        env.run('pip install -e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-redactor.git#egg=redactor')
        env.run('pip install -e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-filemanager.git#egg=filemanager')
        env.run('pip install -e git+https://github.com/dokterbob/django-multilingual-model.git#egg=multilingual_model')

    elif mode=='production':
        env.run('pip install git+https://bitbucket.org/guillaumepiot/cotidia-admin-tools.git')
        env.run('pip install git+https://bitbucket.org/guillaumepiot/cotidia-redactor.git')
        env.run('pip install git+https://bitbucket.org/guillaumepiot/cotidia-filemanager.git')
        env.run('pip install git+https://github.com/dokterbob/django-multilingual-model.git')


    print "Setting up Django project"

    with settings(warn_only=True):
        if env.run("cd %s" % project_name).failed:
            env.run('django-admin.py startproject %s' % project_name)

    with env.cd('%s/%s' % (project_name, project_name)):
        with settings(warn_only=True):
            if env.run("cd settings").failed:
                env.run('mkdir settings')
                env.run('cp settings.py settings/__init__.py')
                env.run('rm settings.py')

        with env.cd('settings'):
            env.run('echo "from %s.settings import * \n\nDEBUG=False\nTEMPLATE_DEBUG=DEBUG\n\nALLOWED_HOSTS = []" > staging.py' % project_name)
            env.run('echo "from %s.settings import * \n\nDEBUG=False\nTEMPLATE_DEBUG=DEBUG\n\nALLOWED_HOSTS = []" > production.py' % project_name)

    


    with env.cd('%s/%s' % (project_name, project_name)):
        # CMS Base default settings
        env.run('curl https://gist.github.com/guillaumepiot/6766868/raw/72d53822a1573f309a0326e71f15338b717c0b06/gistfile1.py > settings/__init__.py')
        # Replace project name in settings file
        env.run("cd settings && sed -i .bak 's/{{myproject}}/%s/g' __init__.py" % project_name)
        env.run("cd settings && rm __init__.py.bak")
        # Context processor
        env.run('curl https://gist.github.com/guillaumepiot/5338169/raw/08cc845e2e2fcf8c19ebe9f6127112f20adb2f70/gistfile1.txt > context_processor.py')
        # Admin menu
        env.run('curl https://gist.github.com/guillaumepiot/5391705/raw/ec10eda52976618f6f6e0a1a6efd54c95dfe2ce8/gistfile1.py > menu.py')
        # Admin dashboard
        env.run('curl https://gist.github.com/guillaumepiot/5391722/raw/21d0eba942d22c8ef880703dc5701eade2569b01/gistfile1.py > dashboard.py')
        # URLs conf
        env.run('curl https://gist.github.com/guillaumepiot/5392008/raw/a5dd62e07bc981df703b47ca6867dc296b187d5c/urls.py > urls.py')

    with env.cd('%s' % (project_name)):
        # Create folder for sqlite3 database
        with settings(warn_only=True):
            if env.run("cd dev").failed:
                env.run('mkdir dev')
        env.run('python manage.py syncdb')
        env.run('python manage.py migrate --all')

        print 'Installation complete!'

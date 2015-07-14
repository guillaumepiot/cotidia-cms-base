# Run as local
import sys, random
from fabric.api import *

# Generate a secret key for Django settings.py
def generate_secret_key():
    return ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])


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
        env.run('pip install -e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-filemanager.git#egg=filemanager')
        env.run('pip install git+https://github.com/dokterbob/django-multilingual-model.git')
        env.run('pip install django-form-utils==1.0.2')

    elif mode=='production':
        env.run('pip install git+https://bitbucket.org/guillaumepiot/cotidia-admin-tools.git')
        env.run('pip install git+https://bitbucket.org/guillaumepiot/cotidia-filemanager.git')
        env.run('pip install git+https://github.com/dokterbob/django-multilingual-model.git')
        env.run('pip install django-form-utils==1.0.2')


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
        env.run('curl https://gist.githubusercontent.com/guillaumepiot/6766868/raw/ > settings/__init__.py')
        # Replace project name in settings file
        env.run("cd settings && sed -i .bak 's/{{myproject}}/%s/g' __init__.py" % project_name)
        env.run("cd settings && sed -i .bak 's/{{secretkey}}/%s/g' __init__.py" % generate_secret_key())
        env.run("cd settings && rm __init__.py.bak")
        # Context processor
        env.run('curl https://gist.githubusercontent.com/guillaumepiot/5338169/raw/ > context_processor.py')
        # Admin menu
        env.run('curl https://gist.githubusercontent.com/guillaumepiot/5391705/raw/ > menu.py')
        # Admin dashboard
        env.run('curl https://gist.githubusercontent.com/guillaumepiot/5391722/raw/ > dashboard.py')
        # URLs conf
        env.run('curl https://gist.githubusercontent.com/guillaumepiot/5392008/raw/ > urls.py')

    with env.cd('%s' % (project_name)):
        # Create folder for sqlite3 database
        with settings(warn_only=True):
            if env.run("cd dev").failed:
                env.run('mkdir dev')
        env.run('python manage.py migrate')
        env.run('python manage.py createsuperuser')

        print 'Installation complete!'

import os
from distutils.core import setup
from setuptools import find_packages


VERSION = __import__("cmsbase").VERSION

CLASSIFIERS = [
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
]

install_requires = [
    'django==1.5.1',
    'django-mptt==0.5.5',
    'django-reversion==1.7',
    'django-localeurl==1.5',
    'PIL==1.1.7',
    'sorl-thumbnail==11.12',
    'south==0.7.6',
    # The following must be installed manually until they are packaged adequately
    #'-e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-admin-tools.git#egg=admin_tools',
    #'-e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-redactor.git#egg=redactor',
    #'-e git+https://guillaumepiot@bitbucket.org/guillaumepiot/cotidia-filemanager.git#egg=filemanager',
    #'-e git+https://github.com/dokterbob/django-multilingual-model.git#egg=multilingual_model',
]

# taken from django-registration
# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('cmsbase'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:

        ################################################################################
        # !!! IMPORTANT !!!                                                            #
        # To get the right prefix, enter the index key of the same                     #
        # value as the length of your package folder name, including the slash.        #
        # Eg: for 'cmsbase/'' , key will be 8                                          #
        ################################################################################

        prefix = dirpath[8:] # Strip "cmsbase/" or "cmsbase\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

setup(
    name="cotidia-cms-base",
    description="Django application to manage content publishing",
    version=VERSION,
    author="Guillaume Piot",
    author_email="guillaume@cotidia.com",
    url="https://bitbucket.org/guillaumepiot/cotidia-cms-base",
    download_url="https://bitbucket.org/guillaumepiot/cotidia-cms-base/downloads/cotidia-cms-base-%s.tar.gz" % VERSION,
    package_dir={'cmsbase': 'cmsbase'},
    packages=packages,
    package_data={'cmsbase': data_files},
    include_package_data=True,
    install_requires=install_requires,
    classifiers=CLASSIFIERS,
)

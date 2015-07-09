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
    'django==1.8.3',
    'django-mptt==0.7.0',
    'django-reversion==1.8.6',
    'pillow',
    'django-codemirror-widget',
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
    description="An extensible CMS based on Django, including dynamic page fields in JSON datasets, multilingual localisation and publishing workflow.",
    version=VERSION,
    author="Guillaume Piot",
    author_email="guillaume@cotidia.com",
    url="https://github.com/Cotidia/django-cms-base",
    download_url="https://github.com/Cotidia/django-cms-base/archive/%s.tar.gz" % VERSION,
    package_dir={'cmsbase': 'cmsbase'},
    packages=packages,
    package_data={'cmsbase': data_files},
    include_package_data=True,
    install_requires=install_requires,
    classifiers=CLASSIFIERS,
)

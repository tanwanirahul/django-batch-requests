#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import batch_requests

from setuptools import setup
from setuptools import setup, Command

class PyTest(Command):
    '''
        A command handler for setup.py test.
    '''
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call('py.test --cov-report html --cov batch_requests tests/', shell=True)
        raise SystemExit(errno)

name = 'django-batch-requests'
version = batch_requests.__version__
package = 'batch_requests'
description = 'Create batch APIs for Django.'
long_description = 'Django batch requests allow developers to combine multiple http requests into a single batch request. This is essentially useful to avoid making multiple http requests to save on round trip network latency.'
url = 'https://github.com/tanwanirahul/django-batch-requests'
author = 'Rahul Tanwani'
author_email = 'tanwanirahul@gmail.com'
license = 'MIT'
install_requires = []


def read(*paths):
    """
    Build a file path from paths and return the contents.
    """
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a {0} -m 'version {0}'".format(version))
    print("  git push --tags")
    sys.exit()


setup(
    name=name,
    version=version,
    url=url,
    license=license,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    packages=get_packages(package),
    package_data=get_package_data(package),
    install_requires=install_requires,
    cmdclass = {'test': PyTest},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP'
    ]
)

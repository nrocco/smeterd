#!/usr/bin/env python
import re
from setuptools import setup


def _version():
    with open('smeterd/__init__.py', 'r') as the_file:
        version = re.search(r'^__version__ ?= ?\'([0-9\.]+)\'', the_file.read()).group(1)
    return version

setup(
    name = 'smeterd',
    version = _version(),
    packages = [
        'smeterd'
    ],
    url = 'http://nrocco.github.io/',
    download_url = 'http://github.com/nrocco/smeterd/tags',
    author = 'Nico Di Rocco',
    author_email = 'dirocco.nico@gmail.com',
    description = 'Read smart meter P1 packets',
    long_description = open('README.rst').read(),
    license = open('LICENSE').read(),
    include_package_data = True,
    install_requires = [
        'pyserial==2.6',
        'pycli-tools>=1.6.0',
    ],
    package_data = {
    },
    entry_points = {
        'console_scripts': [
            'smeterd = smeterd.command:parse_and_run',
        ]
    },
    classifiers = [
        'Development Status :: 5 - Production/Stable',
         'Operating System :: OS Independent',
         'Programming Language :: Python :: 2.6',
         'Programming Language :: Python :: 2.7',
         'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

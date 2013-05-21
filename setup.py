#!/usr/bin/env python
from setuptools import setup
import smeterd



setup(
    name = 'smeterd',
    version = smeterd.__version__,
    packages = [
        'smeterd'
    ],
    url = 'http://nrocco.github.io/',
    download_url = 'http://github.com/nrocco/smeterd/tags',
    author = smeterd.__author__,
    author_email = 'dirocco.nico@gmail.com',
    description = smeterd.__description__,
    include_package_data = True,
    install_requires = [
        'pyserial==2.6',
        'bottle==0.11.6',
        'bottle-sqlite==0.1.2',
        'pycli-tools==1.5',
        'Jinja2==2.6'
    ],
    dependency_links = [
    ],
    entry_points = {
        'console_scripts': [
            'smeterd = smeterd.main:parse_and_run',
        ]
    },
    classifiers = [
        'Development Status :: 5 - Production/Stable',
         'Operating System :: OS Independent',
         'Programming Language :: Python :: 2.6',
         'Programming Language :: Python :: 2.7',
         'Topic :: Internet :: WWW/HTTP',
         'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

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

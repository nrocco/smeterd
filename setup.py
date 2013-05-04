#!/usr/bin/env python
from setuptools import setup


setup(
    name='smeterd',
    version='1.5',
    packages=['smeterd'],
    url='http://nrocco.github.io/',
    author='Nico Di Rocco',
    author_email='dirocco.nico@gmail.com',
    description="Read smart meter P1 packets",
    include_package_data=True,
    install_requires=['pyserial==2.6'],
    entry_points = {
        'console_scripts': [
            'smeterd = smeterd.main:parse_and_run',
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
         'Operating System :: OS Independent',
         'Programming Language :: Python :: 2.6',
         'Programming Language :: Python :: 2.7',
         'Topic :: Internet :: WWW/HTTP',
         'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

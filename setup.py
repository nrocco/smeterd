#!/usr/bin/env python
import re
import io
import codecs

from setuptools import setup, find_packages


def load_requirements(filename):
    with io.open(filename, encoding='utf-8') as reqfile:
        return [line.strip() for line in reqfile if not line.startswith('#')]


setup(
    name='smeterd',
    description='Read smart meter P1 packets',
    version='2.9.0',
    author='Nico Di Rocco',
    author_email='dirocco.nico@gmail.com',
    url='https://github.com/nrocco/smeterd',
    license='GPLv3',
    long_description=codecs.open('README.md', 'rb', 'utf-8').read(),
    download_url='https://github.com/nrocco/smeterd/tags',
    include_package_data=True,
    install_requires=load_requirements('requirements.txt'),
    tests_require=[
        'coverage',
    ],
    entry_points={
        'console_scripts': [
            'smeterd=smeterd.cli:cli',
        ]
    },
    packages=find_packages(exclude=['tests']),
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
)

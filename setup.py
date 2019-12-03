#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Define the setup options."""

try:
    import distribute_setup
    distribute_setup.use_setuptools()
except:
    pass

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import os
import re


with open(os.path.join(os.path.dirname(__file__), 
        'src','cacophonyapi', '__init__.py')) as f:
    version = re.search("__version__ = '([^']+)'", f.read()).group(1)

with open('requirements.txt', 'r') as f:
    requires = [x.strip() for x in f if x.strip()]

with open('test-requirements.txt', 'r') as f:
    test_requires = [x.strip() for x in f if x.strip()]

with open('README.md', 'r') as f:
    readme = f.read()


setup(
    name='cacophonyapi',
    version=version,
    description="Cacophony Project REST API client for python",
    long_description=readme,
    url='https://github.com/TheCacophonyProject/python-api',
    license='GNU AFFERO GENERAL PUBLIC License 3 19 November 2007',
    packages=find_packages(exclude=['tests']),
    test_suite='nose2.collector.collector',
    # test_suite='tests',
    tests_require=test_requires,
    install_requires=requires,
    extras_require={'test': test_requires},

    # metadata to display on PyPI
    author="Anthony Uphof, Giampaolo Ferraro, Cameron Ryan-Pears, Menno Finlay-Smits",
    author_email="coredev@cacophony.org.nz",
    keywords="cacophonyproject api client rest",

    project_urls={
        "Bug Tracker": 'https://github.com/TheCacophonyProject/python-api',
        "Documentation": 'https://docs.cacophony.org.nz',
        "Source Code": 'https://github.com/TheCacophonyProject/python-api',
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

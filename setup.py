#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys

from setuptools import setup
from setuptools import find_packages


with io.open('README.md', 'rt', encoding='utf8') as f:
    README = f.read()

if sys.argv[-1] == 'test':
    os.system('python -sm unittest discover tests "*_test.py"')
    sys.exit(0)

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist')
    os.system('twine upload dist/*')
    sys.exit(0)

VERSION = '0.0.7'
REQUIRES = ['google-api-python-client>=1.5.3', 'pandas>=0.22.0', 'fire>=0.1.3']
GITHUB_URL = 'https://github.com/condad/google-objects'

setup(
    name='google_objects',
    packages=find_packages(),
    version=VERSION,
    description="A simple OO wrapper around Google's python API client",
    long_description=README,
    long_description_content_type='text/markdown',
    author='Connor Sullivan',
    author_email='sully4792@gmail.com',
    install_requires=REQUIRES,
    url=GITHUB_URL,
    download_url='https://github.com/condad/google-objects/tarball/' + VERSION,
    keywords=['google api', 'google sheets', 'google drive', 'google slides'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={
        'console_scripts': [
            'sheets-cli = google_objects.cli:main',
        ],
    },
)

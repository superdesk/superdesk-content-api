#!/usr/bin/env python
# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014, 2015 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license


from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.download import PipSession


LONG_DESCRIPTION = open('README.md').read()
REQUIREMENTS = [str(ir.req) for ir in parse_requirements('requirements.txt', session=PipSession())
                if not (getattr(ir, 'link', False) or getattr(ir, 'url', False))]

setup(
    name='Superdesk-Public-API',
    version='0.0.1-dev',
    description='Superdesk PUBLIC API REST server',
    long_description=LONG_DESCRIPTION,
    author='adrian magdas',
    author_email='adrian.magdas@sourcefabric.org',
    url='https://github.com/superdesk/superdesk-public-content_api',
    license='GPLv3',
    platforms=['any'],
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    scripts=[ 'content_api_manage.py' ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)

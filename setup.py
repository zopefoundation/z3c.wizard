##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import os
from setuptools import setup, find_packages


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


setup(
    name='z3c.wizard',
    version='1.0',
    author="Roger Ineichen and the Zope Community",
    author_email="zope-dev@zope.org",
    description="Wizard based on z3c.form for for Zope3",
    long_description='\n\n'.join([
        read('README.txt'),
        '.. contents::',
        read('src', 'z3c', 'wizard', 'README.txt'),
        read('src', 'z3c', 'wizard', 'zcml.txt'),
        read('CHANGES.txt'),
    ]),
    license="ZPL 2.1",
    keywords="zope zope3 z3c form wizard",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
    url='https://github.com/zopefoundation/z3c.wizard',
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    extras_require=dict(
        test=[
            'z3c.macro',
            'zope.app.pagetemplate',
            'zope.app.testing',
            'zope.publisher',
            'zope.testing',
            'zope.browserresource',
        ],
    ),
    install_requires=[
        'setuptools',
        'z3c.form >= 2.0',
        'z3c.formui',
        'z3c.pagelet',
        'zope.browserpage',
        'zope.component',
        'zope.configuration',
        'zope.event',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.location',
        'zope.publisher',
        'zope.schema',
        'zope.security',
        'zope.traversing',
    ],
    zip_safe=False,
)

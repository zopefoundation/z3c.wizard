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

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


setup(
    name='z3c.wizard',
    version='2.0.dev0',
    author="Roger Ineichen and the Zope Community",
    author_email="zope-dev@zope.dev",
    description="Wizard based on z3c.form for for Zope3",
    long_description='\n\n'.join([
        read('README.rst'),
        '.. contents::',
        read('src', 'z3c', 'wizard', 'README.rst'),
        read('src', 'z3c', 'wizard', 'zcml.rst'),
        read('CHANGES.rst'),
    ]),
    license="ZPL 2.1",
    keywords="zope zope3 z3c form wizard",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope :: 3',
    ],
    url='https://github.com/zopefoundation/z3c.wizard',
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    python_requires='>=3.7',
    extras_require=dict(
        test=[
            'z3c.macro',
            'zope.app.pagetemplate',
            'zope.app.testing',
            'zope.browserresource',
            'zope.publisher',
            'zope.testing',
            'zope.testrunner',
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

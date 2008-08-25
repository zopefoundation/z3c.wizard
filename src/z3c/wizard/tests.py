##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
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
"""Wizard button actions implementation
$Id:$
"""
__docformat__ = "reStructuredText"

import unittest
import zope.interface
from zope.testing import doctest
from zope.publisher.browser import TestRequest

import z3c.testing
from z3c.wizard import interfaces
from z3c.wizard import wizard
from z3c.wizard import step
from z3c.wizard import testing


class IContentStub(zope.interface.Interface):
    """Content stub marker."""


class ContentStub(object):
    """Content stub."""

    zope.interface.implements(IContentStub)

    def values(self):
        pass


class StepTestClass(step.Step):
    """Simple test step."""


class WizardTestClass(wizard.Wizard):
    """Wizard Test class providing a step."""

    baseURL = '#'

    def __init__(self, context, request):
        super(WizardTestClass, self).__init__(context, request)
        self.step = StepTestClass(context, request, self)
        self.step.__name__ = 'first'
        self.step.__parent__ = self


def setStubs():
    zope.component.provideAdapter(StepTestClass,
        (IContentStub, None, None), provides=interfaces.IStep, name='first')
    zope.component.provideAdapter(StepTestClass,
        (IContentStub, None, None), provides=interfaces.IStep, name='last')


class TestStep(z3c.testing.InterfaceBaseTest):

    def setUp(self):
        setStubs()

    def getTestInterface(self):
        return interfaces.IStep

    def getTestClass(self):
        return step.Step

    def getTestPos(self):
        content = ContentStub()
        request = TestRequest()
        wiz = wizard.Wizard(content, request)
        return (content, request, wiz)


class TestWizard(z3c.testing.InterfaceBaseTest):

    def setUp(self):
        setStubs()

    def getTestInterface(self):
        return interfaces.IWizard

    def getTestClass(self):
        return WizardTestClass

    def getTestPos(self):
        return (ContentStub(), TestRequest())



def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('README.txt',
            setUp=testing.setUp, tearDown=testing.tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            ),
        doctest.DocFileSuite('zcml.txt',
            setUp=testing.setUp, tearDown=testing.tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,),
        unittest.makeSuite(TestStep),
        unittest.makeSuite(TestWizard),
        ))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

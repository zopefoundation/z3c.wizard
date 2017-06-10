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
"""Wizard button actions implementation."""

from zope.interface.verify import verifyObject, verifyClass
from zope.publisher.browser import TestRequest
import doctest
import unittest
import zope.interface

from z3c.wizard import interfaces
from z3c.wizard import wizard
from z3c.wizard import step
from z3c.wizard import testing


class IContentStub(zope.interface.Interface):
    """Content stub marker."""


@zope.interface.implementer(IContentStub)
class ContentStub(object):
    """Content stub."""

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
    zope.component.provideAdapter(
        StepTestClass,
        (IContentStub, None, None), provides=interfaces.IStep, name='first')
    zope.component.provideAdapter(
        StepTestClass,
        (IContentStub, None, None), provides=interfaces.IStep, name='last')


class TestStep(unittest.TestCase):

    def setUp(self):
        setStubs()

    def test_verifyClass(self):
        self.assertTrue(verifyClass(interfaces.IStep, step.Step))

    def test_verifyObject(self):
        content = ContentStub()
        request = TestRequest()
        wiz = wizard.Wizard(content, request)
        step_inst = step.Step(content, request, wiz)
        self.assertTrue(verifyObject(interfaces.IStep, step_inst))


class TestWizard(unittest.TestCase):

    def setUp(self):
        setStubs()

    def test_verifyClass(self):
        self.assertTrue(verifyClass(interfaces.IWizard, wizard.Wizard))

    def test_verifyObject(self):
        wiz = WizardTestClass(ContentStub(), TestRequest())
        self.assertTrue(verifyObject(interfaces.IWizard, wiz))


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.txt',
            setUp=testing.setUp, tearDown=testing.tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
        ),
        doctest.DocFileSuite(
            'zcml.txt',
            setUp=testing.setUp, tearDown=testing.tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,),
        unittest.makeSuite(TestStep),
        unittest.makeSuite(TestWizard),
    ))

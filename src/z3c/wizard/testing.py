##############################################################################
#
# Copyright (c) 2008-2009 Zope Foundation and Contributors.
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
from zope.app.pagetemplate import metaconfigure
from zope.app.testing import setup
import z3c.macro.tales
import zope.i18n.interfaces
import zope.i18n.negotiator


###############################################################################
#
# testing setup
#
###############################################################################

def setUp(test):
    test.globs = {'root': setup.placefulSetUp(True)}

    zope.component.provideUtility(zope.i18n.negotiator.Negotiator(),
                                  zope.i18n.interfaces.INegotiator)
    metaconfigure.registerType('macro', z3c.macro.tales.MacroExpression)


def tearDown(test):
    setup.placefulTearDown()

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

from z3c.form import button
from z3c.wizard import interfaces


class WizardButtonActions(button.ButtonActions):
    """Wizard Button Actions."""

    @property
    def backActions(self):
        return [action for action in self.values()
                if interfaces.IBackButton.providedBy(action.field)]

    @property
    def forwardActions(self):
        return [action for action in self.values()
                if interfaces.INextButton.providedBy(action.field)]

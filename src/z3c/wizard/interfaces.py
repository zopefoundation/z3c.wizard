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
import zope.i18nmessageid
import zope.interface
import zope.location.interfaces
import zope.schema
from z3c.form import button
from z3c.form import interfaces
from z3c.pagelet.interfaces import IPagelet


_ = zope.i18nmessageid.MessageFactory('z3c')


class IBackButton(interfaces.IButton):
    """A button that redirects to the previous step."""


class INextButton(interfaces.IButton):
    """A button that redirects to the next step."""


class IWizardButtons(zope.interface.Interface):
    """Wizard button interfaces."""

    back = button.Button(
        title=_('Back'),
        condition=lambda form: form.showBackButton)
    zope.interface.alsoProvides(back, (IBackButton,))

    next = button.Button(
        title=_('Next'),
        condition=lambda form: form.showNextButton)
    zope.interface.alsoProvides(next, (INextButton,))

    complete = button.Button(
        title=_('Complete'),
        condition=lambda form: form.showCompleteButton)
    zope.interface.alsoProvides(complete, (INextButton,))


class IStep(interfaces.IForm, IPagelet):
    """An interface marking a step sub-form."""

    available = zope.schema.Bool(
        title='Available',
        description='Marker for available step',
        default=True,
        required=False)

    visible = zope.schema.Bool(
        title='Show step in wizard step menu',
        description='Show step in wizard step menu',
        default=True,
        required=False)

    showRequired = zope.schema.Bool(
        title='Show required label',
        description='Show required label',
        default=True,
        required=False)

    weight = zope.schema.Int(
        title='Step weight in wizard',
        description='Step weight in wizard',
        default=0,
        required=False)

    completed = zope.schema.Bool(
        title='Completed',
        description='Marker for completed step',
        default=False,
        required=False)

    handleApplyOnBack = zope.schema.Bool(
        title='Handle apply changes on back',
        description='Handle apply changes on back will force validation',
        default=False,
        required=False)

    handleApplyOnNext = zope.schema.Bool(
        title='Handle apply changes on next',
        description='Handle apply changes on next will force validation',
        default=True,
        required=False)

    handleApplyOnComplete = zope.schema.Bool(
        title='Handle apply changes on complete',
        description='Handle apply changes on complete will force validation',
        default=True,
        required=False)

    showSaveButton = zope.schema.Bool(
        title='Show save button',
        description='Show save button',
        default=True,
        required=False)

    showBackButton = zope.schema.Bool(
        title='Show back button',
        description='Back button condition',
        default=True,
        required=False)

    showNextButton = zope.schema.Bool(
        title='Show next button',
        description='Next button condition',
        default=True,
        required=False)

    showCompleteButton = zope.schema.Bool(
        title='Show complete button',
        description='Complete button condition',
        default=True,
        required=False)

    def goToStep(stepName):
        """Redirect to step by name."""

    def goToNext():
        """Redirect to next step."""

    def goToBack():
        """Redirect to back step."""

    def applyChanges(data):
        """Generic form save method taken from z3c.form.form.EditForm."""

    def doHandleApply(action):
        """Extract data and calls applyChanges."""

    def doBack(action):
        """Process back action and return True on sucess."""

    def doNext(action):
        """Process next action and return True on sucess."""

    def doComplete(action):
        """Process complete action and return True on sucess."""

    def update():
        """Update the step."""

    def render():
        """Render the step content w/o wrapped layout."""

    def __call__():
        """Compute a response body including the layout"""


class IWizard(zope.location.interfaces.ILocation):
    """An interface marking the controlling wizard form."""

    firstStepAsDefault = zope.schema.Bool(
        title='Show first step as default',
        description='Show first step or first not completed step as default',
        default=True,
        required=True)

    adjustStep = zope.schema.Bool(
        title='Adjust step',
        description='Force fallback (redirect) to last incomplete step',
        default=True,
        required=False)

    confirmationPageName = zope.schema.ASCIILine(
        title='Confirmation page name',
        description='The confirmation page name shown after completed',
        default=None,
        required=False)

    cssActive = zope.schema.ASCIILine(
        title='Active step menu CSS class',
        description='The active step menu CSS class',
        default='selected',
        required=False)

    cssInActive = zope.schema.ASCIILine(
        title='In-Active step menu item CSS class',
        description='The in-active step menu item CSS class',
        default=None,
        required=False)

    stepInterface = zope.interface.Attribute('Step lookup interface.')

    steps = zope.interface.Attribute(
        """List of one or more IStep (can be lazy).""")

    stepMenu = zope.interface.Attribute("""Step menu info.""")

    step = zope.schema.Object(
        title='Current step',
        description='Current step',
        schema=IStep)

    completed = zope.schema.Bool(
        title='Completed',
        description='Marker for completed step',
        default=False,
        required=False)

    isFirstStep = zope.schema.Bool(
        title='Is first step',
        description='Is first step',
        default=False,
        required=False)

    isLastStep = zope.schema.Bool(
        title='Is last step',
        description='Is last step',
        default=False,
        required=False)

    previousStepName = zope.schema.TextLine(
        title='Previous step name',
        description='Previous step name',
        default=None,
        required=False)

    nextStepName = zope.schema.TextLine(
        title='Next step name',
        description='Next step name',
        default=None,
        required=False)

    def doAdjustStep():
        """Ensure traversal is only possible up to first not completed step.

        Trying to traverse to another step redirects to the first incomplete
        one.
        """

    def getDefaultStep():
        """Can return the first or first not completed step as default."""

    def updateActions():
        """Update wizard actions."""

    def publishTraverse(request, name):
        """Traverse to step by it's name."""

    def browserDefault(request):
        """The default step is our browserDefault traversal setp."""

    def goToStep(stepName):
        """Redirect to the step by name."""

    def goToBack():
        """Redirect to next step if previous get sucessfuly processed."""

    def goToNext():
        """Redirect to next step if previous get sucessfuly processed."""

    def doBack(action):
        """Process something if back action get exceuted."""

    def doNext(action):
        """Process something if next action get exceuted."""

    def doComplete(action):
        """Process something if complete action get exceuted."""

    def doFinish():
        """Process something on complete wizard."""

    def update():
        """Adjust step and update actions."""

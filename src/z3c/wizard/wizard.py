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
import zope.component
import zope.interface
from zope.publisher.interfaces import NotFound
from zope.traversing.browser import absoluteURL

from z3c.form import button
from z3c.formui import form
from z3c.wizard import interfaces
from z3c.wizard.button import WizardButtonActions


def nameStep(step, name):
    """Give a step a __name__."""
    step.__name__ = name
    return step


@zope.interface.implementer(interfaces.IWizard)
class Wizard(form.Form):
    """Wizard form.

    The wizard is responsible for manage the steps and offers the wizard menu
    navigation and knows the step order. The wizard can check the conditions
    given from the steps. The wizard is also responsible for delegate the
    back, next and complete actions to the steps.

    This IWizard object is modelled as a Controller known from the MVC
    (Model, view, controller) patter version 2.0 and the step is implemented as
    a view.
    """

    buttons = button.Buttons(interfaces.IWizardButtons)

    # customize this part if needed
    stepInterface = interfaces.IStep

    firstStepAsDefault = True
    adjustStep = True
    confirmationPageName = None
    nextURL = None

    cssActive = 'selected'
    cssInActive = None  # None will skip class attribute in DOM element

    # for internal use
    __name__ = None
    steps = None
    step = None

    @property
    def baseURL(self):
        return absoluteURL(self, self.request)

    def setUpSteps(self):
        """Return a list of steps. This implementation uses IStep adapters.

        Take a look at the addStep method defined in step.py. This method
        allows you to setup steps directly in the method and offers an API for
        customized step setup.
        """
        steps = list(zope.component.getAdapters(
            (self.context, self.request, self), self.stepInterface))
        return [nameStep(step, name) for name, step in steps]

    def filterSteps(self, steps):
        """Make sure to only select available steps and we give a name."""
        return [step for step in steps if step.available]

    def orderSteps(self, steps):
        # order steps by it's weight
        return sorted(steps, key=lambda step: step.weight)

    @property
    def steps(self):
        steps = self.setUpSteps()
        steps = self.filterSteps(steps)
        return self.orderSteps(steps)

    @property
    def completed(self):
        for step in self.steps:
            if not step.completed:
                return False
        return True

    @property
    def isFirstStep(self):
        """See interfaces.IWizard"""
        return self.step and self.step.__name__ == self.steps[0].__name__

    @property
    def isLastStep(self):
        """See interfaces.IWizard"""
        return self.step and self.step.__name__ == self.steps[-1].__name__

    @property
    def showBackButton(self):
        """Ask the step."""
        return self.step and self.step.showBackButton

    @property
    def showNextButton(self):
        """Ask the step."""
        return self.step and self.step.showNextButton

    @property
    def showCompleteButton(self):
        """Ask the step."""
        return self.step.showCompleteButton

    @property
    def previousStepName(self):
        if self.step is None:
            return
        stepNames = [step.__name__ for step in self.steps]
        idx = stepNames.index(self.step.__name__)
        if idx == 0:
            return
        return stepNames[idx - 1]

    @property
    def nextStepName(self):
        if self.step is None:
            return
        stepNames = [step.__name__ for step in self.steps]
        idx = stepNames.index(self.step.__name__)
        if idx == len(stepNames) - 1:
            return
        return stepNames[idx + 1]

    @property
    def stepMenu(self):
        items = []
        append = items.append
        lenght = len(self.steps) - 1
        for idx, step in enumerate(self.steps):
            firstStep = False
            lastStep = False
            if step.visible:
                isSelected = self.step and self.step.__name__ == step.__name__
                cssClass = isSelected and self.cssActive or self.cssInActive
                if idx == 0:
                    firstStep = True
                if idx == lenght:
                    lastStep = True
                append({
                    'name': step.__name__,
                    'title': step.label,
                    'number': str(idx + 1),
                    'url': '%s/%s' % (self.baseURL, step.__name__),
                    'selected': self.step.__name__ == step.__name__,
                    'class': cssClass,
                    'first': firstStep,
                    'last': lastStep
                })
        return items

    def getDefaultStep(self):
        """Can return the first or first not completed step as default."""
        # return first step if this option is set
        if self.firstStepAsDefault:
            return self.steps[0]
        # return first not completed step
        for step in self.steps:
            if not step.completed:
                return step
        # fallback to first step if all steps completed
        return self.steps[0]

    def doAdjustStep(self):
        # Make sure all previous steps got completed. If not, redirect to the
        # last incomplete step
        if not self.adjustStep:
            return False
        for step in self.steps:
            if step.__name__ is self.step.__name__:
                break
            if not step.completed:
                # prepare redirect to not completed step and return True
                self.nextURL = '%s/%s' % (self.baseURL, step.__name__)
                return True
        # or return False
        return False

    def updateActions(self):
        self.actions = WizardButtonActions(self, self.request, self.context)
        self.actions.update()

    def update(self):
        if self.doAdjustStep():
            return
        self.updateActions()

    def publishTraverse(self, request, name):
        """Traverse to step by it's name."""
        # Remove HTML ending
        if '.' in name:
            rawName = name.rsplit('.', 1)[0]
        else:
            rawName = name
        # Find the active step
        for step in self.steps:
            if step.__name__ == rawName:
                self.step = step
                return self.step
        raise NotFound(self, name, request)

    def browserDefault(self, request):
        """The default step is our browserDefault traversal setp."""
        if self.step is None:
            step = self.getDefaultStep()
        # always return default step as default view for our wizard
        return self, (step.__name__,)

    def goToStep(self, stepName):
        self.nextURL = '%s/%s' % (self.baseURL, stepName)

    def goToBack(self):
        # redirect to next step if previous get sucessfuly processed
        self.goToStep(self.previousStepName)

    def goToNext(self):
        # redirect to next step if previous get sucessfuly processed
        self.goToStep(self.nextStepName)

    def doBack(self, action):
        if self.step.doBack(action):
            self.goToBack()

    def doNext(self, action):
        if self.step.doNext(action):
            self.goToNext()

    def doComplete(self, action):
        if self.step.doComplete(action):
            # do finsih after step get completed is completed
            self.doFinish()

    def doFinish(self):
        """Force redirect after doComplete if confirmationPageName is given."""
        if self.confirmationPageName is not None:
            self.nextURL = '%s/%s' % (
                absoluteURL(self.context, self.request),
                self.confirmationPageName)

    @button.handler(interfaces.IWizardButtons['back'])
    def handleBack(self, action):
        self.doBack(action)

    @button.handler(interfaces.IWizardButtons['next'])
    def handleNext(self, action):
        self.doNext(action)

    @button.handler(interfaces.IWizardButtons['complete'])
    def handleComplete(self, action):
        self.doComplete(action)

    def render(self, *args, **kws):
        raise NotImplementedError('render is no supported')

    def __repr__(self):
        return "<%s '%s'>" % (self.__class__.__name__, self.__name__)

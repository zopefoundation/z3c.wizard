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
import zope.event
import zope.lifecycleevent

from z3c.form.interfaces import IDataManager
from z3c.form import button
from z3c.formui import form
from z3c.wizard import interfaces
from z3c.wizard.interfaces import _


def addStep(self, name, label=None, weight=None, available=None, **kws):
    step = zope.component.getMultiAdapter((self.context, self.request, self),
                                          interfaces.IStep, name=name)
    step.__name__ = name
    if label is not None:
        step.label = label
    if weight is not None:
        step.weight = weight
    if available is not None:
        step.available = available
    for name, value in kws.items():
        setattr(step, name, value)
    return step


@zope.interface.implementer(interfaces.IStep)
class Step(form.Form):
    """Wizard base step implementation.

    The step offers hooks for action handlers for all wizard actions. The step
    can also provide own actions and handlers. This actions get rendered as
    step actions. Between the back an next wizard actions.

    A step can access the context or any object which you return by the
    getContent method. See z3c.form for more info about that. If you need a
    complexer wizard setup, you probably have to use a session and store
    temporary collected values in the session and store it if the wizard will
    call doComplete on the last step or in the wizard itself. Such a session
    is not a part of this implementation. This wizard implementation works
    on any context like other z3c.form IForm implementations. For more infos
    see z3c.form which this wizard is based on.
    """

    label = None
    available = True
    visible = True
    weight = 0
    showRequired = True

    handleApplyOnBack = False
    handleApplyOnNext = True
    handleApplyOnComplete = True

    # button condition
    showSaveButton = True

    formErrorsMessage = _('There were some errors.')
    successMessage = _('Data successfully updated.')
    noChangesMessage = _('No changes were applied.')

    def __init__(self, context, request, wizard):
        self.context = context
        self.request = request
        self.wizard = self.__parent__ = wizard

    @property
    def showBackButton(self):
        """Back button condition."""
        return not self.wizard.isFirstStep

    @property
    def showNextButton(self):
        """Next button condition."""
        return not self.wizard.isLastStep

    @property
    def showCompleteButton(self):
        """Complete button condition."""
        return self.wizard.isLastStep and self.wizard.completed

    @property
    def nextURL(self):
        """Next step URL known by wizard."""
        return self.wizard.nextURL

    @property
    def completed(self):
        """Simple default check for find out if a step is complete.

        This method will ensure that we store at least all required form values
        and that this values are valid. You can implement any other or
        additional condition in your custom step implementation.
        """
        content = self.getContent()
        for field in self.fields.values():
            if not field.field.required:
                continue
            dm = zope.component.getMultiAdapter(
                (content, field.field), IDataManager)
            if dm.query(
                    field.field.missing_value) is field.field.missing_value:
                return False
        return True

    def goToStep(self, stepName):
        self.wizard.goToStep(stepName)

    def goToNext(self):
        self.wizard.goToNext()

    def goToBack(self):
        self.wizard.goToBack()

    def applyChanges(self, data):
        """Generic form save method taken from z3c.form.form.EditForm."""
        content = self.getContent()
        changes = form.applyChanges(self, content, data)
        # ``changes`` is a dictionary; if empty, there were no changes
        if changes:
            # Construct change-descriptions for the object-modified event
            descriptions = []
            for interface, names in changes.items():
                descriptions.append(
                    zope.lifecycleevent.Attributes(interface, *names))
            # Send out a detailed object-modified event
            zope.event.notify(
                zope.lifecycleevent.ObjectModifiedEvent(
                    content, *descriptions))
        return changes

    def doHandleApply(self, action):
        """Extract data and calls applyChanges."""
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return False
        changes = self.applyChanges(data)
        if changes:
            self.status = self.successMessage
        else:
            self.status = self.noChangesMessage
        return True

    def doBack(self, action):
        """Process back action and return True on success."""
        if self.handleApplyOnBack:
            return self.doHandleApply(action)
        return True

    def doNext(self, action):
        """Process next action and return True on success."""
        if self.handleApplyOnNext:
            return self.doHandleApply(action)
        return True

    def doComplete(self, action):
        """Process complete action and return True on success."""
        if self.handleApplyOnComplete:
            return self.doHandleApply(action)
        return True

    def update(self):
        # setup wizard actions
        self.wizard.update()
        if self.nextURL is not None:
            # abort and do redirect in render method
            return
        # update and execute step actions
        super(Step, self).update()
        # execute wizard actions
        self.wizard.actions.execute()

    def render(self):
        # render content template
        if self.nextURL is not None:
            self.request.response.redirect(self.nextURL)
            return u''
        return super(Step, self).render()

    def __repr__(self):
        return "<%s '%s'>" % (self.__class__.__name__, self.__name__)


class EditStep(Step):
    """Step with default save button action."""

    @button.buttonAndHandler(_('Apply'), name='apply')
    def handleApply(self, action):
        self.doHandleApply(action)


class UnavailableStep(Step):
    """A step that is not available.

    This class is particularly useful for turning off an adapter step.
    """

    available = False

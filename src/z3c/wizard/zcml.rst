=========================
Wizard and Step directive
=========================

Show how we can use the ``wizard`` and ``wizardStep``
directives. Register the meta configuration for the directive.

  >>> import sys
  >>> from zope.configuration import xmlconfig
  >>> import z3c.wizard
  >>> context = xmlconfig.file('meta.zcml', z3c.wizard)

We need also a custom wizard class:

  >>> import z3c.wizard
  >>> class MyWizard(z3c.wizard.wizard.Wizard):
  ...     """Custom wizard"""

Make them available under the fake package `custom`:

  >>> sys.modules['custom'] = type(
  ...     'Module', (),
  ...     {'MyWizard': MyWizard})()

Register a wizard within the directive with minimal attributes:

  >>> context = xmlconfig.string("""
  ... <configure
  ...     xmlns:z3c="http://namespaces.zope.org/z3c">
  ...   <z3c:wizard
  ...       name="wizard"
  ...       class="custom.MyWizard"
  ...       permission="zope.Public"
  ...       />
  ... </configure>
  ... """, context)

Now define a step,

  >>> import z3c.wizard
  >>> class FirstStep(z3c.wizard.step.Step):
  ...     """First step"""

register the new step classes in the custom module

  >>> sys.modules['custom'].FirstStep = FirstStep

and use them in the ``wizardStep`` directive:

  >>> context = xmlconfig.string("""
  ... <configure
  ...     xmlns:z3c="http://namespaces.zope.org/z3c">
  ...   <z3c:wizardStep
  ...       name="first"
  ...       wizard="custom.MyWizard"
  ...       class="custom.FirstStep"
  ...       permission="zope.Public"
  ...       />
  ... </configure>
  ... """, context)

Let's get the wizard

  >>> import zope.component
  >>> from zope.publisher.browser import TestRequest
  >>> wizard = zope.component.queryMultiAdapter((object(), TestRequest()),
  ...     name='wizard')

and check it:

  >>> wizard
  <MyWizard 'wizard'>

  >>> z3c.wizard.interfaces.IWizard.providedBy(wizard)
  True

Let's get the wizard step

  >>> import zope.component
  >>> from zope.publisher.browser import TestRequest
  >>> firstStep = zope.component.queryMultiAdapter(
  ...     (object(), TestRequest(), wizard), name='first')

and check it

  >>> firstStep
  <FirstStep 'first'>

  >>> firstStep.context
  <object object at ...>

  >>> firstStep.wizard
  <MyWizard 'wizard'>

  >>> z3c.wizard.interfaces.IStep.providedBy(firstStep)
  True

  >>> z3c.wizard.interfaces.IWizard.providedBy(firstStep.wizard)
  True

Clean up the custom module:

  >>> del sys.modules['custom']

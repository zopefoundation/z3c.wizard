======
Wizard
======

The goal of this package is to offer a form wizard. This implementation doesn't
use a session. It just offers the wizard logic, the data which the wizard will
changes or add is not a part of this implementation. If you liek to implement
some add wizard logic you probably need to use a session anf collect the values
in the different wizard steps and create and add an object in the wizard
doComplete or doFinish or the step doComplete method.

All steps are available by it's own url. This allows us to cache each step if
needed. Each step url is only available if we are allowed to access a step. If
a step is accessible depends on the conditions of each step.

Since steps are adapters, we can register steps for already existing wizards
or we can also ovreride existing steps by register a UnavailableStep step which 
always will return False for the ``available`` argument.

If the wizard is completed we get redirected to the confirmation page. If we
access a completed wizard again, we will get redirected to the confirmation 
page again.

Now let's show how this works and setup our tests.


Form support
------------

We need to setup the form defaults first:

  >>> from z3c.form.testing import setupFormDefaults
  >>> setupFormDefaults()

And load the formui confguration, which will make sure that all macros get 
registered correctly.

  >>> from zope.configuration import xmlconfig
  >>> import zope.component
  >>> import zope.viewlet
  >>> import zope.app.component
  >>> import zope.app.publisher.browser
  >>> import z3c.macro
  >>> import z3c.template
  >>> import z3c.formui
  >>> xmlconfig.XMLConfig('meta.zcml', zope.component)()
  >>> xmlconfig.XMLConfig('meta.zcml', zope.viewlet)()
  >>> xmlconfig.XMLConfig('meta.zcml', zope.app.component)()
  >>> xmlconfig.XMLConfig('meta.zcml', zope.app.publisher.browser)()
  >>> xmlconfig.XMLConfig('meta.zcml', z3c.macro)()
  >>> xmlconfig.XMLConfig('meta.zcml', z3c.template)()
  >>> xmlconfig.XMLConfig('configure.zcml', z3c.formui)()

And load the z3c.wizard macro configuration:

  >>> import z3c.wizard
  >>> xmlconfig.XMLConfig('configure.zcml', z3c.wizard)()


Sample data setup
-----------------

Let's define a sample content class:

  >>> import zope.interface
  >>> import zope.schema
  >>> from zope.schema.fieldproperty import FieldProperty
  >>> class IPerson(zope.interface.Interface):
  ...     """Person interface."""
  ...  
  ...     firstName = zope.schema.TextLine(title=u'First Name')
  ...     lastName = zope.schema.TextLine(title=u'Last Name')
  ...     street = zope.schema.TextLine(title=u'Street')
  ...     city = zope.schema.TextLine(title=u'City')

  >>> class Person(object):
  ...     """Person content."""
  ...     zope.interface.implements(IPerson)
  ... 
  ...     firstName = FieldProperty(IPerson['firstName'])
  ...     lastName = FieldProperty(IPerson['lastName'])
  ...     street = FieldProperty(IPerson['street'])
  ...     city = FieldProperty(IPerson['city'])

Setup a person for our wizard:

  >>> person = Person()
  >>> root['person'] = person
  >>> person.__parent__ = root
  >>> person.__name__ = u'person'


Step
----

Let's define some steps. First use a step which knows how to store the name
of a person.

  >>> from z3c.form import form
  >>> from z3c.form import field
  >>> from z3c.wizard import step

  >>> class PersonStep(step.EditStep):
  ...     label = u'Person'
  ...     fields = field.Fields(IPerson).select('firstName', 'lastName')

And another step for collect some address data:

  >>> class AddressStep(step.EditStep):
  ...     label = u'Address'
  ...     fields = field.Fields(IPerson).select('street', 'city')


Wizard
------

Now we can define our ``Wizard`` including our steps. Steps are named
adapters. Let's use the global method addStep for doing the step setup:

  >>> from z3c.wizard import wizard
  >>> class IPersonWizard(z3c.wizard.interfaces.IWizard):
  ...     """Person wizard marker."""

  >>> class PersonWizard(wizard.Wizard):
  ... 
  ...     zope.interface.implements(IPersonWizard)
  ...
  ...     label = u'Person Wizard'
  ... 
  ...     def setUpSteps(self):
  ...         return [
  ...             step.addStep(self, 'person', weight=1),
  ...             step.addStep(self, 'address', weight=2),
  ...             ]

As next, we need to register our steps as named IStep adapters. This can be 
done by the z3c:wizardStep directive. Let's define our adapters with the 
provideAdapter method for now:

  >>> import zope.interface
  >>> from zope.publisher.interfaces.browser import IDefaultBrowserLayer
  >>> from zope.publisher.interfaces.browser import IBrowserRequest
  >>> import z3c.wizard.interfaces
  >>> zope.component.provideAdapter(
  ...     PersonStep, (None, IBrowserRequest, None),
  ...     z3c.wizard.interfaces.IStep, name='person')

  >>> zope.component.provideAdapter(
  ...     AddressStep, (None, IBrowserRequest, None),
  ...     z3c.wizard.interfaces.IStep, name='address')

We need to support the div form layer for our request. This is needed for the
form part we usein our steps. Because our steps are forms:

  >>> from z3c.formui.interfaces import IDivFormLayer
  >>> from zope.interface import alsoProvides
  >>> from z3c.form.testing import TestRequest
  >>> request = TestRequest()
  >>> alsoProvides(request, IDivFormLayer)

Now we can use our wizard. Our wizard will allways force to traverse to the 
current active step. This means the wizard provides a browserDefault which 
returns the default step instead of render the wizard as view. This allows us 
to use the step as an adapter discriminator for viewlets and other adapters 
like the menu implementation uses. The wizard acts like a dispatcher to the 
right step and not as a view itself.

  >>> personWizard = PersonWizard(person, request)
  >>> personWizard.__parent__ = person
  >>> personWizard.__name__ = u'wizard'

Now get the default view (step) arguments from the wizard:

  >>> obj, names = personWizard.browserDefault(request)
  >>> obj
  <PersonWizard u'wizard'>
  
  >>> names
  ('person',)

Now traverse to the step, update and render them:

  >>> personStep = obj.publishTraverse(request, names[0])
  >>> personStep.update()
  >>> print personStep.render()
  <div class="wizard">
      <div class="header">Person Wizard</div>
      <div class="wizardMenu">
        <span class="selected">
            <span>Person</span>
        </span>
        <span>
            <a href="http://127.0.0.1/person/wizard/address">Address</a>
        </span>
      </div>
    <form action="http://127.0.0.1" method="post"
          enctype="multipart/form-data" class="edit-form"
          id="form">
        <div class="viewspace">
            <div class="label">Person</div>
            <div class="required-info">
               <span class="required">*</span>
               &ndash; required
            </div>
          <div class="step">
            <div id="form-widgets-firstName-row" class="row">
                <div class="label">
                  <label for="form-widgets-firstName">
                    <span>First Name</span>
                    <span class="required">*</span>
                  </label>
                </div>
                <div class="widget"><input type="text" id="form-widgets-firstName"
                         name="form.widgets.firstName"
                         class="text-widget required textline-field" value="" />
              </div>
            </div>
            <div id="form-widgets-lastName-row" class="row">
                <div class="label">
                  <label for="form-widgets-lastName">
                    <span>Last Name</span>
                    <span class="required">*</span>
                  </label>
                </div>
                <div class="widget"><input type="text" id="form-widgets-lastName"
                         name="form.widgets.lastName"
                         class="text-widget required textline-field" value="" />
              </div>
            </div>
          </div>
            <div>
              <div class="buttons">
                <span class="back">
                </span>
                <span class="step">
                  <input type="submit" id="form-buttons-apply"
                         name="form.buttons.apply"
                         class="submit-widget button-field" value="Apply" />
                </span>
                <span class="forward">
                  <input type="submit" id="form-buttons-next"
                         name="form.buttons.next"
                         class="submit-widget button-field" value="Next" />
                </span>
              </div>
            </div>
        </div>
    </form>
  </div>


We can't go to the next step if we not complete the first step:

  >>> request = TestRequest(form={'form.buttons.next': 'Next'})
  >>> alsoProvides(request, IDivFormLayer)
  >>> personWizard = PersonWizard(person, request)
  >>> personWizard.__parent__ = person
  >>> personWizard.__name__ = u'wizard'
  >>> personStep = personWizard.publishTraverse(request, names[0])
  >>> personStep.update()
  >>> print personStep.render()
  <div class="wizard">
  ...
    <div class="summary">There were some errors.</div>
  ...
    <div class="error">Required input is missing.</div>
  ...
    <div class="error">Required input is missing.</div>
  ...


We can complete this step if we fill in the required values and click next:

  >>> request = TestRequest(form={'form.widgets.firstName': u'Roger',
  ...                             'form.widgets.lastName': u'Ineichen',
  ...                             'form.buttons.next': 'Next'})
  >>> alsoProvides(request, IDivFormLayer)
  >>> personWizard = PersonWizard(person, request)
  >>> personWizard.__parent__ = person
  >>> personWizard.__name__ = u'wizard'
  >>> personStep = personWizard.publishTraverse(request, names[0])
  >>> personStep.update()
  >>> print personStep.render()

As you can see the step get processed and the wizard will redirect to the next
step using the response redirect concept:

  >>> personWizard.nextURL
  'http://127.0.0.1/person/wizard/address'

Let's access the next step using the traverser. This will setup the next step
and tehm.

  >>> request = TestRequest()
  >>> alsoProvides(request, IDivFormLayer)
  >>> personWizard = PersonWizard(person, request)
  >>> personWizard.__parent__ = person
  >>> personWizard.__name__ = u'wizard'

As you can see we see our next step is the address step:

  >>> addressStep = personWizard.publishTraverse(request, 'address')
  >>> addressStep
  <AddressStep 'address'>

Update and render them:

  >>> addressStep.update()
  >>> print addressStep.render()
  <div class="wizard">
      <div class="header">Person Wizard</div>
      <div class="wizardMenu">
        <span>
            <a href="http://127.0.0.1/person/wizard/person">Person</a>
        </span>
        <span class="selected">
            <span>Address</span>
        </span>
      </div>
    <form action="http://127.0.0.1" method="post"
          enctype="multipart/form-data" class="edit-form"
          id="form">
        <div class="viewspace">
            <div class="label">Address</div>
            <div class="required-info">
               <span class="required">*</span>
               &ndash; required
            </div>
          <div class="step">
            <div id="form-widgets-street-row" class="row">
                <div class="label">
                  <label for="form-widgets-street">
                    <span>Street</span>
                    <span class="required">*</span>
                  </label>
                </div>
                <div class="widget"><input type="text" id="form-widgets-street"
                         name="form.widgets.street"
                         class="text-widget required textline-field" value="" />
              </div>
            </div>
            <div id="form-widgets-city-row" class="row">
                <div class="label">
                  <label for="form-widgets-city">
                    <span>City</span>
                    <span class="required">*</span>
                  </label>
                </div>
                <div class="widget"><input type="text" id="form-widgets-city"
                         name="form.widgets.city"
                         class="text-widget required textline-field" value="" />
              </div>
            </div>
          </div>
            <div>
              <div class="buttons">
                <span class="back">
                  <input type="submit" id="form-buttons-back"
                         name="form.buttons.back"
                         class="submit-widget button-field" value="Back" />
                </span>
                <span class="step">
                  <input type="submit" id="form-buttons-apply"
                         name="form.buttons.apply"
                         class="submit-widget button-field" value="Apply" />
                </span>
                <span class="forward">
                </span>
              </div>
            </div>
        </div>
    </form>
  </div>

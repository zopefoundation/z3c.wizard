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
import zope.interface
import zope.component
import zope.schema
import zope.configuration.fields
import zope.security.checker
import zope.security.zcml
from zope.configuration.exceptions import ConfigurationError
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from zope.browserpage.metaconfigure import _handle_for
from zope.browserpage.metaconfigure import _handle_permission
from zope.browserpage.metaconfigure import _handle_allowed_interface
from zope.browserpage.metaconfigure import _handle_allowed_attributes

import z3c.pagelet.zcml

from z3c.wizard import interfaces
from z3c.wizard import step
from z3c.wizard import wizard


class IWizardDirective(z3c.pagelet.zcml.IPageletDirective):
    """A directive to register a new wizard.

    The wizard directive also supports an undefined set of keyword arguments
    that are set as attributes on the wizard after creation.
    """


class IWizardStepDirective(zope.interface.Interface):
    """A directive to register a new wizard step.

    The wizard step directive also supports an undefined set of keyword
    arguments that are set as attributes on the wizard step after creation.
    """

    name = zope.schema.TextLine(
        title=u"The name of the pagelet.",
        description=u"The name shows up in URLs/paths. For example 'foo'.",
        required=True)

    class_ = zope.configuration.fields.GlobalObject(
        title=u"Class",
        description=u"A class that provides attributes used by the pagelet.",
        required=True)

    permission = zope.security.zcml.Permission(
        title=u"Permission",
        description=u"The permission needed to use the pagelet.",
        required=True)

    for_ = zope.configuration.fields.GlobalObject(
        title=u"Context",
        description=u"The content interface or class this pagelet is for.",
        required=False)

    layer = zope.configuration.fields.GlobalInterface(
        title=u"The layer the view is in.",
        description=u"""
        A skin is composed of layers. It is common to put skin
        specific views in a layer named after the skin. If the 'layer'
        attribute is not supplied, it defaults to 'default'.""",
        required=False)

    wizard = zope.configuration.fields.GlobalObject(
        title=u"Wizard",
        description=u"The wizard interface or class this step is for.",
        required=False)

    provides = zope.configuration.fields.GlobalInterface(
        title=u"The interface this pagelets provides.",
        description=u"""
        A pagelet can provide an interface.  This would be used for
        views that support other views.""",
        required=False,
        default=interfaces.IPagelet)

    allowed_interface = zope.configuration.fields.Tokens(
        title=u"Interface that is also allowed if user has permission.",
        description=u"""
        By default, 'permission' only applies to viewing the view and
        any possible sub views. By specifying this attribute, you can
        make the permission also apply to everything described in the
        supplied interface.

        Multiple interfaces can be provided, separated by
        whitespace.""",
        required=False,
        value_type=zope.configuration.fields.GlobalInterface())

    allowed_attributes = zope.configuration.fields.Tokens(
        title=u"View attributes that are also allowed if the user"
              u" has permission.",
        description=u"""
        By default, 'permission' only applies to viewing the view and
        any possible sub views. By specifying 'allowed_attributes',
        you can make the permission also apply to the extra attributes
        on the view object.""",
        required=False,
        value_type=zope.configuration.fields.PythonIdentifier())


# Arbitrary keys and values are allowed to be passed to the wizard.
IWizardDirective.setTaggedValue('keyword_arguments', True)


# Arbitrary keys and values are allowed to be passed to the step.
IWizardStepDirective.setTaggedValue('keyword_arguments', True)


# wizard directive
def wizardDirective(
        _context, class_, name, permission, for_=zope.interface.Interface,
        layer=IDefaultBrowserLayer, provides=interfaces.IWizard,
        allowed_interface=None, allowed_attributes=None, **kwargs):

    # Security map dictionary
    required = {}

    # Get the permission; mainly to correctly handle CheckerPublic.
    permission = _handle_permission(_context, permission)

    # The class must be specified.
    if not class_:
        raise ConfigurationError("Must specify a class.")

    if not zope.interface.interfaces.IInterface.providedBy(provides):
        raise ConfigurationError("Provides interface provide IInterface.")

    ifaces = list(zope.interface.Declaration(provides).flattened())
    if interfaces.IWizard not in ifaces:
        raise ConfigurationError("Provides interface must inherit IWizard.")

    # Build a new class that we can use different permission settings if we
    # use the class more then once.
    cdict = {}
    cdict['__name__'] = name
    cdict.update(kwargs)
    new_class = type(class_.__name__, (class_, wizard.Wizard), cdict)

    # Set up permission mapping for various accessible attributes
    _handle_allowed_interface(
        _context, allowed_interface, permission, required)
    _handle_allowed_attributes(
        _context, allowed_attributes, permission, required)
    _handle_allowed_attributes(
        _context, kwargs.keys(), permission, required)
    _handle_allowed_attributes(
        _context, ('__call__', 'browserDefault', 'update', 'render',
                   'publishTraverse'), permission, required)

    # Register the interfaces.
    _handle_for(_context, for_)

    # provide the custom provides interface if not allready provided
    if not provides.implementedBy(new_class):
        zope.interface.classImplements(new_class, provides)

    # Create the security checker for the new class
    zope.security.checker.defineChecker(
        new_class, zope.security.checker.Checker(required))

    # register pagelet
    _context.action(
        discriminator=('pagelet', for_, layer, name),
        callable=zope.component.zcml.handler,
        args=('registerAdapter',
              new_class, (for_, layer), provides, name, _context.info),)


def wizardStepDirective(
        _context, class_, name, permission, for_=zope.interface.Interface,
        layer=IDefaultBrowserLayer, wizard=interfaces.IWizard,
        provides=interfaces.IStep, allowed_interface=None,
        allowed_attributes=None, **kwargs):

    # Security map dictionary
    required = {}

    # Get the permission; mainly to correctly handle CheckerPublic.
    permission = _handle_permission(_context, permission)

    # The class must be specified.
    if not class_:
        raise ConfigurationError("Must specify a class.")

    if not zope.interface.interfaces.IInterface.providedBy(provides):
        raise ConfigurationError("Provides interface provide IInterface.")

    ifaces = list(zope.interface.Declaration(provides).flattened())
    if interfaces.IPagelet not in ifaces:
        raise ConfigurationError("Provides interface must inherit IPagelet.")

    if not interfaces.IWizard.implementedBy(wizard):
        raise ConfigurationError("Provides interface must inherit IWizard.")

    # Build a new class that we can use different permission settings if we
    # use the class more then once.
    cdict = {}
    cdict['__name__'] = name
    cdict.update(kwargs)
    new_class = type(class_.__name__, (class_, step.Step), cdict)

    # Set up permission mapping for various accessible attributes
    _handle_allowed_interface(
        _context, allowed_interface, permission, required)
    _handle_allowed_attributes(
        _context, allowed_attributes, permission, required)
    _handle_allowed_attributes(
        _context, kwargs.keys(), permission, required)
    _handle_allowed_attributes(
        _context, ('__call__', 'browserDefault', 'update', 'render',
                   'publishTraverse'), permission, required)

    # Register the interfaces.
    _handle_for(_context, for_)

    # provide the custom provides interface if not allready provided
    if not provides.implementedBy(new_class):
        zope.interface.classImplements(new_class, provides)

    # Create the security checker for the new class
    zope.security.checker.defineChecker(
        new_class, zope.security.checker.Checker(required))

    # register pagelet
    _context.action(
        discriminator=('pagelet', for_, layer, name),
        callable=zope.component.zcml.handler,
        args=('registerAdapter',
              new_class, (for_, layer, wizard), provides, name, _context.info))

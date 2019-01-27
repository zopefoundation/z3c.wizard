=======
CHANGES
=======

1.1 (unreleased)
----------------

- Add support for Python 3.7.


1.0 (2017-06-16)
----------------

- Add support for Python 3.4 up to 3.6, PyPy2 and PyPy3.


0.9.1 (2011-10-28)
------------------

- Using Python's ``doctest`` module instead of depreacted
  ``zope.testing.doctest``.

- Allowing in step complete check that values are not existing on
  context. This is consistent with the way `z3c.form` handles not existing
  values.

0.9.0 (2009-12-29)
------------------

- Avoid `z3c.form.testing` in tests: It depends on `lxml`, but `lxml`
  features are not needed here.

- Using ``requiredInfo`` property to render the information about
  required fields. This property returns an i18n message id making the
  information translateable.


0.8.0 (2009-11-30)
------------------

- Adjusted dependencies, reflecting changes in zope packages: use new
  packages and skip dependency to `zope.app.publisher`.


0.7.1 (2009-10-27)
------------------

- Bugfix for z3c.form 2.2.0 changes. Removed name definition in Step
  class. This will prevent to run into an error based on the z3c.form
  changes.


0.7.0 (2009-08-15)
------------------

- Added support for field groups in step template. (Copied over from
  z3c.formui.)

- There were two metal define-slots named `header`. Renamed the first
  one to `wizard-header`.



0.6.0 (2009-07-10)
------------------

- Remove dependency on z3c.i18n as it wasn't really used and we can
  easily recreate a message factory for the "z3c" domain.

- Fixed tests to work with z3c.form 2.0.

- Added another doctest to the `long_description`.

- Changed package's mailing list address to zope-dev at zope.org instead
  of the retired zope3-dev one.

0.5.0 (2009-02-22)
------------------

- Initial Release

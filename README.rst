=========
symbolism
=========

Extensible combinator library for building symbolic Python expressions that are compatible with serialization and can be evaluated at a later time.

|pypi| |readthedocs| |actions| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/symbolism.svg
   :target: https://badge.fury.io/py/symbolism
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/symbolism/badge/?version=latest
   :target: https://symbolism.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |actions| image:: https://github.com/reity/symbolism/workflows/lint-test-cover-docs/badge.svg
   :target: https://github.com/reity/symbolism/actions/workflows/lint-test-cover-docs.yml
   :alt: GitHub Actions status.

.. |coveralls| image:: https://coveralls.io/repos/github/reity/symbolism/badge.svg?branch=master
   :target: https://coveralls.io/github/reity/symbolism?branch=master
   :alt: Coveralls test coverage summary.

Purpose
-------
In many scenarios that require some form of lazy evaluation, it is sufficient to employ lambda expressions, generators/iterables, or abstract syntax trees (via the `ast <https://docs.python.org/3/library/ast.html>`_ and/or `inspect <https://docs.python.org/3/library/inspect.html>`_ modules). However, there are certain cases where none of these are an option (for example, employing lambda expressions precludes serialization and employing the `ast <https://docs.python.org/3/library/ast.html>`_ or `inspect <https://docs.python.org/3/library/inspect.html>`_ modules usually involves introducing boilerplate that expands the solution beyond one line of code). The purpose of this library is to fill those gaps and make it possible to write concise symbolic expressions that are embedded directly in the concrete syntax of the language.

Package Installation and Usage
------------------------------
The package is available on `PyPI <https://pypi.org/project/symbolism/>`_::

    python -m pip install symbolism

The library can be imported in the usual ways::

    import symbolism
    from symbolism import *

Examples
^^^^^^^^
The library makes it possible to construct symbolic Python expressions (as instances of the ``symbol`` class) that can be evaluated at a later time. A symbolic expression involving addition of integers is created in the example below::

    >>> from symbolism import *
    >>> addition = symbol(lambda x, y: x + y)
    >>> summation = addition(symbol(1), symbol(2))

The expression above can be evaluated at a later time::

    >>> summation.evaluate()
    3

Symbol instances are compatible with all built-in infix and prefix operators. When an operator is applied to one or more ``symbol`` instances, a new ``symbol`` instance is created::

    >>> summation = symbol(1) + symbol(2)
    >>> summation.evaluate()
    3

Pre-defined constants are also provided for all built-in operators::

    >>> conjunction = and_(symbol(True), symbol(False))
    >>> conjunction.evaluate()
    False

Documentation
-------------
.. include:: toc.rst

The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org/>`_::

    cd docs
    python -m pip install -r requirements.txt
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. ../setup.py && make html

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org/>`_ (see ``setup.cfg`` for configuration details)::

    python -m pip install pytest pytest-cov
    python -m pytest

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python symbolism/symbolism.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    python -m pip install pylint
    python -m pylint symbolism

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/reity/symbolism>`_ for this library.

Versioning
----------
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.

Publishing
----------
This library can be published as a `package on PyPI <https://pypi.org/project/symbolism/>`_ by a package maintainer. Install the `wheel <https://pypi.org/project/wheel/>`_ package, remove any old build/distribution files, and package the source into a distribution archive::

    python -m pip install wheel
    rm -rf dist *.egg-info
    python setup.py sdist bdist_wheel

Next, install the `twine <https://pypi.org/project/twine/>`_ package and upload the package distribution archive to PyPI::

    python -m pip install twine
    python -m twine upload dist/*

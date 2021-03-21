=========
symbolism
=========

Extensible combinator library for building symbolic Python expressions that are compatible with serialization and can be evaluated at a later time.

|pypi| |travis| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/symbolism.svg
   :target: https://badge.fury.io/py/symbolism
   :alt: PyPI version and link.

.. |travis| image:: https://travis-ci.com/reity/symbolism.svg?branch=master
   :target: https://travis-ci.com/reity/symbolism

.. |coveralls| image:: https://coveralls.io/repos/github/reity/symbolism/badge.svg?branch=master
   :target: https://coveralls.io/github/reity/symbolism?branch=master

Purpose
-------
In many scenarios that require some form of lazy evaluation, it is sufficient to employ lambda expressions, generators/iterables, or abstract syntax trees (via the `ast <https://docs.python.org/3/library/ast.html>`_ and/or `inspect <https://docs.python.org/3/library/inspect.html>`_ modules). However, there are certain cases where none of these are an option (for example, employing lambda expressions precludes serialization and employing the `ast <https://docs.python.org/3/library/ast.html>`_ or `inspect <https://docs.python.org/3/library/inspect.html>`_ modules usually involves introducing boilerplate that expands the solution beyond one line of code). The purpose of this library is to fill those gaps and make it possible to write concise symbolic expressions that are embedded directly in the concrete syntax of the language.

Package Installation and Usage
------------------------------
The package is available on PyPI::

    python -m pip install symbolism

The library can be imported in the usual ways::

    import symbolism
    from symbolism import *

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `nose <https://nose.readthedocs.io/>`_ (see ``setup.cfg`` for configution details)::

    nosetests

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python symbolism/symbolism.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    pylint symbolism

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the GitHub page for this library.

Versioning
----------
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.

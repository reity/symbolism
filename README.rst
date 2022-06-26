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

.. |coveralls| image:: https://coveralls.io/repos/github/reity/symbolism/badge.svg?branch=main
   :target: https://coveralls.io/github/reity/symbolism?branch=main
   :alt: Coveralls test coverage summary.

Purpose
-------
In many scenarios that require some form of lazy evaluation, it is sufficient to employ lambda expressions, generators/iterables, or abstract syntax trees (via the `ast <https://docs.python.org/3/library/ast.html>`__ and/or `inspect <https://docs.python.org/3/library/inspect.html>`__ modules). However, there are certain cases where none of these are an option (for example, employing lambda expressions precludes serialization and employing the `ast <https://docs.python.org/3/library/ast.html>`__ or `inspect <https://docs.python.org/3/library/inspect.html>`__ modules usually involves introducing boilerplate that expands the solution beyond one line of code). The purpose of this library is to fill those gaps and make it possible to write concise symbolic expressions that are embedded directly in the concrete syntax of the language.

Installation and Usage
----------------------
This library is available as a `package on PyPI <https://pypi.org/project/symbolism>`__::

    python -m pip install symbolism

The library can be imported in the usual ways::

    import symbolism
    from symbolism import *

Examples
^^^^^^^^

.. |symbol| replace:: ``symbol``
.. _symbol: https://symbolism.readthedocs.io/en/latest/_source/symbolism.html#symbolism.symbolism.symbol

The library makes it possible to construct symbolic Python expressions (as instances of the |symbol|_ class) that can be evaluated at a later time. A symbolic expression involving addition of integers is created in the example below::

    >>> from symbolism import *
    >>> addition = symbol(lambda x, y: x + y)
    >>> summation = addition(symbol(1), symbol(2))

The expression above can be evaluated at a later time::

    >>> summation.evaluate()
    3

Instances of |symbol|_ are compatible with `common built-in infix and prefix arithmetic, logical, and relational operators <https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types>`__. When an operator is applied to one or more |symbol|_ instances, a new |symbol|_ instance is created::

    >>> summation = symbol(1) + symbol(2)
    >>> summation.evaluate()
    3

Pre-defined constants are also provided for all built-in operators supported by the |symbol|_ class::

    >>> conjunction = and_(symbol(True), symbol(False))
    >>> conjunction.evaluate()
    False

Development
-----------
All installation and development dependencies are fully specified in ``pyproject.toml``. The ``project.optional-dependencies`` object is used to `specify optional requirements <https://peps.python.org/pep-0621>`__ for various development tasks. This makes it possible to specify additional options (such as ``docs``, ``lint``, and so on) when performing installation using `pip <https://pypi.org/project/pip>`__::

    python -m pip install .[docs,lint]

Documentation
^^^^^^^^^^^^^
The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org>`__::

    python -m pip install .[docs]
    cd docs
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. && make html

Testing and Conventions
^^^^^^^^^^^^^^^^^^^^^^^
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org>`__ (see the ``pyproject.toml`` file for configuration details)::

    python -m pip install .[test]
    python -m pytest

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`__::

    python src/symbolism/symbolism.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org>`__::

    python -m pip install .[lint]
    python -m pylint src/symbolism

Contributions
^^^^^^^^^^^^^
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/reity/symbolism>`__ for this library.

Versioning
^^^^^^^^^^
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`__.

Publishing
^^^^^^^^^^
This library can be published as a `package on PyPI <https://pypi.org/project/symbolism>`__ by a package maintainer. First, install the dependencies required for packaging and publishing::

    python -m pip install .[publish]

Remove any old build/distribution files and package the source into a distribution archive::

    rm -rf build dist src/*.egg-info
    python -m build --sdist --wheel .

Finally, upload the package distribution archive to `PyPI <https://pypi.org>`__ using the `twine <https://pypi.org/project/twine>`__ package::

    python -m twine upload dist/*

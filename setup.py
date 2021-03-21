from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="symbolism",
    version="0.1.0",
    packages=["symbolism",],
    install_requires=[],
    license="MIT",
    url="https://github.com/reity/symbolism",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Extensible combinator library for building symbolic "+\
                "expressions that can be evaluated at a later time.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)

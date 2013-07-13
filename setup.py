#!/usr/bin/env python
from setuptools import setup


setup(
    name="radio.rest",
    version="0.1.0",
    license="BSD",
    description="REST API for the R/a/dio service.",
    author="R/a/dio",
    author_email="radio@wessie.info",
    url="http://github.com/R-a-dio/radio.core",
    namespace_packages=["radio"],
    install_requires=[
        "radio.core",
        "web.py",
    ],
    packages=["radio.rest"],
    tests_require=["pytest"],
)

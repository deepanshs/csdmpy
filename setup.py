#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import find_packages
from setuptools import setup

# from csdfpy._version import __version__

# import sys
# from shutil import rmtree

# Package meta-data.
NAME = "csdfpy"
DESCRIPTION = (
    "A python module for importing and exporting CSD model file-format."
)
URL = "https://github.com/DeepanshS/csdfpy"
EMAIL = "srivastava.89@osu.edu"
AUTHOR = "Deepansh Srivastava"
REQUIRES_PYTHON = ">=3.5"
VERSION = "0.0.11"

# What packages are required for this module to be executed?
REQUIRED = [
    "requests>=2.21.0",
    "astropy>=3.0",
    "numpy>=1.10.1",
    "pytest-runner>=5.0",
    "pytest",
    "setuptools>=27.3",
]

# What packages are optional?
EXTRAS = {"fancy feature": ["matplotlib>=3.0.2", "sounddevice"]}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier
# for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    setup_requires=["pytest-runner", "numpy>=1.10.1"],
    tests_require=["pytest"],
    include_package_data=True,
    license="BSD-3-Clause",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha"
        "Programming Language :: Python :: 3.5",
        # 'Programming Language :: Python :: Implementation :: CPython',
        # 'Programming Language :: Python :: Implementation :: PyPy'
    ],
)

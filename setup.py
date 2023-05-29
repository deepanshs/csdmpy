#!/usr/bin/env python
import os

from setuptools import find_packages
from setuptools import setup

# Load package version number.
with open("csdmpy/__init__.py") as f:
    for line in f.readlines():
        if "__version__" in line:
            before_keyword, keyword, after_keyword = line.partition("=")
            version = after_keyword.strip()[1:-1]


# What packages are required for this module to be executed?
required = [
    "numpy>=1.20",
    "setuptools>=27.3",
    "requests>=2.21.0",
    "numexpr>=2.7.0",
]
extras = {"matplotlib": ["matplotlib>=3.0"]}
setup_requires = ["setuptools>=27.3"]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = ""


setup(
    name="csdmpy",
    version=version,
    description="A python module for the core scientific dataset model.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Deepansh Srivastava",
    author_email="srivastava.89@osu.edu",
    python_requires=">=3.7",
    url="https://github.com/DeepanshS/csdmpy/",
    packages=find_packages(),
    install_requires=required,
    setup_requires=setup_requires,
    extras_require=extras,
    tests_require=["pytest", "pytest-runner"],
    include_package_data=True,
    license="BSD-3-Clause",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
    ],
)

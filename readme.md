The csdmpy package
==================

[![Build Status](https://travis-ci.org/DeepanshS/csdmpy.svg?branch=master)](https://travis-ci.org/DeepanshS/csdmpy)
[![Documentation Status](https://readthedocs.org/projects/csdmpy/badge/?version=stable)](https://csdmpy.readthedocs.io/en/stable/?badge=stable)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![GitHub issues](https://img.shields.io/github/issues-raw/deepanshs/csdmpy)
![GitHub release](https://img.shields.io/github/release/deepanshs/csdmpy)
[![PyPI version](https://badge.fury.io/py/csdmpy.svg)](https://badge.fury.io/py/csdmpy)

The *csdmpy* package is a Python support for the core scientific
dataset (CSD) model file exchange-format.
The package is based on the core scientific dataset (CSD) model which is
designed as a building block in the development of a more sophisticated
portable scientific dataset file standard.
The CSD model is capable of handling a wide variety of
scientific datasets both within and across disciplinary fields.

The main objective of this python package is to facilitate an easy import and
export of the CSD model serialized JSON files for Python users. The
package utilizes Numpy library and, therefore, offers the end users versatility
to process or visualize the imported datasets with any third party package(s)
compatible with Numpy.

For further reading, refer to the [documentation](https://csdmpy.readthedocs.io/en/latest/).

You can [![](https://img.shields.io/badge/Download-CSDM%20sample%20files-blueviolet)](https://osu.box.com/s/bq10pc5jyd3mu67vqvhw4xmrqgsd0x8u)
used in the project.

The core scientific dataset (CSD) model
---------------------------------------

The core scientific dataset (CSD) model is a *light-weight*, *portable*,
*versatile*, and *standalone* data model capable of handling a variety of
scientific datasets. The model only encapsulates
data values and the minimum metadata, to accurately represent a *p*-component
dependent variable,
discretely sampled at *M* unique points in a *d*-dimensional coordinate space.
The model is not intended to encapsulate
any information on how the data might be acquired, processed, or visualized.

The data model is *versatile* in allowing many use cases for most spectroscopy,
diffraction, and imaging techniques. As
such the model supports multi-component datasets associated with continuous
physical quantities that are discretely sampled in a multi-dimensional space
associated with other carefully controlled quantities, for e.g., a mass as a
function of temperature, a current as a function of voltage and time, a signal
voltage as a function of magnetic field gradient strength, a color image with
a red, green, and blue (RGB) light intensity components as a function of two
independent spatial dimensions, or the six components of the symmetric
second-rank diffusion tensor MRI as a function of three independent spatial
dimensions. Additionally, the model supports multiple dependent variables
sharing the same *d*-dimensional coordinate space. For instance,
the simultaneous measurement of current and voltage as a function of time.
Another example would be the simultaneous acquisition of air temperature,
pressure, wind velocity, and
solar-flux as a function of Earth’s latitude and longitude coordinates. We
refer to these dependent variables as *correlated-datasets*.

The CSD model is independent of the hardware,
operating system, application software, programming language, and the
object-oriented file-serialization format utilized in serializing the CSD model
to the file. Out of numerous file serialization formats, XML, JSON, property
list, we adopt the data-exchange oriented JSON (JavaScript Object Notation)
file-serialization format because it is *human-readable*, and *easily integrable* with any number of programming languages
and field related application-software.

Installing *csdmpy* package
---------------------------

We recommend installing [anaconda](https://www.anaconda.com/distribution/)
distribution for python version 3.6 or higher. The anaconda distribution
ships with numerous packages and modules including Numpy, Scipy, and Matplotlib
which are useful packages for handling scientific datasets.

**Using PIP**:

PIP is a package manager for Python packages and is included with
python version 3.4 and higher.

    $ pip install csdmpy

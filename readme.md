# The csdmpy project

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Deployment   | [![PyPI version](https://img.shields.io/pypi/v/csdmpy.svg?style=flat&logo=pypi&logoColor=white)](https://pypi.python.org/pypi/csdmpy)                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Build Status | [![Build Status](https://travis-ci.org/DeepanshS/csdmpy.svg?branch=master)](https://travis-ci.org/DeepanshS/csdmpy) [![Documentation Status](https://readthedocs.org/projects/csdmpy/badge/?version=stable)](https://csdmpy.readthedocs.io/en/stable/?badge=stable)                                                                                                                                                                                                                                                                                                          |
| License      | [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Metrics      | [![PyPI - Downloads](https://img.shields.io/pypi/dm/csdmpy.svg)](https://img.shields.io/pypi/dm/csdmpy)[![Total alerts](https://img.shields.io/lgtm/alerts/g/DeepanshS/csdmpy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/DeepanshS/csdmpy/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/DeepanshS/csdmpy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/DeepanshS/csdmpy/context:python) [![codecov](https://codecov.io/gh/DeepanshS/csdmpy/branch/master/graph/badge.svg)](https://codecov.io/gh/DeepanshS/csdmpy) |
| GitHub       | ![GitHub issues](https://img.shields.io/github/issues-raw/deepanshs/csdmpy)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

The _csdmpy_ package is a Python support for the core scientific
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

> **Download the examples files using in this package** > [![](https://img.shields.io/badge/Download-CSDM%20sample%20files-blueviolet)](https://osu.box.com/s/bq10pc5jyd3mu67vqvhw4xmrqgsd0x8u)

> **See example gallery** > [![](https://img.shields.io/badge/View-Example%20Gallery-Purple?size=large)](https://csdmpy.readthedocs.io/en/latest/auto_examples/index.html)

## The core scientific dataset (CSD) model

The core scientific dataset (CSD) model is a _light-weight_, _portable_,
_versatile_, and _standalone_ data model capable of handling a variety of
scientific datasets. The model only encapsulates
data values and the minimum metadata, to accurately represent a _p_-component
dependent variable,
discretely sampled at _M_ unique points in a _d_-dimensional coordinate space.
The model is not intended to encapsulate
any information on how the data might be acquired, processed, or visualized.

The data model is _versatile_ in allowing many use cases for most spectroscopy,
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
sharing the same _d_-dimensional coordinate space. For instance,
the simultaneous measurement of current and voltage as a function of time.
Another example would be the simultaneous acquisition of air temperature,
pressure, wind velocity, and
solar-flux as a function of Earth’s latitude and longitude coordinates. We
refer to these dependent variables as _correlated-datasets_.

The CSD model is independent of the hardware,
operating system, application software, programming language, and the
object-oriented file-serialization format utilized in serializing the CSD model
to the file. Out of numerous file serialization formats, XML, JSON, property
list, we adopt the data-exchange oriented JSON (JavaScript Object Notation)
file-serialization format because it is _human-readable_, and _easily integrable_ with any number of programming languages
and field related application-software.

## Installing _csdmpy_ package

**Using PIP**:

PIP is a package manager for Python packages and is included with
python version 3.4 and higher.

    $ pip install csdmpy

## Citation

Srivastava D.J., Vosegaard T., Massiot D., Grandinetti P.J. (2020) Core Scientific Dataset Model: A lightweight and portable model and file format for multi-dimensional scientific data. [PLOS ONE 15(1): e0225953.](https://doi.org/10.1371/journal.pone.0225953)

## Check out the media coverage.

- [<img src="https://inc.cnrs.fr/sites/institut_inc/files/styles/top_left/public/image/cnrs_20180120_0025%20%281%29.jpg?itok=i3wlyGBq" height="64" width="64"> Des chimistes élaborent un nouveau format pour le partage de données scientifiques](https://inc.cnrs.fr/fr/cnrsinfo/des-chimistes-elaborent-un-nouveau-format-pour-le-partage-de-donnees-scientifiques)

- [<img src="https://www.technology.org/texorgwp/wp-content/uploads/2020/01/1920_data-1536x1024.jpg" height="64" width="64"> Simplifying how scientists share data](https://www.technology.org/2020/01/03/simplifying-how-scientists-share-data/)

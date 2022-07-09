# The csdmpy project

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Deployment   | [![PyPI version](https://img.shields.io/pypi/v/csdmpy.svg?style=flat&logo=pypi&logoColor=white)](https://pypi.python.org/pypi/csdmpy) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/csdmpy)                                                                                                                                                                                                                                                                                                                                                                |
| Build Status | [![Github workflow](<https://img.shields.io/github/workflow/status/deepanshs/csdmpy/CI%20(pip)?logo=GitHub>)](https://github.com/DeepanshS/csdmpy/actions) [![Documentation Status](https://readthedocs.org/projects/csdmpy/badge/?version=stable)](https://csdmpy.readthedocs.io/en/stable/?badge=stable)                                                                                                                                        |
| License      | [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Metrics      | [![Total alerts](https://img.shields.io/lgtm/alerts/g/DeepanshS/csdmpy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/DeepanshS/csdmpy/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/DeepanshS/csdmpy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/DeepanshS/csdmpy/context:python) [![codecov](https://codecov.io/gh/DeepanshS/csdmpy/branch/master/graph/badge.svg)](https://codecov.io/gh/DeepanshS/csdmpy) |
| GitHub       | ![GitHub issues](https://img.shields.io/github/issues-raw/deepanshs/csdmpy)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Citations    | [![DOI](<https://img.shields.io/badge/DOI-PLOS%20ONE%2015(1):%20e0225953-blueviolet>)](https://doi.org/10.1371/journal.pone.0225953)                                                                                                                                                                                                                                                                                                                               |

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

> **See example gallery**
>
> [![View](https://img.shields.io/badge/View-Example%20Gallery-Purple?size=large)](https://csdmpy.readthedocs.io/en/latest/auto_examples/index.html)

## The core scientific dataset (CSD) model

The core scientific dataset (CSD) model is a _light-weight_, _portable_,
_versatile_, and _standalone_ data model capable of handling a variety of
scientific datasets. The model only encapsulates
data values and the minimum metadata, to accurately represent a **_p_-component
dependent variable,
discretely sampled at _M_ unique points in a _d_-dimensional coordinate space**.
The model is not intended to encapsulate
any information on how the data might be acquired, processed, or visualized.

---
### Use cases
The data model is _versatile_ in allowing many **use cases for most spectroscopy,
diffraction, and imaging techniques**.

![](/docs/_static/csdm.png "")

### Data Model

The model supports multi-component datasets associated with continuous
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

**Example**
```py
"csdm": {
  "version": "1.0",
  # A list of Linear, Monotonic, or Labeled dimensions of the multi-dimensional space.
  "dimensions": [{
    "type": "linear",
    "count": 1608,
    "increment": "0.08333333333 yr",
    "coordinates_offset": "1880.0416666667 yr",
  }],
  # A list of dependent variables sampling the multi-dimensional space.
  "dependent_variables": [{
    "type": "internal",
    "unit": "mm",
    "numeric_type": "float32",
    "quantity_type": "scalar",
    "component_labels": ["GMSL"],
    "components": [
      ["-183.0, -171.125, ..., 59.6875, 58.5"]
    ]
  }]
}
```
## Installing _csdmpy_ package

    $ pip install csdmpy

## How to cite

Please cite the following when used in publication.

1. Srivastava D.J., Vosegaard T., Massiot D., Grandinetti P.J. (2020) Core Scientific Dataset Model: A lightweight and portable model and file format for multi-dimensional scientific data. [PLOS ONE 15(1): e0225953.](https://doi.org/10.1371/journal.pone.0225953)

## Check out the media coverage.

- [<img src="https://inc.cnrs.fr/sites/institut_inc/files/styles/top_left/public/image/cnrs_20180120_0025%20%281%29.jpg?itok=i3wlyGBq" height="64" width="64"> Des chimistes élaborent un nouveau format pour le partage de données scientifiques](https://inc.cnrs.fr/fr/cnrsinfo/des-chimistes-elaborent-un-nouveau-format-pour-le-partage-de-donnees-scientifiques)

- [<img src="https://www.technology.org/texorgwp/wp-content/uploads/2020/01/1920_data-1536x1024.jpg" height="64" width="64"> Simplifying how scientists share data](https://www.technology.org/2020/01/03/simplifying-how-scientists-share-data/)

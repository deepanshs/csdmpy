"""The data model build on the Core Scientific Dataset Model."""
import datetime
import json
from urllib.parse import urlparse

import numpy as np

from .csdm import as_dependent_variable  # NOQA
from .csdm import as_dimension  # NOQA
from .csdm import CSDM  # NOQA
from .csdm import DependentVariable  # NOQA
from .csdm import Dimension  # NOQA
from .csdm import LabeledDimension  # NOQA
from .csdm import LinearDimension  # NOQA
from .csdm import MonotonicDimension  # NOQA
from .dependent_variable import download  # NOQA
from .helper_functions import _preview  # NOQA
from .numpy_wrapper import apodize  # NOQA
from .tests import *  # NOQA
from .units import Quantity  # NOQA
from .units import ScalarQuantity  # NOQA
from .units import string_to_quantity  # NOQA
from .utils import QuantityType  # NOQA
from .utils import validate  # NOQA

now = datetime.datetime.now()
year = now.year

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__copyright__ = f"Copyright 2019-{year}, The CSDMpy Project."
__credits__ = ["Deepansh J. Srivastava"]
__license__ = "BSD License"
__maintainer__ = "Deepansh J. Srivastava"
__status__ = "Beta"
__version__ = "0.6.0"

__all__ = [
    "parse_dict",
    "load",
    "loads",
    "new",
    "as_csdm",
    "as_dependent_variable",
    "as_dimension",
    "plot",
]


def _import_json(filename, verbose=False):
    res = urlparse(filename)
    if res[0] not in ["file", ""]:
        filename = download.download_file_from_url(filename, verbose)
    with open(filename, "rb") as f:
        content = f.read()
        return json.loads(str(content, encoding="UTF-8"))


def _check_csdm_root_key_value(dictionary):
    """Check the root level key and value type of the csdm object"""
    key_list_root = dictionary.keys()
    if "CSDM" in key_list_root:
        raise KeyError(
            "'CSDM' is not a valid keyword for the CSD model. Did you mean 'csdm'?"
        )

    if "csdm" not in key_list_root:
        raise KeyError("Missing a required `csdm` key from the data model.")

    # inside csdm object
    optional_keys = [
        "read_only",
        "timestamp",
        "geographic_coordinate",
        "application",
        "tags",
        "description",
    ]
    required_keys = ["version"]
    all_keys = optional_keys + required_keys

    key_list_csdm = list(dictionary["csdm"].keys())
    key_list_csdm_lower_case = [item.lower() for item in key_list_csdm]

    for i, item in enumerate(key_list_csdm):
        if item not in all_keys and key_list_csdm_lower_case[i] in all_keys:
            raise KeyError(
                f"{item} is an invalid key for the CSDM object. "
                f"Did you mean '{key_list_csdm_lower_case[i]}'?"
            )

    for item in required_keys:
        if item not in key_list_csdm:
            raise KeyError(f"Missing a required `{item}` key from the CSDM object.")

    _version = dictionary["csdm"]["version"]
    validate(_version, "version", str)


def parse_dict(dictionary):
    """Parse a CSDM compliant python dictionary and return a CSDM object.

    Args:
        dictionary: A CSDM compliant python dictionary.
    """
    _check_csdm_root_key_value(dictionary)
    csdm_dict = dictionary["csdm"]
    filename = dictionary["filename"] if "filename" in dictionary else None

    if "timestamp" in csdm_dict:
        csdm_dict["timestamp"] = validate(csdm_dict["timestamp"], "timestamp", str)

    return CSDM(filename=filename, **csdm_dict)


def load(filename=None, application=False, verbose=False):
    r"""Loads a .csdf/.csdfe file and returns an instance of the :ref:`csdm_api` class.

    The file must be a JSON serialization of the CSD Model.

    Example:
        >>> data1 = cp.load('local_address/file.csdf') # doctest: +SKIP
        >>> data2 = cp.load('url_address/file.csdf') # doctest: +SKIP

    Args:
        filename (str): A local or a remote address to the `.csdf or `.csdfe` file.
        application (bool): If true, the application metadata from application that
                last serialized the file will be imported. Default is False.
        verbose (bool): If the filename is a URL, this option will show the progress
                bar for the file download status, when True.

    Returns:
        A CSDM instance.
    """
    if filename is None:
        raise Exception("Missing the value for the required `filename` attribute.")

    dictionary = _import_json(filename, verbose)
    dictionary["filename"] = filename
    csdm_object = parse_dict(dictionary)

    if application is False:
        csdm_object.application = None
        for dim in csdm_object.dimensions:
            dim.application = None
            if hasattr(dim, "reciprocal") and dim.type != "label":
                dim.reciprocal.application = None
        for dim in csdm_object.dependent_variables:
            dim.application = None
            # if hasattr(dim., 'dimension indexes'):
            #     dim.reciprocal.application = {}
    # csdm_objects = []
    # for file_ in csdm_files:
    #     csdm_objects.append(_load(file_, application=application))
    return csdm_object


def loads(string):
    """Loads a JSON serialized string as a CSDM object.

    Args:
        string: A JSON serialized CSDM string.
    Returns:
        A CSDM object.

    Example:
        >>> object_from_string = cp.loads(cp.new('A test dump').dumps())
        >>> print(object_from_string.data_structure)  # doctest: +SKIP
        {
          "csdm": {
            "version": "1.0",
            "timestamp": "2019-10-21T20:33:17Z",
            "description": "A test dump",
            "dimensions": [],
            "dependent_variables": []
          }
        }
    """
    dictionary = json.loads(string)
    csdm_object = parse_dict(dictionary)
    return csdm_object


def new(description=""):
    """
    Creates a new instance of the :ref:`csdm_api` class containing a 0D{0} dataset.

    Args:
        description (str): A string describing the csdm object. This is optional.

    Example:
        >>> import csdmpy as cp
        >>> empty_data = cp.new(description='Testing Testing 1 2 3')
        >>> print(empty_data.data_structure)
        {
          "csdm": {
            "version": "1.0",
            "description": "Testing Testing 1 2 3"
          }
        }

    Returns:
        A CSDM instance.
    """
    return CSDM(description=description)


def as_csdm(array, unit="", quantity_type="scalar"):
    """Generate and return a view of the nD numpy array as a csdm object.
    The nD array is the dependent variable of the csdm object of the given quantity
    type. The shape of the nD array is used to generate Dimension object of `linear`
    subtype.

    Args:
        array: The nD numpy array.
        unit: The unit for the dependent variable. The default is empty string.
        quantity_type: The quantity type of the dependent variable.

    Example:
        >>> array = np.arange(30).reshape(3, 10)
        >>> csdm_obj = cp.as_csdm(array)
        >>> print(csdm_obj)
        CSDM(
        DependentVariable(
        [[[ 0  1  2  3  4  5  6  7  8  9]
          [10 11 12 13 14 15 16 17 18 19]
          [20 21 22 23 24 25 26 27 28 29]]], quantity_type=scalar, numeric_type=int64),
        LinearDimension([0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]),
        LinearDimension([0. 1. 2.])
        )
    """
    q_type = QuantityType(quantity_type)
    if q_type.p == 1:
        array = array[np.newaxis, :]

    if q_type.p != array.shape[0]:
        raise ValueError(
            f"Expecting exactly {q_type.p} components for quantity type, "
            f"`{quantity_type}`, found {array.shape[0]}. Make sure `array.shape[0]` "
            f"is equal to the number of components supported by {quantity_type}."
        )

    ar_shape = array.shape[::-1][:-1]
    dim = [Dimension(type="linear", count=i, increment="1") for i in ar_shape]
    dv = DependentVariable(
        type="internal",
        components=array,
        unit=unit,
        quantity_type=quantity_type,
    )
    return CSDM(dimensions=dim, dependent_variables=[dv])


def plot(csdm_object, reverse_axis=None, range=None, **kwargs):
    """A supplementary function for plotting basic 1D and 2D datasets only.

    Args:
        csdm_object: The CSDM object.
        reverse_axis: An ordered array of boolean specifying which dimensions will be
            displayed on a reverse axis.
        range: A list of minimum and maximum coordinates along the dimensions. The range
            along each dimension is given as [min, max]
        kwargs: Additional keyword arguments are used in matplotlib plotting functions.
            We implement the following matplotlib methods for the one and
            two-dimensional datasets.

            - The 1D{1} scalar dataset use the plt.plot() method.
            - The 1D{2} vector dataset use the plt.quiver() method.
            - The 2D{1} scalar dataset use the plt.imshow() method if the two
              dimensions have a `linear` subtype. If any one of the dimension is
              `monotonic`, plt.NonUniformImage() method is used instead.
            - The 2D{2} vector dataset use the plt.quiver() method.
            - The 2D{3} pixel dataset use the plt.imshow(), assuming the pixel dataset
              as an RGB image.

    Returns:
        A matplotlib figure instance.

    Example:
        >>> cp.plot(data_object) # doctest: +SKIP
    """
    return _preview(csdm_object, reverse_axis, range, **kwargs)

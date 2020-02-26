# -*- coding: utf-8 -*-
"""The data model build on the Core Scientific Dataset Model."""
from __future__ import division
from __future__ import print_function

import json
import warnings
from urllib.parse import urlparse

import numpy as np

from csdmpy.csdm import as_dependent_variable  # lgtm [py/import-own-module]
from csdmpy.csdm import as_dimension  # lgtm [py/import-own-module]
from csdmpy.csdm import CSDM  # lgtm [py/import-own-module]
from csdmpy.csdm import DependentVariable  # lgtm [py/import-own-module]
from csdmpy.csdm import Dimension  # lgtm [py/import-own-module]
from csdmpy.csdm import LabeledDimension  # lgtm [py/import-own-module]
from csdmpy.csdm import LinearDimension  # lgtm [py/import-own-module]
from csdmpy.csdm import MonotonicDimension  # lgtm [py/import-own-module]
from csdmpy.dependent_variables import download  # lgtm [py/import-own-module]
from csdmpy.helper_functions import _preview  # lgtm [py/import-own-module]
from csdmpy.numpy_wrapper import apodize  # lgtm [py/import-own-module]
from csdmpy.tests import *  # lgtm [py/import-own-module]
from csdmpy.units import ScalarQuantity  # lgtm [py/import-own-module]
from csdmpy.units import string_to_quantity  # lgtm [py/import-own-module]
from csdmpy.utils import QuantityType  # lgtm [py/import-own-module]
from csdmpy.utils import validate  # lgtm [py/import-own-module]


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__copyright__ = "Copyright 2019-2020, The CSDMpy Project."
__credits__ = ["Deepansh J. Srivastava"]
__license__ = "BSD License"
__maintainer__ = "Deepansh J. Srivastava"
__status__ = "Development"
__version__ = "0.2"

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


def parse_dict(dictionary):
    """Parse a CSDM compliant python dictionary and return a CSDM object.

        Args:
            dictionary: A CSDM compliant python dictionary.
    """
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

    for i in range(len(key_list_csdm)):
        if key_list_csdm[i] not in all_keys and key_list_csdm_lower_case[i] in all_keys:
            raise KeyError(
                f"{key_list_csdm[i]} is an invalid key for the CSDM object. "
                f"Did you mean '{key_list_csdm_lower_case[i]}'?"
            )

    for item in required_keys:
        if item not in key_list_csdm:
            raise KeyError(f"Missing a required `{item}` key from the CSDM object.")

    _version = dictionary["csdm"]["version"]
    validate(_version, "version", str)

    if "filename" in dictionary.keys():
        filename = dictionary["filename"]
    else:
        filename = None
    csdm = CSDM(filename=filename, version=_version)

    if "timestamp" in dictionary["csdm"].keys():
        _timestamp = dictionary["csdm"]["timestamp"]
        validate(_timestamp, "timestamp", str)
        csdm._timestamp = _timestamp

    if "dimensions" in key_list_csdm:
        for dim in dictionary["csdm"]["dimensions"]:
            csdm.add_dimension(dim)

    if "dependent_variables" in key_list_csdm:
        for dat in dictionary["csdm"]["dependent_variables"]:
            csdm.add_dependent_variable(dat)

    for key in optional_keys:
        if key in key_list_csdm:
            setattr(csdm, "_" + key, dictionary["csdm"][key])

    return csdm


def load(filename=None, application=False, verbose=False):
    r"""
    Loads a .csdf/.csdfe file and returns an instance of the :ref:`csdm_api` class.

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
        csdm_object.application = {}
        for dim in csdm_object.dimensions:
            dim.application = {}
            if hasattr(dim, "reciprocal") and dim.type != "label":
                dim.reciprocal.application = {}
        for dim in csdm_object.dependent_variables:
            dim.application = {}
            # if hasattr(dim., 'dimension indexes'):
            #     dim.reciprocal.application = {}
    # csdm_objects = []
    # for file_ in csdm_files:
    #     csdm_objects.append(_load(file_, application=application))
    return csdm_object


def loads(string):
    """
        Loads a JSON serialized string as a CSDM object.

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
    r"""
    Creates a new instance of the :ref:`csdm_api` class containing a 0D{0} dataset.

    Args:
        description (str): A string describing the csdm object. This is optional.

    Example:
        >>> import csdmpy as cp
        >>> emptydata = cp.new(description='Testing Testing 1 2 3')
        >>> print(emptydata.data_structure)
        {
          "csdm": {
            "version": "1.0",
            "description": "Testing Testing 1 2 3",
            "dimensions": [],
            "dependent_variables": []
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

    csdm = new()

    # dimensions should be added first
    shape = array.shape[::-1]
    for i in shape[:-1]:
        csdm.add_dimension(LinearDimension(count=i, increment="1"))

    csdm.add_dependent_variable(
        type="internal",
        components=array.ravel(),
        unit=unit,
        quantity_type=quantity_type,
    )

    return csdm


def plot(csdm_object, reverse_axis=None, range=None, **kwargs):
    """
    A supplementary function for plotting basic 1D and 2D datasets only.

    Args:
        csdm_object: The CSDM object.
        reverse_axis: An ordered array of boolean specifying which dimensions will be
                displayed on a reverse axis.
        kwargs: Additional keyword arguments are used in matplotlib plotting functions.
                We implement the following matplotlib methods for the one and
                two-dimensional datasets.

                - The 1D{1} scalar dataset use the plt.plot() method.
                - The 1D{2} vector dataset use the plt.quiver() method.
                - The 2D{1} scalar dataset use the plt.imshow() method if the two dimensions have a `linear` subtype. If any one of the dimension is `monotonic`, plt.NonUniformImage() method is used instead.
                - The 2D{2} vector dataset use the plt.quiver() method.
                - The 2D{3} pixel dataset use the plt.imshow(), assuming the pixel dataset as an RGB image.

    Example:
        >>> cp.plot(data_object) # doctest: +SKIP
    """
    _preview(csdm_object, reverse_axis, range, **kwargs)

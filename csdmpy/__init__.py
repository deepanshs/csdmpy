# -*- coding: utf-8 -*-
"""CSDM."""
from __future__ import division
from __future__ import print_function

import json
from os import listdir
from os.path import isdir
from os.path import join
from urllib.parse import urlparse

from numpy.fft import fftshift

from csdmpy.csdm import CSDM
from csdmpy.dependent_variables import DependentVariable
from csdmpy.dependent_variables.download import download_file_from_url
from csdmpy.dimensions import Dimension
from csdmpy.helper_functions import _preview
from csdmpy.utils import validate


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__version__ = "0.1.4"


__all__ = ["load", "new", "plot"]


def _import_json(filename):
    res = urlparse(filename)
    if res[0] not in ["file", ""]:
        filename = download_file_from_url(filename)
    with open(filename, "rb") as f:
        content = f.read()
        return json.loads(str(content, encoding="UTF-8"))


def load(filename=None, application=False):
    r"""
    Load a .csdf/.csdfe file and return an instance of :ref:`csdm_api` class.

    The file must be a JSON serialization of the CSD Model.

    Example:
        >>> data1 = cp.load('local_address/file.csdf') # doctest: +SKIP
        >>> data2 = cp.load('url_address/file.csdf') # doctest: +SKIP

    Args:
        filename (str): A local or remote address to the `.csdf or `.csdfe` file.
        application (bool): If true, the application metadata from application that
                last serialized the file will be imported. Default is False.
        sort_fft_order (bool): If true, the coordinates and the components
                corresponding to the dimension with `complex_fft` as True will be
                sorted upon import and the corresponding `complex_fft` key-value
                will be set to False. Default is True.

    Returns:
        A CSDM instance.
    """
    if filename is None:
        raise Exception("Missing a required data file address.")

    # if isdir(filename):
    #     csdm_files = [f for f in listdir(filename) if f.endswith((".csdf", ".csdfe"))]
    #     if len(csdm_files) > 1:
    #         raise Exception(
    #             ("The given path is a folder. More that one csdf(e) files found in this folder")
    #         )
    #     if len(csdm_files) == 0:
    #         raise Exception(
    #             ("The given path is a folder. No csdf(e) file found in the folder.")
    #         )
    #     csd_file = join(filename, csdm_files[0])
    # else:
    #     csd_file = filename

    try:
        dictionary = _import_json(filename)
    except Exception as e:
        raise Exception(e)

    dictionary["filename"] = filename
    csdm_object = parse_dict(dictionary)

    # if sort_fft_order:
    #     axes = []
    #     for i, dim in enumerate(csdm_object.dimensions):
    #         if dim.type == "linear":
    #             if dim.complex_fft:
    #                 n_points = dim.count
    #                 if n_points % 2 == 0:
    #                     temp = n_points * dim.increment / 2.0
    #                 else:
    #                     temp = (n_points - 1) * dim.increment / 2.0
    #                 dim.coordinates_offset = dim.coordinates_offset - temp

    #                 axes.append(-i - 1)
    #                 # dim.complex_fft = False

    #     for var in csdm_object.dependent_variables:
    #         var.components = fftshift(var.components, axes=axes)

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


def parse_dict(dictionary):
    """Parse a CSDM compliant python dictionary and return a CSDM object.

        Args:
            dictionary: A CSDM compliant python dictionary.
    """
    key_list_root = dictionary.keys()
    if "CSDM" in key_list_root:
        raise KeyError("'CSDM' is not a valid keyword. Did you mean 'csdm'?")

    if "csdm" not in key_list_root:
        raise KeyError("Missing a required `csdm` key.")

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
                (
                    f"{key_list_csdm[i]} is not a valid keyword. "
                    f"Did you mean '{key_list_csdm_lower_case[i]}'?"
                )
            )

    for item in required_keys:
        if item not in key_list_csdm:
            raise KeyError(f"Missing a required `{item}` key.")

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

    n_points = [item.count for item in csdm.dimensions]
    if n_points != []:
        csdm._reshape(n_points[::-1])

    for key in optional_keys:
        if key in key_list_csdm:
            setattr(csdm, "_" + key, dictionary["csdm"][key])

    return csdm


def loads(string):
    """
        Loads a JSON serialized string as a CSDM object.

        Args:
            string: A JSON serialized CSDM string.
        Returns:
            A CSDM object

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
    Create a new instance of the :ref:`csdm_api` class containing a 0D{0} dataset.

    Args:
        description (str): A string describing the the csdm object. This is optional.

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


def plot(data_object, *args, **kwargs):
    _preview(data_object, *args, **kwargs)

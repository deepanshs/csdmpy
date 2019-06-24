# -*- coding: utf-8 -*-
"""CSDModel."""
from __future__ import division
from __future__ import print_function

import json
from os import listdir
from os.path import isdir
from os.path import join
from urllib.parse import urlparse

from numpy.fft import fftshift

from csdfpy.csdm import CSDModel
from csdfpy.dependent_variables import DependentVariable
from csdfpy.dependent_variables.download import download_file_from_url
from csdfpy.dimensions import Dimension
from csdfpy.helper_functions import _preview
from csdfpy.version import __version__


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


def _import_json(filename):
    res = urlparse(filename)
    if res[0] not in ["file", ""]:
        filename = download_file_from_url(filename)
    with open(filename, "rb") as f:
        content = f.read()
        return json.loads(str(content, encoding="UTF-8"))


def load(filename=None, application=False, sort_fft_order=False):
    r"""
    Load a .csdf/.csdfe file and return an instance of :ref:`csdm_api` class.

    The file must be a JSON serialization of the CSD Model.

    .. doctest::

        >>> data1 = cp.load('local_address/file.csdf') # doctest: +SKIP
        >>> data2 = cp.load('url_address/file.csdf') # doctest: +SKIP

    :params: filename: A local or remote address to the `.csdf or
                        `.csdfe` file.
    :returns: A ``CSDModel`` instance.
    """
    if filename is None:
        raise Exception("Missing a required data file address.")

    if isdir(filename) and filename.endswith((".csdm", ".csdm/")):
        csdm_files = [
            f for f in listdir(filename) if f.endswith((".csdf", ".csdfe"))
        ]
        if len(csdm_files) != 1:
            raise Exception(
                ("More that one csdf(e) files encountered in the .csdm folder")
            )
        csd_file = join(filename, csdm_files[0])
    else:
        csd_file = filename

    csdm_object = _load(csd_file)

    if sort_fft_order:
        axes = []
        for i, dim in enumerate(csdm_object.dimensions):
            if dim.fft_output_order:
                n_points = dim.count
                if n_points % 2 == 0:
                    temp = n_points * dim.increment / 2.0
                else:
                    temp = (n_points - 1) * dim.increment / 2.0
                dim.index_zero_coordinate = dim.index_zero_coordinate - temp

                axes.append(-i - 1)
                dim.fft_output_order = False

        for var in csdm_object.dependent_variables:
            var.components = fftshift(var.components, axes=axes)

    if application is False:
        csdm_object.application = {}
        for dim in csdm_object.dimensions:
            dim.application = {}
            if hasattr(dim, "reciprocal") and dim.type != "label":
                dim.reciprocal.application = {}
        for dim in csdm_object.dependent_variables:
            dim.application = {}
            # if hasattr(dim., 'sparse_dimensions'):
            #     dim.reciprocal.application = {}
    # csdm_objects = []
    # for file_ in csdm_files:
    #     csdm_objects.append(_load(file_, application=application))
    return csdm_object


def _load(filename):
    try:
        dictionary = _import_json(filename)
    except Exception as e:
        raise Exception(e)

    optional_keys = [
        "read_only",
        "timestamp",
        "geographic_coordinate",
        "application",
        "tags",
        "description",
    ]

    # required_keys = ["csdm", "version"]

    key_list_root = dictionary.keys()

    if "CSDM" in key_list_root:
        raise KeyError("'CSDM' is not a valid keyword. Did you mean 'csdm'?")

    if "csdm" not in key_list_root:
        raise KeyError("'csdm' key is not present.")

    _version = dictionary["csdm"]["version"]
    # is version key required?

    key_list_csdm = dictionary["csdm"].keys()

    csdm = CSDModel(filename, _version)

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

    # if "description" in key_list_csdm:
    #     csdm._description = dictionary["csdm"]["description"]

    # if "read_only" in key_list_csdm:
    #     csdm._read_only = dictionary["csdm"]["read_only"]

    # if "timestamp" in key_list_csdm:
    #     csdm._timestamp = dictionary["csdm"]["timestamp"]

    # if "geographic_coordinate" in key_list_csdm:
    #     csdm._geographic_coordinate = dictionary["csdm"][
    #         "geographic_coordinate"
    #     ]

    # if "application" in key_list_csdm:
    #     csdm._application = dictionary["csdm"]["application"]

    # if "tags" in key_list_csdm:
    #     csdm._tags = dictionary["csdm"]["tags"]

    return csdm


def new(description=""):
    r"""
    Return a new instance of :ref:`csdm_api` class containing a 0D{0} dataset.

    Optionally, a description may be provided as an argument to this method,
    for example,

    .. doctest::

        >>> import csdfpy as cp
        >>> emptydata = cp.new(description='Testing Testing 1 2 3')
        >>> print(emptydata.data_structure)
        {
          "csdm": {
            "version": "0.0.12",
            "description": "Testing Testing 1 2 3",
            "dimensions": [],
            "dependent_variables": []
          }
        }

    :returns: A ``CSDModel`` instance
    """
    return CSDModel(description=description)


def plot(data_object):
    _preview(data_object)

# -*- coding: utf-8 -*-
"""The DependentVariable SubType classes."""
from __future__ import division
from __future__ import print_function

import base64
import warnings
from copy import deepcopy
from os import path
from urllib.parse import urlparse
from urllib.request import urlopen

import numpy as np

from ._utils import _assign_and_check_unit_consistency
from ._utils import _check_encoding
from ._utils import _check_quantity
from ._utils import _type_message
from ._utils import NumericType
from ._utils import numpy_dtype_to_numeric_type
from ._utils import QuantityType
from ._utils_download_file import _get_proper_url_parse
from .units import value_object_format


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


# Decode data functions #
def _decode_base64(_components, _dtype):
    _components = np.asarray(
        [
            np.frombuffer(base64.b64decode(item), dtype=_dtype)
            for item in _components
        ]
    )
    return _components


def _decode_none(_components, _dtype):
    if _dtype in ["<c8", "<c16"]:
        _components = np.asarray(
            [
                np.asarray(item[0::2]) + 1j * np.asarray(item[1::2])
                for item in _components
            ],
            dtype=_dtype,
        )
    else:
        _components = np.asarray(
            [np.asarray(item) for item in _components], dtype=_dtype
        )
    return _components


def _decode_raw(_components, _dtype, _component_num):
    _components = np.frombuffer(_components, dtype=_dtype)
    _components.shape = _component_num, int(_components.size / _component_num)
    return _components


def _get_absolute_data_address(data_path, file):
    """
    Return the absolute path address of a local data file.

    :params: data_path:
    """
    _file_abs_path = path.abspath(file)
    _path, _file = path.split(_file_abs_path)
    _join = path.join(_path, data_path)
    _join = path.normpath(_join)
    return "file:" + _join


def _get_absolute_uri_path(url, file):
    res = _get_proper_url_parse(url)
    path = res.geturl()
    if res.scheme in ["file", ""]:
        if res.netloc == "":
            path = _get_absolute_data_address(res.path, file)
    return path


def _get_relative_uri_path(dataset_index, filename):
    index = str(dataset_index)
    _absolute_path = _get_absolute_uri_path("", filename)

    _name = path.splitext(path.split(filename)[1])[0] + "_" + index + ".dat"

    _url_relative_path = path.join("file:.", _name)

    absolute_path = path.abspath(
        urlparse(
            path.join(_absolute_path, urlparse(_url_relative_path).path)
        ).path
    )
    return _url_relative_path, absolute_path


# =========================================================================== #
#                             SparseSampling Class                            #
# =========================================================================== #


class SparseSampling:
    r"""Declare a SparseSampling class."""

    __slots__ = (
        "_sparse_dimensions",
        "_sparse_grid_vertexes",
        "_encoding",
        "_quantity_type",
        "_numeric_type",
        "_description",
        "_application",
    )

    def __init__(
        self,
        _sparse_dimensions,
        _sparse_grid_vertexes,
        _encoding="none",
        _quantity_type="scalar",
        _numeric_type="int64",
        _description="",
        _application={},
    ):
        """Initialize a SparseDimension class."""
        # encoding
        self.encoding = _encoding

        # numeric type
        self._numeric_type = NumericType(_numeric_type)

        # quantity_type
        self._quantity_type = QuantityType(_quantity_type)

        # description
        self.description = _description

        # application
        self.application = _application

        # sparse dimensions
        self._sparse_dimensions = _sparse_dimensions

        # sparse grid vertexes
        self._sparse_grid_vertexes = _decode_components(
            [_sparse_grid_vertexes], self
        )

    # encoding
    @property
    def encoding(self):
        r"""Return the data encoding method."""
        return deepcopy(self._encoding)

    @encoding.setter
    def encoding(self, value):
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))
        value = _check_encoding(value)
        self._encoding = value

    # numeric type
    @property
    def numeric_type(self):
        r"""Return the numeric type of data values."""
        return deepcopy(self._numeric_type)

    @numeric_type.setter
    def numeric_type(self, value):
        self._numeric_type._update(value)

    # application
    @property
    def application(self):
        """Return an application metadata dictionary."""
        return deepcopy(self._application)

    @application.setter
    def application(self, value):
        if not isinstance(value, dict):
            raise ValueError(
                "A dict value is required, found {0}".format(type(value))
            )
        self._application = value

    # description
    @property
    def description(self):
        r"""Return the description of the object."""
        return deepcopy(self._description)

    @description.setter
    def description(self, value):
        if isinstance(value, str):
            self._description = value
        else:
            raise ValueError(
                (
                    "Description requires a string, {0} given".format(
                        type(value)
                    )
                )
            )

    # sparse dimensions
    @property
    def sparse_dimensions(self):
        """List of dimension indexes corresponding to sparse dimensions."""
        return deepcopy(self._sparse_dimensions)

    # sparse grid vertexes
    @property
    def sparse_grid_vertexes(self):
        """List of grid vertexes corresponding to sparse dimensions."""
        return deepcopy(self._sparse_dimensions)


# =========================================================================== #
#               	       BaseDependentVariable Class      			      #
# =========================================================================== #


class BaseDependentVariable:
    r"""Declare a BaseDependentVariable class."""

    __slots__ = (
        "_name",
        "_unit",
        "_quantity_name",
        "_encoding",
        "_numeric_type",
        "_quantity_type",
        "_component_labels",
        "_components",
        "_total_components",
        "_application",
        "_description",
    )

    def __init__(
        self,
        _name="",
        _unit="",
        _quantity_name=None,
        _encoding="none",
        _numeric_type="float32",
        _quantity_type="scalar",
        _components=None,
        _component_labels=None,
        _description="",
        _application={},
    ):
        r"""Instantiate a BaseDependentVariable class."""
        # name
        self.name = _name

        # unit
        _va = _assign_and_check_unit_consistency(_unit, None)
        self._unit = _va.unit

        # quantity_name
        self._quantity_name = _check_quantity(_quantity_name, self._unit)

        # encoding
        self.encoding = _encoding

        # numeric type
        self._numeric_type = NumericType(_numeric_type)

        # quantity_type
        self._quantity_type = QuantityType(_quantity_type)

        # components label
        self.set_components_label(_component_labels)

        # description
        self.description = _description

        # application
        self.application = _application

        # components
        self._components = _components

    def set_components_label(self, component_labels):
        """
        Assign an array of strings, based on the number of components.

        If no label is provided, a default values,
        :math:`['', '', N_k]`, is assigned. If the number of component labels
        does not match the total number of components, a warning is raised and
        the inconsistency is resolved by appropriate truncating or adding the
        required number of strings.
        """
        _n = self._quantity_type._p
        if component_labels is None:
            _labels = ["" for i in range(_n)]
            self._component_labels = _labels
            return

        if not isinstance(component_labels, list):
            raise ValueError(
                (
                    "A list of string labels is required, " "{0} provided."
                ).format(type(component_labels))
            )

        _component_length = len(component_labels)
        if _component_length != _n:
            warnings.warn(
                (
                    "The number of component labels, {0}, is not equal to the "
                    "number of components, {1}. The inconsistency is resolved "
                    "by appropriate truncation or addition of the strings."
                ).format(len(component_labels), _n)
            )

            if _component_length > _n:
                self._component_labels = component_labels[:_n]
            else:
                _lables = ["" for i in range(_n)]
                for i, item in enumerate(component_labels):
                    _lables[i] = item
                self._component_labels = _lables
            return

        self._component_labels = component_labels

    # ----------------------------------------------------------------------- #
    #                     BaseIndependentVariable Attributes                  #
    # ----------------------------------------------------------------------- #

    # name
    @property
    def name(self):
        """Dependent variable name."""
        return deepcopy(self._name)

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))
        self._name = value

    # unit
    @property
    def unit(self):
        """Dependent variable name."""
        return deepcopy(self._unit)

    # quantity_name
    @property
    def quantity_name(self):
        """Return quantity name."""
        return deepcopy(self._quantity_name)

    @quantity_name.setter
    def quantity_name(self, value=""):
        raise NotImplementedError(
            ("The `quantity_name` attribute cannot be modified.")
        )

    # encoding
    @property
    def encoding(self):
        r"""Return the data encoding method."""
        return deepcopy(self._encoding)

    @encoding.setter
    def encoding(self, value):
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))
        value = _check_encoding(value)
        self._encoding = value

    # numeric type
    @property
    def numeric_type(self):
        r"""Return the numeric type of data values."""
        return deepcopy(self._numeric_type)

    @numeric_type.setter
    def numeric_type(self, value):
        self._numeric_type._update(value)

    # quantity type
    @property
    def quantity_type(self):
        r"""Return the quantity type of the dataset."""
        return deepcopy(self._quantity_type)

    @quantity_type.setter
    def quantity_type(self, value):
        self._quantity_type._update(value)

    # component labels
    @property
    def component_labels(self):
        r"""Return an ordered array of labels."""
        return self._component_labels

    @component_labels.setter
    def component_labels(self, value):
        self.set_components_label(value)

    # application
    @property
    def application(self):
        """Return application metadata dictionary."""
        return deepcopy(self._application)

    @application.setter
    def application(self, value):
        if not isinstance(value, dict):
            raise ValueError(
                "A dict value is required, found {0}".format(type(value))
            )
        self._application = value

    # description
    @property
    def description(self):
        r"""Return the description of the object."""
        return deepcopy(self._description)

    @description.setter
    def description(self, value):
        if isinstance(value, str):
            self._description = value
        else:
            raise ValueError(
                "Description requires a string, {0} given".format(type(value))
            )

    # components
    @property
    def components(self):
        """Return components array."""
        dtype = self._numeric_type._nptype
        if self._components.dtype != dtype:
            self._components = np.asarray(self._components, dtype)
        return self._components

    @components.setter
    def components(self, value):
        value = np.asarray(value)
        if value.shape == self.components.shape:
            _set_components(self, value)
        else:
            raise ValueError(
                (
                    "The shape of `{0}`, `{1}`, is not consistent\nwith the "
                    "shape of the components array, `{2}`."
                ).format(
                    value.__class__.__name__,
                    value.shape,
                    self.components.shape,
                )
            )

    # ----------------------------------------------------------------------- #
    #                      BaseIndependentVariable Methods                    #
    # ----------------------------------------------------------------------- #

    def _get_dictionary(
        self, filename=None, dataset_index=None, for_display=True, version=None
    ):
        r"""Return a dictionary object of the base class."""
        dictionary = {}
        if self._description.strip() != "":
            dictionary["description"] = str(self._description)

        if self._name.strip() != "":
            dictionary["name"] = self._name

        if str(self._unit) != "":
            dictionary["unit"] = value_object_format(
                1.0 * self._unit, numerical_value=False
            )

        if self._quantity_name not in ["dimensionless", "unknown", None]:
            dictionary["quantity_name"] = self._quantity_name

        dictionary["encoding"] = str(self._encoding)
        dictionary["numeric_type"] = str(self._numeric_type)

        if str(self._quantity_type) != "scalar":
            dictionary["quantity_type"] = str(self._quantity_type)

        print_label = False
        for label in self._component_labels:
            if label.strip() != "":
                print_label = True
                break

        if print_label:
            dictionary["component_labels"] = self._component_labels

        if self._application != {}:
            dictionary["application"] = self._application

        if for_display:
            dictionary["components"] = _reduced_display(
                self._components
            )  # [:-2]
            del dictionary["encoding"]
            return dictionary

        c = _ravel_data(self)

        if self.encoding == "none":
            dictionary["components"] = c.tolist()

        if self.encoding == "base64":
            dictionary["components"] = [
                base64.b64encode(item).decode("utf-8") for item in c
            ]

        if self.encoding == "raw":
            _url_relative_path, absolute_path = _get_relative_uri_path(
                dataset_index, filename
            )

            c.ravel().tofile(absolute_path)

            dictionary["type"] = "external"
            dictionary["components_url"] = _url_relative_path

        del c
        return dictionary


def _check_number_of_components_and_encoding_key(length, obj_):
    """Verify the consistency of encoding wrt the number of components."""
    if length != obj_._quantity_type._p:
        raise Exception(
            (
                "quantity_type '{0}' requires exactly {1} component(s), "
                "found {2}."
            ).format(
                obj_._quantity_type._value, obj_._quantity_type._p, length
            )
        )


def _decode_components(_components, obj):
    """
    Decode the components based on the encoding key value.

    The valid encodings are 'base64', 'none' (text), and 'raw' (binary).
    """
    _val_len = len(_components)

    if obj._encoding == "base64":
        _check_number_of_components_and_encoding_key(_val_len, obj)
        return _decode_base64(_components, obj._numeric_type._nptype)

    if obj._encoding == "none":
        _check_number_of_components_and_encoding_key(_val_len, obj)
        return _decode_none(_components, obj._numeric_type._nptype)

    if obj._encoding == "raw":
        _dtype = obj._numeric_type._nptype
        _component_num = obj._quantity_type._p
        return _decode_raw(_components, _dtype, _component_num)

    raise Exception(
        "'{0}' is an invalid data 'encoding'.".format(obj._encoding)
    )


def _set_components(member, _components, _numeric_type=None):
    # numeric type
    if _numeric_type is None:
        _numeric_type = numpy_dtype_to_numeric_type(str(_components.dtype))
    member._numeric_type._update(_numeric_type)

    # components
    member._components = np.asarray(_components, member._numeric_type._nptype)


def _ravel_data(member):
    """Encode data based on the encoding key value."""
    _n = member._quantity_type._p
    size = member._components[0].size
    if member._numeric_type._value in ["complex64", "complex128"]:

        if member._numeric_type._value == "complex64":
            c = np.empty((_n, size * 2), dtype=np.float32)

        if member._numeric_type._value == "complex128":
            c = np.empty((_n, size * 2), dtype=np.float64)

        for i in range(_n):
            c[i, 0::2] = member._components.real[i].ravel()
            c[i, 1::2] = member._components.imag[i].ravel()

    else:
        c = np.empty((_n, size), dtype=member._numeric_type._nptype)
        for i in range(_n):
            c[i] = member._components[i].ravel()

    return c


def _reduced_display(_components):
    r"""
        Reduced display for quick view of the data structure.

        The method shows the first and the last two data values.
    """
    # _str = ""
    _string = []
    for i in range(len(_components)):
        temp = _components[i].ravel()
        lst = [str(temp[0]), str(temp[0]), str(temp[-2]), str(temp[-2])]
        _string.append([("{0}, {1}, ..., {2}, {3}").format(*lst)])
        # _str = _str + _string
    temp = None
    return _string


# =========================================================================== #
#                             InternalDataset Class                           #
# =========================================================================== #


class InternalDataset(BaseDependentVariable):
    """InternalDataset class."""

    __slots__ = ("_components", "_sparse_sampling")

    def __init__(
        self,
        _name="",
        _unit="",
        _quantity_name=None,
        _encoding="none",
        _numeric_type=None,
        _quantity_type="scalar",
        _component_labels=None,
        _components=None,
        _description="",
        _application={},
        _sparse_dimensions=None,
        _sparse_grid_vertexes=None,
        _sparse_encoding="none",
        _sparse_numeric_type="int64",
        _sparse_description="",
        _sparse_application={},
    ):
        """Initialize."""
        self._sparse_sampling = {}

        if isinstance(_components, list) and _components != []:
            if isinstance(_components[0], np.ndarray):
                _components = np.asarray(_components)

        if isinstance(_components, np.ndarray):
            if _numeric_type is None:
                _numeric_type = numpy_dtype_to_numeric_type(
                    str(_components.dtype)
                )
                self._components = _components
            else:
                self._components = _components.astype(_numeric_type)

        super(InternalDataset, self).__init__(
            _name=_name,
            _unit=_unit,
            _quantity_name=_quantity_name,
            _encoding=_encoding,
            _numeric_type=_numeric_type,
            _quantity_type=_quantity_type,
            _components=_components,
            _component_labels=_component_labels,
            _description=_description,
            _application=_application,
        )

        # super base class must be initialized before retrieving
        # the components array.

        if not isinstance(_components, np.ndarray):
            _components = _decode_components(_components, self)
            self._components = _components

        if _sparse_dimensions is not None:
            self._sparse_sampling = SparseSampling(
                _sparse_dimensions=_sparse_dimensions,
                _sparse_grid_vertexes=_sparse_grid_vertexes,
                _encoding=_sparse_encoding,
                _numeric_type=_sparse_numeric_type,
                _application=_sparse_application,
                _description=_sparse_description,
            )

    def _get_python_dictionary(
        self, filename=None, dataset_index=None, for_display=True, version=None
    ):
        """Return the InternalData object as a python dictionary."""
        dictionary = {}

        dictionary["type"] = "internal"
        dictionary.update(
            self._get_dictionary(filename, dataset_index, for_display, version)
        )
        return dictionary


# =========================================================================== #
#                            ExternalDataset Class                            #
# =========================================================================== #


class ExternalDataset(BaseDependentVariable):
    """ExternalDataset class."""

    __slots__ = ("_components", "_components_url", "_sparse_sampling")

    def __init__(
        self,
        _name="",
        _unit="",
        _quantity_name=None,
        _encoding="none",
        _numeric_type=None,
        _quantity_type="scalar",
        _component_labels=None,
        _components_url=None,
        _filename="",
        _description="",
        _application={},
        _sparse_dimensions=None,
        _sparse_grid_vertexes=None,
        _sparse_encoding="none",
        _sparse_numeric_type="int64",
        _sparse_description="",
        _sparse_application={},
    ):
        """Initialize."""
        self._sparse_sampling = {}

        super(ExternalDataset, self).__init__(
            _name=_name,
            _unit=_unit,
            _quantity_name=_quantity_name,
            _encoding=_encoding,
            _numeric_type=_numeric_type,
            _quantity_type=_quantity_type,
            _components=None,
            _component_labels=_component_labels,
            _description=_description,
            _application=_application,
        )

        _absolute_URI = _get_absolute_uri_path(_components_url, _filename)
        self._components_url = _components_url

        _components = urlopen(_absolute_URI).read()
        self._components = _decode_components(_components, self)

        if _sparse_dimensions is not None:
            self._sparse_sampling = SparseSampling(
                _sparse_dimensions=_sparse_dimensions,
                _sparse_grid_vertexes=_sparse_grid_vertexes,
                _encoding=_sparse_encoding,
                _numeric_type=_sparse_numeric_type,
                _application=_sparse_application,
                _description=_sparse_description,
            )

    @property
    def components_url(self):
        """Return components_url of the CSDM serialized file."""
        return self._components_url

    def _get_python_dictionary(
        self, filename=None, dataset_index=None, for_display=True, version=None
    ):
        """Return the InternalData object as a python dictionary."""
        dictionary = {}

        dictionary["type"] = "internal"
        dictionary.update(
            self._get_dictionary(filename, dataset_index, for_display, version)
        )
        return dictionary

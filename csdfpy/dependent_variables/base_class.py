# -*- coding: utf-8 -*-
"""The Base DependentVariable class."""
from __future__ import division
from __future__ import print_function

import base64
import warnings
from copy import deepcopy

import numpy as np

from csdfpy.dependent_variables.download import _get_relative_uri_path
from csdfpy.units import check_quantity_name
from csdfpy.units import ScalarQuantity
from csdfpy.utils import _check_encoding
from csdfpy.utils import _type_message
from csdfpy.utils import NumericType
from csdfpy.utils import numpy_dtype_to_numeric_type
from csdfpy.utils import QuantityType

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"

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
        name="",
        unit="",
        quantity_name=None,
        encoding="none",
        numeric_type="float32",
        quantity_type="scalar",
        components=None,
        component_labels=None,
        description="",
        application={},
        **kwargs,
    ):
        r"""Instantiate a BaseDependentVariable class."""
        # name
        self.name = name

        # unit
        _va = ScalarQuantity(f"1 {unit}").quantity
        self._unit = _va.unit

        # quantity_name
        self._quantity_name = check_quantity_name(quantity_name, self._unit)

        # encoding
        self.encoding = encoding

        # numeric type
        self._numeric_type = NumericType(numeric_type)

        # quantity_type
        self._quantity_type = QuantityType(quantity_type)

        # components label
        self.set_components_label(component_labels)

        # description
        self.description = description

        # application
        self.application = application

        # components
        self._components = components

    def set_components_label(self, component_labels):
        """
        Assign an array of strings, based on the number of components.

        If no label is provided, a default values,
        :math:`['', '', N_k]`, is assigned. If the number of component labels
        does not match the total number of components, a warning is raised and
        the inconsistency is resolved by appropriate truncating or adding the
        required number of strings.
        """
        _n = self._quantity_type.p
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
        self._numeric_type.update(value)

    # quantity type
    @property
    def quantity_type(self):
        r"""Return the quantity type of the dataset."""
        return deepcopy(self._quantity_type)

    @quantity_type.setter
    def quantity_type(self, value):
        self._quantity_type.update(value)

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
        obj = {}
        if self._description.strip() != "":
            obj["description"] = str(self._description)

        if self._name.strip() != "":
            obj["name"] = self._name

        if str(self._unit) != "":
            obj["unit"] = ScalarQuantity(1.0 * self._unit).format("unit")

        if self._quantity_name not in ["dimensionless", "unknown", None]:
            obj["quantity_name"] = self._quantity_name

        obj["encoding"] = str(self._encoding)
        obj["numeric_type"] = str(self._numeric_type)

        if str(self._quantity_type) != "scalar":
            obj["quantity_type"] = str(self._quantity_type)

        print_label = False
        for label in self._component_labels:
            if label.strip() != "":
                print_label = True
                break

        if print_label:
            obj["component_labels"] = self._component_labels

        if self._application != {}:
            obj["application"] = self._application

        if for_display:
            obj["components"] = _reduced_display(self._components)
            del obj["encoding"]
            return obj

        c = _ravel_data(self)

        if self.encoding == "none":
            obj["components"] = c.tolist()

        if self.encoding == "base64":
            obj["components"] = [
                base64.b64encode(item).decode("utf-8") for item in c
            ]

        if self.encoding == "raw":
            _url_relative_path, absolute_path = _get_relative_uri_path(
                dataset_index, filename
            )

            c.ravel().tofile(absolute_path)

            obj["type"] = "external"
            obj["components_url"] = _url_relative_path

        del c
        return obj


def _set_components(member, _components, _numeric_type=None):
    # numeric type
    if _numeric_type is None:
        _numeric_type = numpy_dtype_to_numeric_type(str(_components.dtype))
    member._numeric_type.update(_numeric_type)

    # components
    member._components = np.asarray(_components, member._numeric_type._nptype)


def _ravel_data(member):
    """Encode data based on the encoding key value."""
    _n = member._quantity_type.p
    size = member._components[0].size
    if member._numeric_type.value in ["complex64", "complex128"]:

        if member._numeric_type.value == "complex64":
            c = np.empty((_n, size * 2), dtype=np.float32)

        if member._numeric_type.value == "complex128":
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
    temp = None
    return _string

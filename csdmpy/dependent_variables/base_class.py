# -*- coding: utf-8 -*-
"""The Base DependentVariable class."""
from __future__ import division
from __future__ import print_function

import base64
import warnings
from copy import deepcopy

import numpy as np

from csdmpy.dependent_variables.download import get_relative_url_path
from csdmpy.units import check_quantity_name
from csdmpy.units import ScalarQuantity
from csdmpy.utils import check_encoding
from csdmpy.utils import NumericType
from csdmpy.utils import numpy_dtype_to_numeric_type
from csdmpy.utils import QuantityType
from csdmpy.utils import validate


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["BaseDependentVariable"]


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
        self.name = name
        self._unit = ScalarQuantity(f"1 {unit}").quantity.unit
        self._quantity_name = check_quantity_name(quantity_name, self._unit)
        self.encoding = encoding
        self._numeric_type = NumericType(numeric_type)
        self._quantity_type = QuantityType(quantity_type)
        self.set_component_labels(component_labels)
        self.description = description
        self.application = application
        self._components = components

    def __eq__(self, other):
        """Overrides the default implementation"""
        check = [
            self.name == other.name,
            self._unit == other._unit,
            self._quantity_name == other._quantity_name,
            self._encoding == other._encoding,
            self._numeric_type == other._numeric_type,
            self._quantity_type == other._quantity_type,
            self._component_labels == other._component_labels,
            self._description == other._description,
            self._application == other._application,
            np.allclose(self._components, other._components),
        ]
        if False in check:
            return False
        return True

    def set_component_labels(self, component_labels):
        """
        Assign an array of strings, based on the number of components.

        If no label is provided, a default values,
        :math:`['', '', N_k]`, is assigned. If the number of component labels
        does not match the total number of components, a warning is raised and
        the inconsistency is resolved by appropriate truncating or adding the
        required number of strings.
        """
        n = self._quantity_type.p
        if component_labels is None:
            self._component_labels = ["" for i in range(n)]
            return

        validate(component_labels, "component_labels", list)

        component_length = len(component_labels)
        if component_length == n:
            self._component_labels = component_labels
            return

        warning_statement = (
            f"The number of component labels, {component_length}, is not equal"
            f" to the number of components, {n}. The inconsistency is resolved"
            f" by appropriate truncation or addition of the strings."
        )
        warnings.warn(warning_statement)

        if component_length > n:
            self._component_labels = component_labels[:n]
            return

        lables = ["" for i in range(n)]
        for i, item in enumerate(component_labels):
            lables[i] = item
        self._component_labels = lables
        return

    # ----------------------------------------------------------------------- #
    #                                Attributes                               #
    # ----------------------------------------------------------------------- #
    @property
    def name(self):
        """Return name associated with the dependent variable."""
        return deepcopy(self._name)

    @name.setter
    def name(self, value):
        self._name = validate(value, "name", str)

    @property
    def unit(self):
        """Return uint associated with the dependent variable."""
        return deepcopy(self._unit)

    @property
    def quantity_name(self):
        """Return quantity name associated with the physical quantity."""
        return deepcopy(self._quantity_name)

    @quantity_name.setter
    def quantity_name(self, value=""):
        raise NotImplementedError("The `quantity_name` attribute cannot be modified.")

    @property
    def encoding(self):
        r"""Return encoding method used in storing dependent variable."""
        return deepcopy(self._encoding)

    @encoding.setter
    def encoding(self, value):
        self._encoding = validate(value, "encoding", str, method=check_encoding)

    @property
    def numeric_type(self):
        r"""Return numeric type associated with dependent variable."""
        return deepcopy(self._numeric_type)

    @numeric_type.setter
    def numeric_type(self, value):
        self._numeric_type.update(value)

    @property
    def quantity_type(self):
        r"""Return quantity type associated with dependent variable."""
        return deepcopy(self._quantity_type)

    @quantity_type.setter
    def quantity_type(self, value):
        self._quantity_type.update(value)

    @property
    def component_labels(self):
        r"""
        Return an ordered array of labels associated with each component of the
        dependent variable.
        """
        return self._component_labels

    @component_labels.setter
    def component_labels(self, value):
        self.set_component_labels(value)

    @property
    def application(self):
        """Return the application metadata dictionary, if any."""
        return self._application

    @application.setter
    def application(self, value):
        self._application = validate(value, "application", dict)

    @property
    def description(self):
        r"""Return a description of the dependent variable."""
        return deepcopy(self._description)

    @description.setter
    def description(self, value):
        self._description = validate(value, "description", str)

    @property
    def components(self):
        """Return components array."""
        dtype = self._numeric_type.dtype
        if self._components.dtype != dtype:
            self._components = np.asarray(self._components, dtype)
        return self._components

    @components.setter
    def components(self, value):
        value = np.asarray(value)
        if value.shape == self.components.shape:
            self.set_components(value)
            return
        raise ValueError(
            f"The shape of the `{value.__class__.__name__}`, `{value.shape}`, is "
            f"inconsistent with the shape of the components array, "
            f"`{self.components.shape}`."
        )

    # ----------------------------------------------------------------------- #
    #                                  Methods                                #
    # ----------------------------------------------------------------------- #

    def _get_dictionary(
        self, filename=None, dataset_index=None, for_display=False, version=None
    ):
        r"""Return a dictionary object of the base class."""
        obj = {}
        if self._description.strip() != "":
            obj["description"] = str(self._description)

        if self._name.strip() != "":
            obj["name"] = self._name

        if str(self._unit) != "":
            obj["unit"] = ScalarQuantity(1.0 * self._unit).__format__("unit")

        if self._quantity_name not in ["dimensionless", "unknown", None]:
            obj["quantity_name"] = self._quantity_name

        obj["encoding"] = str(self._encoding)
        obj["numeric_type"] = str(self._numeric_type)
        obj["quantity_type"] = str(self._quantity_type)

        # print_label = False
        for label in self._component_labels:
            if label.strip() != "":
                obj["component_labels"] = self._component_labels
                break

        # if print_label:
        #     obj["component_labels"] = self._component_labels

        if self._application != {}:
            obj["application"] = self._application

        if for_display:
            obj["components"] = reduced_display(self._components)
            del obj["encoding"]
            return obj

        c = self.ravel_data()

        if self.encoding == "none":
            obj["components"] = c.tolist()

        if self.encoding == "base64":
            obj["components"] = [base64.b64encode(item).decode("utf-8") for item in c]

        if self.encoding == "raw":
            url_relative_path, absolute_path = get_relative_url_path(
                dataset_index, filename
            )

            c.ravel().tofile(absolute_path)

            obj["type"] = "external"
            obj["components_url"] = url_relative_path
            del obj["encoding"]

        del c
        return obj

    def set_components(self, _components, _numeric_type=None):
        if _numeric_type is None:
            _numeric_type = numpy_dtype_to_numeric_type(str(_components.dtype))
        self._numeric_type.update(_numeric_type)

        self._components = np.asarray(_components, self._numeric_type.dtype)

    def ravel_data(self):
        """Encode data based on the encoding key value."""
        n = self._quantity_type.p
        size = self._components[0].size
        if self._numeric_type.value in ["complex64", "complex128"]:

            if self._numeric_type.value == "complex64":
                c = np.empty((n, size * 2), dtype=np.float32)

            if self._numeric_type.value == "complex128":
                c = np.empty((n, size * 2), dtype=np.float64)

            for i in range(n):
                c[i, 0::2] = self._components.real[i].ravel()
                c[i, 1::2] = self._components.imag[i].ravel()

        else:
            c = np.empty((n, size), dtype=self._numeric_type.dtype)
            for i in range(n):
                c[i] = self._components[i].ravel()

        return c


def reduced_display(_components):
    r"""
        Reduced display for quick view of the data structure.

        The method shows the first and the last two data values.
    """
    _string = []
    for i in range(len(_components)):
        temp = _components[i].ravel()
        lst = [str(temp[0]), str(temp[1]), str(temp[-2]), str(temp[-1])]
        _string.append([("{0}, {1}, ..., {2}, {3}").format(*lst)])
    return _string

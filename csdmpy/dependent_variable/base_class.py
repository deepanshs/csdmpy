"""The Base DependentVariable class."""
import base64
import warnings
from copy import deepcopy

import numpy as np

from csdmpy.dependent_variable.download import get_relative_url_path
from csdmpy.dependent_variable.sparse import SparseSampling
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
    """BaseDependentVariable class."""

    __slots__ = (
        "_name",
        "_unit",
        "_quantity_name",
        "_encoding",
        "_numeric_type",
        "_quantity_type",
        "_component_labels",
        "_application",
        "_description",
        "_sparse_sampling",
        "_components",
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
        application=None,
        sparse_sampling=None,
        **kwargs,
    ):
        """Init BaseDependentVariable class."""
        self._name = name
        self._unit = ScalarQuantity(f"1 {unit}").quantity.unit
        self._quantity_name = check_quantity_name(quantity_name, self._unit)
        self._encoding = encoding
        self._numeric_type = NumericType(numeric_type)
        self._quantity_type = QuantityType(quantity_type)
        self.set_component_labels(component_labels)
        self._description = description
        self._application = application
        self._components = components
        self._sparse_sampling = (
            SparseSampling(**sparse_sampling) if sparse_sampling != {} else {}
        )

    def __eq__(self, other):
        check = [
            getattr(self, _) == getattr(other, _) for _ in __class__.__slots__[:-1]
        ]
        check += [np.allclose(self._components, other._components)]
        return False if False in check else True

    def set_component_labels(self, component_labels):
        """Assign an array of strings, based on the number of components.

        If no label is provided, a default values,
        :math:`['', '', N_k]`, is assigned. If the number of component labels
        does not match the total number of components, a warning is raised and
        the inconsistency is resolved by appropriate truncating or adding the
        required number of strings.
        """
        n_1 = self._quantity_type.p
        if component_labels is None:
            self._component_labels = ["" for i in range(n_1)]
            return

        validate(component_labels, "component_labels", list)

        component_length = len(component_labels)
        if component_length == n_1:
            self._component_labels = component_labels
            return

        warning_statement = (
            f"The number of component labels, {component_length}, is not equal"
            f" to the number of components, {n_1}. The inconsistency is resolved"
            " by appropriate truncation or addition of the strings."
        )
        warnings.warn(warning_statement)

        if component_length > n_1:
            self._component_labels = component_labels[:n_1]
            return

        labels = ["" for i in range(n_1)]
        for i, item in enumerate(component_labels):
            labels[i] = item
        self._component_labels = labels
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
        return deepcopy(str(self._quantity_name))

    @quantity_name.setter
    def quantity_name(self, value=""):
        raise NotImplementedError("The `quantity_name` attribute cannot be modified.")

    @property
    def encoding(self):
        """Return encoding method used in storing dependent variable."""
        return deepcopy(self._encoding)

    @encoding.setter
    def encoding(self, value):
        self._encoding = validate(value, "encoding", str, method=check_encoding)

    @property
    def numeric_type(self):
        """Return numeric type associated with dependent variable."""
        return deepcopy(self._numeric_type)

    @numeric_type.setter
    def numeric_type(self, value):
        self._numeric_type.update(value)

    @property
    def quantity_type(self):
        """Return quantity type associated with dependent variable."""
        return deepcopy(self._quantity_type)

    @quantity_type.setter
    def quantity_type(self, value):
        self._quantity_type.update(value)

    @property
    def component_labels(self):
        """Return an ordered array of labels associated with each component of the
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
        self._application = validate(value, "application", (dict, type(None)))

    @property
    def description(self):
        """Return a description of the dependent variable."""
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
            "inconsistent with the shape of the components array, "
            f"`{self.components.shape}`."
        )

    # ----------------------------------------------------------------------- #
    #                                  Methods                                #
    # ----------------------------------------------------------------------- #

    def to_dict(self, filename=None, dataset_index=None, for_display=False):
        """Alias to the `dict()` method of the class."""
        return self.dict(filename, dataset_index, for_display)

    def dict(self, filename=None, dataset_index=None, for_display=False):
        """Return a dictionary object of the base class."""
        obj = {}
        obj["description"] = self._description.strip()
        obj["name"] = self._name.strip()
        obj["unit"] = (
            ScalarQuantity(1.0 * self._unit).__format__("unit")
            if str(self._unit) != ""
            else ""
        )
        obj["quantity_name"] = self._quantity_name
        obj["encoding"] = str(self._encoding)
        obj["numeric_type"] = str(self._numeric_type)
        obj["quantity_type"] = str(self._quantity_type)

        for label in self._component_labels:
            if label.strip() != "":
                obj["component_labels"] = self._component_labels
                break

        obj["application"] = self._application

        empty_values = [[], "", {}, "dimensionless", "unknown", None]
        _ = [obj.pop(_) for _ in [k for k, v in obj.items() if v in empty_values]]

        if for_display:
            obj["components"] = reduced_display(self._components)
            del obj["encoding"]
            return obj

        self.get_proper_encoded_data(obj, filename, dataset_index)
        return obj

    def get_proper_encoded_data(self, obj, filename=None, dataset_index=None):
        """Encode dependent variables to encoding type."""
        data = self.ravel_data()

        if self.encoding == "none":
            obj["components"] = data.tolist()

        if self.encoding == "base64":
            obj["components"] = [base64.b64encode(_).decode("utf-8") for _ in data]

        if self.encoding == "raw":
            url_relative_path, absolute_path = get_relative_url_path(
                dataset_index, filename
            )

            data.ravel().tofile(absolute_path)

            obj["type"] = "external"
            obj["components_url"] = url_relative_path
            del obj["encoding"]

    def set_components(self, _components, _numeric_type=None):
        """Set dependent variable components."""
        if _numeric_type is None:
            _numeric_type = numpy_dtype_to_numeric_type(str(_components.dtype))
        self._numeric_type.update(_numeric_type)
        self._components = np.asarray(_components, self._numeric_type.dtype)

    def ravel_data(self):
        """Encode data based on the encoding key value."""
        n_1 = self._quantity_type.p
        size = self._components[0].size
        if self._numeric_type.value in ["complex64", "complex128"]:

            if self._numeric_type.value == "complex64":
                data = np.empty((n_1, size * 2), dtype=np.float32)

            if self._numeric_type.value == "complex128":
                data = np.empty((n_1, size * 2), dtype=np.float64)

            for i in range(n_1):
                data[i, 0::2] = self._components.real[i].ravel()
                data[i, 1::2] = self._components.imag[i].ravel()

        else:
            data = np.empty((n_1, size), dtype=self._numeric_type.dtype)
            for i in range(n_1):
                data[i] = self._components[i].ravel()

        return data


def reduced_display(_components):
    """Reduced display for quick view of the data structure. The method shows the
    first and the last two data values.
    """
    _string = []
    for _, item in enumerate(_components):
        temp = item.ravel()
        lst = [str(temp[0]), str(temp[1]), str(temp[-2]), str(temp[-1])]
        _string.append([("{}, {}, ..., {}, {}").format(*lst)])
    return _string

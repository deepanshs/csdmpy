# -*- coding: utf-8 -*-
"""Helper methods for CSDM class."""
from __future__ import print_function

import numpy as np
from astropy.units.quantity import Quantity

from csdmpy.units import ScalarQuantity

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"

__all__ = ["literals_encoding", "QuantityType", "NumericType"]

literals_quantity_type = {
    "scalar": lambda n: 1,
    "vector": lambda n: n,
    "matrix": lambda n: n,
    "audio": lambda n: n,
    "pixel": lambda n: n,
    "symmetric_matrix": lambda n: int(n * (n + 1) / 2),
}

literals_encoding = ("base64", "none", "raw")
literals_quantity_type_ = [
    "scalar",
    "vector_n",
    "matrix_n_m",
    # "audio_n",
    "pixel_n",
    "symmetric_matrix_n",
]


class QuantityType:
    """
    Validate the quantity_type string value.

    The valid options are `scalar`, `vector_n`, `pixel_n`,
    `matrix_n_m`, and `symmetric_matrix_n`.

    :returns: The quantity_type key-value, if the value is valid.
    :raises KeyError: Otherwise.
    """

    __slots__ = ("value", "p")

    def __init__(self, element):
        r"""Instantiate a QuantityType class instance."""
        self.update(element)

    def __str__(self):
        r"""Return a string with the quantity type."""
        return self.value

    def __eq__(self, other):
        """Overrides the default implementation"""
        check = [self.value == other.value, self.p == other.p]
        if False in check:
            return False
        return True

    def update(self, element):
        """Update the quantity type."""
        validate(element, "quantity_type", str, self._check_quantity_type)

    @classmethod
    def _get_number_of_components(cls, keyword, numbers):
        return int(literals_quantity_type[keyword](numbers.prod()))

    def _check_quantity_type(self, element):
        list_values = element.strip().split("_")
        numbers = np.asarray([int(item) for item in list_values if item.isnumeric()])
        keyword = "_".join([item for item in list_values if not item.isnumeric()])

        lst = literals_quantity_type
        if keyword not in lst:
            message = (
                "The value, `{0}`, is an invalid `quantity_type` enumeration literal. "
                "The allowed values are {1}."
            )

            raise ValueError(
                message.format(
                    keyword, "'" + "', '".join(literals_quantity_type_) + "'"
                )
            )

        components = self._get_number_of_components(keyword, numbers)
        self.value = element
        self.p = components


class NumericType:
    """
    Validate the numeric_type string value.

    The valid options are
    `uint8`, `uint16`, `uint32`, `uint64`, `int8`, `int16`, `int32`, `int64`,
    `float32`, `float64`, `complex64`, and `complex128`.
    The byte order for multi-byte numeric_types are assumed to follow the
    little endianness format.

    :returns: The numeric_type value, if the value is valid.
    :raises KeyError: Otherwise.
    """

    __slots__ = ("value", "dtype")

    _lst = {
        "uint8": "<u1",
        "uint16": "<u2",
        "uint32": "<u4",
        "uint64": "<u8",
        "int8": "<i1",
        "int16": "<i2",
        "int32": "<i4",
        "int64": "<i8",
        # "float16": "<f2",
        "float32": "<f4",
        "float64": "<f8",
        "complex64": "<c8",
        "complex128": "<c16",
        ">u1": "<u1",
        ">u2": "<u2",
        ">u4": "<u4",
        ">u8": "<u8",
        ">i1": "<i1",
        ">i2": "<i2",
        ">i4": "<i4",
        ">i8": "<i8",
        # ">f2": "<f2",
        ">f4": "<f4",
        ">f8": "<f8",
        ">c8": "<c8",
        ">c16": "<c16",
    }

    literals = (
        "uint8",
        "uint16",
        "uint32",
        "uint64",
        "int8",
        "int16",
        "int32",
        "int64",
        # "float16",
        "float32",
        "float64",
        "complex64",
        "complex128",
    )

    def __init__(self, element="float32"):
        """Instantiate a NumericType class instance."""
        self.update(element)

    def update(self, element):
        """Update the numeric type."""
        validate(
            element, "numeric_type", (str, type, np.dtype), self._check_numeric_type
        )

    def __str__(self):
        """Return a string with the numeric type."""
        return self.value

    def __eq__(self, other):
        """Overrides the default implementation"""
        check = [self.value == other.value, self.dtype == other.dtype]
        if False in check:
            return False
        return True

    def _check_numeric_type(self, element):
        if isinstance(element, np.dtype):
            self.dtype = element
            self.value = str(element)
            return

        if isinstance(element, type):
            self.dtype = np.dtype(element)
            self.value = str(self.dtype)
            return

        lst = self.__class__._lst
        if element not in lst.keys():
            message = (
                "The value, `{0}`, is an invalid `numeric_type` enumeration literal. "
                "The allowed values are {1}."
            )
            literals = self.__class__.literals
            raise ValueError(message.format(element, "'" + "', '".join(literals) + "'"))

        self.value = element
        self.dtype = np.dtype(lst[element])


def validate(value, attr, types, method=None):
    if isinstance(value, types):
        if method is None:
            return value
        return method(value)
    raise TypeError(type_error(types, attr, value))


def type_error(a, b, c):
    if isinstance(a, tuple):
        a = [item.__name__ for item in a]
        a = " or ".join(a)
    else:
        a = a.__name__
    return ("Expecting an instance of type `{0}` for {1}, got `{2}`.").format(
        a, b, type(c).__name__
    )


def attribute_error(a, b):
    return "`{0}` has no attribute `{1}`.".format(a.__class__.__name__, b)


def _axis_label(label, unit=None, label_type=""):
    if unit is not None:
        if label_type == "":
            return f"{label} / ({unit})"
        # if label_type == "latex":
        #     return "{0} / ({1})".format(label, unit.to_string("latex"))
    return label


def _get_dictionary(*arg, **kwargs):
    if arg != ():
        if isinstance(arg[0], dict):
            input_dict = arg[0]
            return input_dict

        raise Exception(
            "The argument is either a dictionary with the allowed keywords or a "
            "collection of valid arguments."
        )
    else:
        input_dict = kwargs
    return input_dict


def check_encoding(element):
    """
    Validate the encoding string value.

    The valid options are `base64`, `none`, and `raw`.

    :returns: The encoding key-value, if the value is valid.
    :raises KeyError: Otherwise.
    """
    if element in literals_encoding:
        return element

    message = (
        "The value, `{0}`, is an invalid `encoding` enumeration literal. "
        "The allowed values are '{1}', '{2}' and '{3}'."
    )
    raise ValueError(message.format(element, *literals_encoding))


def numpy_dtype_to_numeric_type(element):
    """Return a valid numeric_type value based on the dtype of numpy array."""
    lst = {
        "<u1": "uint8",
        "<u2": "uint16",
        "<u4": "uint32",
        "<u8": "uint64",
        "<i1": "int8",
        "<i2": "int16",
        "<i4": "int32",
        "<i8": "int64",
        # "<f2": "float16",
        "<f4": "float32",
        "<f8": "float64",
        "<c8": "complex64",
        "<c16": "complex128",
        ">u1": "uint8",
        ">u2": "uint16",
        ">u4": "uint32",
        ">u8": "uint64",
        ">i1": "int8",
        ">i2": "int16",
        ">i4": "int32",
        ">i8": "int64",
        # ">f2": "float16",
        ">f4": "float32",
        ">f8": "float64",
        ">c8": "complex64",
        ">c16": "complex128",
    }

    lst2 = (
        "uint8",
        "uint16",
        "uint32",
        "uint64",
        "int8",
        "int16",
        "int32",
        "int64",
        # "float16",
        "float32",
        "float64",
        "complex64",
        "complex128",
    )

    if element in lst.keys():
        return lst[element]
    if element in lst2:
        return element
    raise ValueError("The dtype, {0}, is not supported.".format(element))


def check_and_assign_bool(element):
    if element is None:
        return False
    return validate(element, "boolean", bool)


def check_scalar_object(other, operator=""):
    """Check if the object is scalar:
        int, float, complex, np.ndarray, Quantity, or ScalarQuantity.
        Returns: The other object.
    """
    if not isinstance(
        other, (int, float, complex, np.ndarray, Quantity, ScalarQuantity)
    ):
        raise TypeError(
            f"unsupported operand type(s) {operator}: 'CSDM' and "
            f"'{other.__class__.__name__}'."
        )
    if isinstance(other, np.ndarray):
        if other.ndim != 0:
            raise ValueError("Only scalar multiplication or division is allowed.")

    if isinstance(other, ScalarQuantity):
        return other.quantity

    return other


def _get_broadcast_shape(array, ndim, axis):
    """Return the broadcast array for numpy ndarray operations."""
    s = [None for i in range(ndim)]
    s[axis] = slice(None, None, None)
    return array[tuple(s)]

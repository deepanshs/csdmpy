# -*- coding: utf-8 -*-
"""Helper methods for CSDModel class."""
from __future__ import print_function

import numpy as np

from csdfpy.units import ScalarQuantity

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


literals_quantity_type = {
    "RGB": lambda n: 3,
    "RGBA": lambda n: 4,
    "scalar": lambda n: 1,
    "vector": lambda n: n,
    "matrix": lambda n: n,
    "audio": lambda n: n,
    "symmetric_matrix": lambda n: int(n * (n + 1) / 2),
}

literals_encoding = ("base64", "none", "raw")
literals_quantity_type_ = [
    "RGB",
    "RGBA",
    "scalar",
    "vector_n",
    "matrix_n_m",
    "audio_n",
    "symmetric_matrix_n",
]


def _type_message(a, b):
    return ("Expecting instance of type, `{0}`, but got `{1}`.").format(
        a.__name__, b.__name__
    )


def _attribute_message(a, b):
    return "{0} has no attribute `{1}`.".format(a, b)


def _axis_label(
    label,
    unit,
    made_dimensionless=False,
    dimensionless_unit=None,
    label_type="",
):
    if made_dimensionless:
        if dimensionless_unit != "":
            return "{0} / {1}".format(label, dimensionless_unit)
        return label

    if unit != "":
        if label_type == "":
            return "{0} / ({1})".format(
                label, ScalarQuantity(1 * unit).format("unit")
            )
        if label_type == "latex":
            return "{0} / ({1})".format(label, unit.to_string("latex"))
    return label


def _get_dictionary(*arg, **kwargs):
    if arg != ():
        if isinstance(arg[0], dict):
            input_dict = arg[0]
            return input_dict

        raise Exception(
            (
                "The argument is either a dictionary with allowed keywords "
                "or a collection of valid arguments. Use the keys attribute "
                "of the object to list the set of allowed keys."
            )
        )
    else:
        input_dict = kwargs
    return input_dict


def _is_numeric(element):
    return element.isnumeric()


def _check_encoding(element):
    """
    Validate the encoding string value.

    The valid options are `base64`, `none`, and `raw`.

    :returns: The encoding key-value, if the value is valid.
    :raises KeyError: Otherwise.
    """
    if element in literals_encoding:
        return element

    message = (
        "`{0}` is not a valid `encoding` enumeration literal. "
        "The allowed values are '{1}', '{2}' and '{3}'."
    )
    raise ValueError(message.format(element, *literals_encoding))


class QuantityType:
    """
    Validate the quantity_type string value.

    The valid options are `RGB`, `RGBA`, `scalar`, `vector_n`,
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

    def update(self, element):
        """Update the quantity type."""
        if not isinstance(element, str):
            raise TypeError(_type_message(str, type(element)))
        self._check_quantity_type(element)

    @classmethod
    def _get_number_of_components(cls, keyword, numbers):
        return int(literals_quantity_type[keyword](numbers.prod()))

    def _check_quantity_type(self, element):
        list_values = element.strip().split("_")
        numbers = np.asarray(
            [int(item) for item in list_values if item.isnumeric()]
        )
        keyword = "_".join(
            [item for item in list_values if not item.isnumeric()]
        )

        lst = literals_quantity_type
        if keyword not in lst:
            message = (
                "`{0}` is not a valid `quantity_type` enumeration literal. "
                "The allowed values are '{1}', '{2}', '{3}', '{4}', '{5}' and "
                "'{6}'."
            )
            raise ValueError(message.format(keyword, *literals_quantity_type_))

        components = self._get_number_of_components(keyword, numbers)
        self.value = element
        self.p = components


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
        "<f2": "float16",
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
        ">f2": "float16",
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
        "float16",
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


class NumericType:
    """
    Validate the numeric_type string value.

    The valid options are
    `uint8`, `uint16`, `uint32`, `uint64`, `int8`, `int16`, `int32`, `int64`,
    `float16`, `float32`, `float64`, `complex64`, and `complex128`.
    The byte order for multi-byte numeric_types are assumed to follow the
    little endianness format.

    :returns: The numeric_type value, if the value is valid.
    :raises KeyError: Otherwise.
    """

    __slots__ = ("value", "_nptype")

    _lst = {
        "uint8": "<u1",
        "uint16": "<u2",
        "uint32": "<u4",
        "uint64": "<u8",
        "int8": "<i1",
        "int16": "<i2",
        "int32": "<i4",
        "int64": "<i8",
        "float16": "<f2",
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
        ">f2": "<f2",
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
        "float16",
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
        if not isinstance(element, str):
            raise TypeError(_type_message(str, type(element)))
        self._check_numeric_type(element)

    def __str__(self):
        """Return a string with the numeric type."""
        return self.value

    def _check_numeric_type(self, element):
        lst = self.__class__._lst
        # print(lst.keys())
        if element not in lst.keys():
            raise ValueError(
                (
                    "`{0}`, is not a valid `numeric_type` enumeration literal."
                    " The allowed values are {1}".format(
                        element,
                        "'" + "', '".join(self.__class__.literals) + "'",
                    )
                )
            )

        self.value = element
        self._nptype = np.dtype(lst[element])


def _check_and_assign_bool(element):
    if element is None:
        element = False
        return element

    if isinstance(element, bool):
        return element

    raise TypeError(
        "'Boolean' type is required for '{0}', given '{1}' ".format(
            str(element), element.__class__.__name__
        )
    )

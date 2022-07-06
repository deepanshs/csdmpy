"""Helper methods for CSDM class."""
from copy import deepcopy

import numpy as np
from astropy.units.quantity import Quantity

from .units import ScalarQuantity

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"

__all__ = ["LITERALS_ENCODING", "QuantityType", "NumericType"]

literals_quantity_type = {
    "scalar": lambda n: 1,
    "vector": lambda n: n,
    "matrix": lambda n: n,
    "audio": lambda n: n,
    "pixel": lambda n: n,
    "symmetric_matrix": lambda n: int(n * (n + 1) / 2),
}

LITERALS_ENCODING = ("base64", "none", "raw")
literals_quantity_type_ = [
    "scalar",
    "vector_n",
    "matrix_n_m",
    # "audio_n",
    "pixel_n",
    "symmetric_matrix_n",
]

numpy_scalars = (
    np.uint8,
    np.uint16,
    np.uint32,
    np.uint64,
    np.int8,
    np.int16,
    np.int32,
    np.int64,
    np.float32,
    np.float64,
    np.complex64,
    np.complex128,
)


class QuantityType:
    """Validate the quantity_type string value.

    The valid options are `scalar`, `vector_n`, `pixel_n`, `matrix_n_m`, and
    `symmetric_matrix_n`.

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
        return False if False in check else True

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
                f"The value, `{keyword}`, is an invalid `quantity_type` enumeration "
                f"literal. The allowed values are {literals_quantity_type_}."
            )
            raise ValueError(message)

        components = self._get_number_of_components(keyword, numbers)
        self.value = element
        self.p = components


class NumericType:
    """Validate the numeric_type string value.

    The valid options are `uint8`, `uint16`, `uint32`, `uint64`, `int8`, `int16`,
    `int32`, `int64`, `float32`, `float64`, `complex64`, and `complex128`. The byte
    order for multi-byte numeric_types are assumed to follow the little endianness
    format.

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
        return False if False in check else True

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
            literals = self.__class__.literals
            message = (
                f"The value, `{element}`, is an invalid `numeric_type` enumeration "
                f"literal. The allowed values are {literals}."
            )
            raise ValueError(message)

        self.value = element
        self.dtype = np.dtype(lst[element])


def validate(value, attr, types, method=None):
    if isinstance(value, types):
        if method is None:
            return value
        return method(value)
    raise TypeError(type_error(types, attr, value))


def type_error(types, attr, value):
    types = (
        " or ".join([item.__name__ for item in types])
        if isinstance(types, tuple)
        else types.__name__
    )
    val_type = type(value).__name__
    return f"Expecting an instance of type `{types}` for {attr}, got `{val_type}`."


def _axis_label(label, unit=None):
    """Return a formatted label with units."""
    return f"{label} / ({unit})" if unit not in [None, ""] else label


def _get_dictionary(*arg, **kwargs):
    if arg != ():
        if isinstance(arg[0], dict):
            return arg[0]

        raise Exception(
            "The argument is either a dictionary with the allowed keywords or a "
            "collection of valid arguments."
        )
    return kwargs


def check_encoding(element):
    """Validate the encoding string value.

    The valid options are `base64`, `none`, and `raw`.

    :returns: The encoding key-value, if the value is valid.
    :raises KeyError: Otherwise.
    """
    if element in LITERALS_ENCODING:
        return element

    message = (
        f"The value, `{element}`, is an invalid `encoding` enumeration literal. "
        f"The allowed values are '{LITERALS_ENCODING}'."
    )
    raise ValueError(message)


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

    if element in lst:
        return lst[element]
    if element in lst2:
        return element
    raise ValueError(f"The dtype, {element}, is not supported.")


def check_and_assign_bool(element):
    if element is None:
        return False
    return validate(element, "boolean", bool)


def check_scalar_object(other, operator=""):
    """Check if the object is scalar: int, float, complex, np.ndarray, Quantity, or
    ScalarQuantity.

    Returns: The other object.
    """
    if isinstance(other, numpy_scalars):
        return other

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


def _check_dimension_indices(d, index=-1):
    """Check the list of indexes to ensure that each index is an integer
    and within the counts of dimensions.
    """
    index = deepcopy(index)

    def _correct_index(i, d):
        if not isinstance(i, int):
            raise TypeError(f"{message}, found {type(i)}")
        if i < 0:
            i += d
        if i > d:
            raise IndexError(
                f"The `index` {index} cannot be greater than the total number of "
                f"dimensions - 1, {d}."
            )
        return -1 - i

    message = "Index/Indices are expected as integer(s)"
    # convert to list and correct the list elements in the following section.
    if isinstance(index, tuple):
        index = list(index)
    if isinstance(index, (tuple, list, np.ndarray)):
        for i, item in enumerate(index):
            index[i] = _correct_index(item, d)
        return tuple(index)
    if isinstance(index, int):
        return _correct_index(index, d)
    raise TypeError(f"{message}, found {type(index)}")


"""Helper methods for CSDModel class."""

from __future__ import print_function
import numpy as np
import warnings
from .unit import string_to_quantity, value_object_format


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


literals_quantity_type = {
    'RGB': lambda n: 3,
    'RGBA': lambda n: 4,
    'scalar': lambda n: 1,
    'vector': lambda n: n,
    'matrix': lambda n: n,
    'audio': lambda n: n,
    'symmetric_matrix': lambda n: int(n*(n+1)/2)
}

literals_encoding = (
    'base64',
    'none',
    'raw'
)

def _type_message(a, b):
    return (
        'Expecting instance of type, `{0}`, but got `{1}`.'
    ).format(a.__name__, b.__name__)


def _attribute_message(a, b):
    return '{0} has no attribute `{1}`.'.format(a, b)


def _axis_label(label, unit, made_dimensionless=False,
                dimensionless_unit=None, label_type=''):
    if made_dimensionless:
        if dimensionless_unit != '':
            return '{0} / {1}'.format(label, dimensionless_unit)
        return label

    if unit != '':
        if label_type == '':
            return '{0} / ({1})'.format(
                label, value_object_format(1*unit, numerical_value=False)
            )
        if label_type == 'latex':
            return '{0} / ({1})'.format(label, unit.to_string('latex'))
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


def _is_physical_quantity(element=None):
    print(element)

# class EncodingType(Enum):
#     base64


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
        "`{0}` is an not a valid `encoding` value. "
        "Available options are '{1}', '{2}' and '{3}'."
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

    __slots__ = (
        '_value',
        '_p'
    )

    def __init__(self, element):
        r"""Instantiate a QuantityType class instance."""
        self._update(element)

    def __str__(self):
        r"""Return a string with the quantity type."""
        return self._value

    def _update(self, element):
        """Update the quantity tpye."""
        if not isinstance(element, str):
            raise TypeError(_type_message(str, type(element)))
        self._check_quantity_type(element)

    @classmethod
    def _get_number_of_components(cls, keyword, numbers):
        return int(literals_quantity_type[keyword](numbers.prod()))

    def _check_quantity_type(self, element):
        list_values = element.strip().split('_')
        numbers = np.asarray(
            [int(item) for item in list_values if item.isnumeric()]
        )
        keyword = '_'.join([item for item in list_values
                            if not item.isnumeric()])

        lst = literals_quantity_type.keys() 
        if keyword not in lst:
            message = (
                "`{0}` is not a valid `quantity_type` value. Available "
                "options are {1}, {2}, {3}, {4}, {5} and {6}."
            )
            raise ValueError(message.format(keyword, *lst))

        components = self._get_number_of_components(keyword, numbers)
        self._value = element
        self._p = components


def numpy_dtype_to_numeric_type(element):
    """Return a valid numeric_type value based on the dtype of nunpy array."""
    lst = {
        '<u1': 'uint8',
        '<u2': 'uint16',
        '<u4': 'uint32',
        '<u8': 'uint64',
        '<i1': 'int8',
        '<i2': 'int16',
        '<i4': 'int32',
        '<i8': 'int64',
        '<f2': 'float16',
        '<f4': 'float32',
        '<f8': 'float64',
        '<c8': 'complex64',
        '<c16': 'complex128',
        '>u1': 'uint8',
        '>u2': 'uint16',
        '>u4': 'uint32',
        '>u8': 'uint64',
        '>i1': 'int8',
        '>i2': 'int16',
        '>i4': 'int32',
        '>i8': 'int64',
        '>f2': 'float16',
        '>f4': 'float32',
        '>f8': 'float64',
        '>c8': 'complex64',
        '>c16': 'complex128',
    }

    lst2 = ('uint8', 'uint16', 'uint32', 'uint64',
            'int8', 'int16', 'int32', 'int64',
            'float16', 'float32', 'float64',
            'complex64', 'complex128')

    if element in lst.keys():
        return lst[element]
    if element in lst2:
        return element
    raise ValueError(
        "The dtype, {0}, is not supported.".format(element)
    )


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

    __slots__ = (
        '_value',
        '_nptype'
    )

    _lst = {
        'uint8': '<u1',
        'uint16': '<u2',
        'uint32': '<u4',
        'uint64': '<u8',
        'int8': '<i1',
        'int16': '<i2',
        'int32': '<i4',
        'int64': '<i8',
        'float16': '<f2',
        'float32': '<f4',
        'float64': '<f8',
        'complex64': '<c8',
        'complex128': '<c16',
        '>u1': '<u1',
        '>u2': '<u2',
        '>u4': '<u4',
        '>u8': '<u8',
        '>i1': '<i1',
        '>i2': '<i2',
        '>i4': '<i4',
        '>i8': '<i8',
        '>f2': '<f2',
        '>f4': '<f4',
        '>f8': '<f8',
        '>c8': '<c8',
        '>c16': '<c16'
        }

    literals = ('uint8', 'uint16', 'uint32', 'uint64',
                'int8', 'int16', 'int32', 'int64',
                'float16', 'float32', 'float64',
                'complex64', 'complex128')

    def __init__(self, element='float32'):
        """Instantiate a NumericType class instance."""
        self._update(element)

    def _update(self, element):
        """Update the numeric tpye."""
        if not isinstance(element, str):
            raise TypeError(_type_message(str, type(element)))
        self._check_numeric_type(element)

    def __str__(self):
        """Return a string with the numeric type."""
        return self._value

    def _check_numeric_type(self, element):
        lst = self.__class__._lst
        # print(lst.keys())
        if element not in lst.keys():
            raise ValueError((
                "The `numeric_type`, `{0}`, is not a valid enumeration literal"
                ". The allowed values are {1}".format(
                    element,
                    "'"+"', '".join(self.__class__.literals)+"'"
                )
            ))

        self._value = element
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


def _check_value_object(element, unit=None):
    return _check_assignment_and_then_check_unit_consistency(element, unit)


def _check_assignment_and_then_check_unit_consistency(element, unit):
    if element is None:
        element = 0.0*unit
    else:
        element = _assign_and_check_unit_consistency(element, unit)
    return element


def _assign_and_check_unit_consistency(element, unit):
    element = _default_units(string_to_quantity(str(element)))
    _fitsUnitFormat = element.unit.to_string('fits').strip()
    element = element.to(_fitsUnitFormat)
    if unit is not None:
        return _check_unit_consistency(element, unit)
    return element


def _check_unit_consistency(element, unit):
    if element.unit.physical_type != unit.physical_type:
        options = [
            str(element.unit),
            str(element.unit.physical_type),
            str(unit),
            unit.physical_type
        ]
        message = (
            "The unit '{0}' ({1}) is inconsistent with the unit '{2}' ({3})."
        )
        raise Exception(message.format(*options))
    return element


def _default_units(element):
    if element.unit.physical_type == 'frequency':
        element = element.to('Hz')
    return element


def _check_quantity(element, unit):
    if element is None:
        element = unit.physical_type
        return element

    if unit.physical_type == 'unknown':
        warnings.warn(
            (
                "The quantity name associated with the unit, {0}, "
                "is not defined in astropy.units package. Continuing "
                "with '{1}' as the quantity name."
            ).format(str(unit), element)
        )
        return element

    if element.lower() != unit.physical_type:
        raise Exception(
            (
                "The physical quantity name, '{0}', is not consistent "
                "with the unit, '{1}'."
            ).format(element, str(unit))
        )

    return element.lower()


if __name__ == '__main__':
    # print (_check_encoding('base64'))
    # print (_check_encoding('raw'))
    # print (_check_encoding('none'))
    # print (_check_encoding('text'))

    print(_check_quantity('time', string_to_quantity('1 s/m').unit))

    # print (_check_quantity_type('RgB'))
    # print (_check_quantity_type('RGBA'))
    # print (_check_quantity_type('scalar'))
    # print (_check_quantity_type('vector_15'))
    # print (_check_quantity_type('matrix_13_3'))
    # print (_check_quantity_type('symmetric_matrix_10'))
    # v = valueObject('5 s')
    # t = valueObject('15 s')
    # print (t + v)
    # print (v)
    # print (v.value)

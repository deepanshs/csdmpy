
"""Helper methods for CSDModel class."""

from __future__ import print_function
import numpy as np
import warnings
from .unit import string_to_quantity, value_object_format
# import os
# import collections

# cds.enable()

# class SequenceProxy(collections.Sequence):
#     """Proxy class to make something appear to be an (immutable)
#        sized iterable container based on just the two functions
#        (or bound methods) provided to the constructor.
#     """
#     def __init__(self, item_getter, length_getter):
#         self._item_getter = item_getter
#         self._get_length = length_getter

#     def __getitem__(self, index):
#         return self._item_getter(index)

#     def __len__(self):
#         return self._get_length()

# class valueObject:
#     default_type = 'physical'

#     __slots__ = ['_object_value', '_object_type']

#     def __init__(self, object_value, object_type=default_type):
#         """
#         The class returns a value object. There are two types of
#         value objects: *physical* and *string*.

#         For physical value objects, the ``valueObject`` class
#         use the ``Quantity`` class from ``Astropy`` package to handle
#         the physical quantities. For string value oject, the class
#         uses Python strings.
#         """
#         # _val_obj  = valueObject(object_value, object_type)
#         # print (object_type)
#         if object_type == 'physical':
#             quantity = _check_value_object(object_value)

#         if object_type == 'string':
#             quantity = object_value

#         super(valueObject, self).__setattr__('_object_type', object_type)
#         super(valueObject, self).__setattr__('_object_value', quantity)

#     def __str__(self):
#         return '< valueObject > ' + str(self._object_value)

#     @property
#     def object_type(self):
#         """
#         The attribute returns the type of object value. It is either
#         *physical* or *string*
#         """
#         return self._object_type

#     @property
#     def value(self):
#         """
#         The attribute returns the type of object value. It is either
#         *physical* or *string*
#         """
#         if self._object_type == 'physical':
#             return self._object_value.value

#         if self._object_type == 'string':
#             return self._object_value

#     @property
#     def unit(self):
#         if self._object_type == 'string':
#             raise Exception(
#                   'string value objects do not have unit attribute.'
#             )
#         else:
#             return self._unit

#     def to(self, another_unit):
#         if self._value_type != 'physical':
#             raise Exception('
#                   This method is only valid physical value objects.')
#         if self._value_type == 'physical':
#             _another_object_value = self._object_value.to(another_unit)
#             super(valueObject, self).__setattr__(
#                   '_object_value', _another_object_value)

#     def __add__(self, a):
#         if self._object_type == 'physical':
#             return valueObject(
#                   self._object_value + a._object_value, 'physical')


def _type_message(a, b):
    return (
        'Expecting instance of type, `{0}`, but got `{1}`.'
    ).format(a.__name__, b.__name__)


def _attribute_message(a, b):
    return '{0} has no attribute `{1}`.'.format(a, b)


def _axis_label(label, unit, made_dimensionless=False,
                dimensionless_unit=None):
    if made_dimensionless:
        if dimensionless_unit != '':
            return '{0} / {1}'.format(label, dimensionless_unit)
        return label

    if unit != '':
        return '{0} / ({1})'.format(
            label, value_object_format(1*unit, numerical_value=False)
        )
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


def _check_encoding(element):
    """
    Validate the encoding string value.

    The valid options are `base64`, `none`, and `raw`.

    :returns: The encoding key-value, if the value is valid.
    :raises KeyError: Otherwise.
    """
    lst = [
        'base64',
        'none',
        'raw'
    ]

    if element in lst:
        return element

    message = (
        "`{0}` is an not a valid `encoding` value. "
        "Available options are '{1}', '{2}' and '{3}'."
    )
    raise ValueError(message.format(element, *lst))


def _check_dataset_type(element):
    """
    Validate the dataset_type string value.

    The valid options are `RGB`, `RGBA`, `scalar`, `vector_n`,
    `matrix_n_m`, and `symmetric_matrix_n`.

    :returns: The dataset_type key-value, if the value is valid.
    :raises KeyError: Otherwise.
    """
    list_values = element.strip().split('_')
    numbers = np.asarray(
        [int(item) for item in list_values if item.isnumeric()]
    )
    keyword = '_'.join([item for item in list_values if not item.isnumeric()])

    lst = {
        'RGB': 3,
        'RGBA': 4,
        'scalar': 1,
        'vector': numbers.prod(),
        'matrix': numbers.prod(),
        'symmetric_matrix': int(numbers.prod() * (numbers.prod() + 1)/2.0)
    }

    if keyword not in lst.keys():
        message = (
            "`{0}` is not a valid `dataset_type` value. Available options are "
            "{1}, {2}, {3}, {4}, {5} and {6}."
        )
        raise ValueError(message.format(keyword, *lst.keys()))

    return element, lst[keyword]


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
    lst2 = ['uint8', 'uint16', 'uint32', 'uint64',
            'int8', 'int16', 'int32', 'int64',
            'float16', 'float32', 'float64',
            'complex64', 'complex128']

    if element in lst.keys():
        return lst[element]
    if element in lst2:
        return element
    raise ValueError(
        "The dtype, {0}, is not supported.".format(element)
    )


def _check_numeric_type(element):
    """
    Validate the numeric_type string value.

    The valid options are
    `uint8`, `uint16`, `uint32`, `uint64`, `int8`, `int16`, `int32`, `int64`,
    `float16`, `float32`, `float64`, `complex64`, and `complex128`. The byte
    order for multi-byte numeric_types are assumed to follow the little
    endianness format.

    :returns: The dataset_type key-value, if the value is valid.
    :raises KeyError: Otherwise.
    """
    lst = {
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

    if element in lst.keys():
        return element, np.dtype(lst[element])
    raise ValueError(
        "The `numeric_type`, `{0}`, is not a valid value.".format(element)
    )


def _check_value_object(element, unit=None):
    return _check_assignment_and_then_check_unit_consistency(element, unit)


def _check_assignment_and_then_check_unit_consistency(element, unit):
    if element is None:
        element = 0*unit
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

    # print (_check_dataset_type('RgB'))
    # print (_check_dataset_type('RGBA'))
    # print (_check_dataset_type('scalar'))
    # print (_check_dataset_type('vector_15'))
    # print (_check_dataset_type('matrix_13_3'))
    # print (_check_dataset_type('symmetric_matrix_10'))
    # v = valueObject('5 s')
    # t = valueObject('15 s')
    # print (t + v)
    # print (v)
    # print (v.value)

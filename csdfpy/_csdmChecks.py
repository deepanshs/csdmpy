from __future__ import print_function
import numpy as np
import warnings
from .unit import string_to_quantity
import os
import collections

# cds.enable()

# class SequenceProxy(collections.Sequence):
#     """Proxy class to make something appear to be an (immutable) sized iterable
#        container based on just the two functions (or bound methods) provided to
#        the constructor.
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
#             raise Exception('string value objects do not have unit attribute.')
#         else:
#             return self._unit

#     def to(self, another_unit):
#         if self._value_type != 'physical':
#             raise Exception('This method is only valid physical value objects.')
#         if self._value_type == 'physical':
#             _another_object_value = self._object_value.to(another_unit)
#             super(valueObject, self).__setattr__('_object_value', _another_object_value)

#     def __add__(self, a):
#         if self._object_type == 'physical':
#             return valueObject(self._object_value + a._object_value, 'physical')

            

def _axis_label(label, unit, made_dimensionless, dimensionless_unit):
    if made_dimensionless:
        if dimensionless_unit != '':
            return label + ' / ' + dimensionless_unit
        else:
            return label
    if not made_dimensionless:
        if unit != '':
            return label + ' / ' + unit
        else:
            return label



def _is_numeric(element):
    return element.isnumeric()

def _is_physical_quantity(element):
    pass

def _check_encoding(element):

    lst = ['base64', 'none', 'raw']
    if element in lst:
        return element
    else:
        options = ''.join(["'"+item+"', " for item in lst[:-1]])
        raise Exception("Invalid 'encoding'. Available options are "+ options+"and '"+lst[-1]+"'.")

def _check_dataset_type(element):
    lst = ['RGB', 'RGBA', 'scalar', 'vector', 'matrix', 'symmetric_matrix']
    listValues = element.strip().split('_')

    if listValues[0] not in lst:
        if (listValues[0] + listValues[1] != 'symmetricmatrix'):
            options = ''.join(["'"+item+"', " for item in lst[:-1]])
            raise Exception("'dataset_type' '{0}' is not recognized. Available options are ".format(element)+ options+"and '"+lst[-1]+"'.")
    
    if listValues[0] == 'RGB':
        return element, 3
    if listValues[0] == 'RGBA':
        return element, 4
    if listValues[0] == 'scalar':
        return element, 1
    if listValues[0] == 'vector':
        return element, int(listValues[1])
    if listValues[0] == 'matrix':
        return element, int(listValues[1]*listValues[2])
    if listValues[0] + listValues[1] == 'symmetricmatrix':
        return element, int(int(listValues[2])*(int(listValues[2])+1)/2)
    else:
        raise Exception("'dataset_type' cannot be identified.")

def _check_numeric_type(element):
    lst = {'uint8' : '<u1',
           'uint16': '<u2',
           'uint32': '<u4',
           'uint64': '<u8',
           'int8' : '<i1',
           'int16': '<i2',
           'int32': '<i4',
           'int64': '<i8',
           'float16': '<f2',
           'float32': '<f4',
           'float64': '<f8',
           'complex64':'<c8',
           'complex128':'<c16'}
    if element in lst.keys():
        return element, np.dtype(lst[element])
    else:
        raise Exception("'numeric_type' '{0}' not recognized.".format(element))







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
    else:
        return element


def _check_unit_consistency(element, unit):
    if element.unit.physical_type != unit.physical_type:
        # try: element.unit.to(unit)
        # except Exception as e:
        #     raise Exception(e)
        raise Exception("The unit '{0}' ({1}) is inconsistent with the unit '{2}' ({3}).".format(
                str(element.unit), str(element.unit.physical_type), str(unit), unit.physical_type))
    else:
        return element


def _default_units(element):
    # print (element.unit.physical_type)
    if element.unit.physical_type == 'frequency':
        element = element.to('Hz')
    return element







def _check_and_assign_bool(element):
    if element is None:
        element = False
        return element
    else:
        if isinstance(element, bool):
            return element
        else:
            raise Exception("Bool type is required for '{0}', given '{1}' ".format( 
                str(element), element.__class__.__name__))

def _check_quantity(element, unit):
    if element == None:
        element = unit.physical_type
        return element
    
    if unit.physical_type == 'unknown':
        warnings.warn("The quantity name associated with the unit, {0}, is not defined in astropy.units package. Continuing with '{1}' as the quantity name.".format(str(unit), element))
        return element
    
    if element.lower() != unit.physical_type:
        raise Exception("The physical quantity name '{0}' is not consistent with the unit '{1}'".format(element, str(unit)) )
    
    return element.lower()


if __name__ == '__main__':
    v = valueObject('5 s')
    t = valueObject('15 s')
    print (t + v)
    print (v)
    print (v.value)
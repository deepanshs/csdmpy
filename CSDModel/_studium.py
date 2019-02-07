from __future__ import print_function
import numpy as np
import warnings
from .unit import stringToQuantity
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

def _checkValueObject(element, unit):
    return _checkAssignmentAndThenCheckUnitConsistency(element, unit)

def _defaultUnits(element):
    # print (element.unit.physical_type)
    if element.unit.physical_type == 'frequency':
        element = element.to('Hz')
    return element


def _checkEncoding(element):

    lst = ['base64', 'none', 'raw']
    if element in lst:
        return element
    else:
        options = ''.join(["'"+item+"', " for item in lst[:-1]])
        raise Exception("Invalid 'encoding'. Available options are "+ options+"and '"+lst[-1]+"'.")

def _checkDatasetType(element):
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

def _checkNumericType(element):
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

def _checkUnitConsistency(element, unit):
    if element.unit.physical_type != unit.physical_type:
        raise Exception("The unit of '{0}' ({1}) is inconsistent with unit '{2}' ({3}).".format(
                    str(element), str(element.unit.physical_type), str(unit), unit.physical_type))
    else:
        return element

def _assignAndCheckUnitConsistency(element, unit):
    element = _defaultUnits(stringToQuantity(str(element)))
    if unit is not None:
        return _checkUnitConsistency(element, unit)
    else:
        return element

def _checkAssignmentAndThenCheckUnitConsistency(element, unit):
    if element is None:
        element = 0*unit
    else:
        element = _assignAndCheckUnitConsistency(element, unit)
    return element

def _checkAndAssignBool(element):
    if element is None:
        element = False
        return element
    else:
        if isinstance(element, bool):
            return element
        else:
            raise Exception("Bool type is required for '{0}', given '{1}' ".format( 
                str(element), element.__class__.__name__))

def _checkQuantity(element, unit):
    if element == None:
        element = unit.physical_type
        return element
    
    if unit.physical_type == 'unknown':
        warnings.warn("The quantity name associated with the unit, {0}, is not defined in astropy.units package. Continuing with '{1}' as the quantity name.".format(str(unit), element))
        return element
    
    if element.lower() != unit.physical_type:
        raise Exception("The physical quantity name '{0}' is not consistent with the unit '{1}'".format(element, str(unit)) )
    
    return element.lower()

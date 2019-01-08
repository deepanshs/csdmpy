from __future__ import print_function
import numpy as np
# from astropy import units as u
from unit import stringToQuantity, quantityFormat, unitToLatex, _ppm
import base64
import os
import collections

# cds.enable()

class SequenceProxy(collections.Sequence):
    """Proxy class to make something appear to be an (immutable) sized iterable
       container based on just the two functions (or bound methods) provided to
       the constructor.
    """
    def __init__(self, item_getter, length_getter):
        self._item_getter = item_getter
        self._get_length = length_getter

    def __getitem__(self, index):
        return self._item_getter(index)

    def __len__(self):
        return self._get_length()

# class _physical_quantity:

#     __slots__ = ['_unit', '_value']

#     def __init__(self, element, unit):
#         super(_physical_quantity, self).__setattr__('_value', element)
#         super(_physical_quantity, self).__setattr__('_unit', unit)
    
#     def __str__(self):
#         return str(self._value) + ' '+ str(self._unit)
    
#     def __getattr__(self, name=None):
#         return self._value

#     def __setattr__(self, name, value):
#         raise AttributeError("Attribute '{0}' cannot be modified.".format(name))

#     def __delattr__(self, name):
#         raise AttributeError("Attribute '{0}' cannot be deleted.".format(name))

#     def to(self, unit):
#         unit = _assignAndCheckUnitConsistency(unit, self._unit).unit
#         _factor = self._unit.to(unit)
#         super(_physical_quantity, self).__setattr__('_value', self._value*_factor)
#         super(_physical_quantity, self).__setattr__('_unit', unit)
#         return self

#     def __add__(self, other):
#         pass

def _is_numeric(element):
    return element.isnumeric()

def _is_physical_quantity(element):
    
def _defaultUnits(element):
    # print (element.unit.physical_type)
    if element.unit.physical_type == 'frequency':
        element = element.to('Hz')
    return element


def _checkFileFormat(element):

    lst = ['base64', 'none', 'raw']
    if element in lst:
        return element
    else:
        options = ''.join(["'"+item+"', " for item in lst[:-1]])
        raise Exception("Invalid 'encoding'. Available options are "+ options+"and '"+lst[-1]+"'.")

def _checkDataType(element):
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

def _checkNumberType(element):
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

def _assignAndCheckUnitConsistency(value_object, element, unit):
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
    else:
        if element != unit.physical_type:
            raise Exception("The physical quantity name '{0}' is not consistent with the unit '{1}'".format(element, str(unit)) )
        else:
            element = unit.physical_type
            return element

def _checkValueObjectType(element):
    value_objects = ['physical', 'numerical', 'currency', 'string']
    if element in value_objects:
        return element
    else:
        raise ValueError("The value object type '{0}' is not supported".format(element))

class _reciprocalVariableObject:
    _slots__ = ['_value_object_type',
                '_sampling_type',
                '_reciprocal_sampling_interval',
                '_reciprocal_number_of_points',
                '_reciprocal_reference_offset',
                '_reciprocal_origin_offset',
                '_reciprocal_quantity',
                '_reciprocal_label',
                '_reciprocal_reverse',
                '_reciprocal_periodic']

    def __init__(self, _sampling_type='grid',
                _value_object_type='physical',
                _reciprocal_sampling_interval=None,
                _reciprocal_number_of_points=None,
                _reciprocal_reference_offset=None,
                _reciprocal_origin_offset=None,
                _reciprocal_quantity='',
                _reciprocal_label='',
                _reciprocal_reverse=False,
                _reciprocal_periodic=False):

        _value_object_type = _checkValueObjectType(_value_object_type)
        super(commonAttributes, self).__setattr__('_value_object_type', _value_object_type)
        super(commonAttributes, self).__setattr__('_sampling_type', _sampling_type)

        _value = _checkAndAssignBool(_reverse)
        super(commonAttributes, self).__setattr__('_reverse', _value)

        super(commonAttributes, self).__setattr__('_label', _label)    

class commonAttributes:
    __slots__ = ['_sampling_type', '_value_object_type', '_label', \
                 '_reverse']

    def __init__(self, _sampling_type, 
                       _value_object_type,
                       _reverse,
                       _label):

        _value_object_type = _checkValueObjectType(_value_object_type)
        super(commonAttributes, self).__setattr__('_value_object_type', _value_object_type)
        super(commonAttributes, self).__setattr__('_sampling_type', _sampling_type)

        _value = _checkAndAssignBool(_reverse)
        super(commonAttributes, self).__setattr__('_reverse', _value)

        super(commonAttributes, self).__setattr__('_label', _label)


    ## label
    @property
    def label(self):
        if self._label.strip() == '':
            return self._quantity + ' / ' + unitToLatex(self._coordinates.unit)
        else:
            return self._label + ' / ' + unitToLatex(self._coordinates.unit)
    @label.setter
    def label(self, label=''):
        self._setAttribute('_label', label)


    ## reverse
    @property
    def reverse(self):
        return self._reverse
    @reverse.setter
    def reverse(self, value=False):
        _value = _checkAndAssignBool(value)
        self._setAttribute('_reverse', _value)





class nonQuantitativeControlledVariable:
    __slots__ = ['_sampling_type', '_value_object_type', '_label', \
                 '_coordinates', '_reverse']

    def __init__(self, _sampling_type, 
                       _value_object_type,
                       _coordinates,
                       _reverse,
                       _label):

        



class linearControlledVariable:
    __slots__ = ['_number_of_points', '_sampling_interval', '_unit', \
                 '_reciprocal_number_of_points', '_reciprocal_sampling_interval', \
                 '_reciprocal_unit', '_fft_output_order']

    def __init__(self):
        self._setAttribute('_number_of_points', _number_of_points)
        self._setAttribute('_reciprocal_number_of_points', _number_of_points)
        
        _value = _assignAndCheckUnitConsistency(_sampling_interval, None)
        self._setAttribute('_sampling_interval', _value)

        _unit = self._sampling_interval.unit
        _reciprocal_unit = _unit**-1

        self._setAttribute('_unit', _unit)
        self._setAttribute('_reciprocal_unit', _reciprocal_unit)

        if _reciprocal_sampling_interval is None:
            _value = (1/(_number_of_points*self._sampling_interval.value)) * _reciprocal_unit
        else:
            _value = _assignAndCheckUnitConsistency(_reciprocal_sampling_interval, _reciprocal_unit)
            self._setAttribute('_reciprocal_sampling_interval', _value)

        quantitativeControlledVariable

    def _setAttribute(self, name, value):
        super(quantitativeLinearControlledVariable, self).__setattr__(name, value)

class quantitativeControlledVariable:

    __slots__ = ['_coordinates', '_number_of_points', '_sampling_interval', '_unit', \
                 '_reciprocal_unit', '_reciprocal_sampling_interval', \
                 '_reference_offset', '_reciprocal_reference_offset',\
                 '_origin_offset', '_reciprocal_origin_offset', \
                 '_made_dimensionless', '_reciprocal_made_dimensionless', \
                 '_reverse', '_reciprocal_reverse', '_fft_output_order', '_periodic', '_reciprocal_periodic', \
                 '_quantity', '_reciprocal_quantity', '_label', '_reciprocal_label', \
                 '_sampling_type', '_value_object_type']

    def __init__(self,  _number_of_points, 
                        _sampling_interval,  
                        _reference_offset = None,  
                        _origin_offset = None, 
                        _made_dimensionless = None , 
                        _quantity = None,
                        _reverse = False, 
                        _label='',
                        _periodic = False, 
                        _fft_output_order = False,

                        _reciprocal_number_of_points = None,
                        _reciprocal_sampling_interval = None,
                        _reciprocal_reference_offset = None, 
                        _reciprocal_origin_offset = None,
                        _reciprocal_made_dimensionless = False, 
                        _reciprocal_quantity = None,
                        _reciprocal_reverse = False, 
                        _reciprocal_label='',
                        _reciprocal_periodic = False,
                        
                        _sampling_type = "grid",
                        _value_object_type = "physical"):

        self._setAttribute('_number_of_points', _number_of_points)
        self._setAttribute('_reciprocal_number_of_points', _number_of_points)
        
        _value_object_type = _checkValueObjectType(_value_object_type)
        self._setAttribute('_value_object_type', _value_object_type)
        self._setAttribute('_sampling_type', _sampling_type)

        _value = _assignAndCheckUnitConsistency(_sampling_interval, None)
        self._setAttribute('_sampling_interval', _value)
        # self._setAttribute('_sampling_interval', _value)

        _unit = self._sampling_interval.unit
        _reciprocal_unit = _unit**-1

        # self._setAttribute('_ppm', u.Unit('ppm'))
        self._setAttribute('_unit', _unit)
        self._setAttribute('_reciprocal_unit', _reciprocal_unit)

        if _reciprocal_sampling_interval is None:
            _value = (1/(_number_of_points*self._sampling_interval.value)) * _reciprocal_unit
        else:
            _value = _assignAndCheckUnitConsistency(_reciprocal_sampling_interval, _reciprocal_unit)
            self._setAttribute('_reciprocal_sampling_interval', _value)
        # self._setAttribute('_reciprocal_sampling_interval', _value)

        
        ## reference Offset
        _value = _checkAssignmentAndThenCheckUnitConsistency(_reference_offset, _unit)
        self._setAttribute('_reference_offset', _value)
        _value = _checkAssignmentAndThenCheckUnitConsistency(_reciprocal_reference_offset, _reciprocal_unit)
        self._setAttribute('_reciprocal_reference_offset', _value)
        
        ## origin offset
        _value = _checkAssignmentAndThenCheckUnitConsistency(_origin_offset, _unit)
        self._setAttribute('_origin_offset', _value)
        _value =  _checkAssignmentAndThenCheckUnitConsistency(_reciprocal_origin_offset, _reciprocal_unit)
        self._setAttribute('_reciprocal_origin_offset', _value)

        ### made dimensionless
        _value = _checkAndAssignBool(_made_dimensionless)
        self._setAttribute('_made_dimensionless', _value)
        _value = _checkAndAssignBool(_reciprocal_made_dimensionless)
        self._setAttribute('_reciprocal_made_dimensionless', _value)

        ### reverse
        _value = _checkAndAssignBool(_reverse)
        self._setAttribute('_reverse', _value)
        _value = _checkAndAssignBool(_reciprocal_reverse)
        self._setAttribute('_reciprocal_reverse', _value)

        _value = _checkAndAssignBool(_fft_output_order)
        self._setAttribute('_fft_output_order', _value)
        _value = _checkAndAssignBool(_periodic)
        self._setAttribute('_periodic', _value)
        _value = _checkAndAssignBool(_reciprocal_periodic)
        self._setAttribute('_reciprocal_periodic', _value)


        ## quantity
        _value = _checkQuantity(_quantity, _unit)
        self._setAttribute('_quantity', _value)
        _value = _checkQuantity(_reciprocal_quantity, _reciprocal_unit)
        self._setAttribute('_reciprocal_quantity', _value)

        ## label
        self._setAttribute('_label', _label)
        self._setAttribute('_reciprocal_label', _reciprocal_label)
        self._setAttribute('_coordinates', None)
        self._getCoordinates()

    def _setAttribute(self, name, value):
        super(quantitativeLinearControlledVariable, self).__setattr__(name, value)
        
    def _dimensionlessConversion(self, unit, _oldValue):
        denominator = (self._origin_offset + self._reference_offset)
        # print (denominator)
        # print (self._coordinates, unit, denominator)
        if denominator.value != 0:
            if self._made_dimensionless and _oldValue: return
            if not self._made_dimensionless and not _oldValue: return
            if self._made_dimensionless and not _oldValue:
                _value = (self._coordinates / denominator).to(_ppm)
                self._setAttribute('_coordinates', _value)
                return
            if not self._made_dimensionless and _oldValue:
                _value = (self._coordinates * denominator).to(unit)
                self._setAttribute('_coordinates', _value)
        else:
            self._setAttribute('_made_dimensionless', _oldValue)
            print("Zero division encountered: Dimension cannot be made dimensionsless with \n'origin_offset' {0} and 'reference_offset' {1}. No changes made.".format(self._origin_offset, self._reference_offset))

    def __delattr__(self, name):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' of class '{1}' cannot be deleted.".format(name, __class__.__name__))

    def __setattr__(self, name, value):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' cannot be modified".format(name))
        elif name in __class__.__dict__.keys():
            return self._setAttribute(name, value)
        else:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(__class__.__name__, name))

    def info(self):
        _response =[self._number_of_points, 
                    str(self._sampling_interval),
                    str(self._reference_offset),
                    str(self._origin_offset),
                    self._made_dimensionless,
                    self._reverse,
                    self._quantity,
                    str(self._label),
                    self._fft_output_order,
                    self._periodic,
                    self._sampling_type,
                    self._value_object_type]
        return _response

        
    def __str__(self):
        
        block = ['\tnumber_of_points \t= {0}\n',\
                 '\tsampling_interval \t= {1}\n', \
                 '\treference_offset \t= {2}\n', \
                 '\torigin_offset \t\t= {3}\n', \
                 '\tmade_dimensionless \t= {4}\n', \
                 '\treverse \t\t= {5}\n', \
                 '\tquantity \t\t= {6}\n', \
                 '\tlabel \t\t\t= {7}\n', \
                 '\tftFlag \t\t\t= {8}\n', \
                 '\tperiodic \t\t= {9}\n', \
                 '\tsampling_type \t\t= {10}\n', \
                 '\tvalue_object_type \t\t= {11}\n']

        # inverseBlock = ['\n\treciprocal_sampling_interval \t= {0}\n', \
        #          '\treciprocal_reference_offset \t= {1}\n', \
        #          '\treciprocal_origin_offset \t\t= {2}\n', \
        #          '\treciprocal_made_dimensionless\t= {3}\n', \
        #          '\treciprocal_reverse \t\t= {4}\n', \
        #          '\treciprocal_quantity \t\t= {5}\n', \
        #          '\treciprocal_label \t\t\t= {6}\n' ]

        string = ''.join(block).format(self._number_of_points, 
                                    self._sampling_interval,
                                    self._reference_offset,
                                    self._origin_offset,
                                    self._made_dimensionless,
                                    self._reverse,
                                    self._quantity,
                                    self._label,
                                    self._fft_output_order,
                                    self._periodic,
                                    self._sampling_type,
                                    self._value_object_type)

        # string2 = ''.join(inverseBlock).format(self._reciprocal_sampling_interval, 
        #                             self._reciprocal_reference_offset,
        #                             self._reciprocal_origin_offset, 
        #                             self._reciprocal_made_dimensionless,
        #                             self._reciprocal_reverse, 
        #                             self._reciprocal_quantity, 
        #                             self._reciprocal_label)
        return string

    def _swapValues(self, a, b):
        temp = self.__getattribute__(a)
        # print (self.__getattribute__(b))
        self._setAttribute(a, self.__getattribute__(b))
        self._setAttribute(b, temp)
        temp = None
        del temp


    def _reciprocal(self):
        self._swapValues('_sampling_interval', '_reciprocal_sampling_interval')
        self._swapValues('_reference_offset', '_reciprocal_reference_offset')
        self._swapValues('_origin_offset', '_reciprocal_origin_offset')
        self._swapValues('_made_dimensionless', '_reciprocal_made_dimensionless')
        self._swapValues('_reverse', '_reciprocal_reverse')
        self._swapValues('_unit', '_reciprocal_unit')

        if self._fft_output_order:
            self._setAttribute('_fft_output_order', False)
        else:
            self._setAttribute('_fft_output_order', True)

        self._swapValues('_quantity', '_reciprocal_quantity')
        self._swapValues('_label', '_reciprocal_label')
        self._swapValues('_periodic', '_reciprocal_periodic')
        self._getCoordinates()



    def getJsonDictionary(self):
        d = {}
        d['reciprocal'] = {}
        d['value_object_type'] = self._value_object_type
        d['sampling_type'] = self._sampling_type
        d['number_of_points'] = self._number_of_points
        d['sampling_interval'] = quantityFormat(self._sampling_interval)

        if self._reference_offset is not None and self._reference_offset.value != 0:
            d['reference_offset'] = quantityFormat(self._reference_offset)
        if self._reciprocal_reference_offset is not None and self._reciprocal_reference_offset.value != 0:
            d['reciprocal']['reference_offset'] = quantityFormat(self._reciprocal_reference_offset)


        if self._origin_offset is not None:
            # if type(self._origin_offset) == type(np.datetime64()):
            #     d['origin_offset'] = str(self._origin_offset)
            if self._origin_offset.value != 0:
                d['origin_offset'] = quantityFormat(self._origin_offset)
        # if self._origin_offset is not None and self._origin_offset.value != 0:
        #     d['origin_offset'] = quantityFormat(self._origin_offset)

        if self._reciprocal_origin_offset is not None:
            # if type(self._reciprocal_origin_offset) == type(np.datetime64()):
            #     d['reciprocal']['origin_offset'] = str(self._reciprocal_origin_offset)
            if self._reciprocal_origin_offset.value != 0:
                d['reciprocal']['origin_offset'] = quantityFormat(self._reciprocal_origin_offset)

        # if self._reciprocal_origin_offset is not None and self._reciprocal_origin_offset.value != 0:
        #     d['reciprocal']['origin_offset'] = quantityFormat(self._reciprocal_origin_offset)

        # if self._made_dimensionless is True:
        #     d['made_dimensionless'] = True
        # if self._reciprocal_made_dimensionless is True:
        #     d['reciprocal_made_dimensionless'] = True

        if self._reverse is True:
            d['reverse'] = True
        if self._reciprocal_reverse is True:
            d['reciprocal']['reverse'] = True

        if self._fft_output_order is True:
            d['fft_output_order'] = True

        if self._periodic is True:
            d['periodic'] = True
        if self._reciprocal_periodic is True:
            d['reciprocal']['periodic'] = True

        if self._value_object_type is 'physical':
            if self._quantity not in [None, "unknown", "dimensionless"]:
                d['quantity'] = self._quantity

        if self._reciprocal_quantity not in [None, "unknown", "dimensionless"]:
            d['reciprocal']['quantity'] = self._reciprocal_quantity

        if self._label.strip() != "":
            d['label'] = self._label

        if self._reciprocal_label.strip() != "":
            d['reciprocal']['label'] = self._reciprocal_label

        if d['reciprocal'] == {}:
            del d['reciprocal']

        return d
    ## setter -------------------------


    ## Periodic
    @property
    def periodic(self):
        return self._periodic
    @periodic.setter
    def periodic(self, value = True):
        self._setAttribute('_periodic', _checkAndAssignBool(value))
    
    ## Quantity
    @property
    def quantity(self):
        return self._quantity
    @quantity.setter
    def quantity(self, string = ''):
        self._setAttribute('_quantity', string)


    @property
    def unit(self):
        return self._unit

    ## label
    @property
    def label(self):
        # print (unitToLatex(self._coordinates.unit))
        if self._label.strip() == '':
            return self._quantity + ' / ' + unitToLatex(self._coordinates.unit)
        else:
            return self._label + ' / ' + unitToLatex(self._coordinates.unit)
    @label.setter
    def label(self, label=''):
        self._setAttribute('_label', label)
    

    ## inverseLabel
    @property
    def reciprocal_label(self):
        return self._reciprocal_label
    @reciprocal_label.setter
    def reciprocal_label(self, label=''):
        self._setAttribute('_reciprocal_label', label)

    @property
    def type(self):
        return self._type

    ## made dimensionless
    @property
    def made_dimensionless(self):
        return self._made_dimensionless
    @made_dimensionless.setter
    def made_dimensionless(self, value=False):
        _oldValue = self._made_dimensionless
        _value = _checkAndAssignBool(value)
        self._setAttribute('_made_dimensionless', _value)
        self._dimensionlessConversion(self._unit, _oldValue)

    ## inverse made dimensionless
    @property
    def reciprocal_made_dimensionless(self):
        return self._reciprocal_made_dimensionless
    @reciprocal_made_dimensionless.setter
    def reciprocal_made_dimensionless(self, value=False):
        _oldValue = self._reciprocal_made_dimensionless
        _value = _checkAndAssignBool(value)
        self._setAttribute('_reciprocal_made_dimensionless', _value)
        # self._dimensionlessConversion(self._reciprocal_unit, _oldValue)


    ## reverse
    @property
    def reverse(self):
        return self._reverse
    @reverse.setter
    def reverse(self, value=False):
        _value = _checkAndAssignBool(value)
        self._setAttribute('_reverse', _value)


    ## inverse reverse
    @property
    def reciprocal_reverse(self):
        return self._reciprocal_reverse
    @reciprocal_reverse.setter
    def reciprocal_reverse(self, value=False):
        _value = _checkAndAssignBool(value)
        self._setAttribute('_reciprocal_reverse', _value)


    ## reference offset
    @property
    def reference_offset(self):
        return self._reference_offset
    @reference_offset.setter
    def reference_offset(self, value):
        _value = _assignAndCheckUnitConsistency(value, self._unit)
        self._setAttribute('_reference_offset', _value)
        self._getCoordinates()


    ## inverse reference offset
    @property
    def reciprocal_reference_offset(self):
        return self._reciprocal_reference_offset
    @reciprocal_reference_offset.setter
    def reciprocal_reference_offset(self, value):
        _value = _assignAndCheckUnitConsistency(value, self._reciprocal_unit)
        self._setAttribute('_reciprocal_reference_offset', _value)


    ## origin offset
    @property
    def origin_offset(self):
        return self._origin_offset
    @origin_offset.setter
    def origin_offset(self, value):
        _value = _assignAndCheckUnitConsistency(value, self._unit)
        self._setAttribute('_origin_offset', _value)
        self._getCoordinates()


    ## inverse origin offset
    @property
    def reciprocal_origin_offset(self):
        return self._reciprocal_origin_offset
    @reciprocal_origin_offset.setter
    def reciprocal_origin_offset(self, value):
        _value = _assignAndCheckUnitConsistency(value, self._reciprocal_unit)
        self._setAttribute('_reciprocal_origin_offset', _value)


    ## sampling interval
    @property
    def sampling_interval(self):
        return self._sampling_interval
    @sampling_interval.setter
    def sampling_interval(self, value):
        _value = _assignAndCheckUnitConsistency(value, self._unit)
        self._setAttribute('_sampling_interval', _value)
        self._getCoordinates()


    ## inverse sampling interval
    @property
    def reciprocal_sampling_interval(self):
        return self._reciprocal_sampling_interval
    @reciprocal_sampling_interval.setter
    def reciprocal_sampling_interval(self, value):
        _value = _assignAndCheckUnitConsistency(value, self._reciprocal_unit)
        self._setAttribute('_reciprocal_sampling_interval', _value)

    ## npts
    @property
    def number_of_points(self):
        return self._number_of_points
    @number_of_points.setter
    def number_of_points(self, value):
        if isinstance(value, int):
            self._setAttribute('_number_of_points', value)
        # self._number_of_points = _assignAndCheckUnitConsistency(value, u.Unit(''))
        self._getCoordinates()

    
    def _getCoordinates(self):
        _unit = self._unit
        _number_of_points = self._number_of_points
        _sampling_interval = self._sampling_interval.to(_unit)
        _reference_offset = self._reference_offset.to(_unit)
        if self._fft_output_order:
            _value = ( np.arange(_number_of_points, dtype=np.float64)* _sampling_interval \
                            - (0.5*_sampling_interval*_number_of_points) - _reference_offset)
        else:
            _value = ( np.arange(_number_of_points, dtype=np.float64)* _sampling_interval \
                            - _reference_offset )
        if self._made_dimensionless:
            _origin_offset = self._origin_offset.to(_unit)
            _value/=(_origin_offset + _reference_offset)
            _value = _value.to(_ppm)
        # self._coordinates = _value
        self._setAttribute('_coordinates', _value)

    def getInverseCoordinates(self, parameter_list):
        pass

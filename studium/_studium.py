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
    if listValues[0] == 'square_matrix':
        return element, int(listValues[1])


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

def _assignAndCheckUnitConsistency(element, unit):
    # print (element, type(element))
    # a = stringToQuantity(element)
    # print (a, a.unit, type(a.unit), a.unit.physical_type)
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




class _nusDimensionObject:

    __slots__ = ['_coordinates', '_number_of_points', '_unit', \
                 '_reference_offset', '_origin_offset', \
                 '_made_dimensionless', '_reverse', '_periodic', \
                 '_quantity', '_label' ]

    def __init__(self,  _coordinates, 
                        _reference_offset,
                        _origin_offset,
                        _made_dimensionless,
                        _reverse=False, 
                        _periodic=False,
                        _quantity=None, 
                        _label='',
                        _type = 'non-uniform physical dimension'):

        super(_nusDimensionObject, self).__setattr__('_number_of_points', len(_coordinates))

        _unit = _assignAndCheckUnitConsistency(_coordinates[0], None).unit
        # super(_nusDimensionObject, self).__setattr__('_ppm', u.Unit('ppm'))
        super(_nusDimensionObject, self).__setattr__('_unit', _unit)

        ## reference
        _value = _checkAssignmentAndThenCheckUnitConsistency(_reference_offset, _unit)
        super(_nusDimensionObject, self).__setattr__('_reference_offset', _value)
        
        ## origin offset
        _value = _checkAssignmentAndThenCheckUnitConsistency(_origin_offset, _unit)
        super(_nusDimensionObject, self).__setattr__('_origin_offset', _value)

        ### made dimensionless
        _value = _checkAndAssignBool(_made_dimensionless)
        super(_nusDimensionObject, self).__setattr__('_made_dimensionless', _value)
       
        ### reverse
        _value = _checkAndAssignBool(_reverse)
        super(_nusDimensionObject, self).__setattr__('_reverse', _value)

        _value = _checkAndAssignBool(_periodic)
        super(_nusDimensionObject, self).__setattr__('_periodic', _value)

        ## quantity
        _value = _checkQuantity(_quantity, _unit)
        super(_nusDimensionObject, self).__setattr__('_quantity', _value)
    
        ## label
        super(_nusDimensionObject, self).__setattr__('_label', _label)

        # [print (item) for item in _coordinates]
        _value = [_assignAndCheckUnitConsistency(item, _unit).to(_unit).value \
                                for item in _coordinates]
        # print (_value)
        _value = np.asarray(_value, dtype=np.float64)*_unit
        super(_nusDimensionObject, self).__setattr__('_coordinates', _value)

    def _dimensionlessConversion(self, unit, _oldValue):
        denominator = (self._origin_offset + self._reference_offset)
        if denominator.value != 0:
            if self._made_dimensionless and _oldValue: return
            if not self._made_dimensionless and not _oldValue: return
            if self._made_dimensionless and not _oldValue:
                _value = (self._coordinates/ denominator).to(_ppm)
                super(_nusDimensionObject, self).__setattr__('_coordinates', _value)
                return
            if not self._made_dimensionless and _oldValue:
                _value = (self._coordinates * denominator).to(unit)
                super(_nusDimensionObject, self).__setattr__('_coordinates', _value)
        else:
            self._made_dimensionless=_oldValue
            print("Zero division encountered: Dimension cannot be made dimensionsless with \n'origin_offset' {0} and 'reference_offset' {1}. No changes made.".format(self._origin_offset, self._reference_offset))


    def __delattr__(self, name):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' of class '{1}' cannot be deleted.".format(name, __class__.__name__))

    def __setattr__(self, name, value):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' cannot be modified".format(name))
        elif name in __class__.__dict__.keys():
            return super(_nusDimensionObject, self).__setattr__(name, value)
        else:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(__class__.__name__, name))

    def info(self):
        _response =[self._number_of_points, 
                    str(self._reference_offset),
                    str(self._origin_offset),
                    self._made_dimensionless,
                    self._reverse,
                    self._quantity,
                    str(self._label),
                    self._periodic]
        return _response
        
    def __str__(self):
        
        block = ['\tnumber_of_points \t= {0}\n',\
                 '\treference_offset \t= {2}\n', \
                 '\torigin_offset \t\t= {3}\n', \
                 '\tmade_dimensionless \t= {4}\n', \
                 '\treverse \t\t= {5}\n', \
                 '\tquantity \t\t= {6}\n', \
                 '\tlabel \t\t\t= {7}\n', \
                 '\tperiodic \t\t= {9}\n']

        string = ''.join(block).format(self._number_of_points, 
                                    self._reference_offset,
                                    self._origin_offset,
                                    self._made_dimensionless,
                                    self._reverse,
                                    self._quantity,
                                    self._label,
                                    self._periodic)
        return string


    def getJsonDictionary(self):
        d = {}
        d['coordinates'] = [quantityFormat(item) for item in self._coordinates]

        if self._reference_offset is not None and self._reference_offset.value != 0:
            d['reference_offset'] = quantityFormat(self._reference_offset)
     
        if self._origin_offset is not None and self._origin_offset.value != 0:
            d['origin_offset'] = quantityFormat(self._origin_offset)
     
        if self._made_dimensionless is True:
            d['made_dimensionless'] = True
    
        if self._reverse is True:
            d['reverse'] = True
  
        if self._periodic is True:
            d['periodic'] = True

        if self._quantity is not None:
            d['quantity'] = self._quantity

        if self._label.strip() != "":
            d['label'] = self._label

        return d

    ## Periodic
    @property
    def periodic(self):
        return self._periodic
    @periodic.setter
    def periodic(self, value = True):
        super(_nusDimensionObject, self).__setattr__('_periodic', _checkAndAssignBool(value))
    
    ## Quantity
    @property
    def quantity(self):
        return self._quantity
    @quantity.setter
    def quantity(self, string = ''):
        super(_nusDimensionObject, self).__setattr__('_quantity', string)

    @property
    def unit(self):
        return self._unit


    ## label
    @property
    def label(self):
        if self._label.strip() == '':
            return self._quantity + ' / ' + unitToLatex(self._coordinates.unit)
        else:
            return self._label + ' / ' + unitToLatex(self._coordinates.unit)
    @label.setter
    def label(self, label=''):
        super(_nusDimensionObject, self).__setattr__('_label', label)
    

    ## made dimensionless
    @property
    def made_dimensionless(self):
        return self._made_dimensionless
    @made_dimensionless.setter
    def made_dimensionless(self, value=False):
        _oldValue = self._made_dimensionless
        _value = _checkAndAssignBool(value)
        super(_nusDimensionObject, self).__setattr__('_made_dimensionless', _value)
        self._dimensionlessConversion(self._unit, _oldValue)

    ## reverse
    @property
    def reverse(self):
        return self._reverse
    @reverse.setter
    def reverse(self, value=False):
        _value = _checkAndAssignBool(value)
        super(_nusDimensionObject, self).__setattr__('_reverse', _value)

    @property
    def type(self):
        return self._type

    
    ## reference offset
    @property
    def reference_offset(self):
        return self._reference_offset
    @reference_offset.setter
    def reference_offset(self, value):
        _value = _assignAndCheckUnitConsistency(value, self._unit)
        super(_nusDimensionObject, self).__setattr__('_reference_offset', _value)
        self._getCoordinates()


    ## origin offset
    @property
    def origin_offset(self):
        return self._origin_offset
    @origin_offset.setter
    def origin_offset(self, value):
        _value = _assignAndCheckUnitConsistency(value, self._unit)
        super(_nusDimensionObject, self).__setattr__('_origin_offset', _value)
        self._getCoordinates()



class Dimension:

    __slots__ = ['_coordinates', '_number_of_points', '_sampling_interval', '_unit', \
                 '_inverse_unit', '_inverse_sampling_interval', \
                 '_reference_offset', '_inverse_reference_offset',\
                 '_origin_offset', '_inverse_origin_offset', \
                 '_made_dimensionless', '_inverse_made_dimensionless', \
                 '_reverse', '_inverse_reverse', '_fft_output_order', '_periodic', '_inverse_periodic', \
                 '_quantity', '_inverse_quantity', '_label', '_inverse_label', \
                 '_type']

    def __init__(self,  _number_of_points, 
                        _sampling_interval, 
                        _reference_offset = None,  
                        _origin_offset = None, 
                        _made_dimensionless = None , 
                        _reverse = False, 
                        _fft_output_order = False, 
                        _periodic = False, 
                        _quantity = None, 
                        _label='',
                        _inverse_sampling_interval = None,
                        _inverse_reference_offset = None, 
                        _inverse_origin_offset = None,
                        _inverse_made_dimensionless = False, 
                        _inverse_reverse = False, 
                        _inverse_quantity = None,
                        _inverse_periodic = False,
                        _inverse_label='',
                        _type = 'uniform physical dimension' ):

        super(Dimension, self).__setattr__('_number_of_points', _number_of_points)

        _value = _assignAndCheckUnitConsistency(_sampling_interval, None)
        super(Dimension, self).__setattr__('_sampling_interval', _value)

        _unit = self._sampling_interval.unit
        _inverse_unit = _unit**-1

        # super(Dimension, self).__setattr__('_ppm', u.Unit('ppm'))
        super(Dimension, self).__setattr__('_unit', _unit)
        super(Dimension, self).__setattr__('_inverse_unit', _inverse_unit)

        if _inverse_sampling_interval is None:
            _value = (1/(_number_of_points*self._sampling_interval.value)) * _inverse_unit
        else:
            _value = _assignAndCheckUnitConsistency(_inverse_sampling_interval, _inverse_unit)
        super(Dimension, self).__setattr__('_inverse_sampling_interval', _value)

        
        ## reference Offset
        _value = _checkAssignmentAndThenCheckUnitConsistency(_reference_offset, _unit)
        super(Dimension, self).__setattr__('_reference_offset', _value)
        _value = _checkAssignmentAndThenCheckUnitConsistency(_inverse_reference_offset, _inverse_unit)
        super(Dimension, self).__setattr__('_inverse_reference_offset', _value)
        
        ## origin offset
        _value = _checkAssignmentAndThenCheckUnitConsistency(_origin_offset, _unit)
        super(Dimension, self).__setattr__('_origin_offset', _value)
        _value =  _checkAssignmentAndThenCheckUnitConsistency(_inverse_origin_offset, _inverse_unit)
        super(Dimension, self).__setattr__('_inverse_origin_offset', _value)

        ### made dimensionless
        _value = _checkAndAssignBool(_made_dimensionless)
        super(Dimension, self).__setattr__('_made_dimensionless', _value)
        _value = _checkAndAssignBool(_inverse_made_dimensionless)
        super(Dimension, self).__setattr__('_inverse_made_dimensionless', _value)

        ### reverse
        _value = _checkAndAssignBool(_reverse)
        super(Dimension, self).__setattr__('_reverse', _value)
        _value = _checkAndAssignBool(_inverse_reverse)
        super(Dimension, self).__setattr__('_inverse_reverse', _value)

        _value = _checkAndAssignBool(_fft_output_order)
        super(Dimension, self).__setattr__('_fft_output_order', _value)
        _value = _checkAndAssignBool(_periodic)
        super(Dimension, self).__setattr__('_periodic', _value)
        _value = _checkAndAssignBool(_inverse_periodic)
        super(Dimension, self).__setattr__('_inverse_periodic', _value)


        ## quantity
        _value = _checkQuantity(_quantity, _unit)
        super(Dimension, self).__setattr__('_quantity', _value)
        _value = _checkQuantity(_inverse_quantity, _inverse_unit)
        super(Dimension, self).__setattr__('_inverse_quantity', _value)

        ## label
        super(Dimension, self).__setattr__('_label', _label)
        super(Dimension, self).__setattr__('_inverse_label', _inverse_label)
        super(Dimension, self).__setattr__('_coordinates', None)
        self._getCoordinates()

    def _dimensionlessConversion(self, unit, _oldValue):
        denominator = (self._origin_offset + self._reference_offset)
        # print (denominator)
        # print (self._coordinates, unit, denominator)
        if denominator.value != 0:
            if self._made_dimensionless and _oldValue: return
            if not self._made_dimensionless and not _oldValue: return
            if self._made_dimensionless and not _oldValue:
                _value = (self._coordinates / denominator).to(_ppm)
                super(Dimension, self).__setattr__('_coordinates', _value)
                return
            if not self._made_dimensionless and _oldValue:
                _value = (self._coordinates * denominator).to(unit)
                super(Dimension, self).__setattr__('_coordinates', _value)
        else:
            super(Dimension, self).__setattr__('_made_dimensionless', _oldValue)
            print("Zero division encountered: Dimension cannot be made dimensionsless with \n'origin_offset' {0} and 'reference_offset' {1}. No changes made.".format(self._origin_offset, self._reference_offset))

    def __delattr__(self, name):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' of class '{1}' cannot be deleted.".format(name, __class__.__name__))

    def __setattr__(self, name, value):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' cannot be modified".format(name))
        elif name in __class__.__dict__.keys():
            return super(Dimension, self).__setattr__(name, value)
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
                    self._periodic]
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
                 '\tperiodic \t\t= {9}\n']

        # inverseBlock = ['\n\tinverse_sampling_interval \t= {0}\n', \
        #          '\tinverse_reference_offset \t= {1}\n', \
        #          '\tinverse_origin_offset \t\t= {2}\n', \
        #          '\tinverse_made_dimensionless\t= {3}\n', \
        #          '\tinverse_reverse \t\t= {4}\n', \
        #          '\tinverse_quantity \t\t= {5}\n', \
        #          '\tinverse_label \t\t\t= {6}\n' ]

        string = ''.join(block).format(self._number_of_points, 
                                    self._sampling_interval,
                                    self._reference_offset,
                                    self._origin_offset,
                                    self._made_dimensionless,
                                    self._reverse,
                                    self._quantity,
                                    self._label,
                                    self._fft_output_order,
                                    self._periodic)

        # string2 = ''.join(inverseBlock).format(self._inverse_sampling_interval, 
        #                             self._inverse_reference_offset,
        #                             self._inverse_origin_offset, 
        #                             self._inverse_made_dimensionless,
        #                             self._inverse_reverse, 
        #                             self._inverse_quantity, 
        #                             self._inverse_label)
        return string

    def _swapValues(self, a, b):
        temp = self.__getattribute__(a)
        # print (self.__getattribute__(b))
        super(Dimension, self).__setattr__(a, self.__getattribute__(b))
        super(Dimension, self).__setattr__(b, temp)
        temp = None
        del temp


    def _inverse(self):
        self._swapValues('_sampling_interval', '_inverse_sampling_interval')
        self._swapValues('_reference_offset', '_inverse_reference_offset')
        self._swapValues('_origin_offset', '_inverse_origin_offset')
        self._swapValues('_made_dimensionless', '_inverse_made_dimensionless')
        self._swapValues('_reverse', '_inverse_reverse')
        self._swapValues('_unit', '_inverse_unit')

        if self._fft_output_order:
            super(Dimension, self).__setattr__('_fft_output_order', False)
        else:
            super(Dimension, self).__setattr__('_fft_output_order', True)

        self._swapValues('_quantity', '_inverse_quantity')
        self._swapValues('_label', '_inverse_label')
        self._swapValues('_periodic', '_inverse_periodic')
        self._getCoordinates()



    def getJsonDictionary(self):
        d = {}
        d['reciprocal'] = {}
        d['number_of_points'] = self._number_of_points
        d['sampling_interval'] = quantityFormat(self._sampling_interval)

        if self._reference_offset is not None and self._reference_offset.value != 0:
            d['reference_offset'] = quantityFormat(self._reference_offset)
        if self._inverse_reference_offset is not None and self._inverse_reference_offset.value != 0:
            d['reciprocal']['reference_offset'] = quantityFormat(self._inverse_reference_offset)

        if self._origin_offset is not None and self._origin_offset.value != 0:
            d['origin_offset'] = quantityFormat(self._origin_offset)
        if self._inverse_origin_offset is not None and self._inverse_origin_offset.value != 0:
            d['reciprocal']['origin_offset'] = quantityFormat(self._inverse_origin_offset)

        # if self._made_dimensionless is True:
        #     d['made_dimensionless'] = True
        # if self._inverse_made_dimensionless is True:
        #     d['inverse_made_dimensionless'] = True

        if self._reverse is True:
            d['reverse'] = True
        if self._inverse_reverse is True:
            d['reciprocal']['reverse'] = True

        if self._fft_output_order is True:
            d['fft_output_order'] = True

        if self._periodic is True:
            d['periodic'] = True
        if self._inverse_periodic is True:
            d['reciprocal']['periodic'] = True

        if self._quantity not in [None, "unknown", "dimensionless"]:
            d['quantity'] = self._quantity

        if self._inverse_quantity not in [None, "unknown", "dimensionless"]:
            d['reciprocal']['quantity'] = self._inverse_quantity

        if self._label.strip() != "":
            d['label'] = self._label

        if self._inverse_label.strip() != "":
            d['reciprocal']['label'] = self._inverse_label

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
        super(Dimension, self).__setattr__('_periodic', _checkAndAssignBool(value))
    
    ## Quantity
    @property
    def quantity(self):
        return self._quantity
    @quantity.setter
    def quantity(self, string = ''):
        super(Dimension, self).__setattr__('_quantity', string)


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
        super(Dimension, self).__setattr__('_label', label)
    

    ## inverseLabel
    @property
    def inverse_label(self):
        return self._inverse_label
    @inverse_label.setter
    def inverse_label(self, label=''):
        super(Dimension, self).__setattr__('_inverse_label', label)

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
        super(Dimension, self).__setattr__('_made_dimensionless', _value)
        self._dimensionlessConversion(self._unit, _oldValue)

    ## inverse made dimensionless
    @property
    def inverse_made_dimensionless(self):
        return self._inverse_made_dimensionless
    @inverse_made_dimensionless.setter
    def inverse_made_dimensionless(self, value=False):
        _oldValue = self._inverse_made_dimensionless
        _value = _checkAndAssignBool(value)
        super(Dimension, self).__setattr__('_inverse_made_dimensionless', _value)
        # self._dimensionlessConversion(self._inverse_unit, _oldValue)


    ## reverse
    @property
    def reverse(self):
        return self._reverse
    @reverse.setter
    def reverse(self, value=False):
        _value = _checkAndAssignBool(value)
        super(Dimension, self).__setattr__('_reverse', _value)


    ## inverse reverse
    @property
    def inverse_reverse(self):
        return self._inverse_reverse
    @inverse_reverse.setter
    def inverse_reverse(self, value=False):
        _value = _checkAndAssignBool(value)
        super(Dimension, self).__setattr__('_inverse_reverse', _value)


    ## reference offset
    @property
    def reference_offset(self):
        return self._reference_offset
    @reference_offset.setter
    def reference_offset(self, value):
        _value = _assignAndCheckUnitConsistency(value, self._unit)
        super(Dimension, self).__setattr__('_reference_offset', _value)
        self._getCoordinates()


    ## inverse reference offset
    @property
    def inverse_reference_offset(self):
        return self._inverse_reference_offset
    @inverse_reference_offset.setter
    def inverse_reference_offset(self, value):
        _value = _assignAndCheckUnitConsistency(value, self._inverse_unit)
        super(Dimension, self).__setattr__('_inverse_reference_offset', _value)


    ## origin offset
    @property
    def origin_offset(self):
        return self._origin_offset
    @origin_offset.setter
    def origin_offset(self, value):
        _value = _assignAndCheckUnitConsistency(value, self._unit)
        super(Dimension, self).__setattr__('_origin_offset', _value)
        self._getCoordinates()


    ## inverse origin offset
    @property
    def inverse_origin_offset(self):
        return self._inverse_origin_offset
    @inverse_origin_offset.setter
    def inverse_origin_offset(self, value):
        _value = _assignAndCheckUnitConsistency(value, self._inverse_unit)
        super(Dimension, self).__setattr__('_inverse_origin_offset', _value)


    ## sampling interval
    @property
    def sampling_interval(self):
        return self._sampling_interval
    @sampling_interval.setter
    def sampling_interval(self, value):
        _value = _assignAndCheckUnitConsistency(value, self._unit)
        super(Dimension, self).__setattr__('_sampling_interval', _value)
        self._getCoordinates()


    ## inverse sampling interval
    @property
    def inverse_sampling_interval(self):
        return self._inverse_sampling_interval
    @inverse_sampling_interval.setter
    def inverse_sampling_interval(self, value):
        _value = _assignAndCheckUnitConsistency(value, self._inverse_unit)
        super(Dimension, self).__setattr__('_inverse_sampling_interval', _value)

    ## npts
    @property
    def number_of_points(self):
        return self._number_of_points
    @number_of_points.setter
    def number_of_points(self, value):
        if isinstance(value, int):
            super(Dimension, self).__setattr__('_number_of_points', value)
        # self._number_of_points = _assignAndCheckUnitConsistency(value, u.Unit(''))
        self._getCoordinates()

    
    def _getCoordinates(self):
        _unit = self._unit
        _number_of_points = self._number_of_points
        _sampling_interval = self._sampling_interval.to(_unit)
        _reference_offset = self._reference_offset.to(_unit)
        _origin_offset = self._origin_offset.to(_unit)
        if self._fft_output_order:
            _value = ( np.arange(_number_of_points, dtype=np.float64)* _sampling_interval \
                            - (0.5*_sampling_interval*_number_of_points) - _reference_offset)
        else:
            _value = ( np.arange(_number_of_points, dtype=np.float64)* _sampling_interval \
                            - _reference_offset )
        if self._made_dimensionless:
            _value/=(_origin_offset + _reference_offset)
            _value = _value.to(_ppm)
        # self._coordinates = _value
        super(Dimension, self).__setattr__('_coordinates', _value)

    def getInverseCoordinates(self, parameter_list):
        pass










class _datasetObject:
    """
        keywork aruament :
          name : any string
          format : either 'binary' or 'text'.
          data_type : one of 'float32', 'float64', 'comple64' or 'complex128'.
          unit : unit associated with the dataset.
          quantity : the physical qunatity associated with the dataset.
          values : ordered array in format specified at keywords 'format' and 'data_type'.
    """

    __slots__ = ['_name', '_encoding', '_dataset_type', '_numeric_type', '_npType', '_filename',\
                 '_unit', '_label', '_quantity', '_components', '_components_url', '_channels']

    def __init__(self, 
                _name = None,
                _unit = None,
                _quantity = None, 
                _label = None,
                _encoding = None, 
                _numeric_type = None,
                _dataset_type = None,
                _uncertainty = None,
                _components = None,
                _uncertainties = None,
                _components_url = None,
                _uncertainties_url = None,
                _filename = ''):

        if _components is None and _components_url is None:
            raise ValueError("No dataset found.")

        if _components != None and _encoding is None: _encoding = 'none'
        elif _components_url != None and _encoding is None: _encoding = 'raw'

        super(_datasetObject, self).__setattr__('_encoding', _checkFileFormat(_encoding))
        _va = _assignAndCheckUnitConsistency(_unit, None).unit
        super(_datasetObject, self).__setattr__('_unit', _va)
        super(_datasetObject, self).__setattr__('_name', _name)
        super(_datasetObject, self).__setattr__('_quantity', _checkQuantity(_quantity, self._unit))
        _va, npType = _checkNumberType(_numeric_type)
        
        super(_datasetObject, self).__setattr__('_numeric_type', _va)
        _va, total_components = _checkDataType(_dataset_type)
        super(_datasetObject, self).__setattr__('_dataset_type', _va)
        super(_datasetObject, self).__setattr__('_label', _label)
        
        

        if _components is not None:
            _val_len = len(_components)
            if _val_len != total_components:
                raise Exception("dataset_type '{0}' is non consistent with total number of components, {1}".format(self._dataset_type, _val_len))

            if self._encoding == 'base64':
                _components = np.asarray([np.fromstring(base64.b64decode(item), \
                                dtype=npType) for item in _components])*self._unit
            elif self._encoding == 'none' or self._encoding is None:
                if _numeric_type[:7] == 'complex':
                    _components = np.asarray([np.asarray(item[0::2]) + 1j*np.asarray(item[1::2]) \
                                for item in _components])*self._unit 
                else:
                    _components = np.asarray([np.asarray(item) \
                                for item in _components])*self._unit 
            else:
                raise Exception("'{0}' is an invalid data 'encoding'.".format(self._encoding))

        if _components_url is not None:  
            if self._encoding == 'raw' or self._encoding is None:
                splt = os.path.split(_filename)
                # print (splt)
                _components = np.fromfile( os.path.join(splt[0], _components_url), dtype=npType)
                _components = _components.reshape(total_components, int(_components.size/total_components))*self._unit 
            else:
                raise Exception("'{0}' is an invalid data 'encoding'.".format(self._encoding))



        super(_datasetObject, self).__setattr__('_channels', total_components)
        super(_datasetObject, self).__setattr__('_npType', npType)

        _components = np.asarray(_components, dtype=npType).swapaxes(0,-1)
        super(_datasetObject, self).__setattr__('_components', _components)
        super(_datasetObject, self).__setattr__('_components_url', _components_url)

    def __setattr__(self, name, value):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' cannot be modified".format(name))
        elif name in __class__.__dict__.keys():
            return super(_datasetObject, self).__setattr__(name, value)
        else:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(__class__.__name__, name))

    # def __getattr__(self, name):
    #     if name not in __class__.__slots__ and name not in __class__.__dict__.keys():
    #         raise AttributeError("'{0}' has not attribute with name '{1}'.".format(__class__.__name__, name))
    #     return 

    def getJsonDictionary(self, filename, datasetIndex):
        d = {}
        if self._name.strip() != '':
            d['name'] = self._name
        if str(self._unit) != '':
            d['unit'] = str(self._unit)

        if self._quantity != 'dimensionless' and self._quantity != 'unknown':
            d['quantity'] = self._quantity

        if self._label != '':
            d['label'] = self._label

        if self._encoding not in ['none', 'raw', None]:
            d['encoding'] = str(self._encoding)

        # if self._numeric_type != 'float32':
        d['numeric_type'] = str(self._numeric_type)

        if self._dataset_type != 'scalar':
            d['dataset_type'] = self._dataset_type
        
        size = self._components[...,0].size
        if self._numeric_type[:7] == 'complex':
            if self._numeric_type == 'complex64':
                c = np.empty((self._channels, size*2), dtype=np.float32)
            if self._numeric_type == 'complex128':
                c = np.empty((self._channels, size*2), dtype=np.float64)

            for i in range(self._channels):
                c[i, 0::2] = self._components.real[...,i].ravel()
                c[i, 1::2] = self._components.imag[...,i].ravel()
        else:
            c = np.empty((self._channels, size), dtype=self._npType)
            for i in range(self._channels):
                c[i] = self._components[...,i].ravel()

        # print (c)
        if self._encoding == 'none':
            d['components'] = c.tolist()
        if self._encoding == 'base64':
            d['components'] = [base64.b64encode(item).decode("utf-8") \
                            for item in c]

        print ("_studium", self._encoding)
        if self._encoding == 'raw':
            if self.name == '': 
                index = str(datasetIndex)
            else:
                index = self.name

            splt = os.path.split(filename)
            fname = os.path.splitext(splt[1])[0]
            d['components_url'] = fname + '_' + index + '.dat'
            c.ravel().tofile( os.path.join(splt[0], d['components_url'] ))

        c = None
        del c               
        return d

    @property
    def components_url(self):
        return self._components_url

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        super(_datasetObject, self).__setattr__('_name', value)
    
    @property
    def encoding(self):
        return self._encoding
    @encoding.setter
    def encoding(self, value):
        value = _checkFileFormat(value)
        super(_datasetObject, self).__setattr__('_encoding', value)

    @property
    def dataset_type(self):
        return self._dataset_type
    @dataset_type.setter
    def dataset_type(self, value):
        value = _checkDataType(value)
        super(_datasetObject, self).__setattr__('_dataset_type', value)

    
    @property
    def numeric_type(self):
        return self._numeric_type
    @numeric_type.setter
    def numeric_type(self, value):
        _va, npType = _checkNumberType(value)
        super(_datasetObject, self).__setattr__('_numeric_type', value)
        super(_datasetObject, self).__setattr__('_npType', npType)
        super(_datasetObject, self).__setattr__('_components', \
                np.asarray(self._components, dtype=npType))

    @property
    def unit(self):
        return self._unit
    
    @property
    def label(self):
        return self._label
    @label.setter
    def label(self, value):
        super(_datasetObject, self).__setattr__('_label', value)

    @property
    def quantity(self):
        return self._quantity


    def info(self):
        _response =[self._url, 
                    self._name,
                    str(self._unit),
                    self._quantity,
                    self._label,
                    self._encoding,
                    self._numeric_type,
                    self._dataset_type]
        return _response


    def _channelMethod(self, i):
        return self._components[...,i]

    def scale(self, value):
        value = _assignAndCheckUnitConsistency(value, self._unit)
        value = value.to(self._unit).value
        super(_datasetObject, self).__setattr__('_components',self._components*value)


    def reshape(self, shape):
        shape = shape + (self._channels,)
        nptype = self._npType
        super(_datasetObject, self).__setattr__('_components', \
            np.asarray(self._components.reshape(shape), dtype=nptype))


    def __getattr__(self, name):
        if name == 'component':
            return SequenceProxy(self._channelMethod, self._channel)
        # if name == 'component':
            # return self.channel

        # length = self._stopDataset
        # while i < 0:
        #     i += length
        # if 0 <= i < length:
        #     return self._values[...,i]
        # raise IndexError('Index out of range: {}'.format(i))


    #def __str__(self):
    #    return( str(self._values) + ' '+ str(self._unit))
        # block = ['\turl \t= {0}\n',\
        #          '\tformat \t= {1}\n', \
        #          '\tdtype \t= {2}\n', \
        #          '\tname \t\t= {3}\n', \
        #          '\tmade_dimensionless \t= {4}\n', \
        #          '\treverse \t\t= {5}\n', \
        #          '\tquantity \t\t= {6}\n', \
        #          '\tlabel \t\t\t= {7}\n', \
        #          '\tftFlag \t\t\t= {8}\n', \
        #          '\tperiodic \t\t= {9}\n']
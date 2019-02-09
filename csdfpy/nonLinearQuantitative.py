from __future__ import print_function, division
import numpy as np
import json
from .unit import valueObjectFormat, unitToLatex, _ppm
from ._csdmChecks import (_assignAndCheckUnitConsistency, 
                      _checkUnitConsistency,
                      _checkAndAssignBool,
                      _checkQuantity,
                      _checkValueObject,
                      _defaultUnits,
                      stringToQuantity,
                      _axis_label)

class _nonLinearQuantitativeControlledVariable:

    __slots__ = ['_sampling_type',
                 '_non_quantitative',
                 '_quantity',
                 '_number_of_points',
                 '_coordinates',
                 '_reference_offset',
                 '_origin_offset', 
                 '_reverse',
                 '_label',
                 '_period',
                 '_made_dimensionless',

                 '_reciprocal_coordinates',
                 '_reciprocal_quantity',
                 '_reciprocal_number_of_points', 
                 '_reciprocal_origin_offset',
                 '_reciprocal_reference_offset', 
                 '_reciprocal_reverse',
                 '_reciprocal_label',
                 '_reciprocal_period',
                 '_reciprocal_made_dimensionless',

                 '_unit',
                 '_dimensionless_unit',
                 '_reciprocal_unit',
                 '_reciprocal_dimensionless_unit',
                 
                 '_absolute_coordinates',
                 '_reciprocal_absolute_coordinates',
                 
                 '_type']

    def __init__(self,  _coordinates, 
                        _reference_offset = None,
                        _origin_offset = None,
                        _quantity=None, 
                        _reverse=False, 
                        _label='',
                        _period=None,
                        _made_dimensionless = False,
                         
                        _sampling_type = 'grid',
                        _non_quantitative = False,

                        _reciprocal_reference_offset = None, 
                        _reciprocal_origin_offset = None,
                        _reciprocal_quantity = None,
                        _reciprocal_reverse = False, 
                        _reciprocal_label='',
                        _reciprocal_period = None,
                        _reciprocal_made_dimensionless = False):

        self.setAttribute('_sampling_type', _sampling_type)
        self.setAttribute('_non_quantitative', _non_quantitative)
        self.setAttribute('_type', 'non-linear')

        self.setAttribute('_number_of_points', len(_coordinates))
        self.setAttribute('_reciprocal_number_of_points', self.number_of_points)

        _unit = _assignAndCheckUnitConsistency(_coordinates[0], None).unit
        _reciprocal_unit =  _unit**-1

        self.setAttribute('_unit', _unit)
        self.setAttribute('_reciprocal_unit', _reciprocal_unit)
        self.setAttribute('_dimensionless_unit', '')
        self.setAttribute('_reciprocal_dimensionless_unit', '')

        ## reference
        _value = _checkValueObject(_reference_offset, _unit)
        self.setAttribute('_reference_offset', _value)
        _value = _checkValueObject(_reciprocal_reference_offset, _reciprocal_unit)
        self.setAttribute('_reciprocal_reference_offset', _value)
        
        ## origin offset
        _value = _checkValueObject(_origin_offset, _unit)
        self.setAttribute('_origin_offset', _value)
        _value =  _checkValueObject(_reciprocal_origin_offset, _reciprocal_unit)
        self.setAttribute('_reciprocal_origin_offset', _value)

        ### made dimensionless
        _value = _checkAndAssignBool(_made_dimensionless)
        self.setAttribute('_made_dimensionless', _value)
        _value = _checkAndAssignBool(_reciprocal_made_dimensionless)
        self.setAttribute('_reciprocal_made_dimensionless', _value)
       
        ### reverse
        _value = _checkAndAssignBool(_reverse)
        self.setAttribute('_reverse', _value)
        _value = _checkAndAssignBool(_reciprocal_reverse)
        self.setAttribute('_reciprocal_reverse', _value)

        ## period
        _value = _checkValueObject(_period, _unit)
        self.setAttribute('_period', _value)
        _value = _checkValueObject(_reciprocal_period, _reciprocal_unit)
        self.setAttribute('_reciprocal_period', _value)

        ## quantity
        _value = _checkQuantity(_quantity, _unit)
        self.setAttribute('_quantity', _value)
        _value = _checkQuantity(_reciprocal_quantity, _reciprocal_unit)
        self.setAttribute('_reciprocal_quantity', _value)
    
        ## label
        self.setAttribute('_label', _label)
        self.setAttribute('_reciprocal_label', _reciprocal_label)

        # [print (item) for item in _coordinates]
        _value = [_assignAndCheckUnitConsistency(item, _unit).to(_unit).value \
                                for item in _coordinates]
        # print (_value)
        _value = np.asarray(_value, dtype=np.float64)*_unit
        self.setAttribute('_coordinates', _value)
        self.setAttribute('_reciprocal_coordinates', None)
        # self.setAttribute('_reciprocal_absolute_coordinates', None)
        self._getCoordinates()

    def setAttribute(self, name, value):
        super(_nonLinearQuantitativeControlledVariable, self).__setattr__(name, value)

    def __delattr__(self, name):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' of class '{1}' cannot be deleted.".format(name, __class__.__name__))

    def __setattr__(self, name, value):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' cannot be modified".format(name))
        elif name in __class__.__dict__.keys():
            return self.setAttribute(name, value)
        else:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(__class__.__name__, name))


### --------------- Attributes ------------------ ###
    ## sampling_type
    @property
    def sampling_type(self):
        return self._sampling_type

    ## non_quantitative
    @property
    def non_quantitative(self):
        return self._non_quantitative

    ## period
    @property
    def period(self):
        return self._period
    @period.setter
    def period(self, value):
        self.setAttribute('_period', _checkValueObject(value, self.unit))
    
    ## reciprocal period
    @property
    def reciprocal_period(self):
        return self._reciprocal_period
    @reciprocal_period.setter
    def reciprocal_period(self, value):
        self.setAttribute('_reciprocal_period', \
                        _checkValueObject(value, self.reciprocal_unit))

    ## Quantity
    @property
    def quantity(self):
        return self._quantity
    @quantity.setter
    def quantity(self, string = ''):
        self.setAttribute('_quantity', string)

    ## reciprocal Quantity
    @property
    def reciprocal_quantity(self):
        return self._reciprocal_quantity
    @reciprocal_quantity.setter
    def reciprocal_quantity(self, string = ''):
        self.setAttribute('_reciprocal_quantity', string)


    @property
    def unit(self):
        if self._made_dimensionless:
            unit = self._dimensionless_unit
        else:
            unit = self._unit
        return unit

    @property
    def reciprocal_unit(self):
        if self._reciprocal_made_dimensionless:
            unit = self._reciprocal_dimensionless_unit
        else:
            unit = self._reciprocal_unit
        return unit

    ## label
    @property
    def label(self):
        return self._label
    @label.setter
    def label(self, label=''):
        self.setAttribute('_label', label)

    @property
    def axis_label(self):
        return _axis_label(self.label, 
                           self._unit,
                           self.made_dimensionless,
                           self._dimensionless_unit)
    
    ## reciprocalLabel
    @property
    def reciprocal_label(self):
        return self._reciprocal_label
    @reciprocal_label.setter
    def reciprocal_label(self, label=''):
        self.setAttribute('_reciprocal_label', label)

    ## made dimensionless
    @property
    def made_dimensionless(self):
        return self._made_dimensionless
    @made_dimensionless.setter
    def made_dimensionless(self, value=False):
        if value:
            denominator = (self.origin_offset + self.reference_offset)
            if denominator.value == 0:
                raise ZeroDivisionError("Dimension cannot be made dimensionsless with \n'origin_offset' {0} and 'reference_offset' {1}. No changes made.".format(self.origin_offset, self.reference_offset))
        self.setAttribute('_made_dimensionless', value)


    ## reciprocal made dimensionless
    @property
    def reciprocal_made_dimensionless(self):
        return self._reciprocal_made_dimensionless
    @reciprocal_made_dimensionless.setter
    def reciprocal_made_dimensionless(self, value=False):
        if value:
            denominator = (self.reciprocal_origin_offset + self.reciprocal_reference_offset)
            if denominator.value == 0:
                raise ZeroDivisionError("Dimension cannot be made dimensionsless with \n'origin_offset' {0} and 'reference_offset' {1}. No changes made.".format(self.origin_offset, self.reference_offset))
        self.setAttribute('_reciprocal_made_dimensionless', value)

    ## reverse
    @property
    def reverse(self):
        return self._reverse
    @reverse.setter
    def reverse(self, value=False):
        _value = _checkAndAssignBool(value)
        self.setAttribute('_reverse', _value)

    ## reciprocal reverse
    @property
    def reciprocal_reverse(self):
        return self._reciprocal_reverse
    @reciprocal_reverse.setter
    def reciprocal_reverse(self, value=False):
        _value = _checkAndAssignBool(value)
        self.setAttribute('_reciprocal_reverse', _value)
    
    ## reference offset
    @property
    def reference_offset(self):
        return self._reference_offset
    @reference_offset.setter
    def reference_offset(self, value):
        _value = _assignAndCheckUnitConsistency(value, self.unit)
        self.setAttribute('_reference_offset', _value)
        self._getCoordinates()

    ## reciprocal reference offset
    @property
    def reciprocal_reference_offset(self):
        return self._reciprocal_reference_offset
    @reciprocal_reference_offset.setter
    def reciprocal_reference_offset(self, value):
        _value = _assignAndCheckUnitConsistency(value, self.reciprocal_unit)
        self.setAttribute('_reciprocal_reference_offset', _value)
        self._getreciprocalCoordinates()

    ## origin offset
    @property
    def origin_offset(self):
        return self._origin_offset
    @origin_offset.setter
    def origin_offset(self, value):
        _value = _assignAndCheckUnitConsistency(value, self.unit)
        self.setAttribute('_origin_offset', _value)
        self._getCoordinates()

    ## reciprocal origin offset
    @property
    def reciprocal_origin_offset(self):
        return self._reciprocal_origin_offset
    @reciprocal_origin_offset.setter
    def reciprocal_origin_offset(self, value):
        _value = _assignAndCheckUnitConsistency(value, self.reciprocal_unit)
        self.setAttribute('_reciprocal_origin_offset', _value)
        # self._getreciprocalCoordinates()

    ## number_of_points
    @property
    def number_of_points(self):
        return self._number_of_points

    ## coordinates
    @property
    def coordinates(self):
        _value = 1.0
        if self._made_dimensionless:
            _value=(self._origin_offset + self._reference_offset)
        return (self._coordinates/_value).to(self.unit)

    ## absolute_coordinates
    @property
    def absolute_coordinates(self):
        return self._absolute_coordinates

    ## reciprocal_coordinates
    @property
    def reciprocal_coordinates(self):
        return self._reciprocal_coordinates

    ## reciprocal_absolute_coordinates
    @property
    def reciprocal_absolute_coordinates(self):
        return self._reciprocal_absolute_coordinates

###--------------Private Methods------------------###

    # def _dimensionlessConversion(self, unit, _oldValue):
    #     denominator = (self.origin_offset + self.reference_offset)
    #     if denominator.value != 0:
    #         if self.made_dimensionless and _oldValue: return
    #         if not self.made_dimensionless and not _oldValue: return
    #         if self.made_dimensionless and not _oldValue:
    #             _value = (self.coordinates/ denominator).to(_ppm)
    #             self.setAttribute('_coordinates', _value)
    #             return
    #         if not self.made_dimensionless and _oldValue:
    #             _value = (self.coordinates * denominator).to(unit)
    #             self.setAttribute('_coordinates', _value)
    #     else:
    #         self._made_dimensionless=_oldValue
    #         print("Zero division encountered: Dimension cannot be made dimensionsless with \n'origin_offset' {0} and 'reference_offset' {1}. No changes made.".format(self.origin_offset, self.reference_offset))

    def _info(self):
        _response =[self.sampling_type,
                    self.non_quantitative,
                    self.number_of_points, 
                    str(self.reference_offset),
                    str(self.origin_offset),
                    self.made_dimensionless,
                    self.reverse,
                    self.quantity,
                    str(self._label),
                    self.period]
        return _response
        
    # def __str__(self):
        
    #     block = ['\tsampling_type \t\t= {0}\n', \
    #              '\tnon_quantitative \t\t= {1}\n', \
    #              '\tnumber_of_points \t= {2}\n',\
    #              '\treference_offset \t= {3}\n', \
    #              '\torigin_offset \t\t= {4}\n', \
    #              '\tmade_dimensionless \t= {5}\n', \
    #              '\treverse \t\t= {6}\n', \
    #              '\tquantity \t\t= {7}\n', \
    #              '\tlabel \t\t\t= {8}\n', \
    #              '\tperiod \t\t= {9}\n']

    #     string = ''.join(block).format(self.sampling_type,
    #                                 self.non_quantitative,
    #                                 self.number_of_points, 
    #                                 self.reference_offset,
    #                                 self.origin_offset,
    #                                 self.made_dimensionless,
    #                                 self.reverse,
    #                                 self.quantity,
    #                                 self._label,
    #                                 self.period)
    #     return string

    def _getCoordinates(self):
        _unit = self._unit
        _reference_offset = self.reference_offset.to(_unit)
        _value = ( self.coordinates - _reference_offset )
        _origin_offset = self.origin_offset.to(_unit)
        # if self.made_dimensionless:
        #     _value/=(_origin_offset + _reference_offset)
            # _value = _value.to(_ppm)
        self.setAttribute('_coordinates', _value)
        self.setAttribute('_absolute_coordinates', _value + _origin_offset)

    def _get_python_dictonary(self):
        dictionary = {}
        dictionary['reciprocal'] = {}

        dictionary['coordinates'] = [valueObjectFormat(item) for item in self.coordinates]

        if self.reference_offset is not None and self.reference_offset.value != 0:
            dictionary['reference_offset'] = valueObjectFormat(self.reference_offset)
        if self.reciprocal_reference_offset is not None and self.reciprocal_reference_offset.value != 0:
            dictionary['reciprocal']['reference_offset'] = valueObjectFormat(self.reciprocal_reference_offset)

        if self.origin_offset is not None and self.origin_offset.value != 0:
            dictionary['origin_offset'] = valueObjectFormat(self.origin_offset)
        if self.reciprocal_origin_offset is not None and self.reciprocal_origin_offset.value != 0:
            dictionary['reciprocal']['origin_offset'] = valueObjectFormat(self.reciprocal_origin_offset)

        # if self.made_dimensionless is True:
        #     d['made_dimensionless'] = True
    
        if self.reverse is True:
            dictionary['reverse'] = True
        if self.reciprocal_reverse is True:
            dictionary['reciprocal']['reverse'] = True

        if self.period.value not in [0.0, np.inf, None]:
            dictionary['period'] = valueObjectFormat(self.period)
        if self.reciprocal_period.value not in [0.0, np.inf, None]:
            dictionary['reciprocal']['period'] = valueObjectFormat(self.reciprocal_period)

        if self.quantity is not None:
            dictionary['quantity'] = self.quantity
        if self.reciprocal_quantity not in [None, "unknown", "dimensionless"]:
            dictionary['reciprocal']['quantity'] = self.reciprocal_quantity

        if self.label.strip() != "":
            dictionary['label'] = self.label
        if self.reciprocal_label.strip() != "":
            dictionary['reciprocal']['label'] = self.reciprocal_label

        if dictionary['reciprocal'] == {}:
            del dictionary['reciprocal']

        return dictionary

### ------------- Public Methods ------------------ ###
    def __str__(self):
        dictionary = self._get_python_dictonary()
        return (json.dumps(dictionary, sort_keys=False, indent=2))

    def to(self, unit):
        if unit.strip() == 'ppm': 
            self.setAttribute('_dimensionless_unit', _ppm)
        else:
            self.setAttribute('_unit', _checkUnitConsistency(stringToQuantity('1 '+unit), self.unit).unit)
        return self.coordinates

    def __iadd__(self, other):
        self.reference_offset -= _assignAndCheckUnitConsistency(other, self.unit) 

    def __isub__(self, other):
        self.reference_offset += _assignAndCheckUnitConsistency(other, self.unit) 
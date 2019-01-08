from __future__ import print_function, division
import numpy as np
import json
from unit import stringToQuantity, quantityFormat, unitToLatex, _ppm
from ._studium import (_assignAndCheckUnitConsistency, 
                      _checkAndAssignBool,
                      _checkQuantity,
                      _checkAssignmentAndThenCheckUnitConsistency)

class _nonQuantitativeControlledVariable:

    __slots__ = ['_sampling_type',
                 '_quantitative',
                 '_number_of_points',
                 '_coordinates', 
                 '_reverse',
                 '_label'
                 ]

    def __init__(self,  _coordinates, 
                        _sampling_type='grid',
                        _quantitative=False,
                        _reverse=False, 
                        _label=''):

        self.setAttribute('_sampling_type', _sampling_type)
        self.setAttribute('_quantitative', False)

        self.setAttribute('_number_of_points', len(_coordinates))

        ### reverse
        _value = _checkAndAssignBool(_reverse)
        self.setAttribute('_reverse', _value)

        ## label
        self.setAttribute('_label', _label)

        # print (_value)
        _value = np.asarray(_coordinates)
        self.setAttribute('_coordinates', _value)

    def setAttribute(self, name, value):
        super(_nonQuantitativeControlledVariable, self).__setattr__(name, value)

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

    ## quantitative
    @property
    def quantitative(self):
        return self._quantitative

    ## label
    @property
    def label(self):
        if self._label.strip() == '':
            return self.quantity + ' / ' + unitToLatex(self.coordinates.unit)
        else:
            return self._label + ' / ' + unitToLatex(self.coordinates.unit)
    @label.setter
    def label(self, label=''):
        self.setAttribute('_label', label)
    
    ## reverse
    @property
    def reverse(self):
        return self._reverse
    @reverse.setter
    def reverse(self, value=False):
        _value = _checkAndAssignBool(value)
        self.setAttribute('_reverse', _value)

    ## number_of_points
    @property
    def number_of_points(self):
        return self._number_of_points

    ## coordinates
    @property
    def coordinates(self):
        return self._coordinates


###--------------Private Methods------------------###

    def _info(self):
        _response =[self.sampling_type,
                    self.quantitative,
                    self.number_of_points,
                    self.reverse,
                    str(self._label)]
        return _response
        
    # def __str__(self):
        
    #     block = ['\tsampling_type \t\t= {0}\n', \
    #              '\tquantitative \t\t= {1}\n', \
    #              '\tnumber_of_points \t= {2}\n',\
    #              '\treverse \t\t= {3}\n', \
    #              '\tlabel \t\t\t= {4}\n']

    #     string = ''.join(block).format(self.sampling_type,
    #                                 self.quantitative,
    #                                 self.number_of_points,
    #                                 self.reverse,
    #                                 self._label,
    #                                 )
    #     return string

    def _getPythonDictonary(self):
        dictionary = {}

        dictionary['coordinates'] = self.coordinates.tolist()

        if self.reverse is True:
            dictionary['reverse'] = True

        if self._label.strip() != "":
            dictionary['label'] = self._label

        return dictionary

### ------------- Public Methods ------------------ ###

    def __str__(self):
        dictionary = self._getPythonDictonary()
        return (json.dumps(dictionary, sort_keys=False, indent=2))
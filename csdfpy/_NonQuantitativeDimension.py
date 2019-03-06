
"""Grid-controlled variable classes."""

from __future__ import print_function, division
import numpy as np
from .unit import value_object_format
from ._utils import (
                    _assign_and_check_unit_consistency,
                    _check_and_assign_bool,
                    _check_quantity,
                    _check_value_object,
                    )

# =========================================================================== #
#                Non quantitative Controlled Variable Dimension               #
# =========================================================================== #

class _NonQuantitativeDimension:

    __slots__ = [
        '_sampling_type',
        '_non_quantitative',
        '_number_of_points',
        '_coordinates',
        '_values',
        '_reverse',
        '_label'
    ]

    def __init__(
            self,
            _values,
            _sampling_type='grid',
            _non_quantitative=True,
            _reverse=False,
            _label=''):

        self.set_attribute('_sampling_type', _sampling_type)
        self.set_attribute('_non_quantitative', _non_quantitative)

        self.set_attribute('_number_of_points', len(_values))

# reverse
        _value = _check_and_assign_bool(_reverse)
        self.set_attribute('_reverse', _value)

# label
        self.set_attribute('_label', _label)
        self._get_coordinates(_values)

# --------------------------------------------------------------------------- #
#                                Class Methods                                #
# --------------------------------------------------------------------------- #

    def _get_coordinates(self, _values):
        _value = np.asarray(_values)
        self.set_attribute('_values', _value)
        self.set_attribute('_coordinates', _value)

    def set_attribute(self, name, value):
        super(_NonQuantitativeDimension, self).__setattr__(name, value)

    @classmethod
    def __delattr__(cls, name):
        if name in cls.__slots__:
            raise AttributeError(
                "Attribute '{0}' of class '{1}' cannot \
                be deleted.".format(name, cls.__name__)
            )

    def __setattr__(self, name, value):
        if name in self.__class__.__slots__:
            raise AttributeError(
                "Attribute '{0}' cannot be \
                modified.".format(name)
            )

        elif name in self.__class__.__dict__.keys():
            return self.set_attribute(name, value)

        else:
            raise AttributeError(
                "'{0}' object has no attribute \
                '{1}'.".format(self.__class__.__name__, name)
            )

    def _getparams(self):
        lst = [
            '_sampling_type',
            '_non_quantitative',
            '_values',
            '_reverse',
        ]
        return np.asarray([getattr(self, item) for item in lst])

    def _info(self):
        _response = [
            self.sampling_type,
            self._non_quantitative,
            self._number_of_points,
            self.reverse,
            str(self._label)
        ]
        return _response

    def _get_python_dictionary(self):
        dictionary = {}

        dictionary['values'] = self._values.tolist()
        dictionary['non_quantitative'] = True
        if self._reverse is True:
            dictionary['reverse'] = True

        if self._label.strip() != "":
            dictionary['label'] = self._label

        return dictionary

# --------------------------------------------------------------------------- #
#                               Class Attributes                              #
# --------------------------------------------------------------------------- #

# gcv type
    @property
    def variable_type(self):
        """Return a string specifying the grid-controlled variable type."""
        return "Non-quantitative grid controlled variable"

    @property
    def axis_label(self):
        return self.label

# coordinates
    @property
    def coordinates(self):
        """
        :Return type: ``numpy array`` of strings.

        The attribute returns the controlled variable coordinates
        along the dimension. The order of these coordinates
        depends on the value of the ``reverse`` attribute of the class.
        """
        coordinates = self._coordinates
        if self._reverse:
            coordinates = coordinates[::-1]
        return coordinates


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
#               Arbitrarily Sampled Controlled Variable Dimension             #
# =========================================================================== #

class _ArbitrarilySampledDimension:
    r"""
    An arbitrarily sampled grid controlled dimension.

    .. warning ::
        This class should not be used directly. Instead,
        use the ``CSDModel`` object to access the attributes
        and methods of this class. See example, :ref:`asgd`.

    This class returns an object which represents a physical
    controlled variable, sampled arbitrarily along a grid dimension.
    Let :math:`\mathbf{A}_k` be an ordered array of physical
    quantities, :math:`c_k` be the reference offset, and
    :math:`o_k` be the origin offset along the :math:`k^{th}`
    grid dimension, then the coordinates along this dimension
    are given as

    .. math ::
        \mathbf{X}_k^\mathrm{ref} = \mathbf{A}_k - c_k \mathbf{1},
    .. math ::
        \mathbf{X}_k^\mathrm{abs} = \mathbf{X}_k^\mathrm{ref} + o_k \mathbf{1},

    where :math:`\mathbf{X}_k^\mathrm{ref}` is an ordered array of the
    reference controlled variable coordinates,
    :math:`\mathbf{X}_k^\mathrm{abs}` is an ordered array of the absolute
    controlled variable coordinates, and
    :math:`\mathbf{1}` is an array of ones.
    """

    __slots__ = (
        '_sampling_type',
        '_non_quantitative',
        '_quantity',
        '_number_of_points',
        '_reference_offset',
        '_origin_offset',
        '_reverse',
        '_label',
        '_period',
        '_made_dimensionless',
        '_coordinates',
        '_values',
        '_equivalencies',

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

        '_type'
    )

    def __init__(
            self,
            _values,
            _reference_offset=None,
            _origin_offset=None,
            _quantity=None,
            _reverse=False,
            _label='',
            _period=None,
            _made_dimensionless=False,

            _sampling_type='grid',
            _non_quantitative=False,

            _reciprocal_reference_offset=None,
            _reciprocal_origin_offset=None,
            _reciprocal_quantity=None,
            _reciprocal_reverse=False,
            _reciprocal_label='',
            _reciprocal_period=None,
            _reciprocal_made_dimensionless=False):

        self.set_attribute('_sampling_type', _sampling_type)
        self.set_attribute('_non_quantitative', _non_quantitative)
        self.set_attribute('_type', 'non-linear')

        _unit = _assign_and_check_unit_consistency(_values[0], None).unit
        _reciprocal_unit = _unit**-1

        self.set_attribute('_unit', _unit)
        self.set_attribute('_reciprocal_unit', _reciprocal_unit)
        self.set_attribute('_dimensionless_unit', '')
        self.set_attribute('_reciprocal_dimensionless_unit', '')

# reference
        _value = _check_value_object(_reference_offset, _unit)
        self.set_attribute('_reference_offset', _value)
        _value = _check_value_object(_reciprocal_reference_offset,
                                     _reciprocal_unit)
        self.set_attribute('_reciprocal_reference_offset', _value)

# origin offset
        _value = _check_value_object(_origin_offset, _unit)
        self.set_attribute('_origin_offset', _value)
        _value = _check_value_object(_reciprocal_origin_offset,
                                     _reciprocal_unit)
        self.set_attribute('_reciprocal_origin_offset', _value)

# made dimensionless
        _value = _check_and_assign_bool(_made_dimensionless)
        self.set_attribute('_made_dimensionless', _value)
        _value = _check_and_assign_bool(_reciprocal_made_dimensionless)
        self.set_attribute('_reciprocal_made_dimensionless', _value)

# reverse
        _value = _check_and_assign_bool(_reverse)
        self.set_attribute('_reverse', _value)
        _value = _check_and_assign_bool(_reciprocal_reverse)
        self.set_attribute('_reciprocal_reverse', _value)

# period
        _value = _check_value_object(_period, _unit)
        if _value.value == 0.0:
            _value = np.inf*_value.unit
        self.set_attribute('_period', _value)
        _value = _check_value_object(_reciprocal_period, _reciprocal_unit)
        if _value.value == 0.0:
            _value = np.inf*_value.unit
        self.set_attribute('_reciprocal_period', _value)

# quantity
        _value = _check_quantity(_quantity, _unit)
        self.set_attribute('_quantity', _value)
        _value = _check_quantity(_reciprocal_quantity, _reciprocal_unit)
        self.set_attribute('_reciprocal_quantity', _value)

# label
        self.set_attribute('_label', _label)
        self.set_attribute('_reciprocal_label', _reciprocal_label)

# coordinates
        self._get_coordinates(_values)

# reciprocal coordinates
        self.set_attribute('_reciprocal_coordinates', None)

# --------------------------------------------------------------------------- #
#                                Class Methods                                #
# --------------------------------------------------------------------------- #

    def set_attribute(self, name, value):
        super(_ArbitrarilySampledDimension, self).__setattr__(name, value)

    @classmethod
    def __delattr__(cls, name):
        if name in cls.__slots__:
            raise AttributeError(
                "attribute '{0}' of class '{1}' cannot be \
                deleted.".format(name, cls.__name__)
            )

    def __setattr__(self, name, value):
        if name in self.__class__.__slots__:
            raise AttributeError(
                "attribute '{0}' cannot be modified".format(name)
            )

        elif name in self.__class__.__dict__.keys():
            return self.set_attribute(name, value)
        else:
            raise AttributeError(
                "'{0}' object has no attribute \
                '{1}'".format(self.__class__.__name__, name)
            )

    def _getparams(self):
        lst = [
            '_sampling_type',
            '_non_quantitative',
            '_quantity',
            '_number_of_points',
            '_reference_offset',
            '_origin_offset',
            '_reverse',
            '_period',
            '_values',

            '_reciprocal_quantity',
            '_reciprocal_number_of_points',
            '_reciprocal_origin_offset',
            '_reciprocal_reference_offset',
            '_reciprocal_reverse',
            '_reciprocal_period',
        ]
        return np.asarray([getattr(self, item) for item in lst])

    # def _info(self):
    #     _response = [
    #         self.sampling_type,
    #         self._non_quantitative,
    #         self._number_of_points,
    #         str(self.reference_offset),
    #         str(self.origin_offset),
    #         self.made_dimensionless,
    #         self.reverse,
    #         self.quantity,
    #         str(self._label),
    #         self.period
    #     ]
    #     return _response

    def _get_coordinates(self, values):
        _unit = self._unit
        _value = [_assign_and_check_unit_consistency(
            item, _unit).to(_unit).value for item in values]

        _value = np.asarray(_value, dtype=np.float64)*_unit
        self.set_attribute('_number_of_points', _value.size)
        self.set_attribute('_reciprocal_number_of_points',
                           self._number_of_points)

        self.set_attribute('_values', values)
        self.set_attribute('_coordinates', _value)

    def _get_python_dictionary(self):
        dictionary = {}
        dictionary['reciprocal'] = {}

        dictionary['values'] = self._values

        if self._reference_offset is not None \
                and self._reference_offset.value != 0:
            dictionary['reference_offset'] = value_object_format(
                self._reference_offset
            )

        if self._reciprocal_reference_offset is not None \
                and self._reciprocal_reference_offset.value != 0:
            dictionary['reciprocal']['reference_offset'] = value_object_format(
                self._reciprocal_reference_offset
            )

        if self._origin_offset is not None \
                and self._origin_offset.value != 0:
            dictionary['origin_offset'] = value_object_format(
                self._origin_offset
            )

        if self._reciprocal_origin_offset is not None \
                and self._reciprocal_origin_offset.value != 0:
            dictionary['reciprocal']['origin_offset'] = value_object_format(
                self._reciprocal_origin_offset
            )

        if self._reverse is True:
            dictionary['reverse'] = True

        if self._reciprocal_reverse is True:
            dictionary['reciprocal']['reverse'] = True

        if self._period.value not in [0.0, np.inf, None]:
            dictionary['period'] = value_object_format(self._period)

        if self._reciprocal_period.value not in [0.0, np.inf, None]:
            dictionary['reciprocal']['period'] = value_object_format(
                self._reciprocal_period
            )

        if self._quantity is not None:
            dictionary['quantity'] = self._quantity

        if self._reciprocal_quantity not in [None, "unknown", "dimensionless"]:
            dictionary['reciprocal']['quantity'] = self._reciprocal_quantity

        if self._label.strip() != "":
            dictionary['label'] = self._label

        if self._reciprocal_label.strip() != "":
            dictionary['reciprocal']['label'] = self._reciprocal_label

        if dictionary['reciprocal'] == {}:
            del dictionary['reciprocal']

        return dictionary

# --------------------------------------------------------------------------- #
#                               Class Attributes                              #
# --------------------------------------------------------------------------- #

# gcv type
    @property
    def variable_type(self):
        r"""Return a string specifying the grid-controlled variable type."""
        return "Arbitrarily sampled grid controlled variable"

    @property
    def unit(self):
        """
        Return the unit associated with the physical dimension.

        For example, a unit of "cm". This attribute cannot be updated.

        :Return type: ``string``
        """
        if self._made_dimensionless:
            unit = self._dimensionless_unit
        else:
            unit = self._unit
        return unit

    @property
    def reciprocal_unit(self):
        """
        Return the unit associated with the reciprocal grid dimension.

        For example, a unit a "cm^-1". This attribute cannot be updated.

        :Return type: ``string``
        """
        if self._reciprocal_made_dimensionless:
            unit = self._reciprocal_dimensionless_unit
        else:
            unit = self._reciprocal_unit
        return unit

# made dimensionless
    @property
    def made_dimensionless(self):
        return self._made_dimensionless

    @made_dimensionless.setter
    def made_dimensionless(self, value=False):
        if value:
            denominator = (self._origin_offset + self._reference_offset)
            if denominator.value == 0:
                raise ZeroDivisionError(
                    "Dimension cannot be made dimensionless \
                    with \n'origin_offset' {0} and \
                    'reference_offset' {1}. No changes were \
                    made.".format(self._origin_offset,
                                  self._reference_offset)
                )

        self.set_attribute('_made_dimensionless', value)

# reciprocal made dimensionless
    @property
    def reciprocal_made_dimensionless(self):
        return self._reciprocal_made_dimensionless

    @reciprocal_made_dimensionless.setter
    def reciprocal_made_dimensionless(self, value=False):
        if value:
            denominator = (self._reciprocal_origin_offset +
                           self._reciprocal_reference_offset)
            if denominator.value == 0:
                raise ZeroDivisionError(
                    "Dimension cannot be made dimensionless \
                    with \n'origin_offset' {0} and \
                    'reference_offset' {1}. No changes \
                    made.".format(self._origin_offset,
                                  self._reference_offset)
                )

        self.set_attribute('_reciprocal_made_dimensionless', value)

# coordinates
    @property
    def coordinates(self):
        r"""
        Control variable coordinates along the dimension.

        The ordered array, :math:`\mathbf{X}_k^\mathrm{ref}`,
        along the grid dimension. The order of these coordinates
        depends on the value of the ``reverse`` attributes of the class.

        :Return type: ``Quantity`` object
        """
        _value = 1.0
        coordinates = self._coordinates[:self._number_of_points]
        if self._made_dimensionless:
            _value = (self._origin_offset + self._reference_offset)
        coordinates = (coordinates/_value).to(self.unit)
        if self._reverse:
            coordinates = coordinates[::-1]
        return coordinates - self._reference_offset.to(self.unit)

# reciprocal_coordinates
    @property
    def reciprocal_coordinates(self):
        return self._reciprocal_coordinates

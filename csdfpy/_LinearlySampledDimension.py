
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
#                Linearly Sampled Controlled Variable Dimension               #
# =========================================================================== #

class _LinearlySampledDimension:
    r"""
    A linearly sampled grid controlled dimension.

    .. warning ::
        This class should not be used directly. Instead,
        use the ``CSDModel`` object to access the attributes
        and methods of this class. See example, :ref:`lsgd`.

    This class returns an object which represents a physical
    controlled variable, sampled linearly along a grid dimension.
    Let :math:`m_k` be the sampling interval, :math:`N_k \ge 1` be the
    number of points, :math:`c_k` be the reference offset, and
    :math:`o_k` be the origin offset along the :math:`k^{th}`
    grid dimension, then the coordinates along the
    grid dimension are given as

    .. math ::
        \mathbf{X}_k^\mathrm{ref} = [m_k j ]_{j=0}^{N_k-1} - c_k \mathbf{1},
    .. math ::
        \mathbf{X}_k^\mathrm{abs} = \mathbf{X}_k^\mathrm{ref} + o_k \mathbf{1},

    where :math:`\mathbf{X}_k^\mathrm{ref}` is an ordered array of the
    reference controlled variable coordinates,
    :math:`\mathbf{X}_k^\mathrm{abs}` is an ordered array of the absolute
    controlled variable coordinates, and :math:`\mathbf{1}`
    is an array of ones.
    """

    __slots__ = ('_sampling_type',
                 '_non_quantitative',
                 '_quantity',
                 '_number_of_points',
                 '_sampling_interval',
                 '_origin_offset',
                 '_reference_offset',
                 '_reverse',
                 '_label',
                 '_period',
                 '_fft_output_order',
                 '_made_dimensionless',
                 '_equivalencies',

                 '_reciprocal_quantity',
                 '_reciprocal_number_of_points',
                 '_reciprocal_sampling_interval',
                 '_reciprocal_origin_offset',
                 '_reciprocal_reference_offset',
                 '_reciprocal_reverse',
                 '_reciprocal_label',
                 '_reciprocal_period',
                 '_reciprocal_made_dimensionless',

                 '_coordinates',
                 '_reciprocal_coordinates',

                 '_unit',
                 '_dimensionless_unit',
                 '_reciprocal_unit',
                 '_reciprocal_dimensionless_unit',

                 '_string_type',
                 '_type')

    def __init__(self,
                 _number_of_points,
                 _sampling_interval,
                 _reference_offset=None,
                 _origin_offset=None,
                 _quantity=None,
                 _reverse=False,
                 _label='',
                 _period=None,
                 _fft_output_order=False,
                 _made_dimensionless=False,

                 _sampling_type="grid",
                 _non_quantitative=False,

                 _reciprocal_sampling_interval=None,
                 _reciprocal_reference_offset=None,
                 _reciprocal_origin_offset=None,
                 _reciprocal_quantity=None,
                 _reciprocal_reverse=False,
                 _reciprocal_label='',
                 _reciprocal_period=None,
                 _reciprocal_made_dimensionless=False):

        # self.set_attribute('_string_type', {})

        self.set_attribute('_sampling_type', _sampling_type)
        self.set_attribute('_non_quantitative', _non_quantitative)
        self.set_attribute('_type', 'linear')

        self.set_attribute('_number_of_points', _number_of_points)
        self.set_attribute('_reciprocal_number_of_points', _number_of_points)

        _value = _assign_and_check_unit_consistency(_sampling_interval, None)
        self.set_attribute('_sampling_interval', _value)
        # self._string_type['_sampling_interval'] = _sampling_interval

        _unit = self.sampling_interval.unit
        _reciprocal_unit = _unit**-1

        # Unit assignment
        self.set_attribute('_unit', _unit)
        self.set_attribute('_reciprocal_unit', _reciprocal_unit)
        self.set_attribute('_dimensionless_unit', '')
        self.set_attribute('_reciprocal_dimensionless_unit', '')

        # Inverse sampling interval is calculated assuming a Fourier inverse.
        if _reciprocal_sampling_interval is None:
            _value = (1/(_number_of_points*self.sampling_interval.value)
                      ) * _reciprocal_unit
        else:
            _value = _assign_and_check_unit_consistency(
                        _reciprocal_sampling_interval, _reciprocal_unit)
        self.set_attribute('_reciprocal_sampling_interval', _value)
        # self._string_type['_reciprocal_sampling_interval'] = \
        #     _reciprocal_sampling_interval

        # reference Offset
        _value = _check_value_object(_reference_offset, _unit)
        self.set_attribute('_reference_offset', _value)
        # self._string_type['_reference_offset'] = _reference_offset

        _value = _check_value_object(
                    _reciprocal_reference_offset, _reciprocal_unit)
        self.set_attribute('_reciprocal_reference_offset', _value)
        # self._string_type['_reciprocal_reference_offset'] = \
        #     _reciprocal_reference_offset

        # origin offset
        _value = _check_value_object(_origin_offset, _unit)
        self.set_attribute('_origin_offset', _value)
        # self._string_type['_origin_offset'] = _origin_offset

        _value = _check_value_object(
                    _reciprocal_origin_offset, _reciprocal_unit)
        self.set_attribute('_reciprocal_origin_offset', _value)
        # self._string_type['_reciprocal_origin_offset'] = \
        #     _reciprocal_origin_offset

        # made dimensionless, specific to NMR datasets
        _value = _check_and_assign_bool(_made_dimensionless)
        self.set_attribute('_made_dimensionless', _value)
        _value = _check_and_assign_bool(_reciprocal_made_dimensionless)
        self.set_attribute('_reciprocal_made_dimensionless', _value)

        # reverse
        _value = _check_and_assign_bool(_reverse)
        self.set_attribute('_reverse', _value)
        _value = _check_and_assign_bool(_reciprocal_reverse)
        self.set_attribute('_reciprocal_reverse', _value)

        # fft_ouput_order
        _value = _check_and_assign_bool(_fft_output_order)
        self.set_attribute('_fft_output_order', _value)

        # period
        _value = _check_value_object(_period, _unit)
        if _value.value == 0.0:
            _value = np.inf*_value.unit
        self.set_attribute('_period', _value)
        # self._string_type['_period'] = _period

        _value = _check_value_object(_reciprocal_period, _reciprocal_unit)
        if _value.value == 0.0:
            _value = np.inf*_value.unit
        self.set_attribute('_reciprocal_period', _value)
        # self._string_type['_reciprocal_period'] = _reciprocal_period

        # quantity
        _value = _check_quantity(_quantity, _unit)
        self.set_attribute('_quantity', _value)
        _value = _check_quantity(_reciprocal_quantity, _reciprocal_unit)
        self.set_attribute('_reciprocal_quantity', _value)

        # label
        self.set_attribute('_label', _label)
        self.set_attribute('_reciprocal_label', _reciprocal_label)

        # coordinates along the dimension
        self.set_attribute('_coordinates', None)
        self.set_attribute('_reciprocal_coordinates', None)
        self._get_coordinates()
        self._get_reciprocal_coordinates()

# --------------------------------------------------------------------------- #
#                                Class Methods                                #
# --------------------------------------------------------------------------- #

    def set_attribute(self, name, value):
        super(_LinearlySampledDimension, self).__setattr__(name, value)

    @classmethod
    def __delattr__(cls, name):
        if name in cls.__slots__:
            raise AttributeError("Attribute '{0}' of class '{1}' \
                cannot be deleted.".format(name, cls.__name__))

    def __setattr__(self, name, value):
        if name in self.__class__.__slots__:
            raise AttributeError("Attribute '{0}' cannot be \
                modified.".format(name))

        elif name in self.__class__.__dict__.keys():
            return self.set_attribute(name, value)

        else:
            raise AttributeError("'{0}' object has no \
                attribute '{1}'".format(self.__class__.__name__, name))

    def _getparams(self):
        lst = [
            '_sampling_type',
            '_non_quantitative',
            '_quantity',
            '_number_of_points',
            '_sampling_interval',
            '_origin_offset',
            '_reference_offset',
            '_reverse',
            '_period',
            '_fft_output_order',

            '_reciprocal_quantity',
            '_reciprocal_number_of_points',
            '_reciprocal_sampling_interval',
            '_reciprocal_origin_offset',
            '_reciprocal_reference_offset',
            '_reciprocal_reverse',
            '_reciprocal_period',
        ]
        return np.asarray([getattr(self, item) for item in lst])

    def _info(self):
        _response = [
            self._sampling_type,
            self._non_quantitative,
            self._number_of_points,
            str(self.sampling_interval),
            str(self._reference_offset),
            str(self._origin_offset),
            self.made_dimensionless,
            self._reverse,
            self._quantity,
            str(self._label),
            self._fft_output_order,
            self._period
        ]
        return _response

    def _get_coordinates(self):
        _unit = self._unit
        _number_of_points = self._number_of_points
        _sampling_interval = self.sampling_interval.to(_unit)

        _index = np.arange(_number_of_points, dtype=np.float64)

        if self._fft_output_order:
            # print('in fft output order')
            _index = np.empty(_number_of_points, dtype=np.int)
            n = (_number_of_points-1)//2 + 1
            p1 = np.arange(0, n, dtype=np.int)
            _index[:n] = p1
            p2 = np.arange(-(_number_of_points//2), 0, dtype=np.int)
            _index[n:] = p2

        _value = _index * _sampling_interval
        # print(_value)
        self.set_attribute('_coordinates', _value)

    def _get_reciprocal_coordinates(self):
        _unit = self._reciprocal_unit
        _number_of_points = self._number_of_points
        _sampling_interval = self.reciprocal_sampling_interval.to(_unit)

        _index = np.arange(_number_of_points, dtype=np.float64)

        # if not self._fft_output_order:
        #     if _number_of_points % 2 == 0:
        #         _index -= _number_of_points/2.0
        #     else:
        #         _index -= (_number_of_points-1)/2.0
        _value = _index * _sampling_interval

        self.set_attribute('_reciprocal_coordinates', _value)

    def _swap_values(self, a, b):
        temp = self.__getattribute__(a)
        self.set_attribute(a, self.__getattribute__(b))
        self.set_attribute(b, temp)
        temp = None
        del temp

    def _reciprocal(self):
        self._swap_values('_number_of_points', '_reciprocal_number_of_points')

        self._swap_values(
            '_sampling_interval', '_reciprocal_sampling_interval'
        )

        self._swap_values('_reference_offset', '_reciprocal_reference_offset')
        self._swap_values('_origin_offset', '_reciprocal_origin_offset')

        self._swap_values(
            '_made_dimensionless', '_reciprocal_made_dimensionless'
        )

        self._swap_values('_reverse', '_reciprocal_reverse')
        self._swap_values('_unit', '_reciprocal_unit')

        # if self._fft_output_order:
        #     self.set_attribute('_fft_output_order', False)
        # else:
        #     self.set_attribute('_fft_output_order', True)

        self._swap_values('_quantity', '_reciprocal_quantity')
        self._swap_values('_label', '_reciprocal_label')
        self._swap_values('_period', '_reciprocal_period')
        self._swap_values('_coordinates', '_reciprocal_coordinates')

    def _get_python_dictionary(self):
        dictionary = {}
        dictionary['reciprocal'] = {}
        dictionary['number_of_points'] = self._number_of_points

        dictionary['sampling_interval'] = value_object_format(
            self.sampling_interval
        )

        if self._reference_offset is not None \
                and self._reference_offset.value != 0.0:
            dictionary['reference_offset'] = value_object_format(
                self._reference_offset
            )

        if self._reciprocal_reference_offset is not None \
                and self._reciprocal_reference_offset.value != 0.0:
            dictionary['reciprocal']['reference_offset'] = value_object_format(
                self._reciprocal_reference_offset
            )

        if self._origin_offset is not None \
                and self._origin_offset.value != 0.0:
            dictionary['origin_offset'] = value_object_format(
                self._origin_offset
            )

        if self._reciprocal_origin_offset is not None \
                and self._reciprocal_origin_offset.value != 0.0:
            dictionary['reciprocal']['origin_offset'] = value_object_format(
                self._reciprocal_origin_offset
            )

        if self._reverse is True:
            dictionary['reverse'] = True

        if self._reciprocal_reverse is True:
            dictionary['reciprocal']['reverse'] = True

        if self._fft_output_order is True:
            dictionary['fft_output_order'] = True

        if self._period.value not in [0.0, np.inf, None]:
            dictionary['period'] = value_object_format(self._period)

        if self._reciprocal_period.value not in [0.0, np.inf, None]:
            dictionary['reciprocal']['period'] = value_object_format(
                self._reciprocal_period
            )

        if self._quantity not in [None, "unknown", "dimensionless"]:
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
        return "Linearly sampled grid controlled variable"

    @property
    def unit(self):
        # """
        # Returns the unit associated with the physical dimension.
        # For example, a unit of "km/h". This attribute cannot be updated.

        # :Return type: ``string``
        # """
        if self._made_dimensionless:
            unit = self._dimensionless_unit
        else:
            unit = self._unit
        return unit

    @property
    def reciprocal_unit(self):
        # """
        # Returns the unit associated with the reciprocal grid dimension.
        # For example, a unit a "h/km". This attribute cannot be updated.

        # :Return type: ``string``
        # """
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
                    "Dimension cannot be made dimensionsless with \
'origin_offset' {0} and 'reference_offset' {1}. No changes made.".format(
                        self._origin_offset, self._reference_offset)
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
                raise ZeroDivisionError("Dimension cannot be made\
                    dimensionsless with 'origin_offset' {0} and \
                    'reference_offset' {1}. No changes made.".format(
                        self._origin_offset, self._reference_offset)
                )
        self.set_attribute('_reciprocal_made_dimensionless', value)

# sampling interval
    @property
    def sampling_interval(self):
        r"""
        Return sampling interval, :math:`m_k`, along the grid dimension.

        When assigning a value, the dimensionality of the value must be
        consistent with the dimensionality of the other
        members specifying the grid dimension. The numerical value
        associated with the sampling interval must be a positive real
        number. For example, a sampling_interval of "0.2 cm/s".

        .. note:: The sampling interval along a grid and the reciprocal
            grid dimension follow the Nyquist–Shannon sampling theorem.
            Thus, updating the ``sampling_interval`` will trigger an
            update on its reciprocal counterpart.

        :Return type: ``Quantity`` object
        :Assign type: ``string``
        """
        return self._sampling_interval

    @sampling_interval.setter
    def sampling_interval(self, value):
        _value = _assign_and_check_unit_consistency(value, self.unit)
        if _value.value < 0.0:
            raise ValueError(
                'The numerical value of the sampling interval \
                is a positive real number. A value of {0} is \
                provide.'.format(_value)
            )
        self.set_attribute('_sampling_interval', _value)

    # Reciprocal sampling interval is calculated assuming a Fourier inverse #
        self.set_attribute(
            '_reciprocal_sampling_interval',
            1.0/(_value*self._number_of_points)
        )
        # super(_LinearlySampledGridDimension, self).__setattr__(
        #     "_reciprocal_sampling_interval",
        #     1.0/(_value*self._number_of_points)
        #     )
        self._get_coordinates()

# reciprocal sampling interval
    @property
    def reciprocal_sampling_interval(self):
        r"""
        Return sampling interval along the reciprocal grid dimension.

        When assigning a value, the dimensionality of the value must be
        consistent with the dimensionality of the other members
        specifying the reciprocal grid dimension.
        For example, a reciprocal_sampling_interval of "0.5 s/m".

        :Return type: ``Quantity`` object
        :Assign type: ``string``
        """
        return self._reciprocal_sampling_interval

    @reciprocal_sampling_interval.setter
    def reciprocal_sampling_interval(self, value):
        _value = _assign_and_check_unit_consistency(
            value, self.reciprocal_unit)
        if _value.value < 0.0:
            raise ValueError(
                'The numerical value of the reciprocal\
                sampling interval is a positive real\
                number. A value of {0} is provide.\
                '.format(_value)
            )
        self.set_attribute('_reciprocal_sampling_interval', _value)

        # Sampling interval is calculated assuming a Fourier inverse #
        self.set_attribute(
            'sampling_interval', 1.0/(_value*self._number_of_points)
        )
        # super(_LinearlySampledGridDimension, self).__setattr__(
        #     "sampling_interval", 1.0/(_value*self._number_of_points))
        # # self.sampling_interval = 1/(_value*self.number_of_points)
        self._get_reciprocal_coordinates()

# The following properties will control the order of the
# controlled variable coordinates

# coordinates
    @property
    def coordinates(self):
        r"""
        Coordinates along the dimension.

        The ordered array, :math:`\mathbf{X}_k^\mathrm{ref}`,
        along the grid dimension. The order of these coordinates
        depends on the value of the ``reverse`` and the
        ``fft_output_order`` attributes of the class.

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
        """
        Reciprocal coordinates along the dimension.

        An ordered array of controlled variable coordinates
        along the reciprocal grid dimension.
        The order of these coordinates
        depends on the value of the ``reciprocal_reverse``
        attributes of the class.

        :Return type: ``Quantity`` object
        """
        _value = 1.0
        reciprocal_coordinates = self._reciprocal_coordinates[
            :self._number_of_points]
        if self._reciprocal_made_dimensionless:
            _value = (self._reciprocal_origin_offset +
                      self._reciprocal_reference_offset)

            reciprocal_coordinates = (
                reciprocal_coordinates/_value
            ).to(self.reciprocal_unit)

        if self._reciprocal_reverse:
            reciprocal_coordinates = reciprocal_coordinates[::-1]

        return reciprocal_coordinates - self._reciprocal_reference_offset.to(
            self.reciprocal_unit
        )

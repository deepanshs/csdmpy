

from __future__ import print_function, division
from copy import deepcopy
import numpy as np

from numpy import inf

from .unit import (
    value_object_format,
    string_to_unit
)

from ._utils import (
    _assign_and_check_unit_consistency,
    _check_unit_consistency,
    _check_quantity,
    _check_value_object,
    _type_message,
    _check_and_assign_bool
)


# =========================================================================== #
#               		 QuantitativeVariable Class      				      #
# =========================================================================== #


class BaseIndependentVariable:

    __slots__ = (
        '_reference_offset',
        '_origin_offset',
        '_quantity',
        '_period',
        '_equivalencies',
        '_unit',
        '_reciprocal'
    )

    def __init__(
        self,
        _reference_offset=None,
        _origin_offset=None,
        _quantity=None,
        _period=None,
        _unit=None
    ):

        self._set_parameters(
            _reference_offset,
            _origin_offset,
            _quantity,
            _period,
            _unit)

    def _set_parameters(
            self,
            _reference_offset=None,
            _origin_offset=None,
            _quantity=None,
            _period=None,
            _unit=None):

        # unit
        self._unit = _unit

        # reference Offset
        _value = _check_value_object(_reference_offset, _unit)
        self._reference_offset = _value

        # origin offset
        _value = _check_value_object(_origin_offset, _unit)
        self._origin_offset = _value

        # period
        _value = _check_value_object(_period, _unit)
        if _value.value == 0.0:
            _value = np.inf*_value.unit
        self._period = _value

        # quantity
        _value = _check_quantity(_quantity, _unit)
        self._quantity = _value

# --------------------------------------------------------------------------- #
#                     QuantitativeVariable Attributes                         #
# --------------------------------------------------------------------------- #

# reference offset
    @property
    def reference_offset(self):
        r"""The reference offset, :math:`c_k`, along the dimension."""
        return deepcopy(self._reference_offset)

    @reference_offset.setter
    def reference_offset(self, value):
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))

        _value = _assign_and_check_unit_consistency(value, self._unit)
        self._reference_offset = _value

# origin offset
    @property
    def origin_offset(self):
        r"""The origin offset, :math:`o_k`, along the dimension."""
        return deepcopy(self._origin_offset)

    @origin_offset.setter
    def origin_offset(self, value):
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))

        _value = _assign_and_check_unit_consistency(value, self._unit)
        self._origin_offset = _value

# period
    @property
    def period(self):
        r"""The period of the independent variable."""
        return deepcopy(self._period)

    @period.setter
    def period(self, value=None):
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))

        lst = ['inf', 'Inf', 'infinity', 'Infinity', '∞']
        if value.strip().split()[0] in lst:
            value = inf*self._unit
            self._period = value
        else:
            self._period = _check_value_object(value, self._unit)

# Quantity
    @property
    def quantity(self):
        r"""The quantity name associated with the dimension."""
        return deepcopy(self._quantity)

    @quantity.setter
    def quantity(self, value):
        raise NotImplementedError('This attribute is not yet implemented.')

# --------------------------------------------------------------------------- #
#                       QuantitativeVariable Methods                          #
# --------------------------------------------------------------------------- #

    def _get_quantitative_dictionary(self):
        r"""Return the object as a python dictionary."""
        dictionary = {}

        if self._reference_offset.value != 0.0:
            dictionary['reference_offset'] = value_object_format(
                self._reference_offset
            )

        if self._origin_offset.value != 0.0:
            dictionary['origin_offset'] = value_object_format(
                self._origin_offset
            )

        if self._quantity not in [None, "unknown", "dimensionless"]:
            dictionary['quantity'] = self._quantity

        if self._period.value not in [0.0, np.inf]:
            dictionary['period'] = value_object_format(self._period)

        return dictionary

# is_quantitative
    def _is_quantitative(self):
        r"""
        Returns `True`, if the dimension is quantitative,
        otherwise `False`.

        :returns: A Boolean.
        """
        return True

# to()
    def _to(self, unit='', equivalencies=None):
        r"""Convert the unit to given value `unit`."""

        if not isinstance(unit, str):
            raise TypeError(_type_message(str, type(unit)))

        self._unit = _check_unit_consistency(
                1.0*string_to_unit(unit), self._unit
            ).unit

        self._equivalencies = equivalencies


# =========================================================================== #
#                      ReciprocalVariable Dimension Class                     #
# =========================================================================== #


class ReciprocalVariable(BaseIndependentVariable):

    __slots__ = (
        '_reverse',
        '_label',
    )

    def __init__(
            self,
            _reference_offset=None,
            _origin_offset=None,
            _quantity=None,
            _reverse=False,
            _label='',
            _period=None,
            _unit=None):

        self.reverse = _reverse
        self.label = _label

        self._set_parameters(
            _reference_offset,
            _origin_offset,
            _quantity,
            _period,
            _unit)

# --------------------------------------------------------------------------- #
#                                 Attributes                                  #
# --------------------------------------------------------------------------- #

# label
    @property
    def label(self):
        r"""The label associated with the dimension."""
        return deepcopy(self._label)

    @label.setter
    def label(self, label=''):
        if not isinstance(label, str):
            raise TypeError(_type_message(str, type(label)))
        self._label = label

# reverse
    @property
    def reverse(self):
        r"""The order of coordinates along the dimension."""
        return deepcopy(self._reverse)

    @reverse.setter
    def reverse(self, value=False):
        if not isinstance(value, bool):
            raise TypeError(_type_message(bool, type(value)))

        _value = _check_and_assign_bool(value)
        self._reverse = _value

    def _get_reciprocal_dictionary(self):
        dictionary = self._get_quantitative_dictionary()

        if self.reverse is True:
            dictionary['reverse'] = True

        if self.label.strip() != "":
            dictionary['label'] = self.label

        return dictionary


# =========================================================================== #
#                       LinearlySampledDimension Class                        #
# =========================================================================== #


class DimensionWithLinearSpacing(BaseIndependentVariable):
    r"""
    Create a linearly sampled dimension.

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

    __slots__ = (
        '_number_of_points',
        '_sampling_interval',
        '_fft_output_order',
        'reciprocal',
        '_reciprocal_number_of_points',
        '_reciprocal_sampling_interval',
        '_coordinates',
    )

    _type = 'linear_spacing'

    def __init__(
            self,
            _number_of_points,
            _sampling_interval,
            _reference_offset=None,
            _origin_offset=None,
            _quantity=None,
            _period=None,
            _fft_output_order=False,

            _reciprocal_reference_offset=None,
            _reciprocal_origin_offset=None,
            _reciprocal_quantity=None,
            _reciprocal_reverse=False,
            _reciprocal_label='',
            _reciprocal_period=None):

        # number of points
        self._number_of_points = _number_of_points

        # sampling interval
        _value = _assign_and_check_unit_consistency(_sampling_interval, None)
        self._sampling_interval = _value

        # fft_ouput_order
        _value = _check_and_assign_bool(_fft_output_order)
        self._fft_output_order = _value

        self._unit = self._sampling_interval.unit

        self._set_parameters(
            _reference_offset,
            _origin_offset,
            _quantity,
            _period,
            self._unit)

        # create a reciprocal dimension
        _reciprocal_unit = self._unit**-1
        self.reciprocal = ReciprocalVariable(
                                _reciprocal_reference_offset,
                                _reciprocal_origin_offset,
                                _reciprocal_quantity,
                                _reciprocal_reverse,
                                _reciprocal_label,
                                _reciprocal_period,
                                _reciprocal_unit
                            )

        # self.set_attribute('_reciprocal_coordinates', None)
        self._get_coordinates()
        # self._get_reciprocal_coordinates()

# --------------------------------------------------------------------------- #
#                    LinearlySampledDimension Methods                         #
# --------------------------------------------------------------------------- #

    def _get_coordinates(self):
        _unit = self._unit
        _number_of_points = self._number_of_points
        _sampling_interval = self._sampling_interval.to(_unit)

        _index = np.arange(_number_of_points, dtype=np.float64)

        if self._fft_output_order:
            _index = np.empty(_number_of_points, dtype=np.int)
            n = (_number_of_points-1)//2 + 1
            p1 = np.arange(0, n, dtype=np.int)
            _index[:n] = p1
            p2 = np.arange(-(_number_of_points//2), 0, dtype=np.int)
            _index[n:] = p2

        _value = _index * _sampling_interval
        self._coordinates = _value

# _get_python_dictionary()
    def _get_python_dictionary(self):
        dictionary = {}
        dictionary['type'] = self.__class__._type
        dictionary['number_of_points'] = self._number_of_points
        dictionary['sampling_interval'] = value_object_format(
            self.sampling_interval
        )

        dictionary.update(self._get_quantitative_dictionary())

        if self.fft_output_order is True:
            dictionary['fft_output_order'] = True

        reciprocal_dictionary = self.reciprocal._get_reciprocal_dictionary()

        if reciprocal_dictionary == {}:
            del reciprocal_dictionary
        else:
            dictionary['reciprocal'] = reciprocal_dictionary

        return dictionary

# --------------------------------------------------------------------------- #
#                   LinearlySampledDimension Attributes                       #
# --------------------------------------------------------------------------- #

# number_of_points
    @property
    def number_of_points(self):
        r"""The number of points along the dimension."""
        return deepcopy(self._number_of_points)

# sampling interval
    @property
    def sampling_interval(self):
        r"""The sampling interval, :math:`m_k`, along the dimension."""
        return deepcopy(self._sampling_interval)

    @sampling_interval.setter
    def sampling_interval(self, value):
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))
        _value = _assign_and_check_unit_consistency(value, self._unit)
        if _value.value < 0.0:
            raise ValueError(
                'The numerical value of the sampling interval \
                is a positive real number. A value of {0} is \
                provide.'.format(_value)
            )
        self._sampling_interval = _value
        self._get_coordinates()

# fft_ouput_order
    @property
    def fft_output_order(self):
        r"""The coordinates are ordered according to the fft output order."""
        return deepcopy(self._fft_output_order)

    @fft_output_order.setter
    def fft_output_order(self, value):
        if not isinstance(value, bool):
            raise TypeError(_type_message(bool, type(value)))

        self._fft_output_order = value
        self._get_coordinates()
        return


# =========================================================================== #
#                     ArbitrarilySampledDimension Class                       #
# =========================================================================== #


class DimensionWithArbitrarySpacing(BaseIndependentVariable):
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
        '_unit',
        'reciprocal',
        '_number_of_points',
        '_values',
        '_coordinates'
    )

    _type = 'arbitrary_spacing'

    def __init__(
            self,
            _values,
            _reference_offset=None,
            _origin_offset=None,
            _quantity=None,
            _period=None,

            _reciprocal_reference_offset=None,
            _reciprocal_origin_offset=None,
            _reciprocal_quantity=None,
            _reciprocal_reverse=False,
            _reciprocal_label='',
            _reciprocal_period=None):

        # unit
        self._unit = _assign_and_check_unit_consistency(_values[0], None).unit

        self._set_parameters(
            _reference_offset,
            _origin_offset,
            _quantity,
            _period,
            self._unit)

        # reciprocal dimension attributes
        _reciprocal_unit = self._unit**-1
        self.reciprocal = ReciprocalVariable(
                            _reciprocal_reference_offset,
                            _reciprocal_origin_offset,
                            _reciprocal_quantity,
                            _reciprocal_reverse,
                            _reciprocal_label,
                            _reciprocal_period,
                            _reciprocal_unit
                        )

        # coordinates
        self._get_coordinates(_values)

# --------------------------------------------------------------------------- #
#                  ArbitrarilySampledDimension Methods                        #
# --------------------------------------------------------------------------- #

    def _get_coordinates(self, values):
        _unit = self._unit
        _value = [_assign_and_check_unit_consistency(
            item, _unit).to(_unit).value for item in values]

        _value = np.asarray(_value, dtype=np.float64)*_unit

        self._number_of_points = _value.size
        self._values = values
        self._coordinates = _value

    def _get_python_dictionary(self):

        dictionary = {}
        dictionary['type'] = self.__class__._type
        dictionary['values'] = self._values

        dictionary.update(self._get_quantitative_dictionary())
        reciprocal_dictionary = self.reciprocal._get_quantitative_dictionary()

        if reciprocal_dictionary == {}:
            del reciprocal_dictionary
        else:
            dictionary['reciprocal'] = reciprocal_dictionary

        return dictionary

# --------------------------------------------------------------------------- #
#                  ArbitrarilySampledDimension Attributes                     #
# --------------------------------------------------------------------------- #

# values
    @property
    def values(self):
        r"""Returns a list of values along the dimensoion."""
        return deepcopy(self._values)

    @values.setter
    def values(self, array):
        self._get_coordinates(array)


# =========================================================================== #
#                           LabeledDimension Class                            #
# =========================================================================== #


class DimensionWithLabels:

    __slots__ = (
        '_number_of_points',
        '_coordinates',
        '_values',
    )

    _type = 'labeled'

    def __init__(self, _values):

        self._get_coordinates(_values)

# --------------------------------------------------------------------------- #
#                          LabeledDimension Methods                           #
# --------------------------------------------------------------------------- #

    def _get_coordinates(self, _values):
        self._coordinates = np.asarray(_values)
        self._values = _values
        self._number_of_points = len(_values)

# is_quantitative
    def _is_quantitative(self):
        r"""
        Returns `True`, if the dimension is quantitative,
        otherwise `False`.

        :returns: A Boolean.
        """
        return False

    def _get_python_dictionary(self):
        dictionary = {}

        dictionary['type'] = self._type
        dictionary['values'] = self._coordinates.tolist()

        return dictionary

# --------------------------------------------------------------------------- #
#                        LabeledDimension Attributes                          #
# --------------------------------------------------------------------------- #

# values
    @property
    def values(self):
        r"""Returns a list of values along the dimensoion."""
        return deepcopy(self._values)

    @values.setter
    def values(self, _values):
        self._get_coordinates(_values)

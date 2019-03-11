
"""The base ControlledVariable object: attributes and methods."""

from ._independent_variables import (
    DimensionWithLinearSpacing,
    DimensionWithArbitrarySpacing,
    DimensionWithLabels
)

import json
import warnings
from copy import deepcopy

from ._utils import (
    _get_dictionary,
    _type_message,
    _check_and_assign_bool,
    _axis_label
)

_dimension_generators = ['linearly_sampled']


def _check_quantitative(dictionary):
    if not _check_non_quantitative(dictionary):
        if dictionary['number_of_points'] is None and \
                dictionary['sampling_interval'] is None and \
                dictionary['values'] is None:
            raise Exception("either 'number_of_points, sampling_interval' \
or 'values' key is required.")
        return True
    return False


def _check_quantitative_linear(dictionary):
    if _check_quantitative(dictionary) and \
            dictionary['number_of_points'] is not None and \
            dictionary['sampling_interval'] is not None:
        return True
    return False


def _check_quantitative_arbitrary(dictionary):
    if _check_quantitative(dictionary) and \
            dictionary['values'] is not None:
        return True
    return False


def _check_non_quantitative(dictionary):
    is_false = False
    if dictionary['non_quantitative']:
        is_false = True
        if dictionary['values'] is None:
            raise Exception("'values' key is required for \
non-quantitative dimension.")
    return is_false


class IndependentVariable:
    r"""
    The base IndependentVariable class.

    This class returns an object which represents a independent variable.
    There are three types of independent variables based on the three types
    of dimensions: LinearlySampledDimension, ArbitrarilySampledDimension, and
    LabeledDimension, respectively.

    **A linearly sampled independent variable**

    Let :math:`m_k` be the sampling interval, :math:`N_k \ge 1` be the
    number of points, :math:`c_k` be the reference offset, and
    :math:`o_k` be the origin offset along the :math:`k^{th}`
    grid dimension, then the corresponding coordinates along the
    dimension are given as,

    .. math ::
        \begin{align}
        \mathbf{X}_k &= [m_k j ]_{j=0}^{N_k-1} - c_k \mathbf{1}, \\
        \mathbf{X}_k^\mathrm{abs} &= \mathbf{X}_k + o_k \mathbf{1}.
        \end{align}
        :label: eq_linear_gcv

    Here :math:`\mathbf{X}_k` and :math:`\mathbf{X}_k^\mathrm{abs}` are the
    ordered arrays of the reference and absolute independent variable
    coordinates, respectively, and :math:`\mathbf{1}` is an array of ones.

    **An arbitrarily sampled independent variable**

    Let :math:`\mathbf{A}_k` be an ordered array of ascending
    quantities, :math:`c_k` be the reference offset, and
    :math:`o_k` be the origin offset along the :math:`k^{th}`
    grid dimension, then the coordinates along this dimension
    are given as,

    .. math ::
        \begin{align}
        \mathbf{X}_k = \mathbf{A}_k - c_k \mathbf{1},\\
        \mathbf{X}_k^\mathrm{abs} = \mathbf{X}_k + o_k \mathbf{1},
        \end{align}

    where :math:`\mathbf{X}_k`, :math:`\mathbf{X}_k^\mathrm{abs}`,
    and :math:`\mathbf{1}` are the same as described in :eq:`eq_linear_gcv`.


    **A labeled independent variable**

    For labeled dimensions, the coordinates along the dimension are given as

    .. math ::
        \mathbf{X}_k = \mathbf{A}_k.

    where :math:`\mathbf{A}_k` is an array of labeled entities

    **Creating a new independent variable.**

    There are two ways to create a new independent variable using this class,
    both of which return an instance of the IndependentVariable class.

    `From a python dictionary containing valid keywords.`

    .. doctest::

        >>> from csdfpy import IndependentVariable
        >>> py_dictionary = {
        ...     'type': 'linearly_sampled',
        ...     'sampling_interval': '5 G',
        ...     'number_of_points': 10,
        ...     'reference_offset': '-10 mT',
        ...     'origin_offset': '10 T'
        ... }
        >>> x = IndependentVariable(py_dictionary)

    `From valid keyword arguaments.`

    .. doctest::

        >>> x = IndependentVariable(type = 'linearly_sampled',
        ...                         sampling_interval = '5 G',
        ...                         number_of_points = 10,
        ...                         reference_offset = '-10 mT',
        ...                         origin_offset = '10 T')

    """

    __slots__ = (
        'subtype',
        '_label',
        '_reverse'
    )

    # def __new__(cls, *args, **kwargs):
    #     """Create a new instance of ControlVariable object."""
    #     # if args != () and isinstance(args[0], ControlledVariable):
    #     #     print('inside __new__. arg')
    #     #     return args[0]
    #     # else:
    #     instance = super(ControlledVariable, cls).__new__(cls)
    #     # instance.__init__(*args, **kwargs)
    #     return instance

    def __init__(self, *args, **kwargs):
        """Initialize an instance of ControlVariable object."""
        dictionary = {
            'type': '',
            'number_of_points': None,
            'sampling_interval': None,
            'values': None,
            'reference_offset': None,
            'origin_offset': None,
            'reverse': False,
            'fft_output_order': False,
            'period': None,
            'quantity': None,
            'label': '',
            'reciprocal': {
                'sampling_interval': None,
                'reference_offset': None,
                'origin_offset': None,
                'reverse': False,
                'period': None,
                'quantity': None,
                'label': ''}
        }

        default_keys = dictionary.keys()
        input_dict = _get_dictionary(*args, **kwargs)
        input_keys = input_dict.keys()

        if 'reciprocal' in input_keys:
            input_subkeys = input_dict['reciprocal'].keys()
        for key in input_keys:
            if key in default_keys:
                if key == 'reciprocal':
                    for subkey in input_subkeys:
                        dictionary[key][subkey] = input_dict[key][subkey]
                else:
                    dictionary[key] = input_dict[key]

        _valid_types = ['arbitrarily_sampled', 'linearly_sampled', 'labeled']

        if dictionary['type'] not in _valid_types:
            raise ValueError((
                "'{0}' is an invalid value for the dimension type. The "
                "allowed values are 'arbitrarily_sampled', 'linearly_sampled' "
                "and 'labeled'.".format(dictionary['type'])
            ))

        if dictionary['type'] == 'labeled':
            _independent_variable_object = DimensionWithLabels(
                    _values=dictionary['values'],
                    # _reverse=dictionary['reverse'],
                    # _label=dictionary['label']
                    )

        if dictionary['type'] == 'arbitrarily_sampled':
            _independent_variable_object = DimensionWithArbitrarySpacing(
                _values=dictionary['values'],
                _reference_offset=dictionary['reference_offset'],
                _origin_offset=dictionary['origin_offset'],
                _quantity=dictionary['quantity'],
                # _reverse=dictionary['reverse'],
                # _label=dictionary['label'],
                _period=dictionary['period'],

                _reciprocal_reference_offset=dictionary['reciprocal']
                                                       ['reference_offset'],
                _reciprocal_origin_offset=dictionary['reciprocal']
                                                    ['origin_offset'],
                _reciprocal_quantity=dictionary['reciprocal']['quantity'],
                _reciprocal_reverse=dictionary['reciprocal']['reverse'],
                _reciprocal_period=dictionary['reciprocal']['period'],
                _reciprocal_label=dictionary['reciprocal']['label'])

        if dictionary['type'] == 'linearly_sampled':
            _independent_variable_object = DimensionWithLinearSpacing(
                _number_of_points=dictionary['number_of_points'],
                _sampling_interval=dictionary['sampling_interval'],
                _reference_offset=dictionary['reference_offset'],
                _origin_offset=dictionary['origin_offset'],
                _quantity=dictionary['quantity'],
                # _reverse=dictionary['reverse'],
                # _label=dictionary['label'],
                _period=dictionary['period'],
                _fft_output_order=dictionary['fft_output_order'],

                _reciprocal_reference_offset=dictionary['reciprocal']
                                                       ['reference_offset'],
                _reciprocal_origin_offset=dictionary['reciprocal']
                                                    ['origin_offset'],
                _reciprocal_quantity=dictionary['reciprocal']['quantity'],
                _reciprocal_reverse=dictionary['reciprocal']['reverse'],
                _reciprocal_period=dictionary['reciprocal']['period'],
                _reciprocal_label=dictionary['reciprocal']['label'])

        self.subtype = _independent_variable_object
        self.reverse = dictionary['reverse']
        self.label = dictionary['label']

# --------------------------------------------------------------------------- #
#                          IndependentVariable Attributes                     #
# --------------------------------------------------------------------------- #

# reciprocal
    @property
    def reciprocal(self):
        return self.subtype.reciprocal

# dimension type
    @property
    def dimension_type(self):
        r"""
        Returns the dimension type of the independent variable.

        There are three types of independent variables base on the types of
        dimensions, LinearlySampledDimension and ArbitrarilySampledDimension
        and LabeledDimension.
        This attribute cannot be modified.

        .. doctest::

            >>> print(x.dimension_type)
            linearly_sampled

        In the above example, ``x`` is an instance of the IndependentVariable
        class associated with a linearly sampled independent variable.

        :returns: A string.
        :raises AttributeError: When the attribute is modified.
        """
        return self.subtype.__class__._type

#           Attributes defining the control variable sampling type            #
# --------------------------------------------------------------------------- #

# # Sampling type #
#     @property
#     def sampling_type(self):
#         r"""
#         Return sampling type of the controlled variable.

#         This attribute cannot be modified. ::

#             >>> print(x.sampling_type)
#             grid

#         :returns: A string.
#         :raises AttributeError: When the attribute is modified.
#         """
#         return deepcopy(self.subtype._sampling_type)

# =========================================================================== #
#                             Derived Attributes                              #
# =========================================================================== #

# coordinates #
    @property
    def coordinates(self):
        r"""
        Return an array of reference coordinates, :math:`\mathbf{X}_k`, along the dimension.

        The order of these coordinates
        depends on the value of the ``reverse`` and the ``fft_output_order``
        (only applicable when sampling is linear along the dimension)
        attributes of the class. This attribute cannot be modified.

        .. doctest::

            >>> print(x.coordinates)
            [100. 105. 110. 115. 120. 125. 130. 135. 140. 145.] G

        :returns: A ``Quantity array`` when the controlled variable is
                  quantitative.
        :returns: A ``Numpy array`` when the controlled variable is
                  non-quantitative.
        :raises AttributeError: When the attribute is modified.
        """

        coordinates = self.subtype._coordinates[:self.subtype._number_of_points]
        if self._reverse:
            coordinates = coordinates[::-1]
        if self.subtype == 'labeled':
            return coordinates
        else:
            return (coordinates - self.reference_offset).to(self.subtype._unit)

# absolute_coordinates
    @property
    def absolute_coordinates(self):
        r"""
        Return an array of absolute coordinates, :math:`\mathbf{X}_k^\mathrm{abs}`, along the dimension.

        This attribute is
        only `valid` for the quantitative controlled variables. The order of
        these coordinates depends on the value of the ``reverse`` and the
        ``fft_output_order`` (only applicable when sampling is linear along
        the dimension) attributes of the class. This attribute cannot be
        modified.

        .. doctest::

            >>> print(x.origin_offset)
            10.0 T
            >>> print(x.absolute_coordinates)
            [100100. 100105. 100110. 100115. 100120. 100125. 100130. 100135. 100140.
             100145.] G

        In the above example, the absolute coordinate is ``coordinates
        + origin_offset``.

        :returns: A ``Quantity array`` when the controlled
                  variable is quantitative.
        :raises AttributeError: For labeled dimension.
        :raises AttributeError: When the attribute is modified.
        """
        if self.subtype != 'labeled':
            return (self.coordinates + self.origin_offset).to(self.subtype._unit)
        else:
            raise AttributeError((
                "{0} has no attribute '{1}'.".format(
                    self.subtype.__class__.__name__, 'absolute_coordinates')
            ))
        # return self.subtype.absolute_coordinates
        # if self.variable_type in _quantitative_variable_types:
        #     return self.subtype.coordinates + \
        #         self.subtype._origin_offset.to(self.subtype.unit)

        # raise AttributeError(_attribute_message(self.variable_type,
        #                                         'absolute_coordinates'))

# # reciprocal_coordinates
#     @property
#     def reciprocal_coordinates(self):
#         r"""
#         Return an array of coordinates, :math:`\mathbf{X_r}_k^\mathrm{abs}`, along the reciprocal dimension.

#         This attribute is
#         only `valid` for the quantitative controlled variabes. The order of
#         these coordinates depends on the value of the ``reciprocal_reverse``
#         attributes of the class. This attribute cannot be modified.

#         :returns: A ``Quantity`` object when the controlled
#                   variable is quantitative.
#         :raises AttributeError: For non-quantitative controlled variables.
#         :raises AttributeError: When the attribute is modified.
#         """
#         if self.variable_type in _quantitative_variable_types[0]:
#             return self.subtype.reciprocal_coordinates

#         raise AttributeError(_attribute_message(self.variable_type,
#                                                 'reciprocal_coordinates'))

# # reciprocal_absolute_coordinates
#     @property
#     def reciprocal_absolute_coordinates(self):
#         r"""
#         Return an array of absolute coordinates, :math:`\mathbf{X_r}_k^\mathrm{abs}`, along the reciprocal dimension.

#         This attribute is only `valid` for the quantitative controlled
#         variabes. The order of these coordinates depends on the value of the
#         ``reciprocal_reverse`` attributes of the class. This attribute cannot
#         be modified.

#         :returns: A ``Quantity`` object when the controlled
#                   variable is quantitative.
#         :raises AttributeError: For non-quantitative controlled variables.
#         :raises AttributeError: When the attribute is modified.
#         """
#         return self.subtype.reciprocal_coordinates + \
#             self.subtype._reciprocal_origin_offset.to(self.subtype.reciprocal_unit)

# =========================================================================== #
#           Attributes affecting the controlled variable coordinates          #
# =========================================================================== #

# reference offset
    @property
    def reference_offset(self):
        r"""
        Return the reference offset, :math:`c_k`, along the dimension.

        The attribute is only `valid` for quantitative
        dimensions. When assigning a value, the dimensionality of the value
        must be consistent with the dimensionality of the other members
        specifying the dimension. The value is assigned with a string
        containing the reference offset,
        for example,

        .. doctest::

            >>> print(x.reference_offset)
            -10.0 mT
            >>> x.reference_offset = "0 T"
            >>> print(x.coordinates)
            [0.  0.1 0.2 0.3 0.4] G

        :returns: A ``Quantity`` object with the reference offset.
        :raises AttributeError: For non-quantitative controlled variables.
        :raises TypeError: When the assigned value is not a string.
        """
        return self.subtype.reference_offset
        # if self.variable_type in _quantitative_variable_types:
        #     return deepcopy(self.subtype._reference_offset)

        # raise AttributeError(_attribute_message(self.variable_type,
        #                                         'reference_offset'))

    @reference_offset.setter
    def reference_offset(self, value):
        self.subtype.reference_offset = value

        # if self.variable_type in _quantitative_variable_types:
        #     if not isinstance(value, str):
        #         raise TypeError(_type_message(str, type(value)))

        #     _value = _assign_and_check_unit_consistency(
        #         value, self.subtype.unit
        #     )
        #     self.subtype.set_attribute('_reference_offset', _value)
        #     return

        # raise AttributeError(_attribute_message(self.variable_type,
        #                                         'reference_offset'))

# # reciprocal reference offset
#     @property
#     def reciprocal_reference_offset(self):
#         r"""
#         Return the reference offset along the reciprocal dimension.

#         This attribute is only `valid` for the quantitative
#         dimensions. When assigning a value, the dimensionality of the value
#         must be consistent with the dimensionality of other members
#         specifying the reciprocal dimension. The value is assigned with a
#         string containing the reference offset of the reciprocal
#         dimension, for example, ::

#             >>> print(x.reciprocal_reference_offset)
#             0.0 1 / G
#             >>> x.reciprocal_reference_offset = "5 (1/T)"

#         :returns: A ``Quantity`` object with the reference offset
#                   of the reciprocal dimension.
#         :raises TypeError: When the assigned value is not a string.
#         """
#         if self.variable_type in _quantitative_variable_types:
#             return deepcopy(self.subtype._reciprocal_reference_offset)

#         raise AttributeError(
#             _attribute_message(
#                 self.variable_type, 'reciprocal_reference_offset')
#         )

#     @reciprocal_reference_offset.setter
#     def reciprocal_reference_offset(self, value):
#         if self.variable_type in _quantitative_variable_types:
#             if not isinstance(value, str):
#                 raise TypeError(_type_message(str, type(value)))

#             _value = _assign_and_check_unit_consistency(
#                 value, self.subtype.reciprocal_unit)
#             self.subtype.set_attribute('_reciprocal_reference_offset', _value)
#             return

#         raise AttributeError(
#             _attribute_message(
#                 self.variable_type, 'reciprocal_reference_offset')
#         )
# # --------------------------------------------------------------------------- #

# origin offset
    @property
    def origin_offset(self):
        r"""
        Return the origin offset, :math:`o_k`, along the dimension.

        The attribute is only `valid` for quantitative
        dimensions. When assigning a value, the dimensionality of the value
        must be consistent with the dimensionality of other members specifying
        the dimension. The value is assigned with a string containing the
        origin offset, for example,

        .. doctest::

            >>> print(x.origin_offset)
            10.0 T
            >>> x.origin_offset = "1e5 G"
            >>> print(x.absolute_coordinates)
            [100000.  100000.1 100000.2 100000.3 100000.4] G

        :returns: A ``Quantity`` object with the origin offset.
        :raises AttributeError: For non-quantitative controlled variables.
        :raises TypeError: When the assigned value is not a string.
        """
        return self.subtype.origin_offset
        # if self.variable_type in _quantitative_variable_types:
        #     return deepcopy(self.subtype._origin_offset)

        # raise AttributeError(_attribute_message(self.variable_type,
        #                                         'origin_offset'))

    @origin_offset.setter
    def origin_offset(self, value):
        self.subtype.origin_offset = value

        # if self.variable_type in _quantitative_variable_types:
        #     if not isinstance(value, str):
        #         raise TypeError(_type_message(str, type(value)))

        #     _value = _assign_and_check_unit_consistency(value, self.subtype.unit)
        #     self.subtype.set_attribute('_origin_offset', _value)
        #     return

        # raise AttributeError(_attribute_message(self.variable_type,
        #                                         'origin_offset'))

# # reciprocal origin offset
#     @property
#     def reciprocal_origin_offset(self):
#         r"""
#         Return the origin offset along the reciprocal dimension.

#         This attribute is only `valid` for the quantitative dimensions. When
#         assigning a value, the dimensionality of the value must be consistent
#         with the dimensionality of the other members specifying the reciprocal
#         dimension. The value is assigned with a string containing the origin
#         offset of the reciprocal dimension, for example, ::

#             >>> print(x.reciprocal_origin_offset)
#             0.0 1 / G
#             >>> x.reciprocal_origin_offset = "400 (1/µT)"

#         :returns: A ``Quantity`` object with the origin offset of
#                   the reciprocal dimension.
#         :raises AttributeError: For non-quantitative controlled variables.
#         :raises TypeError: When the assigned value is not a string.
#         """
#         return self.subtype.reciprocal.origin_offset
#         # if self.variable_type in _quantitative_variable_types:
#         #     return deepcopy(self.subtype._reciprocal_origin_offset)

#         # raise AttributeError(_attribute_message(self.variable_type,
#         #                                         'reciprocal_origin_offset'))

#     @reciprocal_origin_offset.setter
#     def reciprocal_origin_offset(self, value):
#         if self.variable_type in _quantitative_variable_types:
#             if not isinstance(value, str):
#                 raise TypeError(_type_message(str, type(value)))

#             _value = _assign_and_check_unit_consistency(
#                 value, self.subtype.reciprocal_unit
#             )
#             self.subtype.set_attribute('_reciprocal_origin_offset', _value)
#             return

#         raise AttributeError(_attribute_message(self.variable_type,
#                                                 'reciprocal_origin_offset'))
# # --------------------------------------------------------------------------- #

# sampling interval
    @property
    def sampling_interval(self):
        r"""
        Return the sampling interval, :math:`m_k`, along the dimension.

        The attribute is only `valid` for instances with linearly sampled
        controlled-variable dimensions. When assigning a value,
        the dimensionality of the value must be consistent with the
        dimensionality of other members specifying the grid dimension.
        Additionally, the sampling interval must be a positive real number.
        The value is assigned with a string containing the sampling interval,
        for example,

        .. doctest::

            >>> print(x.sampling_interval)
            5.0 G
            >>> x.sampling_interval = "0.1 G"
            >>> print(x.coordinates)
            [100.  100.1 100.2 100.3 100.4] G

        Here, the original sampling interval, '5 G' is modified to
        '0.1 G'.

        .. note:: The sampling interval along a grid dimension and the
            respective reciprocal grid dimension follow the Nyquist–Shannon
            sampling theorem. Therefore, updating the ``sampling_interval``
            will automatically trigger an update on its reciprocal counterpart.

        :returns: A ``Quantity`` object with the sampling interval.
        :raises AttributeError: For non-quantitative and arbitrarily
                                sampled controlled variables.
        :raises TypeError: When the assigned value is not a string.
        """
        # if self.variable_type == _quantitative_variable_types[0]:
        return self.subtype.sampling_interval

        # raise AttributeError(_attribute_message(self.variable_type,
        #                                         'sampling_interval'))

    @sampling_interval.setter
    def sampling_interval(self, value):
        self.subtype.sampling_interval = value
        # if self.variable_type == _quantitative_variable_types[0]:
        #     if not isinstance(value, str):
        #         raise TypeError(_type_message(str, type(value)))
        #     self.subtype.sampling_interval = value
        #     return

        # raise AttributeError(_attribute_message(self.variable_type,
        #                                         'sampling_interval'))
# --------------------------------------------------------------------------- #

# number_of_points
    @property
    def number_of_points(self):
        r"""
        Return the number of points along the dimension.

        The number of points, :math:`N_k \ge 1`, along the controlled
        variable dimension. The attribute is updated with an
        integer specifying the number of points, for example

        .. doctest::

            >>> print(x.number_of_points)
            10
            >>> x.number_of_points = 5
            >>> print(x.coordinates)
            [100. 105. 110. 115. 120.] G

        :returns: An ``Integer`` with the number of points.
        :raises TypeError: When the assigned value is not an integer.
        """
        return deepcopy(self.subtype._number_of_points)

    @number_of_points.setter
    def number_of_points(self, value):
        # self.subtype.number_of_points = value
        if not isinstance(value, int):
            raise TypeError(_type_message(int, type(value)))

        if value <= 0:
            raise ValueError((
                "A positive integer value is required, given {0}."
                ).format(value)
            )

        if self.dimension_type not in _dimension_generators:
            if value > self.number_of_points:
                raise ValueError((
                    "Cannot set the number of points, {0}, more than the"
                    "number of independent variable coordinates, {1}."
                    ).format(value, self.number_of_points)
                )

            if value < self.number_of_points:
                warnings.warn((
                    "The number of independent variable coordinates, {0}"
                    " are truncated to {1}."
                    ).format(self.number_of_points, value)
                )
                self.subtype._number_of_points = value

        else:
            self.subtype._number_of_points = value
            self.subtype._get_coordinates()
# --------------------------------------------------------------------------- #

# values array
    @property
    def values(self):
        r"""
        An ordered array of values, :math:`\mathbf{A}_k`, along the independent variable dimension.

        For dimensions with arbitrarily spaced coordinates, this array is
        an ascending order of physical quantities.

        .. doctest::

            >>> x1 = IndependentVariable(type='arbitrarily_sampled', values=['cm'])
            >>> print(x1.data_structure)
            {
              "type": "arbitrarily_sampled",
              "values": [
                "cm"
              ],
              "quantity": "length",
              "reciprocal": {
                "quantity": "wavenumber"
              }
            }

            >>> x1.values = ['0cm', '4.1µm', '0.3mm', '5.8m', '32.4km']
            >>> print(x1.data_structure)
            {
              "type": "arbitrarily_sampled",
              "values": [
                "0cm",
                "4.1µm",
                "0.3mm",
                "5.8m",
                "32.4km"
              ],
              "quantity": "length",
              "reciprocal": {
                "quantity": "wavenumber"
              }
            }

            >>> x2 = IndependentVariable(type='labeled', values=[''])
            >>> x2.values = ['Cu', 'Ag', 'Au']
            >>> print(x2.data_structure)
            {
              "type": "labeled",
              "values": [
                "Cu",
                "Ag",
                "Au"
              ]
            }

        In the above examples, ``x1`` and ``x2`` are the instances of the
        :ref:`iv_api` class associated with the arbitrarily sampled
        and the non-quantitative controlled variable respectively.

        :returns: A ``Quantity array`` for arbitrarily sampled controlled
                        variables.
        :returns: A ``Numpy array`` for non-quantitative controlled variables.
        :raises AttributeError: For linearly sampled controlled variables.

        .. todo:
            raise type error if the values are not strings or numpy array
            of stings.
        """
        # if self.variable_type == _quantitative_variable_types[0]:
        #     raise AttributeError(_attribute_message(self.variable_type,
        #                                             'values'))

        return self.subtype.values

    @values.setter
    def values(self, array):
        # if self.variable_type == _quantitative_variable_types[0]:
        #     raise AttributeError(_attribute_message(self.variable_type,
        #                                             'values'))
        self.subtype.values = array
        self.subtype._get_coordinates(array)

# ===================================================================== #
# Attributes affecting the order of the controlled variable coordinates #
# ===================================================================== #

# fft_ouput_order
    @property
    def fft_output_order(self):
        r"""
        Return the coordinates along the dimension according to the fft order.

        A boolean specifying if the coordinates along the controlled
        variable dimension are ordered according to the output of a
        fast Fourier transform (FFT) routine. This attribute is only
        *valid* for linearly sampled controlled variable dimensions. The
        universal behavior of the FFT routine is to order the :math:`N_k`
        output amplitudes by placing the zero `frequency` at the start
        of the output array, with positive `frequencies` increasing in
        magnitude placed at increasing array offset until reaching
        :math:`\frac{N_k}{2} -1` if :math:`N_k` is even, otherwise
        :math:`\frac{N_k-1}{2}`, followed by negative frequencies
        decreasing in magnitude until reaching :math:`N_k-1`.
        This is also the ordering needed for the input of the inverse FFT.
        For example, consider

        .. math ::

            \mathbf{X}_k^\mathrm{ref} = [0, 1, 2, 3, 4, 5] \mathrm{~m/s}

        when the fft output order is false. When the fft output
        order is true, the order follows,

        .. math ::

            \mathbf{X}_k^\mathrm{ref} = [0 ,1, 2, -3, -2, -1] \mathrm{~m/s}

        The following is a test example.

        .. doctest::

            >>> test = IndependentVariable(type='linearly_sampled',
            ...														 sampling_interval = '1',
            ...                            number_of_points = 10)

            >>> print(test.coordinates)
            [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]
            >>> test.fft_output_order
            False

            >>> test.fft_output_order = True
            >>> print(test.coordinates)
            [ 0.  1.  2.  3.  4. -5. -4. -3. -2. -1.]

        :returns: A ``Boolean``.
        :raises TypeError: When the assigned value is not a boolean.
        """
        # if self.variable_type == _quantitative_variable_types[0]:
        return self.subtype.fft_output_order

        # raise AttributeError(_attribute_message(self.variable_type,
        #                                         'fft_output_order'))

    @fft_output_order.setter
    def fft_output_order(self, value):
        self.subtype.fft_output_order = value
        # if self.variable_type == _quantitative_variable_types[0]:
        #     if not isinstance(value, bool):
        #         raise TypeError(_type_message(bool, type(value)))

        #     # print('in fft output order')

        #     self.subtype.set_attribute('_fft_output_order', value)
        #     self.subtype._get_coordinates()
        #     return

        # raise AttributeError(_attribute_message(self.variable_type,
        #                                         'fft_output_order'))
# --------------------------------------------------------------------------- #

# reverse
    @property
    def reverse(self):
        r"""
        Return the coordinates along the dimension in the reverse order.

        The order in which the :math:`\mathbf{X}_k` and
        :math:`\mathbf{X}_k^\mathrm{abs}` coordinates map to the grid indices,
        :math:`\mathbf{G}_k = [0,1,2,...,N_k-1]`. For example, consider

        .. math ::

            \mathbf{X}_k^\mathrm{ref} = [0, 1, 2, 3,...N_{k-1}] \mathrm{~m/s},

        when the reverse is false. We the reverse is true, the mapping is

        .. math ::

            \mathbf{X}_k^\mathrm{ref} = [N_{k-1},...3, 2, 1, 0] \mathrm{~m/s}.

        .. doctest::

            >>> x.reverse
            False
            >>> print(x.coordinates)
            [0.  0.1 0.2 0.3 0.4] G
            >>> x.reverse = True
            >>> print(x.coordinates)
            [0.4 0.3 0.2 0.1 0. ] G

        :returns: A ``Boolean``.
        :raises TypeError: When the assigned value is not a boolean.
        """
        return deepcopy(self._reverse)

    @reverse.setter
    def reverse(self, value=False):
        if not isinstance(value, bool):
            raise TypeError(_type_message(bool, type(value)))

        _value = _check_and_assign_bool(value)
        self._reverse = _value

        # self.subtype.reverse = value
        # if not isinstance(value, bool):
        #     raise TypeError(_type_message(bool, type(value)))

        # _value = _check_and_assign_bool(value)
        # self.subtype.set_attribute('_reverse', _value)

# # reciprocal reverse
#     @property
#     def reciprocal_reverse(self):
#         r"""
#         Return the coordinates along the reciprocal dimension in reverse order.

#         The order in which the :math:`\mathbf{X_r}_k` and
#         :math:`\mathbf{X_r}_k^\mathrm{abs}` (for quantitative dimensions)
#         coordinates are mapped to the grid indices. Let, the grid
#         indices be :math:`[0,1,2,...,N_k-1]`, then when reverse
#         is false, the mapping follows,

#         .. math ::
#             \mathbf{X}_k^\mathrm{ref} = [0, 1, 2, 3, 4] \mathrm{~s/m}

#         and when reverse is false, then the mapping is

#         .. math ::
#             \mathbf{X}_k^\mathrm{ref} = [4, 3, 2, 1, 0] \mathrm{~s/m}

#         :returns: A ``boolean``.
#         :raises TypeError: When the assigned value is not a boolean.
#         """
#         return deepcopy(self.subtype._reciprocal_reverse)

#     @reciprocal_reverse.setter
#     def reciprocal_reverse(self, value=False):
#         if not isinstance(value, bool):
#             raise TypeError(_type_message(bool, type(value)))

#         _value = _check_and_assign_bool(value)
#         self.subtype.set_attribute('_reciprocal_reverse', _value)

# =========================================================================== #
#                            Additional Attributes                            #
# =========================================================================== #

# period
    @property
    def period(self):
        r"""
        Return the period of a quantitative controlled variable dimension.

        The default value of the period is infinity, i.e., the controlled
        variable dimension is non-periodic. The attribute is updated with a
        string containing a quantity which represents the period of the
        controlled variable. For example,

        .. doctest::

            >>> print(x.period)
            inf G
            >>> x.period = '1 T'

        To assign a dimension as non-periodic, one of the following may be
        used,

        .. doctest::

            >>> x.period = '1/0 T'
            >>> x.period = 'infinity µT'
            >>> x.period = '∞ G'

        :return: A ``Quantity`` object with the period of quantitative
            controlled variables.
        :raises AttributeError: For non-quantitative controlled variables.
        :raises TypeError: When the assigned value is not a string.
        """
        # if self.variable_type in _quantitative_variable_types:
        return self.subtype.period

        # raise AttributeError(_attribute_message(
        #                     self.variable_type, 'period'))

    @period.setter
    def period(self, value=None):
        self.subtype.period = value
        # if self.variable_type in _quantitative_variable_types:
        #     if not isinstance(value, str):
        #         raise TypeError(_type_message(str, type(value)))

        #     lst = ['inf', 'Inf', 'infinity', 'Infinity', '∞']
        #     if value.strip().split()[0] in lst:
        #         value = inf*self.subtype.unit
        #         self.subtype.set_attribute('_period', value)
        #     else:
        #         self.subtype.set_attribute(
        #             '_period', _check_value_object(
        #                 value, self.subtype.unit)
        #             )
        #     return
        # raise AttributeError(_attribute_message(
        #                     self.variable_type, 'period'))

# # reciprocal period
#     @property
#     def reciprocal_period(self):
#         r"""
#         Return the period of the reciprocal dimension.

#         The period of the reciprocal controlled variable along
#         the dimension, if any. The default value is infinity,
#         that is, the reciprocal dimension is considered non-periodic.
#         This attribute can be updated with a string containing
#         a physical quantity representing the period, for example,
#         the reciprocal_period of "0.1 h/km". A period of "1/0 h/km"
#         or "inf h/km" or "infinity h/km" will make the dimension
#         non-periodic.

#         :return: A ``Quantity`` object with physical quantity
#                  representing a period.
#         :raises AttributeError: For non-quantitative controlled variables.
#         :raises TypeError: When the assigned value is not a string.
#         """
#         if self.variable_type in _quantitative_variable_types:
#             return deepcopy(self.subtype._reciprocal_period)

#         raise AttributeError(_attribute_message(self.variable_type,
#                                                 'reciprocal_period'))

#     @reciprocal_period.setter
#     def reciprocal_period(self, value=True):
#         if self.variable_type in _quantitative_variable_types:
#             if not isinstance(value, str):
#                 raise TypeError(_type_message(str, type(value)))

#             lst = ['inf', 'Inf', 'infinity', 'Infinity', '∞']
#             if value.strip().split()[0] in lst:
#                 value = inf*self.subtype.reciprocal_unit
#                 self.subtype.set_attribute('_reciprocal_period', value)

#             else:
#                 self.subtype.set_attribute(
#                     '_reciprocal_period', _check_value_object(
#                         value, self.subtype.reciprocal_unit)
#                     )
#             return
#         raise AttributeError(_attribute_message(self.variable_type,
#                                                 'reciprocal_period'))
# # --------------------------------------------------------------------------- #

# Quantity
    @property
    def quantity(self):
        r"""
        Return the quantity name associated with the dimension.

        The attribute is only `valid` for the quantitative
        controlled variables.

        .. doctest::

            >>> print(x.quantity)
            magnetic flux density

        :returns: A string with the quantity name.
        :raises AttributeError: For non-quantitative controlled variables.
        :raises NotImplementedError: When assigning a value.
        """
        return self.subtype.quantity
        # if self.variable_type in _quantitative_variable_types:
        #     return deepcopy(self.subtype._quantity)

        # raise AttributeError(_attribute_message(self.variable_type,
        #                                         'quantity'))

    @quantity.setter
    def quantity(self, value):
        self.subtype.quantity = value
        # raise NotImplementedError('This attribute is not yet implemented.')

# # reciprocal Quantity
#     @property
#     def reciprocal_quantity(self):
#         r"""
#         Return the quantity name associated with the reciprocal dimension.

#         For example, the reciprocal quantity name, "inverse speed".
#         This value cannot be updated.

#         :returns: A string with the quantity name.
#         :raises AttributeError: For non-quantitative controlled variables.
#         """
#         # """
#         # When assigning a value, the
#         # quantity name must be consistent with the other
#         # physical quantities specifying the reciprocal
#         # grid dimension.
#         # """
#         if self.variable_type in _quantitative_variable_types:
#             return deepcopy(self.subtype._reciprocal_quantity)

#         raise AttributeError(_attribute_message(self.variable_type,
#                                                 'reciprocal_quantity'))

#     @reciprocal_quantity.setter
#     def reciprocal_quantity(self, value):
#         raise NotImplementedError('This attribute is not yet implemented.')

#     # @reciprocal_quantity.setter
#     # def reciprocal_quantity(self, string = ''):
#     #     ## To do: add a check for reciprocal quantity
#     #     self.set_attribute('_reciprocal_quantity', string)
# # --------------------------------------------------------------------------- #

# label
    @property
    def label(self):
        r"""
        Return the label associated with the dimension.

        The attribute is updated with a string containing the label, for
        example,

        .. doctest::

            >>> x.label
            ''
            >>> x.label = 'field strength'

        :returns: A ``String`` containing the label.
        :raises TypeError: When the assigned value is not a string.
        """
        return deepcopy(self._label)

    @label.setter
    def label(self, label=''):
        if not isinstance(label, str):
            raise TypeError(_type_message(str, type(label)))
        self._label = label

        # self.subtype.label = label
        # if not isinstance(label, str):
        #     raise TypeError(_type_message(str, type(label)))
        # self.subtype.set_attribute('_label', label)

# # reciprocal_label
#     @property
#     def reciprocal_label(self):
#         r"""
#         Return the label associated with the reciprocal dimension.

#         This attribute can be updated with a string
#         containing the label of the reciprocal dimension,
#         for example, the reciprocal label, "inverse velocity".

#         :returns: A ``string`` containing the label.
#         :raises TypeError: When the assigned value is not a string.
#         """
#         return deepcopy(self.subtype._reciprocal_label)

#     @reciprocal_label.setter
#     def reciprocal_label(self, label=''):
#         self.subtype.set_attribute('_reciprocal_label', label)

# axis label
    @property
    def axis_label(self):
        r"""
        Return a formatted string for displaying the label along the dimension.

        This supplementary attribute is convenient for labeling axes.
        For quantitative controlled variables, this attributes returns a
        string, 'label / unit',  if the `label` is not an empty string. If the
        `label` is an empty string, 'quantity / unit’ is returned instead. Here
        `quantity` and `label` are the attributes of the :ref:`cv_api`
        instances described before, and `unit` is the unit associated with the
        control variable.
        For example, consider a temporal controlled variable where

        .. doctest::

            >>> x.label
            'field strength'
            >>> x.axis_label
            'field strength / (G)'

        For non-quantitative controlled variables, this attribute returns
        the `label`.

        :returns: A ``String``.
        :raises AttributeError: When assigned a value.
        """
        if hasattr(self.subtype, 'quantity'):
            if self._label.strip() == '':
                label = self.quantity
            else:
                label = self.label
            return _axis_label(
                label,
                self.subtype._unit
            )
        else:
            return self.label

        # return self.subtype.axis_label
        # if self.label.strip() == '':
        #     label = self.quantity
        # else:
        #     label = self.label
        # if self.variable_type in _quantitative_variable_types:
        #     return _axis_label(
        #         label,
        #         self.subtype._unit,
        #         self.subtype.made_dimensionless,
        #         self.subtype._dimensionless_unit
        #     )
        # return deepcopy(self.label)

# data_structure()
    @property
    def data_structure(self):
        r"""
        Return the ControlledVariable object as a json object.

        This supplementary attribute is useful for a quick preview of the data
        structure. The attribute cannot be modified.

        .. doctest::

            >>> print(x.data_structure)
            {
              "type": "linearly_sampled",
              "number_of_points": 5,
              "sampling_interval": "0.1 G",
              "origin_offset": "100000.0 G",
              "quantity": "magnetic flux density",
              "reverse": true,
              "label": "field strength"
            }

        :raises AttributeError: When modified.
        """
        dictionary = self._get_python_dictionary()
        return (json.dumps(dictionary, ensure_ascii=False,
                           sort_keys=False, indent=2))

# =========================================================================== #
#                                  Methods                                    #
# =========================================================================== #

# _get_python_dictionary()
    def _get_python_dictionary(self):
        r"""Return the ControlledVariable object as a python dictionary."""
        dictionary = self.subtype._get_python_dictionary()

        if self._reverse is True:
            dictionary['reverse'] = True

        if self._label.strip() != "":
            dictionary['label'] = self.label

        keys = dictionary.keys()
        if 'fft_output_order' in keys:
            dictionary.pop('fft_output_order')
            dictionary['fft_output_order'] = True

        if 'reciprocal' in dictionary.keys():
            reciprocal = dictionary['reciprocal']
            dictionary.pop('reciprocal')
            dictionary['reciprocal'] = reciprocal

        return dictionary

# is_quantitative()
    def is_quantitative(self):
        r"""
        Verify if the control variable dimension is quantitative.

        Returns `True`, if the control variable is quantitative,
        otherwise `False`.

        :returns: A Boolean.
        """
        return self.subtype._is_quantitative()
        # if self.variable_type in _quantitative_variable_types:
        #     return True
        # return False

# to()
    def to(self, unit='', equivalencies=None):
        r"""
        Convert the unit of the controlled variable coordinates to `unit`.

        This method is a wrapper of the `to` method from the
        `Quantity <http://docs.astropy.org/en/stable/api/\
        astropy.units.Quantity.html#astropy.units.Quantity.to>`_ class
        and is only `valid` for physical dimensions.

        For example, if

        .. doctest::

            >>> print(x.coordinates)
            [0.4 0.3 0.2 0.1 0. ] G
            >>> x.to('µT')
            >>> print(x.coordinates)
            [40. 30. 20. 10.  0.] uT

        :params: `unit` : A string containing a unit with the same
            dimensionality as the controlled variable coordinates.
        :raise AttributeError: For non-quantitative controlled variables.
        """
        self.subtype._to(unit, equivalencies)
        # if self.variable_type in _quantitative_variable_types:
        #     if not isinstance(unit, str):
        #         raise TypeError(_type_message(str, type(unit)))

        #     if unit.strip() == 'ppm':
        #         self.subtype.set_attribute('_dimensionless_unit', _ppm)
        #     else:
        #         self.subtype.set_attribute(
        #             '_unit', _check_unit_consistency(
        #                 1.0*string_to_unit(unit), self.subtype.unit
        #             ).unit
        #         )
        #         self.subtype.set_attribute('_equivalencies', equivalencies)

        # else:
        #     raise AttributeError(_attribute_message(self.variable_type, 'to'))

from __future__ import print_function, division
import numpy as np
import json
from scipy.fftpack import fftshift
from .unit import valueObjectFormat, unitToLatex, _ppm, string_to_quantity, string_to_unit
from ._csdmChecks import (
                    _assign_and_check_unit_consistency, 
                    _check_unit_consistency,
                    _check_and_assign_bool,
                    _check_quantity,
                    _check_value_object,
                    _axis_label)

# class gcvObject:
#     def __init__(self, dictionary):



#     def assign_correct_gcv_object(self, dictionary)
#         if dictionary['non_quantitative']:
#             if dictionary['coordinates'] is None:
#                 raise Exception("'coordinates' key is required.")
#             else:
#                 return _nonQuantitativeGridDimension( \
#                         _sampling_type          = dictionary['sampling_type'], \
#                         _non_quantitative       = dictionary['non_quantitative'], \

#                         _coordinates            = dictionary['coordinates'], \
#                         _reverse                = dictionary['reverse'], \
#                         _label                  = dictionary['label'] )

#         if not dictionary['non_quantitative']:
#             if dictionary['number_of_points'] is None and \
#                     dictionary['sampling_interval'] is None and \
#                     dictionary['coordinates'] is None:
#                 raise Exception("either 'number_of_points/sampling_interval' or 'coordinates' key is required.")

#         if not dictionary['non_quantitative'] and dictionary['coordinates'] is not None:
#             return _arbitrarilySampledGridDimension( \
#                     _sampling_type          = dictionary['sampling_type'], \
#                     _non_quantitative       = dictionary['non_quantitative'], \

#                     _coordinates            = dictionary['coordinates'], \
#                     _reference_offset       = dictionary['reference_offset'],  \
#                     _origin_offset          = dictionary['origin_offset'], \
#                     _quantity               = dictionary['quantity'], \
#                     _reverse                = dictionary['reverse'], \
#                     _label                  = dictionary['label'], \
#                     _period                 = dictionary['period'], \
#                     _made_dimensionless     = dictionary['made_dimensionless'], \

#                     _reciprocal_reference_offset    = dictionary['reciprocal']['reference_offset'], 
#                     _reciprocal_origin_offset       = dictionary['reciprocal']['origin_offset'],
#                     _reciprocal_quantity            = dictionary['reciprocal']['quantity'],
#                     _reciprocal_reverse             = dictionary['reciprocal']['reverse'],
#                     _reciprocal_period              = dictionary['reciprocal']['period'],
#                     _reciprocal_label               = dictionary['reciprocal']['label'],
#                     _reciprocal_made_dimensionless  = dictionary['reciprocal']['made_dimensionless'])

#         if not dictionary['non_quantitative'] and \
#                 dictionary['number_of_points'] is not None and \
#                 dictionary['sampling_interval'] is not None:
#             return _linearlySampledGridDimension(
#                 _sampling_type          = dictionary['sampling_type'], \
#                 _non_quantitative       = dictionary['non_quantitative'], \

#                 _number_of_points       = dictionary['number_of_points'], 
#                 _sampling_interval      = dictionary['sampling_interval'], 
#                 _reference_offset       = dictionary['reference_offset'], 
#                 _origin_offset          = dictionary['origin_offset'], 
#                 _quantity               = dictionary['quantity'], 
#                 _reverse                = dictionary['reverse'], 
#                 _label                  = dictionary['label'],
#                 _period                 = dictionary['period'], 
#                 _fft_output_order       = dictionary['fft_output_order'], 
#                 _made_dimensionless     = dictionary['made_dimensionless'],

#                 _reciprocal_sampling_interval   = dictionary['reciprocal']['sampling_interval'],
#                 _reciprocal_reference_offset    = dictionary['reciprocal']['reference_offset'], 
#                 _reciprocal_origin_offset       = dictionary['reciprocal']['origin_offset'],
#                 _reciprocal_quantity            = dictionary['reciprocal']['quantity'],
#                 _reciprocal_reverse             = dictionary['reciprocal']['reverse'],
#                 _reciprocal_period              = dictionary['reciprocal']['period'],
#                 _reciprocal_label               = dictionary['reciprocal']['label'],
#                 _reciprocal_made_dimensionless  = dictionary['reciprocal']['made_dimensionless'])



class _linearlySampledGridDimension:

    """
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
    controlled variable coordinates, and :math:`\mathbf{1}` is an array of ones.
    """

    __slots__ = ['_sampling_type', 
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
                 
                #  '_absolute_coordinates',
                #  '_reciprocal_absolute_coordinates',
                 
                 '_type']

    def __init__(self,  _number_of_points, 
                        _sampling_interval, 
                        _reference_offset = None, 
                        _origin_offset = None, 
                        _quantity = None, 
                        _reverse = False, 
                        _label='',
                        _period = None, 
                        _fft_output_order = False, 
                        _made_dimensionless = False,

                        _sampling_type = "grid",
                        _non_quantitative = False,
                        
                        _reciprocal_sampling_interval = None,
                        _reciprocal_reference_offset = None, 
                        _reciprocal_origin_offset = None,
                        _reciprocal_quantity = None,
                        _reciprocal_reverse = False, 
                        _reciprocal_label='',
                        _reciprocal_period = None,
                        _reciprocal_made_dimensionless = False):

        self.set_attribute('_sampling_type', _sampling_type)
        self.set_attribute('_non_quantitative', _non_quantitative)
        self.set_attribute('_type', 'linear')

        self.set_attribute('_number_of_points', _number_of_points)
        self.set_attribute('_reciprocal_number_of_points', _number_of_points)

        _value = _assign_and_check_unit_consistency(_sampling_interval, None)
        self.set_attribute('_sampling_interval', _value)

        _unit = self.sampling_interval.unit
        _reciprocal_unit =  _unit**-1 #_default_units(1.0*_unit**-1).unit

        ### Unit assignment
        self.set_attribute('_unit', _unit)
        self.set_attribute('_reciprocal_unit', _reciprocal_unit)
        self.set_attribute('_dimensionless_unit', '')
        self.set_attribute('_reciprocal_dimensionless_unit', '')

        ### Inverse sampling interval is calculated assuming a Fourier inverse.
        if _reciprocal_sampling_interval is None:
            _value = (1/(_number_of_points*self.sampling_interval.value)) * _reciprocal_unit
        else:
            _value = _assign_and_check_unit_consistency(_reciprocal_sampling_interval, _reciprocal_unit)
        self.set_attribute('_reciprocal_sampling_interval', _value)
        
        ### reference Offset
        _value = _check_value_object(_reference_offset, _unit)
        self.set_attribute('_reference_offset', _value)
        _value = _check_value_object(_reciprocal_reference_offset, _reciprocal_unit)
        self.set_attribute('_reciprocal_reference_offset', _value)
        
        ### origin offset
        _value = _check_value_object(_origin_offset, _unit)
        self.set_attribute('_origin_offset', _value)
        _value =  _check_value_object(_reciprocal_origin_offset, _reciprocal_unit)
        self.set_attribute('_reciprocal_origin_offset', _value)

        ### made dimensionless, specific to NMR datasets
        _value = _check_and_assign_bool(_made_dimensionless)
        self.set_attribute('_made_dimensionless', _value)
        _value = _check_and_assign_bool(_reciprocal_made_dimensionless)
        self.set_attribute('_reciprocal_made_dimensionless', _value)

        ### reverse
        _value = _check_and_assign_bool(_reverse)
        self.set_attribute('_reverse', _value)
        _value = _check_and_assign_bool(_reciprocal_reverse)
        self.set_attribute('_reciprocal_reverse', _value)

        ### fft_ouput_order
        _value = _check_and_assign_bool(_fft_output_order)
        self.set_attribute('_fft_output_order', _value)

        ### period
        _value = _check_value_object(_period, _unit)
        self.set_attribute('_period', _value)
        _value = _check_value_object(_reciprocal_period, _reciprocal_unit)
        self.set_attribute('_reciprocal_period', _value)

        ### quantity
        _value = _check_quantity(_quantity, _unit)
        self.set_attribute('_quantity', _value)
        _value = _check_quantity(_reciprocal_quantity, _reciprocal_unit)
        self.set_attribute('_reciprocal_quantity', _value)

        ### label
        self.set_attribute('_label', _label)
        self.set_attribute('_reciprocal_label', _reciprocal_label)

        ### coordinates along the dimension
        self.set_attribute('_coordinates', None)
        self.set_attribute('_reciprocal_coordinates', None)
        self._get_coordinates()
        self._get_reciprocal_coordinates()


    def set_attribute(self, name, value):
        super(_linearlySampledGridDimension, self).__setattr__(name, value)

    def __delattr__(self, name):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' of class '{1}' cannot be deleted.".format(name, __class__.__name__))

    def __setattr__(self, name, value):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' cannot be modified".format(name))
        elif name in __class__.__dict__.keys():
            return self.set_attribute(name, value)
        else:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(__class__.__name__, name))


### --------------- Class Attributes ------------------ ###

    ## gcv type
    @property
    def gcv_type(self):
        """
        Returns a string specifying the grid-controlled variable type.
        """
        return "Linearly sampled grid controlled variable"


    ## samping type
    def sampling_type(self):
        return self._sampling_type


    ## non_quantitative
    def non_quantitative(self):
        return self._non_quantitative

    ## period
    @property
    def period(self):
        """ 
        The period of the grid dimension, if periodic.
        The default value is `None`, that is, the grid
        dimension is considered non-periodic.
        This attribute can be updated. For example, a period of "1 km/h".

        :Return type: ``Quantity``
        :Assign type: ``string``
        """
        return self._period
    @period.setter
    def period(self, value = True):
        self.set_attribute('_period', _check_value_object(value, self.unit))

    ## reciprocal period
    @property
    def reciprocal_period(self):
        """ 
        The period of the reciprocal grid dimension, if periodic.
        The default value is `None`, that is, the reciprocal grid
        dimension is considered non-periodic.
        This attribute can be updated. 
        For example, the reciprocal_period of "0.1 h/km".

        :Return type: ``Quantity`` instance
        :Assign type: ``string``
        """
        return self._reciprocal_period
    @reciprocal_period.setter
    def reciprocal_period(self, value = True):
        self.set_attribute('_reciprocal_period', \
                _check_value_object(value, self.reciprocal_unit))
    
    ## Quantity
    @property
    def quantity(self):
        """
        The quantity name associated with the physical dimension.
        For example, the quantity name, "speed".
        In version 0.0.9, this value cannot be updated. 
        
        :Return type: ``string``
        """

        # """
        # When assigning a value, the quantity name must be 
        # consistent with other physical quantities specifying 
        # the grid dimension. 
        # """
        return self._quantity
    # @quantity.setter
    # def quantity(self, string = ''):
    #     ## To do: add a check for quantity
    #     self.set_attribute('_quantity', string)

    ## reciprocal Quantity
    @property
    def reciprocal_quantity(self):
        """
        The quantity name associated with the reciprocal 
        physical dimension. For example, the reciprocal 
        quantity name, "inverse speed".
        In version 0.0.9, this value cannot be updated.

        :Return type: ``string``
        """
        # """
        # When assigning a value, the 
        # quantity name must be consistent with the other 
        # physical quantities specifying the reciprocal 
        # grid dimension.
        # """
        return self._reciprocal_quantity
    # @reciprocal_quantity.setter
    # def reciprocal_quantity(self, string = ''):
    #     ## To do: add a check for reciprocal quantity
    #     self.set_attribute('_reciprocal_quantity', string)

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

    ## label
    @property
    def label(self):
        """
        The label associated with the grid dimension.
        For example, the label, "velocity".
        This attribute can be updated. 

        :Return type: ``string``
        :Assign type: ``string``
        """
        return self._label
    @label.setter
    def label(self, label=''):
        self.set_attribute('_label', label)

    @property
    def axis_label(self):
        return _axis_label(self.label, 
                    self._unit,
                    self.made_dimensionless,
                    self._dimensionless_unit)
    
    ## reciprocal_label
    @property
    def reciprocal_label(self):
        """
        The label associated with the reciprocal grid dimension.
        For example, the reciprocal label, "inverse velocity".
        This attribute can be updated. 

        :Return type: ``string``
        :Assign type: ``string``
        """
        return self._reciprocal_label
    @reciprocal_label.setter
    def reciprocal_label(self, label=''):
        self.set_attribute('_reciprocal_label', label)


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
        self.set_attribute('_made_dimensionless', value)

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
        self.set_attribute('_reciprocal_made_dimensionless', value)

    ## reverse
    @property
    def reverse(self):
        """
        The mapping order of :math:`\mathbf{X}_k^\mathrm{ref}` and 
        :math:`\mathbf{X}_k^\mathrm{abs}` coordinates relative to the grid indices.
        If true, these coordinates are mapped to the grid indices
        in the reverse order. 
        This attribute can be updated. 
        For example, consider

        .. math ::
            \mathbf{X}_k^\mathrm{ref} = [0, 1, 2, 3, 4] \mathrm{ m/s}

        when reverse is false, then, with the reverse set to true, the order
        follows

        .. math ::
            \mathbf{X}_k^\mathrm{ref} = [4, 3, 2, 1, 0] \mathrm{ m/s}

        :Return type: ``boolean``
        :Assign type: ``boolean``
        """
        return self._reverse
    @reverse.setter
    def reverse(self, value=False):
        _value = _check_and_assign_bool(value)
        self.set_attribute('_reverse', _value)


    ## reciprocal reverse
    @property
    def reciprocal_reverse(self):
        """
        The mapping order of :math:`\mathbf{X_r}_k^\mathrm{ref}` and 
        :math:`\mathbf{X_r}_k^\mathrm{ref}` coordinates, 
        from the reciprocal grid dimension, relative to the grid indices.
        If true, these coordinates are mapped to the grid indices in 
        the reverse order. This attribute can be updated.  

        :Return type: ``boolean``
        :Assign type: ``boolean``
        """
        return self._reciprocal_reverse
    @reciprocal_reverse.setter
    def reciprocal_reverse(self, value=False):
        _value = _check_and_assign_bool(value)
        self.set_attribute('_reciprocal_reverse', _value)


    ### Modifying the following attributes triggers an update of 
    ### controlled variable coordinates

    ## reference offset
    @property
    def reference_offset(self):
        """
        The reference offset, :math:`c_k`, along the grid dimension.
        When assigning a value, the dimensionality of the value must be 
        consistent with other members specifying the grid dimension. 
        For example, a reference offset of "-10 m/s".

        :Return type: ``Quantity`` object
        :Assign type: ``string``
        """
        return self._reference_offset
    @reference_offset.setter
    def reference_offset(self, value):
        _value = _assign_and_check_unit_consistency(value, self.unit)
        self.set_attribute('_reference_offset', _value)
        # self._get_coordinates()


    ## reciprocal reference offset
    @property
    def reciprocal_reference_offset(self):
        """
        The reference offset along the reciprocal grid dimension.
        When assigning a value, the dimensionality of the value must be 
        consistent with the dimensionality of the other members 
        specifying the reciprocal grid dimension.
        For example, a reciprocal reference offset of "-3.0 s/cm".

        :Return type: ``Quantity`` object
        :Assign type: ``string``
        """
        return self._reciprocal_reference_offset
    @reciprocal_reference_offset.setter
    def reciprocal_reference_offset(self, value):
        _value = _assign_and_check_unit_consistency(value, self.reciprocal_unit)
        self.set_attribute('_reciprocal_reference_offset', _value)
        # self._get_reciprocal_coordinates()


    ## origin offset
    @property
    def origin_offset(self):
        """
        The origin offset, :math:`o_k`, along the grid dimension.
        When assigning a value, the dimensionality of the value must be 
        consistent with the dimensionality of the other 
        members specifying the grid dimension. 
        For example, an origin offset of "120.2 km/s".

        :Return type: ``Quantity`` object
        :Assign type: ``string``
        """
        return self._origin_offset
    @origin_offset.setter
    def origin_offset(self, value):
        _value = _assign_and_check_unit_consistency(value, self.unit)
        self.set_attribute('_origin_offset', _value)
        # self._get_coordinates()


    ## reciprocal origin offset
    @property
    def reciprocal_origin_offset(self):
        """
        The origin offset along the reciprocal grid dimension.
        When assigning a value, the dimensionality of the value must be 
        consistent with the dimensionality of the other members 
        specifying the reciprocal grid dimension. 
        For example, a reciprocal origin offset of "10.1 s/m".

        :Return type: ``Quantity`` object
        :Assign type: ``string``
        """
        return self._reciprocal_origin_offset
    @reciprocal_origin_offset.setter
    def reciprocal_origin_offset(self, value):
        _value = _assign_and_check_unit_consistency(value, self.reciprocal_unit)
        self.set_attribute('_reciprocal_origin_offset', _value)
        # self._get_reciprocal_coordinates()


    ## sampling interval
    @property
    def sampling_interval(self):
        """
        The sampling interval, :math:`m_k`, along the grid dimension.
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
            raise ValueError('The numerical value of the sampling interval \
is a positive real number. A value of {0} is provide.'.format(_value))
        self.set_attribute('_sampling_interval', _value)
        ### Reciprocal sampling interval is calculated assuming a Fourier inverse 
        super(_linearlySampledGridDimension, self).__setattr__("_reciprocal_sampling_interval", \
                                                                    1/(_value*self.number_of_points))
        self._get_coordinates()


    ## reciprocal sampling interval
    @property
    def reciprocal_sampling_interval(self):
        """
        The sampling interval along the reciprocal grid dimension.
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
        _value = _assign_and_check_unit_consistency(value, self.reciprocal_unit)
        if _value.value < 0.0:
            raise ValueError('The numerical value of the reciprocal sampling interval \
is a positive real number. A value of {0} is provide.'.format(_value))
        self.set_attribute('_reciprocal_sampling_interval', _value)
        ### Sampling interval is calculated assuming a Fourier inverse 
        super(_linearlySampledGridDimension, self).__setattr__("sampling_interval", \
                                                                    1/(_value*self.number_of_points))
        # self.sampling_interval = 1/(_value*self.number_of_points)
        self._get_reciprocal_coordinates()


    ## number_of_points
    @property
    def number_of_points(self):
        """
        The number of points, :math:`N_k \ge 1`, along the grid dimension.
        The value can be updated. 

        :Return type: ``integer``
        :Assign type: ``integer``
        """
        return self._number_of_points
    @number_of_points.setter
    def number_of_points(self, value):
        if not isinstance(value, int):
            raise ValueError('An integer type is required, a type {0} is provided.'.format(type(value)))
        if value <= 0:
            raise ValueError('An positive integer value is required, a value of {0} is provided.'.format(value))
        self.set_attribute('_number_of_points', value)
        self._get_coordinates()

    ### The following properties will control the order of the 
    ### controlled variable coordinates
    ## coordinates
    @property
    def coordinates(self):
        """
        The ordered array, :math:`\mathbf{X}_k^\mathrm{ref}`,
        along the grid dimension. The order of these coordinates
        depends on the value of the ``reverse`` and the 
        ``fft_output_order`` attributes of the class.

        :Return type: ``Quantity`` object
        """
        _value = 1.0
        coordinates = self._coordinates
        if self._made_dimensionless:
            _value=(self._origin_offset + self._reference_offset)
        coordinates = (coordinates/_value).to(self.unit)
        if self.reverse:
            coordinates = coordinates[::-1]
        # if self.fft_output_order:
        #     coordinates = fftshift(coordinates)
        return coordinates - self._reference_offset.to(self.unit)

    ## absolute_coordinates
    @property
    def absolute_coordinates(self):
        """
        An ordered array, :math:`\mathbf{X}_k^\mathrm{abs}`, 
        along the grid dimension. The order of these coordinates
        depends on the value of the ``reverse`` and the 
        ``fft_output_order`` attributes of the class.

        :Return type: ``Quantity`` object
        """
        return self.coordinates + self.origin_offset.to(self.unit)


    ## reciprocal_coordinates
    @property
    def reciprocal_coordinates(self):
        """
        An ordered array of controlled variable coordinates 
        along the reciprocal grid dimension.
        The order of these coordinates
        depends on the value of the ``reciprocal_reverse`` 
        attributes of the class.

        :Return type: ``Quantity`` object
        """
        _value = 1.0
        reciprocal_coordinates = self._reciprocal_coordinates
        if self._reciprocal_made_dimensionless:
            _value=(self._reciprocal_origin_offset + self._reciprocal_reference_offset)
        reciprocal_coordinates = (reciprocal_coordinates/_value).to(self.reciprocal_unit)
        if self.reciprocal_reverse:
            reciprocal_coordinates = reciprocal_coordinates[::-1]
        return reciprocal_coordinates - self._reciprocal_reference_offset.to(self.reciprocal_unit)


    ## reciprocal_absolute_coordinates
    @property
    def reciprocal_absolute_coordinates(self):
        """
        An ordered array of absolute controlled variable coordinates 
        along the reciprocal grid dimension.
        The order of these coordinates
        depends on the value of the ``reciprocal_reverse`` 
        attributes of the class.

        :Return type: ``Quantity`` object
        """
        return self.reciprocal_coordinates + self.reciprocal_origin_offset.to(self.reciprocal_unit)

    ## fft_ouput_order
    @property
    def fft_output_order(self):
        """
        A boolean specifying if the coordinates along the grid dimension
        are ordered according to the output of a fast Fourier transform 
        (FFT) routine. A universal behavior of the FFT routine
        is to order the :math:`N_k` output amplitudes by placing the zero 
        `frequency` at the start of the output array, with 
        positive `frequencies` increasing in magnitude placed at 
        increasing array offset until reaching  :math:`\\frac{N_k}{2} -1` if :math:`N_k` 
        is even, otherwise :math:`\\frac{N_k-1}{2}`, followed by negative frequencies 
        decreasing in magnitude until reaching :math:`N_k-1`.  
        This is also the ordering needed for the input of the inverse FFT. 
        For example, consider

        .. math ::
            \mathbf{X}_k^\mathrm{ref} = [0, 1, 2, 3, 4, 5, 6, 7] \mathrm{ m/s}

        when fft output order is false, then, with the fft output order set to true, the order
        follows

        .. math ::
            \mathbf{X}_k^\mathrm{ref} = [0 ,1 ,2, 3, -4, -3, -2, -1] \mathrm{ m/s}

        :Return type: ``Boolean``
        :Assign type: ``Boolean``
        """
        return self._fft_output_order
    @fft_output_order.setter
    def fft_output_order(self, value):
        self.set_attribute('_fft_output_order', value)
        self._get_coordinates()
        return self.coordinates










###--------------Private Methods------------------###

    # def _dimensionlessConversion(self, unit, _oldValue):
    #     denominator = (self.origin_offset + self.reference_offset)
    #     # print (denominator)
    #     # print (self._coordinates, unit, denominator)
    #     if denominator.value != 0:
    #         if self.made_dimensionless and _oldValue: return
    #         if not self.made_dimensionless and not _oldValue: return
    #         if self.made_dimensionless and not _oldValue:
    #             _value = (self.coordinates / denominator)#.to(_ppm)
    #             self.set_attribute('_coordinates', _value)
    #             return
    #         if not self.made_dimensionless and _oldValue:
    #             _value = (self.coordinates * denominator).to(unit)
    #             self.set_attribute('_coordinates', _value)
    #     else:
    #         self.set_attribute('_made_dimensionless', _oldValue)
    #         raise ZeroDivisionError("Dimension cannot be made dimensionsless with \n'origin_offset' {0} and 'reference_offset' {1}. No changes made.".format(self.origin_offset, self.reference_offset))

    def _info(self):
        _response =[self.sampling_type,
                    self.non_quantitative,
                    self.number_of_points, 
                    str(self.sampling_interval),
                    str(self.reference_offset),
                    str(self.origin_offset),
                    self.made_dimensionless,
                    self.reverse,
                    self.quantity,
                    str(self._label),
                    self.fft_output_order,
                    self.period]
        return _response

    # def __str__(self):
        
    #     block = ['\tsampling_type \t\t= {10}\n', \
    #              '\tnon_quantitative \t\t= {11}\n', \
    #              '\tnumber_of_points \t= {0}\n',\
    #              '\tsampling_interval \t= {1}\n', \
    #              '\treference_offset \t= {2}\n', \
    #              '\torigin_offset \t\t= {3}\n', \
    #              '\tquantity \t\t= {6}\n', \
    #              '\treverse \t\t= {5}\n', \
    #              '\tlabel \t\t\t= {7}\n', \
    #              '\tperiod \t\t= {9}\n',
    #              '\tftt_order_output \t= {8}\n', \
    #              '\tmade_dimensionless \t= {4}\n', ]

    #     string = ''.join(block).format(self.number_of_points, 
    #                                 self.sampling_interval,
    #                                 self.reference_offset,
    #                                 self.origin_offset,
    #                                 self.made_dimensionless,
    #                                 self.reverse,
    #                                 self.quantity,
    #                                 self._label,
    #                                 self.fft_output_order,
    #                                 self.period,
    #                                 self.sampling_type,
    #                                 self.non_quantitative)

    #     return string

    def _get_coordinates(self):
        _unit = self._unit
        _number_of_points = self.number_of_points
        _sampling_interval = self.sampling_interval.to(_unit)

        _index = np.arange(_number_of_points, dtype=np.float64)

        if self.fft_output_order:
            _index = np.empty(_number_of_points, dtype=np.int)
            N = (_number_of_points-1)//2 + 1
            p1 = np.arange(0, N, dtype=np.int)
            _index[:N] = p1
            p2 = np.arange(-(_number_of_points//2), 0, dtype=np.int)
            _index[N:] = p2
        
        _value = _index * _sampling_interval

        # if self.made_dimensionless:
        #     _value/=(_origin_offset + _reference_offset)
        #     _value = _value.to(_ppm)
        self.set_attribute('_coordinates', _value)

    def _get_reciprocal_coordinates(self):
        _unit = self._reciprocal_unit
        _number_of_points = self.number_of_points
        _sampling_interval = self.reciprocal_sampling_interval.to(_unit)

        _index = np.arange(_number_of_points, dtype=np.float64)

        if not self.fft_output_order:
            if _number_of_points%2 == 0:
                _index -= _number_of_points/2.0
            else:
                _index -= (_number_of_points-1)/2.0
        _value =  _index * _sampling_interval 

        self.set_attribute('_reciprocal_coordinates', _value)

    def _swapValues(self, a, b):
        temp = self.__getattribute__(a)
        self.set_attribute(a, self.__getattribute__(b))
        self.set_attribute(b, temp)
        temp = None
        del temp

    def _reciprocal(self):
        self._swapValues('_number_of_points', '_reciprocal_number_of_points')
        self._swapValues('_sampling_interval', '_reciprocal_sampling_interval')
        self._swapValues('_reference_offset', '_reciprocal_reference_offset')
        self._swapValues('_origin_offset', '_reciprocal_origin_offset')
        self._swapValues('_made_dimensionless', '_reciprocal_made_dimensionless')
        self._swapValues('_reverse', '_reciprocal_reverse')
        self._swapValues('_unit', '_reciprocal_unit')
        self._swapValues('_reciprocal_unit', '_reciprocal_dimensionless_unit')

        if self.fft_output_order:
            self.set_attribute('_fft_output_order', False)
        else:
            self.set_attribute('_fft_output_order', True)

        self._swapValues('_quantity', '_reciprocal_quantity')
        self._swapValues('_label', '_reciprocal_label')
        self._swapValues('_period', '_reciprocal_period')
        self._swapValues('_coordinates', '_reciprocal_coordinates')

    def _get_python_dictonary(self):
        dictionary = {}
        dictionary['reciprocal'] = {}
        dictionary['number_of_points'] = self.number_of_points
        dictionary['sampling_interval'] = valueObjectFormat(self.sampling_interval)

        if self.reference_offset is not None and self.reference_offset.value != 0.0:
            dictionary['reference_offset'] = valueObjectFormat(self.reference_offset)
        if self.reciprocal_reference_offset is not None and self.reciprocal_reference_offset.value != 0.0:
            dictionary['reciprocal']['reference_offset'] = valueObjectFormat(self.reciprocal_reference_offset)


        if self.origin_offset is not None and self.origin_offset.value != 0.0:
            dictionary['origin_offset'] = valueObjectFormat(self.origin_offset)
        if self.reciprocal_origin_offset is not None and self.reciprocal_origin_offset.value != 0.0:
            dictionary['reciprocal']['origin_offset'] = valueObjectFormat(self.reciprocal_origin_offset)

        if self.reverse is True:
            dictionary['reverse'] = True
        if self.reciprocal_reverse is True:
            dictionary['reciprocal']['reverse'] = True

        if self.fft_output_order is True:
            dictionary['fft_output_order'] = True

        if self.period.value not in [0.0, np.inf, None]:
            dictionary['period'] = valueObjectFormat(self.period)
        if self.reciprocal_period.value not in [0.0, np.inf, None]:
            dictionary['reciprocal']['period'] = valueObjectFormat(self.reciprocal_period)

        if self.quantity not in [None, "unknown", "dimensionless"]:
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
        """
        Converts the unit of the controlled variable coordinates to 
        `unit`. This method is a wrapper of the `to` method 
        from the `Quantity <http://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity.to>`_ class. 

        Parameters
        ----------
        unit : string
            A string containing a unit with the same dimensionality as the
            controlled variable coordinates.

        """
        if unit.strip() == 'ppm': 
            self.set_attribute('_dimensionless_unit', _ppm)
        else:
            self.set_attribute('_unit', _check_unit_consistency(1.0*string_to_unit(unit), self.unit).unit)
        # return self.coordinates

    def __iadd__(self, other):
        self.reference_offset -= _assign_and_check_unit_consistency(other, self.unit) 

    def __isub__(self, other):
        self.reference_offset += _assign_and_check_unit_consistency(other, self.unit) 














class _arbitrarilySampledGridDimension:

    """
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

    __slots__ = ['_sampling_type',
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

    def __init__(self,  _values, 
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

        self.set_attribute('_sampling_type', _sampling_type)
        self.set_attribute('_non_quantitative', _non_quantitative)
        self.set_attribute('_type', 'non-linear')

        self.set_attribute('_number_of_points', len(_values))
        self.set_attribute('_reciprocal_number_of_points', self.number_of_points)

        _unit = _assign_and_check_unit_consistency(_values[0], None).unit
        _reciprocal_unit =  _unit**-1

        self.set_attribute('_unit', _unit)
        self.set_attribute('_reciprocal_unit', _reciprocal_unit)
        self.set_attribute('_dimensionless_unit', '')
        self.set_attribute('_reciprocal_dimensionless_unit', '')

        ## reference
        _value = _check_value_object(_reference_offset, _unit)
        self.set_attribute('_reference_offset', _value)
        _value = _check_value_object(_reciprocal_reference_offset, _reciprocal_unit)
        self.set_attribute('_reciprocal_reference_offset', _value)
        
        ## origin offset
        _value = _check_value_object(_origin_offset, _unit)
        self.set_attribute('_origin_offset', _value)
        _value =  _check_value_object(_reciprocal_origin_offset, _reciprocal_unit)
        self.set_attribute('_reciprocal_origin_offset', _value)

        ### made dimensionless
        _value = _check_and_assign_bool(_made_dimensionless)
        self.set_attribute('_made_dimensionless', _value)
        _value = _check_and_assign_bool(_reciprocal_made_dimensionless)
        self.set_attribute('_reciprocal_made_dimensionless', _value)
       
        ### reverse
        _value = _check_and_assign_bool(_reverse)
        self.set_attribute('_reverse', _value)
        _value = _check_and_assign_bool(_reciprocal_reverse)
        self.set_attribute('_reciprocal_reverse', _value)

        ## period
        _value = _check_value_object(_period, _unit)
        self.set_attribute('_period', _value)
        _value = _check_value_object(_reciprocal_period, _reciprocal_unit)
        self.set_attribute('_reciprocal_period', _value)

        ## quantity
        _value = _check_quantity(_quantity, _unit)
        self.set_attribute('_quantity', _value)
        _value = _check_quantity(_reciprocal_quantity, _reciprocal_unit)
        self.set_attribute('_reciprocal_quantity', _value)
    
        ## label
        self.set_attribute('_label', _label)
        self.set_attribute('_reciprocal_label', _reciprocal_label)

        ## coordinates ##
        self._getCoordinates(_values)

        ## Reciprocal coordinates ##
        self.set_attribute('_reciprocal_coordinates', None)

        # self.set_attribute('_reciprocal_absolute_coordinates', None)
        

    def set_attribute(self, name, value):
        super(_arbitrarilySampledGridDimension, self).__setattr__(name, value)

    def __delattr__(self, name):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' of class '{1}' cannot be deleted.".format(name, __class__.__name__))

    def __setattr__(self, name, value):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' cannot be modified".format(name))
        elif name in __class__.__dict__.keys():
            return self.set_attribute(name, value)
        else:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(__class__.__name__, name))


### --------------- Attributes ------------------ ###

    ## gcv type
    @property
    def gcv_type(self):
        """
        Returns a string specifying the grid-controlled variable type.
        """
        return "Arbitrarily sampled grid controlled variable"

    ## sampling_type
    @property
    def sampling_type(self):
        return self._sampling_type


    ## non_quantitative
    # @property
    def non_quantitative(self):
        return self._non_quantitative


    ## period
    @property
    def period(self):
        """ 
        The period of the grid dimension, if periodic.
        The default value is `None`, that is, the grid
        dimension is considered non-periodic.
        This attribute can be updated. For example, a period of "1 cm".

        :Return type: ``Quantity``
        :Assign type: ``string``
        """
        return self._period
    @period.setter
    def period(self, value):
        self.set_attribute('_period', _check_value_object(value, self.unit))


    ## reciprocal period
    @property
    def reciprocal_period(self):
        """ 
        The period of the reciprocal grid dimension, if periodic.
        The default value is `None`, that is, the reciprocal grid
        dimension is considered non-periodic.
        This attribute can be updated. 
        For example, the reciprocal_period of "0.1 cm^-1".

        :Return type: ``Quantity`` instance
        :Assign type: ``string``
        """
        return self._reciprocal_period
    @reciprocal_period.setter
    def reciprocal_period(self, value):
        self.set_attribute('_reciprocal_period', \
                        _check_value_object(value, self.reciprocal_unit))


    ## Quantity
    @property
    def quantity(self):
        """
        The quantity name associated with the physical dimension.
        For example, the quantity name, "length".
        In version 0.0.9, this value cannot be updated.

        :Return type: ``string``
        """
        # """ When assigning a value, 
        # this attribute updates the previous 
        # value. The quantity name must be 
        # consistent with other physical quantities specifying 
        # the dimension. """
        return self._quantity
    # @quantity.setter
    # def quantity(self, string = '', force_update=False):
    #     if self._unit.physical_type == string:
    #         self.set_attribute('_quantity', string)
    #     else:
    #         raise Warning('Then quantity name {0} is not recognized \
    #             by the astropy.units library.'.format([string]))


    ## reciprocal Quantity
    @property
    def reciprocal_quantity(self):
        """
        The quantity name associated with the reciprocal 
        physical dimension. For example, the reciprocal 
        quantity name, "wavelength".
        In version 0.0.9, this value cannot be updated.

        :Return type: ``string``
        """
        # """
        # When assigning a value, the 
        # quantity name must be consistent with the other 
        # physical quantities specifying the reciprocal 
        # grid dimension.
        # """
        return self._reciprocal_quantity
    # @reciprocal_quantity.setter
    # def reciprocal_quantity(self, string = ''):
    #     self.set_attribute('_reciprocal_quantity', string)


    @property
    def unit(self):
        """
        Returns the unit associated with the physical dimension.
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
        Returns the unit associated with the reciprocal grid dimension.
        For example, a unit a "cm^-1". This attribute cannot be updated.

        :Return type: ``string``
        """
        if self._reciprocal_made_dimensionless:
            unit = self._reciprocal_dimensionless_unit
        else:
            unit = self._reciprocal_unit
        return unit


    ## label
    @property
    def label(self):
        """
        The label associated with the grid dimension.
        For example, the label, "distance".
        This attribute can be updated. 

        :Return type: ``string``
        :Assign type: ``string``
        """
        return self._label
    @label.setter
    def label(self, label=''):
        self.set_attribute('_label', label)


    @property
    def axis_label(self):
        return _axis_label(self.label, 
                           self._unit,
                           self.made_dimensionless,
                           self._dimensionless_unit)
    

    ## reciprocalLabel
    @property
    def reciprocal_label(self):
        """
        The label associated with the reciprocal grid dimension.
        For example, the reciprocal label, "inverse distance".
        This attribute can be updated. 

        :Return type: ``string``
        :Assign type: ``string``
        """
        return self._reciprocal_label
    @reciprocal_label.setter
    def reciprocal_label(self, label=''):
        self.set_attribute('_reciprocal_label', label)


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
        self.set_attribute('_made_dimensionless', value)


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
        self.set_attribute('_reciprocal_made_dimensionless', value)


    ## reverse
    @property
    def reverse(self):
        """
        The mapping order of :math:`\mathbf{X}_k^\mathrm{ref}` and 
        :math:`\mathbf{X}_k^\mathrm{abs}` coordinates relative to the grid indices.
        If true, these coordinates are mapped to the grid indices
        in the reverse order. 
        This attribute can be updated. 
        For example, consider

        .. math ::
            \mathbf{X}_k^\mathrm{ref} = [0, 1, 2, 3, 4] \mathrm{ cm}

        when reverse is false, then, with the reverse set to true, the order
        follows

        .. math ::
            \mathbf{X}_k^\mathrm{ref} = [4, 3, 2, 1, 0] \mathrm{ cm}

        :Return type: ``boolean``
        :Assign type: ``boolean``
        """
        return self._reverse
    @reverse.setter
    def reverse(self, value=False):
        _value = _check_and_assign_bool(value)
        self.set_attribute('_reverse', _value)


    ## reciprocal reverse
    @property
    def reciprocal_reverse(self):
        """
        The mapping order of :math:`\mathbf{X_r}_k^\mathrm{ref}` and 
        :math:`\mathbf{X_r}_k^\mathrm{ref}` coordinates, 
        from the reciprocal grid dimension, relative to the grid indices.
        If true, these coordinates are mapped to the grid indices in 
        the reverse order. This attribute can be updated.  

        :Return type: ``boolean``
        :Assign type: ``boolean``
        """
        return self._reciprocal_reverse
    @reciprocal_reverse.setter
    def reciprocal_reverse(self, value=False):
        _value = _check_and_assign_bool(value)
        self.set_attribute('_reciprocal_reverse', _value)
    



    ### Modifying the following attributes triggers an update of 
    ### controlled variable coordinates

    ## reference offset
    @property
    def reference_offset(self):
        """
        The reference offset, :math:`c_k`, along the grid dimension.
        When assigning a value, the dimensionality of the value must be 
        consistent with other members specifying the grid dimension. 
        For example, a reference offset of "-10 cm".

        :Return type: ``Quantity`` object
        :Assign type: ``string``
        """
        return self._reference_offset
    @reference_offset.setter
    def reference_offset(self, value):
        _value = _assign_and_check_unit_consistency(value, self.unit)
        self.set_attribute('_reference_offset', _value)


    ## reciprocal reference offset
    @property
    def reciprocal_reference_offset(self):
        """
        The reference offset along the reciprocal grid dimension.
        When assigning a value, the dimensionality of the value must be 
        consistent with the dimensionality of the other members 
        specifying the reciprocal grid dimension.
        For example, a reciprocal reference offset of "0.5 cm^-1".

        :Return type: ``Quantity`` object
        :Assign type: ``string``
        """
        return self._reciprocal_reference_offset
    @reciprocal_reference_offset.setter
    def reciprocal_reference_offset(self, value):
        _value = _assign_and_check_unit_consistency(value, self.reciprocal_unit)
        self.set_attribute('_reciprocal_reference_offset', _value)
        # self._getreciprocalCoordinates()


    ## origin offset
    @property
    def origin_offset(self):
        """
        The origin offset, :math:`o_k`, along the grid dimension.
        When assigning a value, the dimensionality of the value must be 
        consistent with the dimensionality of the other 
        members specifying the grid dimension. 
        For example, an origin offset of "1.0 m".

        :Return type: ``Quantity`` object
        :Assign type: ``string``
        """
        return self._origin_offset
    @origin_offset.setter
    def origin_offset(self, value):
        _value = _assign_and_check_unit_consistency(value, self.unit)
        self.set_attribute('_origin_offset', _value)


    ## reciprocal origin offset
    @property
    def reciprocal_origin_offset(self):
        """
        The origin offset along the reciprocal grid dimension.
        When assigning a value, the dimensionality of the value must be 
        consistent with the dimensionality of the other members 
        specifying the reciprocal grid dimension. 
        For example, an origin offset of "-400.2 cm^-1".

        :Return type: ``Quantity`` object
        :Assign type: ``string``
        """
        return self._reciprocal_origin_offset
    @reciprocal_origin_offset.setter
    def reciprocal_origin_offset(self, value):
        _value = _assign_and_check_unit_consistency(value, self.reciprocal_unit)
        self.set_attribute('_reciprocal_origin_offset', _value)


    ## number_of_points
    @property
    def number_of_points(self):
        """
        The number of points, :math:`N_k`, along the grid dimension.
        The value can be updated. 

        :Return type: ``integer``
        :Assign type: ``integer``
        """
        return self._number_of_points

    @property
    def values(self, array):
        """
        The ordered array, :math:`\mathbf{A}_k`,
        along the grid dimension.

        :Assign type: An array of strings containing the
        physical quantities.
        """
        self._getCoordinates(_values)


    ## coordinates
    @property
    def coordinates(self):
        """
        The ordered array, :math:`\mathbf{X}_k^\mathrm{ref}`,
        along the grid dimension. The order of these coordinates
        depends on the value of the ``reverse`` attributes of the class.

        :Return type: ``Quantity`` object
        """
        _value = 1.0
        coordinates = self._coordinates
        if self._made_dimensionless:
            _value=(self._origin_offset + self._reference_offset)
        coordinates = (coordinates/_value).to(self.unit)
        if self.reverse:
            coordinates = coordinates[::-1]
        return coordinates - self._reference_offset.to(self.unit)

    ## absolute_coordinates
    @property
    def absolute_coordinates(self):
        """
        An ordered array, :math:`\mathbf{X}_k^\mathrm{abs}`, 
        along the grid dimension. The order of these coordinates
        depends on the value of the ``reverse`` attributes of the class.

        :Return type: ``Quantity`` object
        """
        return self.coordinates + self.origin_offset.to(self.unit)

    ## reciprocal_coordinates
    @property
    def reciprocal_coordinates(self):
        return self._reciprocal_coordinates

    ## reciprocal_absolute_coordinates
    @property
    def reciprocal_absolute_coordinates(self):
        return self.reciprocal_coordinates + self.reciprocal_origin_offset

###--------------Private Methods------------------###

    # def _dimensionlessConversion(self, unit, _oldValue):
    #     denominator = (self.origin_offset + self.reference_offset)
    #     if denominator.value != 0:
    #         if self.made_dimensionless and _oldValue: return
    #         if not self.made_dimensionless and not _oldValue: return
    #         if self.made_dimensionless and not _oldValue:
    #             _value = (self.coordinates/ denominator).to(_ppm)
    #             self.set_attribute('_coordinates', _value)
    #             return
    #         if not self.made_dimensionless and _oldValue:
    #             _value = (self.coordinates * denominator).to(unit)
    #             self.set_attribute('_coordinates', _value)
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

    def _getCoordinates(self, _values):
        _unit = self._unit
        _value = [_assign_and_check_unit_consistency(item, _unit).to(_unit).value \
                                for item in _values]
        # print (_value)
        _value = np.asarray(_value, dtype=np.float64)*_unit
        self.set_attribute('_coordinates', _value)
        # self.set_attribute('_coordinates', self._coordinates.to(_unit))


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

    def to(self, unit=''):
        """
        Converts the unit of the controlled variables coordinates to 
        `unit`. This method wraps the ``to`` method from the ``Quantity`` 
        class. 
        """
        if unit.strip() == 'ppm': 
            self.set_attribute('_dimensionless_unit', _ppm)
        else:
            self.set_attribute('_unit', _check_unit_consistency(string_to_quantity('1 '+unit), self.unit).unit)
        # return self.coordinates

    def __iadd__(self, other):
        self.reference_offset -= _assign_and_check_unit_consistency(other, self.unit) 

    def __isub__(self, other):
        self.reference_offset += _assign_and_check_unit_consistency(other, self.unit) 










class _nonQuantitativeGridDimension:

    __slots__ = ['_sampling_type',
                 '_non_quantitative',
                 '_number_of_points',
                 '_coordinates', 
                 '_reverse',
                 '_label'
                 ]

    def __init__(self,  _values, 
                        _sampling_type='grid',
                        _non_quantitative=True,
                        _reverse=False, 
                        _label=''):

        self.set_attribute('_sampling_type', _sampling_type)
        self.set_attribute('_non_quantitative', _non_quantitative)

        self.set_attribute('_number_of_points', len(_coordinates))

        ### reverse
        _value = _check_and_assign_bool(_reverse)
        self.set_attribute('_reverse', _value)

        ## label
        self.set_attribute('_label', _label)
        self._get_coordinates(_values)
        # print (_value)

    def _get_coordinates(self, _values):
        _value = np.asarray(_values)
        self.set_attribute('_coordinates', _value)

    def set_attribute(self, name, value):
        super(_nonQuantitativeGridDimension, self).__setattr__(name, value)

    def __delattr__(self, name):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' of class '{1}' cannot be deleted.".format(name, __class__.__name__))

    def __setattr__(self, name, value):
        if name in __class__.__slots__:
            raise AttributeError("attribute '{0}' cannot be modified".format(name))
        elif name in __class__.__dict__.keys():
            return self.set_attribute(name, value)
        else:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(__class__.__name__, name))


### --------------- Class Attributes ------------------ ###

    ## gcv type
    @property
    def gcv_type(self):
        """
        Returns a string specifying the grid-controlled variable type.
        """
        return "Linearly sampled grid controlled variable"


    ## sampling_type
    @property
    def sampling_type(self):
        return self._sampling_type

    ## non_quantitative
    @property
    def non_quantitative(self):
        return self._non_quantitative

    ## label
    @property
    def label(self):
        """
        :Return type: ``string``
        :Assign type: ``string``

        The attribute returns the label associated 
        with the grid dimension. When assigning a value, 
        this attribute updates the previous value. 
        For example, a ``label`` of "Atom symbols".
        """
        return self._label
    @label.setter
    def label(self, label=''):
        self.set_attribute('_label', label)
    
    @property
    def axis_label(self):
        return self.label

    ## reverse
    @property
    def reverse(self):
        """
        :Return type: ``boolean``
        :Assign type: ``boolean``

        The attribute returns a boolean specifying the
        mapping of the controlled variable coordinates, 
        associated with the grid dimension, to 
        the grid indices. This attribute value can be updated. 
        """
        return self._reverse
    @reverse.setter
    def reverse(self, value=False):
        _value = _check_and_assign_bool(value)
        self.set_attribute('_reverse', _value)

    ## number_of_points
    @property
    def number_of_points(self):
        """
        :Return type: ``integer``

        The attribute returns the number of points along the dimension.
        """
        return self._number_of_points

    ## coordinates
    @property
    def coordinates(self):
        """
        :Return type: ``numpy array`` of strings.

        The attribute returns the controlled variable coordinates
        along the dimension. The order of these coordinates
        depends on the value of the ``reverse`` attribute of the class.
        """
        return self._coordinates


###--------------Private Methods------------------###

    def _info(self):
        _response =[self.sampling_type,
                    self.non_quantitative,
                    self.number_of_points,
                    self.reverse,
                    str(self._label)]
        return _response

    def _get_python_dictonary(self):
        dictionary = {}

        dictionary['coordinates'] = self.coordinates.tolist()
        dictionary['non_quantitative'] = True
        if self.reverse is True:
            dictionary['reverse'] = True

        if self._label.strip() != "":
            dictionary['label'] = self._label

        return dictionary

### ------------- Public Methods ------------------ ###

    def __str__(self):
        dictionary = self._get_python_dictonary()
        return (json.dumps(dictionary, sort_keys=False, indent=2))
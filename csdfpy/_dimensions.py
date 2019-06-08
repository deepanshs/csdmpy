# -*- coding: utf-8 -*-
"""The Dimension SubTypes class."""
from __future__ import division
from __future__ import print_function

from copy import deepcopy

import numpy as np
from astropy.units import Quantity
from numpy import inf

from ._utils import _assign_and_check_unit_consistency
from ._utils import _check_and_assign_bool
from ._utils import _check_quantity
from ._utils import _check_unit_consistency
from ._utils import _check_value_object
from ._utils import _type_message
from .units import string_to_unit
from .units import value_object_format


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


# =========================================================================== #
#               		 QuantitativeVariable Class      				      #
# =========================================================================== #


class BaseIndependentVariable:
    r"""Declare a BaseIndependentVariable class."""

    __slots__ = (
        "_index_zero_value",
        "_origin_offset",
        "_quantity",
        "_period",
        "_label",
        "_description",
        "_application",
        "_equivalencies",
        "_unit",
    )

    def __init__(
        self,
        _description="",
        _application={},
        _index_zero_value=None,
        _origin_offset=None,
        _quantity=None,
        _period=None,
        _label="",
        _unit=None,
    ):
        r"""Instantiate a BaseIndependentVariable class instance."""
        #     self._set_parameters(
        #         _description,
        #         _application,
        #         _index_zero_value,
        #         _origin_offset,
        #         _quantity,
        #         _period,
        #         _label,
        #         _unit,
        #     )

        # def _set_parameters(
        #     self,
        #     _description="",
        #     _application={},
        #     _index_zero_value=None,
        #     _origin_offset=None,
        #     _quantity=None,
        #     _period=None,
        #     _label="",
        #     _unit=None,
        # ):

        # description
        self._description = _description

        # application
        self._application = _application

        # unit
        self._unit = _unit

        # reference Offset
        _value = _check_value_object(_index_zero_value, _unit)
        self._index_zero_value = _value

        # origin offset
        _value = _check_value_object(_origin_offset, _unit)
        self._origin_offset = _value

        # period
        _value = _check_value_object(_period, _unit)
        if _value.value == 0.0:
            _value = np.inf * _value.unit
        self._period = _value

        # quantity
        _value = _check_quantity(_quantity, _unit)
        self._quantity = _value

        # label
        self.label = _label

    # ----------------------------------------------------------------------- #
    #                     QuantitativeVariable Attributes                     #
    # ----------------------------------------------------------------------- #

    # application
    @property
    def application(self):
        """Return application metadata, if available."""
        return deepcopy(self._application)

    @application.setter
    def application(self, value):
        if not isinstance(value, dict):
            raise ValueError(
                "A dict value is required, found {0}".format(type(value))
            )
        self._application = value

    # reference offset
    @property
    def index_zero_value(self):
        r"""Value at index zero, :math:`c_k`, along the dimension."""
        return deepcopy(self._index_zero_value)

    @index_zero_value.setter
    def index_zero_value(self, value):
        if isinstance(value, Quantity):
            value = str(value)
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))

        _value = _assign_and_check_unit_consistency(value, self._unit)
        self._index_zero_value = _value

    # origin offset
    @property
    def origin_offset(self):
        r"""Origin offset, :math:`o_k`, along the dimension."""
        return deepcopy(self._origin_offset)

    @origin_offset.setter
    def origin_offset(self, value):
        if isinstance(value, Quantity):
            value = str(value)
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))

        _value = _assign_and_check_unit_consistency(value, self._unit)
        self._origin_offset = _value

    # period
    @property
    def period(self):
        r"""Period of the data along this dimension."""
        return deepcopy(self._period)

    @period.setter
    def period(self, value=None):
        if isinstance(value, Quantity):
            value = str(value)
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))

        lst = ["inf", "Inf", "infinity", "Infinity", "∞"]
        if value.strip().split()[0] in lst:
            value = inf * self._unit
            self._period = value
        else:
            self._period = _check_value_object(value, self._unit)

    # Quantity
    @property
    def quantity(self):
        r"""Quantity name associated with this dimension."""
        return deepcopy(self._quantity)

    @quantity.setter
    def quantity(self, value):
        raise NotImplementedError("This attribute is not yet implemented.")

    # label
    @property
    def label(self):
        r"""Label associated with this dimension."""
        return deepcopy(self._label)

    @label.setter
    def label(self, label=""):
        if not isinstance(label, str):
            raise TypeError(_type_message(str, type(label)))
        self._label = label

    # description
    @property
    def description(self):
        r"""Brief description of the dimension object."""
        return deepcopy(self._description)

    @description.setter
    def description(self, value):
        if isinstance(value, str):
            self._description = value
        else:
            raise ValueError(
                (
                    "Description requires a string, {0} given".format(
                        type(value)
                    )
                )
            )

    # ----------------------------------------------------------------------- #
    #                       QuantitativeVariable Methods                      #
    # ----------------------------------------------------------------------- #

    def _get_quantitative_dictionary(self):
        r"""Return the object as a python dictionary."""
        dictionary = {}

        # The description key is added to the child class.
        if self._index_zero_value.value != 0.0:
            dictionary["index_zero_value"] = value_object_format(
                self._index_zero_value
            )

        if self._origin_offset.value != 0.0:
            dictionary["origin_offset"] = value_object_format(
                self._origin_offset
            )

        if self._quantity not in [None, "unknown", "dimensionless"]:
            dictionary["quantity"] = self._quantity

        if self._period.value not in [0.0, np.inf]:
            dictionary["period"] = value_object_format(self._period)

        if self.label.strip() != "":
            dictionary["label"] = self.label

        if self._application != {}:
            dictionary["application"] == self._application

        return dictionary

    # is_quantitative
    def _is_quantitative(self):
        r"""Return `True`, if the dimension is quantitative, otherwise `False`.

        :returns: A Boolean.
        """
        return True

    # to()
    def _to(self, unit="", equivalencies=None):
        r"""Convert the unit to given value `unit`."""
        if not isinstance(unit, str):
            raise TypeError(_type_message(str, type(unit)))

        self._unit = _check_unit_consistency(
            1.0 * string_to_unit(unit), self._unit
        ).unit

        self._equivalencies = equivalencies


# =========================================================================== #
#                      ReciprocalVariable Dimension Class                     #
# =========================================================================== #


class ReciprocalVariable(BaseIndependentVariable):
    r"""Declare a ReciprocalVariable class."""

    pass


# =========================================================================== #
#                       LinearlySampledDimension Class                        #
# =========================================================================== #


class LinearDimension(BaseIndependentVariable):
    r"""
    Create a linear grid dimension.

    .. warning ::
        This class should not be used directly. Instead,
        use the ``CSDModel`` object to access the attributes
        and methods of this class. See example, :ref:`lsgd`.

    This class returns an object which represents a physical
    dimension, sampled linearly along a grid dimension.
    Let :math:`m_k` be the increment, :math:`N_k \ge 1` be the
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
        "_number_of_points",
        "_increment",
        "_fft_output_order",
        "reciprocal",
        "_reciprocal_number_of_points",
        "_reciprocal_increment",
        "_coordinates",
    )

    _type = "linear"

    def __init__(
        self,
        _number_of_points,
        _increment,
        _index_zero_value=None,
        _origin_offset=None,
        _quantity=None,
        _period=None,
        _label="",
        _fft_output_order=False,
        _description="",
        _application={},
        _reciprocal_index_zero_value=None,
        _reciprocal_origin_offset=None,
        _reciprocal_quantity=None,
        _reciprocal_label="",
        _reciprocal_period=None,
        _reciprocal_description="",
        _reciprocal_application={},
    ):
        r"""Instantiate a DimensionWithLinearSpacing class instance."""
        # number of points
        self._number_of_points = _number_of_points

        # increment
        _value = _assign_and_check_unit_consistency(_increment, None)
        self._increment = _value

        # fft_ouput_order
        _value = _check_and_assign_bool(_fft_output_order)
        self._fft_output_order = _value

        self._unit = self._increment.unit

        super(LinearDimension, self).__init__(
            # self._set_parameters(
            _description,
            _application,
            _index_zero_value,
            _origin_offset,
            _quantity,
            _period,
            _label,
            self._unit,
        )

        # create a reciprocal dimension
        _reciprocal_unit = self._unit ** -1
        self.reciprocal = ReciprocalVariable(
            _reciprocal_description,
            _reciprocal_application,
            _reciprocal_index_zero_value,
            _reciprocal_origin_offset,
            _reciprocal_quantity,
            _reciprocal_period,
            _reciprocal_label,
            _reciprocal_unit,
        )

        self._get_coordinates()

    # ----------------------------------------------------------------------- #
    #                    LinearlySampledDimension Methods                     #
    # ----------------------------------------------------------------------- #
    def _swap(self):

        # description
        self._description, self.reciprocal._description = (
            self.reciprocal._description,
            self._description,
        )

        # application
        self._application, self.reciprocal._application = (
            self.reciprocal._application,
            self._application,
        )

        # index_zero_value
        self._index_zero_value, self.reciprocal._index_zero_value = (
            self.reciprocal._index_zero_value,
            self._index_zero_value,
        )

        # origin offset
        self._origin_offset, self.reciprocal._origin_offset = (
            self.reciprocal._origin_offset,
            self._origin_offset,
        )

        # period
        self._period, self.reciprocal._period = (
            self.reciprocal._period,
            self._period,
        )

        # quantity
        self._quantity, self.reciprocal._quantity = (
            self.reciprocal._quantity,
            self._quantity,
        )

        # label
        self._label, self.reciprocal._label = (
            self.reciprocal._label,
            self._label,
        )

        # unit
        self._unit, self.reciprocal._unit = self.reciprocal._unit, self._unit

    def _get_coordinates(self):
        _unit = self._unit
        _number_of_points = self._number_of_points
        _increment = self._increment.to(_unit)

        _index = np.arange(_number_of_points, dtype=np.float64)

        if self._fft_output_order:
            _index = np.empty(_number_of_points, dtype=np.int)
            n = (_number_of_points - 1) // 2 + 1
            p1 = np.arange(0, n, dtype=np.int)
            _index[:n] = p1
            p2 = np.arange(-(_number_of_points // 2), 0, dtype=np.int)
            _index[n:] = p2

        _value = _index * _increment
        self._coordinates = _value

    # _get_python_dictionary()
    def _get_python_dictionary(self):
        # dictionary
        dictionary = {}
        dictionary["type"] = self.__class__._type

        if self._description.strip() != "":
            dictionary["description"] = self._description.strip()

        dictionary["number_of_points"] = self._number_of_points
        dictionary["increment"] = value_object_format(self.increment)

        dictionary.update(self._get_quantitative_dictionary())

        if self.fft_output_order is True:
            dictionary["fft_output_order"] = True

        # reciprocal dictionary
        reciprocal_dictionary = {}

        if self.reciprocal._description.strip() != "":
            reciprocal_dictionary[
                "description"
            ] = self.reciprocal._description.strip()

        reciprocal_dictionary.update(
            self.reciprocal._get_quantitative_dictionary()
        )

        if reciprocal_dictionary == {}:
            del reciprocal_dictionary
        else:
            dictionary["reciprocal"] = reciprocal_dictionary

        return dictionary

    # ----------------------------------------------------------------------- #
    #                   LinearlySampledDimension Attributes                   #
    # ----------------------------------------------------------------------- #

    # number_of_points
    @property
    def number_of_points(self):
        r"""Total number of points along the linear dimension."""
        return deepcopy(self._number_of_points)

    # increment
    @property
    def increment(self):
        r"""Increment of the grid points along the linear dimension."""
        return deepcopy(self._increment)

    @increment.setter
    def increment(self, value):
        if isinstance(value, Quantity):
            value = str(value)
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))
        _value = _assign_and_check_unit_consistency(value, self._unit)
        self._increment = _value
        self._get_coordinates()

    # fft_ouput_order
    @property
    def fft_output_order(self):
        """If True, orders the coordinates according to FFT output order."""
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


class MonotonicDimension(BaseIndependentVariable):
    r"""
    A monotonic grid dimension.

    .. warning ::
        This class should not be used directly. Instead,
        use the ``CSDModel`` object to access the attributes
        and methods of this class. See example, :ref:`asgd`.

    This class returns an object which represents a physical
    dimension, sampled monotonically along a grid dimension.
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
        "_unit",
        "reciprocal",
        "_number_of_points",
        "_values",
        "_coordinates",
    )

    _type = "monotonic"

    def __init__(
        self,
        _values,
        _index_zero_value=None,
        _origin_offset=None,
        _quantity=None,
        _period=None,
        _label="",
        _description="",
        _application={},
        _reciprocal_index_zero_value=None,
        _reciprocal_origin_offset=None,
        _reciprocal_quantity=None,
        _reciprocal_label="",
        _reciprocal_period=None,
        _reciprocal_description="",
        _reciprocal_application={},
    ):
        """Instantiate a MonotonicDimension class instance."""
        # unit
        self._unit = _assign_and_check_unit_consistency(_values[0], None).unit

        super(MonotonicDimension, self).__init__(
            # self._set_parameters(
            _description,
            _application,
            _index_zero_value,
            _origin_offset,
            _quantity,
            _period,
            _label,
            self._unit,
        )

        # reciprocal dimension attributes
        _reciprocal_unit = self._unit ** -1
        self.reciprocal = ReciprocalVariable(
            _reciprocal_description,
            _reciprocal_application,
            _reciprocal_index_zero_value,
            _reciprocal_origin_offset,
            _reciprocal_quantity,
            _reciprocal_period,
            _reciprocal_label,
            _reciprocal_unit,
        )

        # coordinates
        self._get_coordinates(_values)

    # ----------------------------------------------------------------------- #
    #                  ArbitrarilySampledDimension Methods                    #
    # ----------------------------------------------------------------------- #

    def _get_coordinates(self, values):
        _unit = self._unit
        _value = [
            _assign_and_check_unit_consistency(item, _unit).to(_unit).value
            for item in values
        ]

        _value = np.asarray(_value, dtype=np.float64) * _unit

        self._number_of_points = _value.size
        self._values = values
        self._coordinates = _value

    def _get_python_dictionary(self):
        # dictionary
        dictionary = {}
        dictionary["type"] = self.__class__._type

        if self._description.strip() != "":
            dictionary["description"] = self._description.strip()

        dictionary["values"] = self._values

        dictionary.update(self._get_quantitative_dictionary())

        # reciprocal dictionary
        reciprocal_dictionary = {}

        if self.reciprocal._description.strip() != "":
            reciprocal_dictionary[
                "description"
            ] = self.reciprocal._description.strip()

        reciprocal_dictionary.update(
            self.reciprocal._get_quantitative_dictionary()
        )

        if reciprocal_dictionary == {}:
            del reciprocal_dictionary
        else:
            dictionary["reciprocal"] = reciprocal_dictionary

        return dictionary

    # ----------------------------------------------------------------------- #
    #                  ArbitrarilySampledDimension Attributes                 #
    # ----------------------------------------------------------------------- #

    # values
    @property
    def values(self):
        r"""Return a list of values along the dimension."""
        return deepcopy(self._values)

    @values.setter
    def values(self, array):
        self._get_coordinates(array)


# =========================================================================== #
#                           LabeledDimension Class                            #
# =========================================================================== #


class LabeledDimension:
    """Declare a LabeledDimension class."""

    __slots__ = (
        "_number_of_points",
        "_coordinates",
        "_values",
        "_label",
        "_description",
        "_application",
    )

    _type = "labeled"

    def __init__(self, _values, _label="", _description="", _application={}):
        r"""Instantiate a LabeledDimension class instance."""
        self._description = _description
        self._application = _application

        self._get_coordinates(_values)
        self._label = _label

    # ----------------------------------------------------------------------- #
    #                          LabeledDimension Methods                       #
    # ----------------------------------------------------------------------- #
    # label
    @property
    def label(self):
        r"""Label associated with the dimension."""
        return deepcopy(self._label)

    @label.setter
    def label(self, label=""):
        if not isinstance(label, str):
            raise TypeError(_type_message(str, type(label)))
        self._label = label

    # description
    @property
    def description(self):
        r"""Return the description of the object."""
        return deepcopy(self._description)

    @description.setter
    def description(self, value):
        if isinstance(value, str):
            self._description = value
        else:
            raise ValueError(
                (
                    "Description requires a string, {0} given".format(
                        type(value)
                    )
                )
            )

    def _get_coordinates(self, _values):
        self._coordinates = np.asarray(_values)
        self._values = _values
        self._number_of_points = len(_values)

    # is_quantitative
    def _is_quantitative(self):
        r"""Return `True`, if the dimension is quantitative, otherwise `False`.

        :returns: A Boolean.
        """
        return False

    def _get_python_dictionary(self):
        dictionary = {}

        dictionary["type"] = self._type

        if self._description.strip() != "":
            dictionary["description"] = self._description.strip()

        dictionary["values"] = self._coordinates.tolist()

        return dictionary

    # ----------------------------------------------------------------------- #
    #                        LabeledDimension Attributes                      #
    # ----------------------------------------------------------------------- #

    # values
    @property
    def values(self):
        r"""Return a list of values along the dimension."""
        return deepcopy(self._values)

    @values.setter
    def values(self, _values):
        self._get_coordinates(_values)

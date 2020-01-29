# -*- coding: utf-8 -*-
"""The MonotonicDimension sub type class."""
from __future__ import division
from __future__ import print_function

import warnings
from copy import deepcopy

import numpy as np

from csdmpy.dimensions.quantitative import BaseQuantitativeDimension
from csdmpy.dimensions.quantitative import ReciprocalVariable
from csdmpy.units import ScalarQuantity
from csdmpy.utils import attribute_error
from csdmpy.utils import validate

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["MonotonicDimension"]

# =========================================================================== #
#                     ArbitrarilySampledDimension Class                       #
# =========================================================================== #


class MonotonicDimension(BaseQuantitativeDimension):
    r"""
    A monotonic grid dimension.

    .. warning ::
        This class should not be used directly. Instead,
        use the ``CSDM`` object to access the attributes
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

    __slots__ = ("reciprocal", "_count", "_values", "_coordinates")

    _type = "monotonic"

    def __init__(self, coordinates, **kwargs):
        """Instantiate a MonotonicDimension class."""
        _unit = ScalarQuantity(coordinates[0]).quantity.unit
        if "reciprocal" not in kwargs.keys():
            kwargs["reciprocal"] = {
                "increment": None,
                "coordinates_offset": None,
                "origin_offset": None,
                "period": None,
                "quantity_name": None,
                "label": "",
                "description": "",
                "application": {},
            }
        super(MonotonicDimension, self).__init__(unit=_unit, **kwargs)

        _reciprocal_unit = self._unit ** -1
        self.reciprocal = ReciprocalVariable(
            unit=_reciprocal_unit, **kwargs["reciprocal"]
        )

        self._get_coordinates(coordinates)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, MonotonicDimension):
            check = [
                self._count == other._count,
                np.all(self._coordinates == other._coordinates),
                self.reciprocal == other.reciprocal,
                # super class
                self._coordinates_offset == other._coordinates_offset,
                self._origin_offset == other._origin_offset,
                self._quantity_name == other._quantity_name,
                self._period == other._period,
                self._label == other._label,
                self._description == other._description,
                self._application == other._application,
                self._unit == other._unit,
                self._equivalencies == other._equivalencies,
            ]
            if False in check:
                return False
            return True
        return False

    # ----------------------------------------------------------------------- #
    #                                 Methods                                 #
    # ----------------------------------------------------------------------- #

    def _get_coordinates(self, values):
        _unit = self._unit
        _value = [
            ScalarQuantity(item, _unit).quantity.to(_unit).value for item in values
        ]
        _value = np.asarray(_value, dtype=np.float64) * _unit
        self._count = _value.size
        self._values = values
        self._coordinates = _value

    def to_dict(self):
        """Return MonotonicDimension as a python dictionary."""
        dictionary = {}

        dictionary["type"] = self.__class__._type

        if self._description.strip() != "":
            dictionary["description"] = self._description.strip()

        dictionary["coordinates"] = self._values
        dictionary.update(self._get_quantitative_dictionary())

        reciprocal_dictionary = {}
        if self.reciprocal._description.strip() != "":
            reciprocal_dictionary["description"] = self.reciprocal._description.strip()
        reciprocal_dictionary.update(self.reciprocal._get_quantitative_dictionary())
        if reciprocal_dictionary == {}:
            del reciprocal_dictionary
        else:
            dictionary["reciprocal"] = reciprocal_dictionary

        return dictionary

    # ----------------------------------------------------------------------- #
    #                                 Attributes                              #
    # ----------------------------------------------------------------------- #
    @property
    def type(self):
        """Return the type of the dimension."""
        return deepcopy(self._type)

    @property
    def count(self):
        r"""Total number of points along the linear dimension."""
        return deepcopy(self._count)

    @count.setter
    def count(self, value):
        value = validate(value, "count", int)
        if value > self.count:
            raise ValueError(
                f"Cannot set the count, {value}, more than the number of coordinates, "
                f"{self.count}, for the monotonic and labeled dimensions."
            )

        if value < self.count:
            warnings.warn(
                f"The number of coordinates, {self.count}, are truncated to {value}."
            )
            self._count = value

    @property
    def coordinates_offset(self):
        raise AttributeError(attribute_error(self, "coordinates_offset"))

    @property
    def coordinates(self):
        """Return the coordinates along the dimensions."""
        n = self._count
        return self._coordinates[:n]

    @coordinates.setter
    def coordinates(self, value):
        self._get_coordinates(value)

    @property
    def absolute_coordinates(self):
        """Return the absolute coordinates along the dimensions."""
        return (self.coordinates + self.origin_offset).to(self._unit)

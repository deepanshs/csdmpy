# -*- coding: utf-8 -*-
"""The MonotonicDimension sub type class."""
from __future__ import division
from __future__ import print_function

import warnings
from copy import deepcopy

import numpy as np

from csdmpy.dimensions.quantitative import BaseQuantitativeDimension
from csdmpy.dimensions.quantitative import ReciprocalVariable
from csdmpy.units import frequency_ratio
from csdmpy.units import ScalarQuantity
from csdmpy.utils import _axis_label
from csdmpy.utils import attribute_error
from csdmpy.utils import check_scalar_object
from csdmpy.utils import validate

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["MonotonicDimension"]

# =========================================================================== #
#                     MonotonicDimension Class                       #
# =========================================================================== #


class MonotonicDimension(BaseQuantitativeDimension):
    r"""
    A monotonic grid dimension.

    Generates an object representing a physical dimension whose coordinates are
    monotonically sampled along a grid dimension. See :ref:`monotonicDimension_uml`
    for details.
    """

    __slots__ = ("reciprocal", "_count", "_values", "_coordinates")

    _type = "monotonic"

    def __init__(self, coordinates, **kwargs):
        """Instantiate a MonotonicDimension class."""
        if isinstance(coordinates, np.ndarray):
            _unit = ScalarQuantity("1").quantity.unit
        else:
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
        super().__init__(unit=_unit, **kwargs)

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

    def __repr__(self):
        properties = ", ".join([f"{k}={v}" for k, v in self.to_dict().items()])
        return f"MonotonicDimension({properties})"

    def __str__(self):
        # properties = ", ".join([f"{k}={v}" for k, v in self.to_dict().items()])
        return f"MonotonicDimension({self.coordinates.__str__()})"

    def __mul__(self, other):
        """Multiply the dimension object by a scalar."""
        return _update_monotonic_dimension_object_by_scalar_(self.copy(), other)

    def __imul__(self, other):
        """Multiply the dimension object by a scalar, in-place."""
        return _update_monotonic_dimension_object_by_scalar_(self, other)

    def _get_coordinates(self, values):
        _unit = self._unit
        if not isinstance(values, np.ndarray):
            _value = [
                ScalarQuantity(item, _unit).quantity.to(_unit).value for item in values
            ]
        if isinstance(values, np.ndarray):
            _value = values * _unit

        _value = np.asarray(_value, dtype=np.float64) * _unit
        self._count = _value.size
        self._values = values
        self._coordinates = _value

    # ----------------------------------------------------------------------- #
    #                                 Attributes                              #
    # ----------------------------------------------------------------------- #
    @property
    def type(self):
        """Return the type of the dimension."""
        return deepcopy(self._type)

    @property
    def count(self):
        r"""Total number of points along the monotonic dimension."""
        return deepcopy(self._count)

    @count.setter
    def count(self, value):
        value = validate(value, "count", int)
        if value > self.count:
            raise ValueError(
                f"Cannot set the count, {value}, more than the number of coordinates, "
                f"{self.count}, for the monotonic dimensions."
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

        unit = self._unit
        equivalent_fn = self._equivalencies
        coordinates = self._coordinates[:n]
        if equivalent_fn is None:
            return coordinates.to(self._unit)
        if equivalent_fn == "nmr_frequency_ratio":
            denominator = self.origin_offset - coordinates[0]
            if denominator.value == 0:
                raise ZeroDivisionError("Cannot convert the coordinates to ppm.")
            return coordinates.to(unit, frequency_ratio(denominator))
        return coordinates.to(unit, equivalent_fn)

    @coordinates.setter
    def coordinates(self, value):
        self._get_coordinates(value)

    @property
    def absolute_coordinates(self):
        """Return the absolute coordinates along the dimensions."""
        return (self.coordinates + self.origin_offset).to(self._unit)

    @property
    def axis_label(self):
        """Return a formatted string for displaying label along the dimension axis."""
        if self.label.strip() == "":
            label = self.quantity_name
        else:
            label = self.label
        return _axis_label(label, self._unit)

    # ----------------------------------------------------------------------- #
    #                                 Methods                                 #
    # ----------------------------------------------------------------------- #

    def to_dict(self):
        """Return the MonotonicDimension as a python dictionary."""
        dictionary = {}

        dictionary["type"] = self.__class__._type

        if self._description.strip() != "":
            dictionary["description"] = self._description.strip()

        dictionary["coordinates"] = self._values
        dictionary.update(self._to_dict())

        reciprocal_dictionary = {}
        if self.reciprocal._description.strip() != "":
            reciprocal_dictionary["description"] = self.reciprocal._description.strip()
        reciprocal_dictionary.update(self.reciprocal._to_dict())
        if reciprocal_dictionary == {}:
            del reciprocal_dictionary
        else:
            dictionary["reciprocal"] = reciprocal_dictionary

        return dictionary

    def copy(self):
        """Return a copy of the object."""
        return deepcopy(self)


def _update_monotonic_dimension_object_by_scalar_(object_, other):
    """Update object by multiplying by a scalar."""
    other = check_scalar_object(other)

    object_._coordinates *= other
    object_._values = [str(item) for item in object_._coordinates]
    object_._coordinates_offset *= other
    object_._origin_offset *= other
    object_._period *= other
    object_._unit *= object_._coordinates.unit
    object_._quantity_name = object_._unit.physical_type
    object_._equivalencies = None
    _reciprocal_unit = object_._unit ** -1
    object_.reciprocal = ReciprocalVariable(unit=_reciprocal_unit)
    return object_

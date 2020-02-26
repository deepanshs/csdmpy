# -*- coding: utf-8 -*-
"""The MonotonicDimension sub type class."""
from __future__ import division
from __future__ import print_function

import json
from copy import deepcopy

import numpy as np
from astropy.units import Quantity

from csdmpy.dimensions.base import _copy_core_metadata
from csdmpy.dimensions.base import check_count
from csdmpy.dimensions.quantitative import BaseQuantitativeDimension
from csdmpy.dimensions.quantitative import ReciprocalDimension
from csdmpy.units import frequency_ratio
from csdmpy.units import scalar_quantity_format
from csdmpy.units import ScalarQuantity
from csdmpy.utils import _axis_label
from csdmpy.utils import attribute_error
from csdmpy.utils import check_scalar_object


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
        if isinstance(coordinates, Quantity):
            _unit = coordinates.unit
        elif isinstance(coordinates, np.ndarray):
            _unit = Quantity(1, "").unit
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
        self.reciprocal = ReciprocalDimension(
            unit=_reciprocal_unit, **kwargs["reciprocal"]
        )

        self._get_coordinates(coordinates)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if hasattr(other, "subtype"):
            other = other.subtype
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
            if np.all(check):
                return True
        return False

    def __repr__(self):
        properties = ", ".join(
            [
                f"coordinates={self._coordinates.__str__()}",
                *[
                    f"{k}={v}"
                    for k, v in self.to_dict().items()
                    if k not in ["type", "coordinates"]
                ],
            ]
        )
        return f"MonotonicDimension({properties})"

    def __str__(self):
        return f"MonotonicDimension({self.coordinates.__str__()})"

    def __mul__(self, other):
        """Multiply the MonotonicDimension object by a scalar."""
        return _update_monotonic_dimension_object_by_scalar(self.copy(), other, "mul")

    def __imul__(self, other):
        """Multiply the MonotonicDimension object by a scalar, in-place."""
        return _update_monotonic_dimension_object_by_scalar(self, other, "mul")

    def __truediv__(self, other):
        """Divide the MonotonicDimension object by a scalar."""
        return _update_monotonic_dimension_object_by_scalar(
            self.copy(), other, "truediv"
        )

    def __itruediv__(self, other):
        """Divide the MonotonicDimension object by a scalar, in-place."""
        return _update_monotonic_dimension_object_by_scalar(self, other, "truediv")

    def _get_coordinates(self, values):
        _unit = self._unit
        if isinstance(values, list):
            _coordinates = [
                ScalarQuantity(item, _unit).quantity.to(_unit).value for item in values
            ]
            self._coordinates = np.asarray(_coordinates, dtype=np.float64) * _unit
            self._values = values
            self._count = self._coordinates.size
            return

        if isinstance(values, Quantity):
            self._coordinates = values
        elif isinstance(values, np.ndarray):
            self._coordinates = values * _unit

        unit = scalar_quantity_format(self._coordinates[0], numerical_value=False)
        self._values = [f"{item.value} {unit}" for item in self._coordinates]
        self._count = self._coordinates.size

    # ----------------------------------------------------------------------- #
    #                                 Attributes                              #
    # ----------------------------------------------------------------------- #
    @property
    def type(self):
        """Return the type of the dimension."""
        return self.__class__._type

    @property
    def count(self):
        r"""Total number of points along the monotonic dimension."""
        return self._count

    @count.setter
    def count(self, value):
        self._count = check_count(value, self._count, "monotonic")

    @property
    def coordinates_offset(self):
        raise AttributeError(attribute_error(self, "coordinates_offset"))

    @property
    def coordinates(self):
        """Return the coordinates along the dimensions."""
        n = self._count
        coordinates = self._coordinates[:n]

        equivalent_fn = self._equivalencies

        if equivalent_fn is None:
            return coordinates.to(self._unit)

        equivalent_unit = self._equivalent_unit
        if equivalent_fn == "nmr_frequency_ratio":
            denominator = self.origin_offset - coordinates[0]
            if denominator.value == 0:
                raise ZeroDivisionError("Cannot convert the coordinates to ppm.")
            return coordinates.to(equivalent_unit, frequency_ratio(denominator))

        return coordinates.to(equivalent_unit, equivalent_fn)

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
        unit = (
            self._equivalent_unit if self._equivalent_unit is not None else self._unit
        )
        return _axis_label(label, unit)

    @property
    def data_structure(self):
        """Json serialized string describing the MonotonicDimension class instance."""
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=False, indent=2)

    # ----------------------------------------------------------------------- #
    #                                 Methods                                 #
    # ----------------------------------------------------------------------- #

    def _copy_metadata(self, obj, copy=False):
        """Copy MonotonicDimension metadata."""
        if hasattr(obj, "subtype"):
            obj = obj.subtype
        if isinstance(obj, MonotonicDimension):
            _copy_core_metadata(self, obj, "monotonic")

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


def _update_monotonic_dimension_object_by_scalar(object_, other, type_):
    """Update object by multiplying by a scalar."""
    other = check_scalar_object(other)

    if type_ == "mul":
        object_._coordinates *= other
        object_._coordinates_offset *= other
        object_._origin_offset *= other
        object_._period *= other

    if type_ == "truediv":
        object_._coordinates /= other
        object_._coordinates_offset /= other
        object_._origin_offset /= other
        object_._period /= other

    object_._values = [str(item) for item in object_._coordinates]
    object_._unit = object_._coordinates.unit
    object_._quantity_name = object_._unit.physical_type
    object_._equivalencies = None
    _reciprocal_unit = object_._unit ** -1
    object_.reciprocal = ReciprocalDimension(unit=_reciprocal_unit)
    return object_

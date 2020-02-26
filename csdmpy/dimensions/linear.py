# -*- coding: utf-8 -*-
"""The LinearDimension sub type class."""
from __future__ import division
from __future__ import print_function

import json
from copy import deepcopy

import numpy as np
from astropy.units import Quantity

from csdmpy.dimensions.base import _copy_core_metadata
from csdmpy.dimensions.quantitative import BaseQuantitativeDimension
from csdmpy.dimensions.quantitative import ReciprocalDimension
from csdmpy.units import frequency_ratio
from csdmpy.units import ScalarQuantity
from csdmpy.utils import _axis_label
from csdmpy.utils import check_and_assign_bool
from csdmpy.utils import check_scalar_object
from csdmpy.utils import validate

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["LinearDimension"]

# =========================================================================== #
#                          LinearDimension Class                              #
# =========================================================================== #


class LinearDimension(BaseQuantitativeDimension):
    r"""
    LinearDimension class.

    Generates an object representing a physical dimension whose coordinates are
    uniformly sampled along a grid dimension. See :ref:`linearDimension_uml` for
    details.
    """

    __slots__ = ("_count", "_increment", "_complex_fft", "reciprocal", "_coordinates")

    _type = "linear"

    def __init__(self, count, increment, complex_fft=False, **kwargs):
        r"""Instantiate a DimensionWithLinearSpacing class instance."""
        self._count = count
        self._increment = ScalarQuantity(increment).quantity
        self._complex_fft = check_and_assign_bool(complex_fft)
        _unit = self._increment.unit
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

        # create a reciprocal dimension
        _reciprocal_unit = self._unit ** -1
        self.reciprocal = ReciprocalDimension(
            unit=_reciprocal_unit, **kwargs["reciprocal"]
        )
        self._get_coordinates()

    def __repr__(self):
        properties = ", ".join(
            [f"{k}={v}" for k, v in self.to_dict().items() if k != "type"]
        )
        return f"LinearDimension({properties})"

    def __str__(self):
        return f"LinearDimension({self.coordinates.__str__()})"

    def __eq__(self, other):
        """Overrides the default implementation"""
        if hasattr(other, "subtype"):
            other = other.subtype
        if isinstance(other, LinearDimension):
            check = [
                self._count == other._count,
                self._increment == other._increment,
                self._complex_fft == other._complex_fft,
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

    def __mul__(self, other):
        """Multiply the LinearDimension object by a scalar."""
        return _update_linear_dimension_object_by_scalar(self.copy(), other, "mul")

    def __imul__(self, other):
        """Multiply the LinearDimension object by a scalar, in-place."""
        return _update_linear_dimension_object_by_scalar(self, other, "mul")

    def __truediv__(self, other):
        """Divide the LinearDimension object by a scalar."""
        return _update_linear_dimension_object_by_scalar(self.copy(), other, "truediv")

    def __itruediv__(self, other):
        """Divide the LinearDimension object by a scalar, in-place."""
        return _update_linear_dimension_object_by_scalar(self, other, "truediv")

    def _swap(self):
        self._description, self.reciprocal._description = (
            self.reciprocal._description,
            self._description,
        )

        self._application, self.reciprocal._application = (
            self.reciprocal._application,
            self._application,
        )

        self._coordinates_offset, self.reciprocal._coordinates_offset = (
            self.reciprocal._coordinates_offset,
            self._coordinates_offset,
        )

        self._origin_offset, self.reciprocal._origin_offset = (
            self.reciprocal._origin_offset,
            self._origin_offset,
        )

        self._period, self.reciprocal._period = (self.reciprocal._period, self._period)

        self._quantity_name, self.reciprocal._quantity_name = (
            self.reciprocal._quantity_name,
            self._quantity_name,
        )

        self._label, self.reciprocal._label = (self.reciprocal._label, self._label)

        self._unit, self.reciprocal._unit = self.reciprocal._unit, self._unit

    def _get_coordinates(self):
        _unit = self._unit
        _count = self._count
        _increment = self._increment.to(_unit)

        _index = np.arange(_count, dtype=np.float64)

        if self._complex_fft:
            _index -= int(_count / 2)

        self._coordinates = _index * _increment

    # ----------------------------------------------------------------------- #
    #                                  Attributes                             #
    # ----------------------------------------------------------------------- #
    @property
    def type(self):
        """Return the type of the dimension."""
        return deepcopy(self.__class__._type)

    @property
    def count(self):
        r"""Total number of points along the linear dimension."""
        return deepcopy(self._count)

    @count.setter
    def count(self, value):
        value = validate(value, "count", int)
        self._count = value
        self._get_coordinates()
        return

    @property
    def increment(self):
        r"""Increment along the linear dimension."""
        return deepcopy(self._increment)

    @increment.setter
    def increment(self, value):
        allowed_types = (Quantity, str, ScalarQuantity)
        value = validate(value, "increment", allowed_types)
        self._increment = ScalarQuantity(value, self._unit).quantity
        self._get_coordinates()

    @property
    def complex_fft(self):
        """If True, orders the coordinates according to FFT output order."""
        return deepcopy(self._complex_fft)

    @complex_fft.setter
    def complex_fft(self, value):
        self._complex_fft = validate(value, "complex_fft", bool)
        self._get_coordinates()

    @property
    def coordinates(self):
        """Return the coordinates along the dimensions."""
        n = self._count
        coordinates = self._coordinates[:n] + self.coordinates_offset

        equivalent_fn = self._equivalencies

        if equivalent_fn is None:
            return coordinates.to(self._unit)

        equivalent_unit = self._equivalent_unit
        if equivalent_fn == "nmr_frequency_ratio":
            denominator = self.origin_offset - self.coordinates_offset
            if denominator.value == 0:
                raise ZeroDivisionError("Cannot convert the coordinates to ppm.")
            return coordinates.to(equivalent_unit, frequency_ratio(denominator))

        return coordinates.to(equivalent_unit, equivalent_fn)

    @coordinates.setter
    def coordinates(self, value):
        raise AttributeError(
            "The attribute cannot be modifed for Dimension objects with `linear` "
            "type. Use the `count`, `increment` or `coordinates_offset` attributes"
            " to update the coordinate along the linear dimension."
        )

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
        """Json serialized string describing the LinearDimension class instance."""
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=False, indent=2)

    # ----------------------------------------------------------------------- #
    #                                 Methods                                 #
    # ----------------------------------------------------------------------- #

    def _copy_metadata(self, obj, copy=False):
        """Copy LinearDimension metadata."""
        if hasattr(obj, "subtype"):
            obj = obj.subtype
        if isinstance(obj, LinearDimension):
            _copy_core_metadata(self, obj, "linear")

    def to_dict(self):
        """Return the LinearDimension as a python dictionary."""
        obj = {}
        obj["type"] = self.__class__._type

        if self._description.strip() != "":
            obj["description"] = self._description.strip()

        obj["count"] = self._count
        obj["increment"] = str(ScalarQuantity(self.increment))
        obj.update(self._to_dict())

        if self.complex_fft:
            obj["complex_fft"] = True

        # reciprocal dictionary
        reciprocal_obj = {}
        if self.reciprocal._description.strip() != "":
            reciprocal_obj["description"] = self.reciprocal._description
        reciprocal_obj.update(self.reciprocal._to_dict())
        if reciprocal_obj == {}:
            del reciprocal_obj
        else:
            obj["reciprocal"] = reciprocal_obj

        return obj

    def copy(self):
        """Return a copy of the object."""
        return deepcopy(self)


def _update_linear_dimension_object_by_scalar(object_, other, type_="mul"):
    """Update object by multiplying by a scalar."""
    other = check_scalar_object(other)

    if type_ == "mul":
        object_._increment *= other
        object_._coordinates *= other
        object_._coordinates_offset *= other
        object_._origin_offset *= other
        object_._period *= other

    if type_ == "truediv":
        object_._increment /= other
        object_._coordinates /= other
        object_._coordinates_offset /= other
        object_._origin_offset /= other
        object_._period /= other

    object_._unit = object_._increment._unit
    object_._quantity_name = object_._unit.physical_type
    object_._equivalencies = None
    _reciprocal_unit = object_._unit ** -1
    object_.reciprocal = ReciprocalDimension(unit=_reciprocal_unit)
    return object_

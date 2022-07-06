"""The LinearDimension sub type class."""
import numpy as np
from astropy.units import Quantity

from csdmpy.dimension.base import _copy_core_metadata
from csdmpy.dimension.quantitative import BaseQuantitativeDimension
from csdmpy.dimension.quantitative import ReciprocalDimension
from csdmpy.units import frequency_ratio
from csdmpy.units import ScalarQuantity
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
    """LinearDimension class.

    Generates an object representing a physical dimension whose coordinates are
    uniformly sampled along a grid dimension. See :ref:`linearDimension_uml` for
    details.
    """

    __slots__ = ("_count", "_increment", "_complex_fft", "reciprocal", "_coordinates")

    _type = "linear"

    def __init__(self, count, increment, complex_fft=False, **kwargs):
        """Instantiate a DimensionWithLinearSpacing class instance."""
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
                "application": None,
            }

        super().__init__(unit=_unit, **kwargs)

        # create a reciprocal dimension
        r_unit = self._unit**-1
        self.reciprocal = ReciprocalDimension(unit=r_unit, **kwargs["reciprocal"])
        self._get_coordinates()

    def __repr__(self):
        meta = [f"{k}={v}" for k, v in self.dict().items() if k != "type"]
        properties = ", ".join(meta)
        return f"LinearDimension({properties})"

    def __str__(self):
        return f"LinearDimension({self.coordinates.__str__()})"

    def __eq__(self, other):
        """Overrides the default implementation"""
        other = other.subtype if hasattr(other, "subtype") else other
        if not isinstance(other, LinearDimension):
            return False
        check = [getattr(self, _) == getattr(other, _) for _ in __class__.__slots__[:4]]
        check += [super().__eq__(other)]
        return np.all(check)

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
        """Swap the value between the dimension and reciprocal dimension object."""
        attrs = [
            "_description",
            "_application",
            "_coordinates_offset",
            "_origin_offset",
            "_period",
            "_quantity_name",
            "_label",
            "_unit",
            "_equivalent_unit",
        ]
        for item in attrs:
            val = getattr(self, item)
            r_val = getattr(self.reciprocal, item)
            setattr(self, item, r_val)
            setattr(self.reciprocal, item, val)

    def _get_coordinates(self):
        index = np.arange(self._count, dtype=np.float64)
        index -= int(self._count / 2) if self._complex_fft else 0
        self._coordinates = index * self._increment.to(self._unit)

    # ----------------------------------------------------------------------- #
    #                                  Attributes                             #
    # ----------------------------------------------------------------------- #
    @property
    def type(self):
        """Return the type of the dimension."""
        return self.__class__._type

    @property
    def count(self):
        """Total number of points along the linear dimension."""
        return self._count

    @count.setter
    def count(self, value):
        value = validate(value, "count", int)
        self._count = value
        self._get_coordinates()

    @property
    def increment(self):
        """Increment along the linear dimension."""
        return self._increment

    @increment.setter
    def increment(self, value):
        allowed_types = (Quantity, str, ScalarQuantity)
        value = validate(value, "increment", allowed_types)
        self._increment = ScalarQuantity(value, self._unit).quantity
        self._get_coordinates()

    @property
    def complex_fft(self):
        """If True, orders the coordinates according to FFT output order."""
        return self._complex_fft

    @complex_fft.setter
    def complex_fft(self, value):
        self._complex_fft = validate(value, "complex_fft", bool)
        self._get_coordinates()

    @property
    def coordinates(self):
        """Return the coordinates along the dimensions."""
        coordinates = self._coordinates[: self._count] + self.coordinates_offset

        equivalent_fn = self._equivalencies
        equivalent_unit = self._equivalent_unit

        if equivalent_fn is None or equivalent_unit is None:
            return coordinates.to(self._unit)

        if equivalent_fn == "nmr_frequency_ratio":
            denominator = self.origin_offset - self.get_nmr_reference_offset()
            if denominator.value == 0:
                raise ZeroDivisionError("Cannot convert the coordinates to ppm.")
            return coordinates.to(equivalent_unit, frequency_ratio(denominator))

        return coordinates.to(equivalent_unit, equivalent_fn)

    @coordinates.setter
    def coordinates(self, value):
        raise AttributeError(
            "The attribute cannot be modified for Dimension objects with `linear` "
            "type. Use the `count`, `increment` or `coordinates_offset` attributes"
            " to update the coordinate along the linear dimension."
        )

    def get_nmr_reference_offset(self):
        """Calculate reference offset for NMR datasets."""
        if self.complex_fft:
            return self.coordinates_offset

        if self.count % 2 != 0:  # odd count
            return self.coordinates_offset + (self.count - 1) * self.increment / 2.0

        # even count
        count = self.count / 2
        if self.increment > 0:  # positive increment
            return self.coordinates_offset + count * self.increment

        # negative increment
        return self.coordinates_offset + (count - 1) * self.increment

    # ----------------------------------------------------------------------- #
    #                                 Methods                                 #
    # ----------------------------------------------------------------------- #

    def _copy_metadata(self, obj):
        """Copy LinearDimension metadata."""
        obj = obj.subtype if hasattr(obj, "subtype") else obj
        if isinstance(obj, LinearDimension):
            _copy_core_metadata(self, obj, "linear")

    def dict(self):
        """Return the LinearDimension as a python dictionary."""
        obj = {}
        obj["type"] = self.__class__._type
        obj["count"] = self._count
        obj["increment"] = str(ScalarQuantity(self.increment))
        obj.update(super().dict())

        if self.complex_fft:
            obj["complex_fft"] = True

        reciprocal_obj = self.reciprocal.dict()
        if reciprocal_obj != {}:
            obj["reciprocal"] = reciprocal_obj

        return obj

    def reciprocal_coordinates(self):
        """Return reciprocal coordinates assuming Nyquist-Shannon theorem."""
        coordinates_offset = self.reciprocal._coordinates_offset
        return self._reciprocal_coordinates() + coordinates_offset

    def _reciprocal_coordinates(self):
        """Return reciprocal coordinates assuming Nyquist-Shannon theorem
        without the coordinates offset."""
        count = self._count
        increment = 1.0 / (count * self._increment)
        coordinates = np.arange(count) * increment
        return (
            coordinates
            if self.complex_fft
            else (coordinates - int(count / 2) * increment)
        )

    def reciprocal_increment(self):
        """Return reciprocal increment assuming Nyquist-Shannon theorem."""
        return 1.0 / (self._count * self._increment)


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
    _reciprocal_unit = object_._unit**-1
    object_.reciprocal = ReciprocalDimension(unit=_reciprocal_unit)
    return object_

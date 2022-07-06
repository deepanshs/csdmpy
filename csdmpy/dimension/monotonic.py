"""The MonotonicDimension sub type class."""
import numpy as np
from astropy.units import Quantity

from csdmpy.dimension.base import _copy_core_metadata
from csdmpy.dimension.base import check_count
from csdmpy.dimension.quantitative import BaseQuantitativeDimension
from csdmpy.dimension.quantitative import ReciprocalDimension
from csdmpy.units import frequency_ratio
from csdmpy.units import scalar_quantity_format
from csdmpy.units import ScalarQuantity
from csdmpy.utils import check_scalar_object


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["MonotonicDimension"]

# =================================================================================== #
#                            MonotonicDimension Class                                 #
# =================================================================================== #


class MonotonicDimension(BaseQuantitativeDimension):
    """Monotonic grid dimension.

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
                "application": None,
            }
        super().__init__(unit=_unit, **kwargs)

        r_unit = self._unit**-1
        self.reciprocal = ReciprocalDimension(unit=r_unit, **kwargs["reciprocal"])
        self._get_coordinates(coordinates)

    def __eq__(self, other):
        other = other.subtype if hasattr(other, "subtype") else other
        if not isinstance(other, MonotonicDimension):
            return False

        check = [
            self._count == other._count,
            np.all(self._coordinates == other._coordinates),
            self.reciprocal == other.reciprocal,
            super().__eq__(other),
        ]
        return np.all(check)

    def __repr__(self):
        meta = [
            f"{k}={v}"
            for k, v in self.dict().items()
            if k not in ["type", "coordinates"]
        ]
        properties = ", ".join([f"coordinates={self._coordinates.__str__()}", *meta])
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

        self._coordinates = values if isinstance(values, Quantity) else values * _unit
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
        raise AttributeError(
            f"`{self.__class__.__name__}` has no attribute `coordinates_offset`."
        )

    @property
    def coordinates(self):
        """Return the coordinates along the dimensions."""
        coordinates = self._coordinates[: self._count]
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

    # ------------------------------------------------------------------------------- #
    #                                     Methods                                     #
    # ------------------------------------------------------------------------------- #

    def _copy_metadata(self, obj):
        """Copy MonotonicDimension metadata."""
        obj = obj.subtype if hasattr(obj, "subtype") else obj
        if isinstance(obj, MonotonicDimension):
            _copy_core_metadata(self, obj, "monotonic")

    def dict(self):
        """Return the MonotonicDimension as a python dictionary."""
        dictionary = {}
        dictionary["type"] = self.__class__._type
        dictionary["coordinates"] = self._values
        dictionary.update(super().dict())
        reciprocal_dictionary = self.reciprocal.dict()
        if reciprocal_dictionary != {}:
            dictionary["reciprocal"] = reciprocal_dictionary

        return dictionary


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
    _reciprocal_unit = object_._unit**-1
    object_.reciprocal = ReciprocalDimension(unit=_reciprocal_unit)
    return object_

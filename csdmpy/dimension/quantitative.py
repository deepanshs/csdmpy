"""Base Quantitative class."""
from copy import deepcopy

import numpy as np
from astropy.units import Quantity

from csdmpy.dimension.base import BaseDimension
from csdmpy.units import check_quantity_name
from csdmpy.units import ScalarQuantity
from csdmpy.utils import _axis_label
from csdmpy.utils import type_error
from csdmpy.utils import validate

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["BaseQuantitativeDimension", "ReciprocalDimension"]

ALLOWED_TYPES = (Quantity, str, ScalarQuantity)
# =========================================================================== #
#                          Base Quantitative Class                            #
# =========================================================================== #


class BaseQuantitativeDimension(BaseDimension):
    """A BaseQuantitativeDimension class."""

    __slots__ = (
        "_coordinates_offset",
        "_origin_offset",
        "_quantity_name",
        "_period",
        "_unit",
        "_equivalent_unit",
        "_equivalencies",
    )

    def __init__(
        self,
        description="",
        application=None,
        coordinates_offset=None,
        origin_offset=None,
        quantity_name=None,
        period=None,
        label="",
        unit=None,
        **kwargs,
    ):
        """Instantiate a BaseIndependentVariable class."""

        super().__init__(label, application, description)

        self._coordinates_offset = ScalarQuantity(coordinates_offset, unit).quantity
        self._origin_offset = ScalarQuantity(origin_offset, unit).quantity
        self._quantity_name = check_quantity_name(quantity_name, unit)

        value = ScalarQuantity(period, unit).quantity
        self._period = np.inf * value.unit if value.value == 0.0 else value

        self._unit = unit
        self._equivalent_unit = None
        self._equivalencies = None

    def __eq__(self, other):
        check = [getattr(self, _) == getattr(other, _) for _ in __class__.__slots__]
        check += [super().__eq__(other)]
        return np.all(check)

    # ----------------------------------------------------------------------- #
    #                                Attributes                               #
    # ----------------------------------------------------------------------- #

    @property
    def coordinates_offset(self):
        """Value at index zero, :math:`c_k`, along the dimension."""
        return deepcopy(self._coordinates_offset)

    @coordinates_offset.setter
    def coordinates_offset(self, value):
        value = validate(value, "coordinates_offset", ALLOWED_TYPES)
        self._coordinates_offset = ScalarQuantity(value, self._unit).quantity

    @property
    def origin_offset(self):
        """Origin offset, :math:`o_k`, along the dimension."""
        return deepcopy(self._origin_offset)

    @origin_offset.setter
    def origin_offset(self, value):
        value = validate(value, "origin_offset", ALLOWED_TYPES)
        self._origin_offset = ScalarQuantity(value, self._unit).quantity

    @property
    def period(self):
        """Period of the data along this dimension."""
        return deepcopy(self._period)

    @period.setter
    def period(self, value=None):
        value = str(value) if isinstance(value, Quantity) else value
        if not isinstance(value, str):
            raise TypeError(type_error(str, "period", value))

        lst = ["inf", "Inf", "infinity", "Infinity", "∞"]
        is_inf = value.strip().split()[0] in lst
        self._period = (
            np.inf * self._unit
            if is_inf
            else ScalarQuantity(value, self._unit).quantity
        )

    @property
    def quantity_name(self):
        """Quantity name associated with this dimension."""
        return deepcopy(str(self._quantity_name))

    @quantity_name.setter
    def quantity_name(self, value):
        raise NotImplementedError("This attribute is not yet implemented.")

    @property
    def absolute_coordinates(self):
        """Return the absolute coordinates along the dimensions."""
        return (self.coordinates + self.origin_offset).to(self._unit)

    @property
    def axis_label(self):
        """Return a formatted string for displaying label along the dimension axis."""
        label = self.quantity_name if self.label.strip() == "" else self.label
        unit = self._equivalent_unit or self._unit
        return _axis_label(label, unit)

    # ----------------------------------------------------------------------- #
    #                                  Methods                                #
    # ----------------------------------------------------------------------- #

    def dict(self):
        """Return the object as a python dictionary."""
        obj = {}

        if self._coordinates_offset.value != 0.0:
            obj["coordinates_offset"] = str(ScalarQuantity(self._coordinates_offset))

        if self._origin_offset.value != 0.0:
            obj["origin_offset"] = str(ScalarQuantity(self._origin_offset))

        if self._quantity_name not in [None, "unknown", "dimensionless"]:
            obj["quantity_name"] = self._quantity_name

        if self._period.value not in [0.0, np.inf]:
            obj["period"] = str(ScalarQuantity(self._period))

        obj.update(super().dict())
        return obj

    def is_quantitative(self):
        """Return `True`, if the dimension is quantitative, otherwise `False`.
        :returns: A Boolean.
        """
        return True

    def to(self, unit="", equivalencies=None):
        """Convert the unit to given value `unit`."""
        unit = validate(unit, "unit", str)
        if equivalencies is None:
            self._unit = ScalarQuantity(unit, self._unit).quantity.unit
            self._equivalent_unit = None
            self._equivalencies = None
            return

        # self._unit = ScalarQuantity(unit).quantity.unit
        self._equivalent_unit = ScalarQuantity(unit).quantity.unit
        self._equivalencies = equivalencies


# =========================================================================== #
#                           ReciprocalDimension Class                         #
# =========================================================================== #


class ReciprocalDimension(BaseQuantitativeDimension):
    """ReciprocalDimension class."""

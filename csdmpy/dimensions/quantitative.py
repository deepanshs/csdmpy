# -*- coding: utf-8 -*-
"""Base Quantitative class."""
from copy import deepcopy

from astropy.units import Quantity
from numpy import inf

from csdmpy.dimensions.base import BaseDimension
from csdmpy.units import check_quantity_name
from csdmpy.units import ScalarQuantity
from csdmpy.utils import type_error
from csdmpy.utils import validate


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["BaseQuantitativeDimension", "ReciprocalDimension"]

# =========================================================================== #
#                          Base Quantitative Class                            #
# =========================================================================== #


class BaseQuantitativeDimension(BaseDimension):
    r"""A BaseQuantitativeDimension class."""

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
        application={},
        coordinates_offset=None,
        origin_offset=None,
        quantity_name=None,
        period=None,
        label="",
        unit=None,
        **kwargs,
    ):
        r"""Instantiate a BaseIndependentVariable class."""

        super().__init__(label, application, description)

        self._coordinates_offset = ScalarQuantity(coordinates_offset, unit).quantity
        self._origin_offset = ScalarQuantity(origin_offset, unit).quantity
        self._quantity_name = check_quantity_name(quantity_name, unit)

        value = ScalarQuantity(period, unit).quantity
        if value.value == 0.0:
            value = inf * value.unit
        self._period = value

        self._unit = unit
        self._equivalent_unit = None
        self._equivalencies = None

    def __eq__(self, other):
        """Overrides the default implementation"""
        check = [
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

    # ----------------------------------------------------------------------- #
    #                                Attributes                               #
    # ----------------------------------------------------------------------- #

    @property
    def coordinates_offset(self):
        r"""Value at index zero, :math:`c_k`, along the dimension."""
        return deepcopy(self._coordinates_offset)

    @coordinates_offset.setter
    def coordinates_offset(self, value):
        allowed_types = (Quantity, str, ScalarQuantity)
        value = validate(value, "coordinates_offset", allowed_types)
        value = ScalarQuantity(value, self._unit).quantity
        self._coordinates_offset = value

    @property
    def origin_offset(self):
        r"""Origin offset, :math:`o_k`, along the dimension."""
        return deepcopy(self._origin_offset)

    @origin_offset.setter
    def origin_offset(self, value):
        allowed_types = (Quantity, str, ScalarQuantity)
        value = validate(value, "origin_offset", allowed_types)
        self._origin_offset = ScalarQuantity(value, self._unit).quantity

    @property
    def period(self):
        r"""Period of the data along this dimension."""
        return deepcopy(self._period)

    @period.setter
    def period(self, value=None):
        if isinstance(value, Quantity):
            value = str(value)
        if not isinstance(value, str):
            raise TypeError(type_error(str, "period", value))

        lst = ["inf", "Inf", "infinity", "Infinity", "∞"]
        if value.strip().split()[0] in lst:
            value = inf * self._unit
            self._period = value
        else:
            self._period = ScalarQuantity(value, self._unit).quantity

    @property
    def quantity_name(self):
        r"""Quantity name associated with this dimension."""
        return deepcopy(self._quantity_name)

    @quantity_name.setter
    def quantity_name(self, value):
        raise NotImplementedError("This attribute is not yet implemented.")

    # ----------------------------------------------------------------------- #
    #                                  Methods                                #
    # ----------------------------------------------------------------------- #

    def _to_dict(self):
        r"""Return the object as a python dictionary."""
        obj = {}

        # The description key is added at the child class level.
        if self._coordinates_offset.value != 0.0:
            obj["coordinates_offset"] = str(ScalarQuantity(self._coordinates_offset))

        if self._origin_offset.value != 0.0:
            obj["origin_offset"] = str(ScalarQuantity(self._origin_offset))

        if self._quantity_name not in [None, "unknown", "dimensionless"]:
            obj["quantity_name"] = self._quantity_name

        if self._period.value not in [0.0, inf]:
            obj["period"] = str(ScalarQuantity(self._period))

        if self.label.strip() != "":
            obj["label"] = self.label

        if self._application != {}:
            obj["application"] = self._application

        return obj

    def is_quantitative(self):
        r"""Return `True`, if the dimension is quantitative, otherwise `False`.
        :returns: A Boolean.
        """
        return True

    def to(self, unit="", equivalencies=None):
        r"""Convert the unit to given value `unit`."""
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
    r"""Declare a ReciprocalDimension class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

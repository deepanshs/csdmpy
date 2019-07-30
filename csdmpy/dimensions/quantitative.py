# -*- coding: utf-8 -*-
from copy import deepcopy

from astropy.units import Quantity
from numpy import inf

from csdmpy.units import check_quantity_name
from csdmpy.units import ScalarQuantity
from csdmpy.utils import type_error
from csdmpy.utils import validate


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["BaseQuantitativeDimension", "ReciprocalVariable"]

# =========================================================================== #
#                          Base Quantitative Class                            #
# =========================================================================== #


class BaseQuantitativeDimension:
    r"""A BaseQuantitativeDimension class."""

    __slots__ = (
        "_coordinates_offset",
        "_origin_offset",
        "_quantity_name",
        "_period",
        "_label",
        "_description",
        "_application",
        "_unit",
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

        self._description = description
        self._application = application
        self._coordinates_offset = ScalarQuantity(coordinates_offset, unit).quantity
        self._origin_offset = ScalarQuantity(origin_offset, unit).quantity
        self._quantity_name = check_quantity_name(quantity_name, unit)

        value = ScalarQuantity(period, unit).quantity
        if value.value == 0.0:
            value = inf * value.unit
        self._period = value

        self.label = label
        self._unit = unit

    # ----------------------------------------------------------------------- #
    #                                Attributes                               #
    # ----------------------------------------------------------------------- #

    @property
    def application(self):
        """Return application metadata, if available."""
        return self._application

    @application.setter
    def application(self, value):
        self._application = validate(value, "application", dict)

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

    @property
    def label(self):
        r"""Label associated with this dimension."""
        return deepcopy(self._label)

    @label.setter
    def label(self, label=""):
        self._label = validate(label, "label", str)

    @property
    def description(self):
        r"""Brief description of the dimension object."""
        return deepcopy(self._description)

    @description.setter
    def description(self, value):
        self._description = validate(value, "description", str)

    # ----------------------------------------------------------------------- #
    #                                  Methods                                #
    # ----------------------------------------------------------------------- #

    def _get_quantitative_dictionary(self):
        r"""Return the object as a python dictionary."""
        obj = {}

        # The description key is added at the child class level.
        if self._coordinates_offset.value != 0.0:
            obj["coordinates_offset"] = ScalarQuantity(
                self._coordinates_offset
            ).format()

        if self._origin_offset.value != 0.0:
            obj["origin_offset"] = ScalarQuantity(self._origin_offset).format()

        if self._quantity_name not in [None, "unknown", "dimensionless"]:
            obj["quantity_name"] = self._quantity_name

        if self._period.value not in [0.0, inf]:
            obj["period"] = ScalarQuantity(self._period).format()

        if self.label.strip() != "":
            obj["label"] = self.label

        if self._application != {}:
            obj["application"] = self._application

        return obj

    def _is_quantitative(self):
        r"""Return `True`, if the dimension is quantitative, otherwise `False`.
        :returns: A Boolean.
        """
        return True

    def _to(self, unit="", equivalencies=None):
        r"""Convert the unit to given value `unit`."""
        unit = validate(unit, "unit", str)
        self._unit = ScalarQuantity(unit, self._unit).quantity.unit
        self._equivalencies = equivalencies


# =========================================================================== #
#                      ReciprocalVariable Dimension Class                     #
# =========================================================================== #


class ReciprocalVariable(BaseQuantitativeDimension):
    r"""Declare a ReciprocalVariable class."""

    pass

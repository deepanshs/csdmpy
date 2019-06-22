# -*- coding: utf-8 -*-
from copy import deepcopy

from astropy.units import Quantity
from numpy import inf

from csdfpy.units import check_quantity_name
from csdfpy.units import ScalarQuantity
from csdfpy.utils import _type_message


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


# =========================================================================== #
#               		   Base Quantitative Class      				      #
# =========================================================================== #


class BaseQuantitativeDimension:
    r"""Declare a BaseQuantitativeDimension class."""

    __slots__ = (
        "_index_zero_coordinate",
        "_origin_offset",
        "_quantity_name",
        "_period",
        "_label",
        "_description",
        "_application",
        "_equivalencies",
        "_unit",
    )

    def __init__(
        self,
        description="",
        application={},
        index_zero_coordinate=None,
        origin_offset=None,
        quantity_name=None,
        period=None,
        label="",
        unit=None,
        **kwargs,
    ):
        r"""Instantiate a BaseIndependentVariable class instance."""

        # description
        self._description = description

        # application
        self._application = application

        # unit
        self._unit = unit

        # reference Offset
        value = ScalarQuantity(index_zero_coordinate, unit).quantity
        self._index_zero_coordinate = value

        # origin offset
        value = ScalarQuantity(origin_offset, unit).quantity
        self._origin_offset = value

        # period
        value = ScalarQuantity(period, unit).quantity
        if value.value == 0.0:
            value = inf * value.unit
        self._period = value

        # quantity_name
        value = check_quantity_name(quantity_name, unit)
        self._quantity_name = value

        # label
        self.label = label

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
    def index_zero_coordinate(self):
        r"""Value at index zero, :math:`c_k`, along the dimension."""
        return deepcopy(self._index_zero_coordinate)

    @index_zero_coordinate.setter
    def index_zero_coordinate(self, value):
        if isinstance(value, Quantity):
            value = str(value)
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))

        value = ScalarQuantity(value, self._unit).quantity
        self._index_zero_coordinate = value

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

        value = ScalarQuantity(value, self._unit).quantity
        self._origin_offset = value

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
            self._period = ScalarQuantity(value, self._unit).quantity

    # quantity_name
    @property
    def quantity_name(self):
        r"""Quantity name associated with this dimension."""
        return deepcopy(self._quantity_name)

    @quantity_name.setter
    def quantity_name(self, value):
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
        obj = {}

        # The description key is added to the child class.
        if self._index_zero_coordinate.value != 0.0:
            obj["index_zero_coordinate"] = ScalarQuantity(
                self._index_zero_coordinate
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

        self._unit = ScalarQuantity(unit, self._unit).quantity.unit
        self._equivalencies = equivalencies


# =========================================================================== #
#                      ReciprocalVariable Dimension Class                     #
# =========================================================================== #


class ReciprocalVariable(BaseQuantitativeDimension):
    r"""Declare a ReciprocalVariable class."""

    pass

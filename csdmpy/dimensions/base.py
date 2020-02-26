# -*- coding: utf-8 -*-
import warnings
from copy import deepcopy

from csdmpy.utils import validate


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


class BaseDimension:
    """Base dimension class."""

    __slots__ = ("_label", "_description", "_application")

    def __init__(self, label, application, description):
        self._description = description
        self._application = application
        self._label = label

    @property
    def label(self):
        r"""Label associated with the dimension."""
        return deepcopy(self._label)

    @label.setter
    def label(self, label=""):
        self._label = validate(label, "label", str)

    @property
    def application(self):
        r"""Return an application dimension associated with the dimensions."""
        return self._application

    @application.setter
    def application(self, value):
        self._application = validate(value, "application", dict)

    @property
    def description(self):
        r"""Return a description of the dimension."""
        return deepcopy(self._description)

    @description.setter
    def description(self, value):
        self._description = validate(value, "description", str)


def check_count(value, total_count, dimension_type):
    """check the value for count."""
    value = validate(value, "count", int)
    if value > total_count:
        raise ValueError(
            f"Cannot set the count, {value}, more than the number of coordinates, "
            f"{total_count}, for the {dimension_type} dimensions."
        )

    if value < total_count:
        warnings.warn(f"The number of labels, {total_count}, are truncated to {value}.")

    return value


def _copy_core_metadata(obj1, obj2, dimension_type):
    """copy metadata from obj2 to obj1."""
    obj1._description = obj2._description
    obj1._application = obj2._application
    obj1._label = obj2._label

    if dimension_type == "labeled":
        return

    obj1._origin_offset = obj2._origin_offset
    obj1._period = obj2._period
    obj1.reciprocal = obj2.reciprocal
    obj1._equivalent_unit = obj2._equivalent_unit
    obj1._equivalencies = obj2._equivalencies

    if dimension_type == "monotonic":
        return

    obj1._complex_fft = obj2._complex_fft
    return

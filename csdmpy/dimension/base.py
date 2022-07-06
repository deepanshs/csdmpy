"""Base Dimension class"""
import json
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

    def __eq__(self, other):
        """Check if two objects are equal"""
        check = [getattr(self, _) == getattr(other, _) for _ in __class__.__slots__]
        return False if False in check else True

    @property
    def label(self):
        """Label associated with the dimension."""
        return deepcopy(self._label)

    @label.setter
    def label(self, label=""):
        self._label = validate(label, "label", str)

    @property
    def application(self):
        """Return an application dimension associated with the dimensions."""
        return self._application

    @application.setter
    def application(self, value):
        self._application = validate(value, "application", (dict, type(None)))

    @property
    def description(self):
        """Return a description of the dimension."""
        return deepcopy(self._description)

    @description.setter
    def description(self, value):
        self._description = validate(value, "description", str)

    @property
    def coordinates(self):
        """Dimension coordinates"""

    @coordinates.setter
    def coordinates(self, value):
        pass

    @property
    def coords(self):
        """Alias for the `coordinates` attribute."""
        return self.coordinates

    @coords.setter
    def coords(self, value):
        self.coordinates = value

    @property
    def axis_label(self):
        """Return a formatted string for displaying label along the dimension axis."""
        return self.label

    def to_dict(self):
        """Alias to the `dict()` method of the class."""
        return self.dict()

    def dict(self):
        """Return BaseDimension as a python dictionary"""
        obj = {}
        obj["label"] = self._label.strip()
        obj["description"] = self._description.strip()
        obj["application"] = self._application
        _ = [
            obj.pop(item) for item in [k for k, v in obj.items() if v in ["", {}, None]]
        ]
        return obj

    def copy(self):
        """Return a copy of the object."""
        return deepcopy(self)

    @property
    def data_structure(self):
        """Json serialized string describing the Dimension object class instance."""
        return json.dumps(self.dict(), ensure_ascii=False, sort_keys=False, indent=2)


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

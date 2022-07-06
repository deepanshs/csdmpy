from collections.abc import MutableSequence

import numpy as np

from .dependent_variable import DependentVariable
from .dimension import Dimension
from .dimension import LabeledDimension
from .dimension import LinearDimension
from .dimension import MonotonicDimension

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"

__all__ = ["DimensionList", "DependentVariableList"]

__dimensions_list__ = (Dimension, LinearDimension, MonotonicDimension, LabeledDimension)


class AbstractList(MutableSequence):
    """Abstract list for objects"""

    def __init__(self, data=[]):
        """Store data list"""
        super().__init__()
        self._list = list(data)

    def __repr__(self):
        """String representation"""
        return self._list.__repr__()

    def __str__(self):
        """String representation"""
        string = ",\n".join([item.__repr__() for item in self._list])
        return f"[{string}]"

    def __len__(self):
        """List length"""
        return len(self._list)

    def __getitem__(self, index):
        """Get a list item"""
        return self._list[index]

    def __delitem__(self, index):
        raise LookupError("Deleting items is not allowed.")

    def check_object(self, obj):
        """Abstract check"""

    def insert(self, index: int, value: object):
        """Insert a list item"""
        self._list.insert(index, self.check_object(value))

    def append(self, value):
        """Append a list item"""
        self._list.append(self.check_object(value))

    def __setitem__(self, index, item):
        """Set item at index"""
        self._list.__setitem__(index, self.check_object(item))

    def __eq__(self, other):
        """Check equality of DependentVariableList."""
        if not isinstance(other, self.__class__):
            return False
        if len(self._list) != len(other._list):
            return False

        check = [self_i == other_i for self_i, other_i in zip(self._list, other._list)]
        return np.all(check)


class DimensionList(AbstractList):
    """List of Dimension objects"""

    def check_object(self, obj):
        """Validate dimension"""
        if isinstance(obj, dict):
            obj = Dimension(**obj)
        if not isinstance(obj, __dimensions_list__):
            name = obj.__class__.__name__
            raise ValueError(f"Expecting a Dimension object, found {name}")
        return obj


class DependentVariableList(AbstractList):
    """List of Dependent variable objects"""

    def check_object(self, obj):
        """Validate dependent variable"""
        if isinstance(obj, dict):
            obj = DependentVariable(**obj)
        if not isinstance(obj, DependentVariable):
            name = obj.__class__.__name__
            raise ValueError(f"Expecting a DependentVariable object, found {name}")
        return obj

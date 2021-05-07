# -*- coding: utf-8 -*-
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
    def __init__(self, data=[]):
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

    def check_object(self, *args):
        pass

    def insert(self, index: int, item: object):
        """Insert a list item"""
        item = self.check_object(item)
        self._list.insert(index, item)

    def append(self, item):
        """Append a list item"""
        item = self.check_object(item)
        self._list.append(item)

    def __setitem__(self, index, item):
        """Set item at index"""
        item = self.check_object(item)
        # if self._list[index].count != item.count:
        #     raise IndexError("Index out of range")
        self._list[index] = item

    def __eq__(self, other):
        """Check equality of DependentVariableList."""
        if not isinstance(other, self.__class__):
            return False
        if len(self._list) != len(other._list):
            return False

        check = [self_i == other_i for self_i, other_i in zip(self._list, other._list)]
        return np.all(check)


class DimensionList(AbstractList):
    def check_object(self, obj):
        if isinstance(obj, dict):
            obj = Dimension(**obj)
        if not isinstance(obj, __dimensions_list__):
            name = obj.__class__.__name__
            raise ValueError(f"Expecting a Dimension object, found {name}")
        return obj


class DependentVariableList(AbstractList):
    def check_object(self, obj):
        if isinstance(obj, dict):
            obj = DependentVariable(**obj)
        if not isinstance(obj, DependentVariable):
            name = obj.__class__.name__
            raise ValueError(f"Expecting a DependentVariable object, found {name}")
        return obj

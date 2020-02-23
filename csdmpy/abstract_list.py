# -*- coding: utf-8 -*-
from collections import MutableSequence

import numpy as np

from csdmpy.dependent_variables import DependentVariable
from csdmpy.dimensions import Dimension
from csdmpy.dimensions import LabeledDimension
from csdmpy.dimensions import LinearDimension
from csdmpy.dimensions import MonotonicDimension

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
        # del self._list[index]

    def insert(self, index, item):
        """Insert a list item"""
        self._list.insert(index, item)

    def append(self, item):
        """Append a list item"""
        self.insert(len(self._list), item)

    def __eq__(self, other):
        """Check equality of DependentVariableList."""
        if not isinstance(other, self.__class__):
            return False
        if len(self._list) != len(other._list):
            return False

        check = []
        for i in range(len(self._list)):
            check.append(self._list[i] == other._list[i])

        if np.all(check):
            return True
        return False


class DimensionList(AbstractList):
    def __init__(self, data=[]):
        super().__init__(data)

    def __setitem__(self, index, item):
        if not isinstance(item, __dimensions_list__):
            raise ValueError(
                f"Expecting a Dimension object, found {item.__class__.__name__}"
            )
        if self._list[index].count != item.count:
            raise ValueError(
                f"Cannot substitute a dimension with {item.count} points to for a "
                f"dimension with {self._list[index].count} points."
            )
        self._list[index] = item


class DependentVariableList(AbstractList):
    def __init__(self, data=[]):
        super().__init__(data)

    def __setitem__(self, index, item):
        if not isinstance(item, DependentVariable):
            raise ValueError(
                f"Expecting a DependentVariable object, found {item.__class__.name__}"
            )
        self._list[index] = item

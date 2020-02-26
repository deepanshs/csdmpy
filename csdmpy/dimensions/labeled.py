# -*- coding: utf-8 -*-
"""The Labeled Dimension sub type class."""
from __future__ import division
from __future__ import print_function

import json
from copy import deepcopy

import numpy as np

from csdmpy.dimensions.base import _copy_core_metadata
from csdmpy.dimensions.base import BaseDimension
from csdmpy.dimensions.base import check_count


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["LabeledDimension"]


class LabeledDimension(BaseDimension):
    """A labeled dimension.

    Generates an object representing a non-physical dimension whose coordinates are
    labels. See :ref:`labeledDimension_uml` for details.
    """

    __slots__ = ("_count", "_labels")

    _type = "labeled"

    def __init__(self, labels, label="", description="", application={}, **kwargs):
        r"""Instantiate a LabeledDimension class."""
        super().__init__(label, application, description)
        self.labels = labels

    def __repr__(self):
        properties = ", ".join(
            [f"{k}={v}" for k, v in self.to_dict().items() if k != "type"]
        )
        return f"LabeledDimension({properties})"

    def __str__(self):
        return f"LabeledDimension({self.coordinates.__str__()})"

    def __eq__(self, other):
        """Overrides the default implementation"""
        if hasattr(other, "subtype"):
            other = other.subtype
        if isinstance(other, LabeledDimension):
            check = [
                self._count == other._count,
                np.all(self._labels == other._labels),
                self._label == other._label,
                self._description == other._description,
                self._application == other._application,
            ]
            if np.all(check):
                return True
        return False

    def is_quantitative(self):
        r"""Return `True`, if the dimension is quantitative, otherwise `False`.
        :returns: A Boolean.
        """
        return False

    # ----------------------------------------------------------------------- #
    #                                 Attributes                              #
    # ----------------------------------------------------------------------- #

    @property
    def type(self):
        """Return the type of the dimension."""
        return self.__class__._type

    @property
    def count(self):
        r"""Total number of labels along the dimension."""
        return self._count

    @count.setter
    def count(self, value):
        self._count = check_count(value, self._count, "labeled")

    @property
    def labels(self):
        r"""Return a list of labels along the dimension."""
        return self._labels

    @labels.setter
    def labels(self, labels):
        if not isinstance(labels, list):
            raise ValueError(f"A list of labels is required, found {type(labels)}.")

        items = np.asarray([isinstance(item, str) for item in labels])
        if np.all(items):
            self._labels = np.asarray(labels)
            self._count = len(labels)
        else:
            i = np.where(items == 0)[0][0]
            raise ValueError(
                "A list of string labels are required, found "
                f"{labels[i].__class__.__name__} at index {i}."
            )

    @property
    def coordinates(self):
        """Return the coordinates along the dimensions. This is an alias for labels."""
        n = self._count
        return self.labels[:n]

    @coordinates.setter
    def coordinates(self, value):
        self.labels = value

    @property
    def axis_label(self):
        """Return a formatted string for displaying label along the dimension axis."""
        return self.label

    @property
    def data_structure(self):
        """Json serialized string describing the LabeledDimension class instance."""
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=False, indent=2)

    # ----------------------------------------------------------------------- #
    #                                 Methods                                 #
    # ----------------------------------------------------------------------- #

    def _copy_metadata(self, obj, copy=False):
        """Copy LabeledDimension metadata."""
        if hasattr(obj, "subtype"):
            obj = obj.subtype
        if isinstance(obj, LabeledDimension):
            _copy_core_metadata(self, obj, "labeled")

    def to_dict(self):
        """Return the LabeledDimension as a python dictionary."""
        dictionary = {}
        dictionary["type"] = self.__class__._type
        if self._description.strip() != "":
            dictionary["description"] = self._description.strip()
        dictionary["labels"] = self._labels.tolist()

        if self._label.strip() != "":
            dictionary["label"] = self._label.strip()

        if self._application != {}:
            dictionary["application"] = self._application
        return dictionary

    def copy(self):
        """Return a copy of the object."""
        return deepcopy(self)

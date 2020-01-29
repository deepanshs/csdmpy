# -*- coding: utf-8 -*-
"""The Labeled Dimension sub type class."""
from __future__ import division
from __future__ import print_function

import warnings
from copy import deepcopy

import numpy as np

from csdmpy.utils import validate


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["LabeledDimension"]


class LabeledDimension:
    """A labeled dimension."""

    __slots__ = ("_count", "_labels", "_label", "_description", "_application")

    _type = "labeled"

    def __init__(self, labels, label="", description="", application={}, **kwargs):
        r"""Instantiate a LabeledDimension class."""
        self._description = description
        self._application = application
        self._label = label
        self.labels = labels

    def __repr__(self):
        properties = ", ".join([f"{k}={v}" for k, v in self.to_dict().items()])
        return f"Dimension({properties})"

    def __str__(self):
        properties = ", ".join([f"{k}={v}" for k, v in self.to_dict().items()])
        return f"Dimension({properties})"

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, LabeledDimension):
            check = [
                self._count == other._count,
                np.all(self._labels == other._labels),
                self._label == other._label,
                self._description == other._description,
                self._application == other._application,
            ]
            if False in check:
                return False
        return True

    # ----------------------------------------------------------------------- #
    #                                 Attributes                              #
    # ----------------------------------------------------------------------- #

    @property
    def type(self):
        """Return the type of the dimension."""
        return deepcopy(self._type)

    @property
    def count(self):
        r"""Total number of points along the linear dimension."""
        return deepcopy(self._count)

    @count.setter
    def count(self, value):
        value = validate(value, "count", int)
        if value > self.count:
            raise ValueError(
                f"Cannot set the count, {value}, more than the number of coordinates, "
                f"{self.count}, for the monotonic and labeled dimensions."
            )

        if value < self.count:
            warnings.warn(
                f"The number of coordinates, {self.count}, are truncated to {value}."
            )
            self._count = value

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
    def label(self):
        r"""Label associated with the dimension."""
        return deepcopy(self._label)

    @label.setter
    def label(self, label=""):
        self._label = validate(label, "label", str)

    @property
    def application(self):
        r"""Return an application dimension associated with the dimensions."""
        return deepcopy(self._application)

    @application.setter
    def application(self, value):
        self._application = value

    @property
    def description(self):
        r"""Return a description of the dimension."""
        return deepcopy(self._description)

    @description.setter
    def description(self, value):
        self._description = validate(value, "description", str)

    @property
    def coordinates(self):
        """Return the coordinates along the dimensions."""
        n = self._count
        return self.labels[:n]

    @coordinates.setter
    def coordinates(self, value):
        self.labels = value

    # ----------------------------------------------------------------------- #
    #                                 Methods                                 #
    # ----------------------------------------------------------------------- #

    def _is_quantitative(self):
        r"""Return `True`, if the dimension is quantitative, otherwise `False`.
        :returns: A Boolean.
        """
        return False

    def to_dict(self):
        """Return LabeledDimension as a python dictionary."""
        dictionary = {}
        dictionary["type"] = self._type
        if self._description.strip() != "":
            dictionary["description"] = self._description.strip()
        dictionary["labels"] = self._labels.tolist()

        if self._label.strip() != "":
            dictionary["label"] = self._label.strip()

        if self._application != {}:
            dictionary["application"] = self._application
        return dictionary

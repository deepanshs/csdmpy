# -*- coding: utf-8 -*-
"""The Labeled Dimension SubTypes class."""
from __future__ import division
from __future__ import print_function

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

    # ----------------------------------------------------------------------- #
    #                                 Attributes                              #
    # ----------------------------------------------------------------------- #

    @property
    def labels(self):
        r"""Return a list of labels along the dimension."""
        return deepcopy(self._labels)

    @labels.setter
    def labels(self, labels):
        if not isinstance(labels, list):
            raise ValueError(f"A list of labels is required, found {type(labels)}.")

        items = np.asarray([isinstance(item, str) for item in labels])
        if np.all(items):
            self._labels = np.asarray(labels)
            self._count = len(labels)
        else:
            i = np.where(items == False)[0][0]
            raise ValueError(
                f"A list of string labels are required, found {type(labels[i])} at index {i}."
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

    # ----------------------------------------------------------------------- #
    #                                 Methods                                 #
    # ----------------------------------------------------------------------- #

    def _is_quantitative(self):
        r"""Return `True`, if the dimension is quantitative, otherwise `False`.
        :returns: A Boolean.
        """
        return False

    def _get_python_dictionary(self):
        dictionary = {}
        dictionary["type"] = self._type
        if self._description.strip() != "":
            dictionary["description"] = self._description.strip()
        dictionary["labels"] = self._labels.tolist()
        return dictionary

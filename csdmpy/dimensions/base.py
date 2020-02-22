# -*- coding: utf-8 -*-
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

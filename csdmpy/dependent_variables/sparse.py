# -*- coding: utf-8 -*-
"""The SparseSampling class."""
from copy import deepcopy

import numpy as np

from csdmpy.dependent_variables.decoder import Decoder
from csdmpy.utils import check_encoding
from csdmpy.utils import NumericType
from csdmpy.utils import QuantityType
from csdmpy.utils import validate

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["SparseSampling"]


class SparseSampling:
    r"""Declare a SparseSampling class."""

    __slots__ = (
        "_sparse_dimensions_indexes",
        "_sparse_grid_vertexes",
        "_encoding",
        "_quantity_type",
        "_unsigned_integer_type",
        "_description",
        "_application",
    )

    def __init__(
        self,
        dimension_indexes,
        sparse_grid_vertexes,
        encoding="none",
        quantity_type="scalar",
        unsigned_integer_type="int64",
        description="",
        application={},
        **kwargs,
    ):
        """Initialize a SparseDimension class."""
        self.encoding = encoding
        self._unsigned_integer_type = NumericType(unsigned_integer_type)
        self._quantity_type = QuantityType(quantity_type)
        self.description = description
        self.application = application
        self._sparse_dimensions_indexes = dimension_indexes
        self._sparse_grid_vertexes = Decoder(
            self._encoding,
            self._quantity_type,
            [sparse_grid_vertexes],
            self._unsigned_integer_type.dtype,
        )

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, SparseSampling):
            check = [
                np.all(
                    self._sparse_dimensions_indexes == other._sparse_dimensions_indexes
                ),
                np.all(self._sparse_grid_vertexes == other._sparse_grid_vertexes),
                self._encoding == other._encoding,
                self._quantity_type == other._quantity_type,
                self._unsigned_integer_type == other._unsigned_integer_type,
                self._description == other._description,
                self._application == other._application,
            ]
            if False in check:
                return False
            return True
        return False

    # ----------------------------------------------------------------------- #
    #                                 Attributes                              #
    # ----------------------------------------------------------------------- #

    @property
    def encoding(self):
        r"""Return the data encoding method."""
        return deepcopy(self._encoding)

    @encoding.setter
    def encoding(self, value):
        self._encoding = validate(value, "encoding", str, check_encoding)

    @property
    def unsigned_integer_type(self):
        r"""Return the unsigned integer type of data values."""
        return deepcopy(self._unsigned_integer_type)

    @unsigned_integer_type.setter
    def unsigned_integer_type(self, value):
        self._unsigned_integer_type.update(value)

    @property
    def application(self):
        """Return an application metadata dictionary."""
        return deepcopy(self._application)

    @application.setter
    def application(self, value):
        self._application = validate(value, "application", dict)

    @property
    def description(self):
        r"""Return the description of the object."""
        return deepcopy(self._description)

    @description.setter
    def description(self, value):
        self._description = validate(value, "description", str)

    @property
    def sparse_dimensions_indexes(self):
        """List of dimension indexes corresponding to sparse dimensions."""
        return deepcopy(self._sparse_dimensions_indexes)

    @property
    def sparse_grid_vertexes(self):
        """List of grid vertexes corresponding to sparse dimensions."""
        return deepcopy(self._sparse_dimensions_indexes)

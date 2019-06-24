# -*- coding: utf-8 -*-
from copy import deepcopy

from csdfpy.dependent_variables.decoder import Decoder
from csdfpy.utils import check_encoding
from csdfpy.utils import NumericType
from csdfpy.utils import QuantityType
from csdfpy.utils import validate


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


class SparseSampling:
    r"""Declare a SparseSampling class."""

    __slots__ = (
        "_sparse_dimensions",
        "_sparse_grid_vertexes",
        "_encoding",
        "_quantity_type",
        "_numeric_type",
        "_description",
        "_application",
    )

    def __init__(
        self,
        dimensions,
        sparse_grid_vertexes,
        encoding="none",
        quantity_type="scalar",
        numeric_type="int64",
        description="",
        application={},
        **kwargs,
    ):
        """Initialize a SparseDimension class."""
        self.encoding = encoding
        self._numeric_type = NumericType(numeric_type)
        self._quantity_type = QuantityType(quantity_type)
        self.description = description
        self.application = application
        self._sparse_dimensions = dimensions
        self._sparse_grid_vertexes = Decoder(
            self._encoding,
            self._quantity_type,
            [sparse_grid_vertexes],
            self._numeric_type.dtype,
        )

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
    def numeric_type(self):
        r"""Return the numeric type of data values."""
        return deepcopy(self._numeric_type)

    @numeric_type.setter
    def numeric_type(self, value):
        self._numeric_type.update(value)

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
    def sparse_dimensions(self):
        """List of dimension indexes corresponding to sparse dimensions."""
        return deepcopy(self._sparse_dimensions)

    @property
    def sparse_grid_vertexes(self):
        """List of grid vertexes corresponding to sparse dimensions."""
        return deepcopy(self._sparse_dimensions)

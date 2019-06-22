# -*- coding: utf-8 -*-
from copy import deepcopy

from csdfpy.dependent_variables.decoder import Decoder
from csdfpy.utils import _check_encoding
from csdfpy.utils import _type_message
from csdfpy.utils import NumericType
from csdfpy.utils import QuantityType


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


# =========================================================================== #
#                             SparseSampling Class                            #
# =========================================================================== #


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
        # encoding
        self.encoding = encoding

        # numeric type
        self._numeric_type = NumericType(numeric_type)

        # quantity_type
        self._quantity_type = QuantityType(quantity_type)

        # description
        self.description = description

        # application
        self.application = application

        # sparse dimensions
        self._sparse_dimensions = dimensions

        # sparse grid vertexes
        self._sparse_grid_vertexes = Decoder(
            self._encoding,
            self._quantity_type,
            [sparse_grid_vertexes],
            self._numeric_type._nptype,
        )

    # encoding
    @property
    def encoding(self):
        r"""Return the data encoding method."""
        return deepcopy(self._encoding)

    @encoding.setter
    def encoding(self, value):
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))
        value = _check_encoding(value)
        self._encoding = value

    # numeric type
    @property
    def numeric_type(self):
        r"""Return the numeric type of data values."""
        return deepcopy(self._numeric_type)

    @numeric_type.setter
    def numeric_type(self, value):
        self._numeric_type.update(value)

    # application
    @property
    def application(self):
        """Return an application metadata dictionary."""
        return deepcopy(self._application)

    @application.setter
    def application(self, value):
        if not isinstance(value, dict):
            raise ValueError(
                "A dict value is required, found {0}".format(type(value))
            )
        self._application = value

    # description
    @property
    def description(self):
        r"""Return the description of the object."""
        return deepcopy(self._description)

    @description.setter
    def description(self, value):
        if isinstance(value, str):
            self._description = value
        else:
            raise ValueError(
                (
                    "Description requires a string, {0} given".format(
                        type(value)
                    )
                )
            )

    # sparse dimensions
    @property
    def sparse_dimensions(self):
        """List of dimension indexes corresponding to sparse dimensions."""
        return deepcopy(self._sparse_dimensions)

    # sparse grid vertexes
    @property
    def sparse_grid_vertexes(self):
        """List of grid vertexes corresponding to sparse dimensions."""
        return deepcopy(self._sparse_dimensions)

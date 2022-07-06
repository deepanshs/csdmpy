"""The SparseSampling class."""
from copy import deepcopy

import numpy as np

from csdmpy.dependent_variable.decoder import Decoder
from csdmpy.utils import check_encoding
from csdmpy.utils import NumericType
from csdmpy.utils import QuantityType
from csdmpy.utils import validate

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["SparseSampling"]


class SparseSampling:
    """Declare a SparseSampling class."""

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
        # dimension_indexes,
        # sparse_grid_vertexes,
        # encoding="none",
        # quantity_type="scalar",
        # unsigned_integer_type="int64",
        # description="",
        # application={},
        **kwargs,
    ):
        """Initialize a SparseDimension class."""
        default = {
            "encoding": "none",
            "quantity_type": "scalar",
            "unsigned_integer_type": "uint64",
            "description": "",
            "application": None,
        }
        default.update(kwargs)
        check_sparse_sampling_key_value(default)
        self.encoding = default["encoding"]
        self._unsigned_integer_type = NumericType(default["unsigned_integer_type"])
        self._quantity_type = QuantityType(default["quantity_type"])
        self.description = default["description"]
        self.application = default["application"]
        self._sparse_dimensions_indexes = default["dimension_indexes"]
        self._sparse_grid_vertexes = Decoder(
            self._encoding,
            self._quantity_type,
            [default["sparse_grid_vertexes"]],
            self._unsigned_integer_type.dtype,
        )

    def __eq__(self, other):
        """Overrides the default implementation"""
        if not isinstance(other, SparseSampling):
            return False
        check = [
            np.all(self._sparse_dimensions_indexes == other._sparse_dimensions_indexes),
            np.all(self._sparse_grid_vertexes == other._sparse_grid_vertexes),
            *[getattr(self, _) == getattr(other, _) for _ in __class__.__slots__[2:]],
        ]
        return np.all(check)

    # ----------------------------------------------------------------------- #
    #                                 Attributes                              #
    # ----------------------------------------------------------------------- #

    @property
    def encoding(self):
        """Return the data encoding method."""
        return deepcopy(self._encoding)

    @encoding.setter
    def encoding(self, value):
        self._encoding = validate(value, "encoding", str, check_encoding)

    @property
    def unsigned_integer_type(self):
        """Return the unsigned integer type of data values."""
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
        self._application = validate(value, "application", (dict, type(None)))

    @property
    def description(self):
        """Return the description of the object."""
        return deepcopy(self._description)

    @description.setter
    def description(self, value):
        self._description = validate(value, "description", str)

    @property
    def dimension_indexes(self):
        """List of dimension indexes corresponding to sparse dimensions."""
        return deepcopy(self._sparse_dimensions_indexes)

    @property
    def sparse_grid_vertexes(self):
        """List of grid vertexes corresponding to sparse dimensions."""
        return deepcopy(self._sparse_grid_vertexes)


def check_sparse_sampling_key_value(input_dict):
    """Check for sparse sampling key value"""

    def message(item):
        return (
            f"Missing a required `{item}` key from the SparseSampling object of the "
            "DependentVariable object."
        )

    sparse_keys = input_dict.keys()
    if "dimension_indexes" not in sparse_keys:
        raise KeyError(message("dimension_indexes"))
    if "sparse_grid_vertexes" not in sparse_keys:
        raise KeyError(message("sparse_grid_vertexes"))
    if "encoding" in sparse_keys:
        code = input_dict["encoding"]
        if code != "none" and "unsigned_integer_type" not in sparse_keys:
            raise KeyError(message("unsigned_integer_type"))

        uint_value = input_dict["unsigned_integer_type"]
        if uint_value not in ["uint8", "uint16", "uint32", "uint64"]:
            raise ValueError(
                f"{uint_value} is an invalid `unsigned_integer_type` enumeration ",
                "literal. The allowed values are `uint8`, `uint16`, `uint32`, ",
                "and `uint64`.",
            )

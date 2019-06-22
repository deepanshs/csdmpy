# -*- coding: utf-8 -*-
import pytest

from csdfpy.utils import _check_encoding
from csdfpy.utils import QuantityType


def test_encoding():
    assert _check_encoding("base64") == "base64"
    assert _check_encoding("raw") == "raw"
    assert _check_encoding("none") == "none"

    error = (
        "is not a valid `encoding` enumeration literal. "
        "The allowed values are"
    )
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        _check_encoding("text")


def test_quantity_type():
    assert QuantityType("RGBA").value == "RGBA"
    assert QuantityType("scalar").value == "scalar"
    assert QuantityType("vector_15").value == "vector_15"
    assert QuantityType("vector_15").p == 15
    assert QuantityType("matrix_13_3").value == "matrix_13_3"
    assert QuantityType("matrix_13_3").p == 39
    assert QuantityType("symmetric_matrix_10").value == "symmetric_matrix_10"
    assert QuantityType("symmetric_matrix_10").p == 55

    error = (
        "is not a valid `quantity_type` enumeration literal. "
        "The allowed values are"
    )
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        QuantityType("RgB")

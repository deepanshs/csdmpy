# -*- coding: utf-8 -*-
import pytest

from csdmpy.utils import check_and_assign_bool
from csdmpy.utils import check_encoding
from csdmpy.utils import NumericType
from csdmpy.utils import QuantityType


def test_encoding():
    assert check_encoding("base64") == "base64"
    assert check_encoding("raw") == "raw"
    assert check_encoding("none") == "none"

    error = "is an invalid `encoding` enumeration literal. The allowed values are"
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        check_encoding("text")


def test_quantity_type():
    assert QuantityType("pixel_4").value == "pixel_4"
    assert QuantityType("pixel_4").p == 4
    assert QuantityType("scalar").value == "scalar"
    assert QuantityType("vector_15").value == "vector_15"
    assert QuantityType("vector_15").p == 15
    assert QuantityType("matrix_13_3").value == "matrix_13_3"
    assert QuantityType("matrix_13_3").p == 39
    assert QuantityType("symmetric_matrix_10").value == "symmetric_matrix_10"
    assert QuantityType("symmetric_matrix_10").p == 55

    error = "is an invalid `quantity_type` enumeration literal. The allowed values are"
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        QuantityType("RGB")


def test_numeric_type():
    assert NumericType("uint8").value == "uint8"
    assert NumericType("uint8").dtype == "<u1"
    assert NumericType("uint16").value == "uint16"
    assert NumericType("uint16").dtype == "<u2"
    assert NumericType("uint32").value == "uint32"
    assert NumericType("uint32").dtype == "<u4"
    assert NumericType("uint64").value == "uint64"
    assert NumericType("uint64").dtype == "<u8"

    assert NumericType("int8").value == "int8"
    assert NumericType("int8").dtype == "<i1"
    assert NumericType("int16").value == "int16"
    assert NumericType("int16").dtype == "<i2"
    assert NumericType("int32").value == "int32"
    assert NumericType("int32").dtype == "<i4"
    assert NumericType("int64").value == "int64"
    assert NumericType("int64").dtype == "<i8"

    # assert NumericType("float16").value == "float16"
    # assert NumericType("float16").dtype == "<f2"
    assert NumericType("float32").value == "float32"
    assert NumericType("float32").dtype == "<f4"
    assert NumericType("float64").value == "float64"
    assert NumericType("float64").dtype == "<f8"

    assert NumericType("complex64").value == "complex64"
    assert NumericType("complex64").dtype == "<c8"
    assert NumericType("complex128").value == "complex128"
    assert NumericType("complex128").dtype == "<c16"

    error = "is an invalid `numeric_type` enumeration literal. The allowed values are"

    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        NumericType("float16")

    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        NumericType("complex256")

    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        NumericType("float128")


def test_boolean():
    assert check_and_assign_bool(None) is False
    assert check_and_assign_bool(False) is False
    assert check_and_assign_bool(True) is True

    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        check_and_assign_bool("True")

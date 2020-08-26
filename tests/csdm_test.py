# -*- coding: utf-8 -*-
"""Test for the csdm object
    1) generate csdm object.
    2) split multiple dependent variables to individual objects.
    3) add, sub, iadd, radd, isub, rsub, mul, imul, for scalar and ScalarQuantity.
    4) rmul, truediv, itruediv, rtruediv, pow, ipow for scalar and ScalarQuantity.
    5) min, max, clip, real, imag, conj, round, angle functions.
"""
import json

import numpy as np
import pytest

import csdmpy as cp


def get_test(type):
    out = np.random.rand(10).astype(type)
    a_test = cp.new()
    a_test.add_dimension(cp.LinearDimension(count=10, increment="1s"))
    a_test.add_dependent_variable(
        {"type": "internal", "quantity_type": "scalar", "unit": "m", "components": out}
    )
    return out, a_test


def get_test_2d(type):
    out = np.random.rand(50).astype(type).reshape(10, 5)
    a_test = cp.new()
    a_test.add_dimension(cp.LinearDimension(count=5, increment="1s"))
    a_test.add_dimension(cp.LinearDimension(count=10, increment="1m"))
    a_test.add_dependent_variable(
        {
            "type": "internal",
            "quantity_type": "scalar",
            "unit": "m",
            "components": out.ravel(),
        }
    )
    return out, a_test


def test_csdm():
    data = cp.new(description="This is a test")

    assert data != "sd"

    assert data.size == 1
    # read_only
    assert data.read_only is False
    data.read_only = True
    assert data.read_only is True
    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.read_only = "True"

    # tags
    assert data.tags == []
    data.tags = ["1", "2", "3"]
    assert data.tags == ["1", "2", "3"]
    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.tags = "23"

    # version
    assert data.version == cp.csdm.CSDM.__latest_CSDM_version__

    # geographic_coordinate
    assert data.geographic_coordinate == {}
    error = "can't set attribute"
    with pytest.raises(AttributeError, match=".*{0}.*".format(error)):
        data.geographic_coordinate = {}

    # description
    assert data.description == "This is a test"
    data.description = "Enough with the tests"
    assert data.description == "Enough with the tests"
    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.description = {}

    # application
    assert data.application == {}
    data.application = {"csdmpy": "Some day"}
    assert data.application == {"csdmpy": "Some day"}
    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.application = "Some other day"

    # filename
    assert data.filename == ""

    # data_structure
    structure = {
        "csdm": {
            "version": "1.0",
            "read_only": True,
            "tags": ["1", "2", "3"],
            "description": "Enough with the tests",
            "application": {"csdmpy": "Some day"},
            "dimensions": [],
            "dependent_variables": [],
        }
    }
    assert data.data_structure == str(
        json.dumps(structure, ensure_ascii=False, sort_keys=False, indent=2)
    )

    assert data.dict() == structure

    # equality check
    dm = data.copy()

    assert dm == data
    assert dm.shape == ()

    dm.add_dimension(cp.LinearDimension(count=10, increment="1s"))

    assert dm != data


def test_split():
    a = cp.new()
    a.add_dimension(cp.LinearDimension(count=10, increment="1m"))
    a.add_dependent_variable(
        {"type": "internal", "components": np.arange(10) + 1, "quantity_type": "scalar"}
    )

    b = cp.new()
    b.add_dimension(cp.LinearDimension(count=10, increment="1m"))
    b.add_dependent_variable(
        {"type": "internal", "components": np.arange(10) + 2, "quantity_type": "scalar"}
    )

    c = cp.new()
    c.add_dimension(cp.LinearDimension(count=10, increment="1m"))
    c.add_dependent_variable(
        {"type": "internal", "components": np.arange(10) + 1, "quantity_type": "scalar"}
    )
    c.add_dependent_variable(
        {"type": "internal", "components": np.arange(10) + 2, "quantity_type": "scalar"}
    )

    a_, b_ = c.split()

    assert a_ == a
    assert b_ == b


a_test = cp.new()
a_test.add_dimension(cp.LinearDimension(count=10, increment="1s"))
a_test.add_dependent_variable(
    {
        "type": "internal",
        "quantity_type": "scalar",
        "unit": "m",
        "components": np.arange(10),
    }
)

a1_test = cp.new()
a1_test.add_dimension(cp.LinearDimension(count=10, increment="1m"))
a1_test.add_dependent_variable(
    {
        "type": "internal",
        "quantity_type": "scalar",
        "unit": "m",
        "components": np.arange(10),
    }
)

b_test = cp.new()
b_test.add_dimension(cp.LinearDimension(count=10, increment="1s"))
b_test.add_dependent_variable(
    {
        "type": "internal",
        "quantity_type": "scalar",
        "unit": "km",
        "components": np.arange(10, dtype=float),
    }
)

b1_test = cp.new()
b1_test.add_dimension(cp.LinearDimension(count=10, increment="1s"))
b1_test.add_dependent_variable(
    {
        "type": "internal",
        "quantity_type": "scalar",
        "unit": "km",
        "components": np.arange(10),
    }
)
b1_test.add_dependent_variable(
    {
        "type": "internal",
        "quantity_type": "vector_2",
        "unit": "km",
        "components": np.arange(20),
    }
)


def test_add_sub():
    # add
    c = a_test + b_test
    out = np.arange(10) + 1000 * np.arange(10)
    assert np.allclose(c.dependent_variables[0].components, [out])

    # sub
    c = a_test - b_test
    out = np.arange(10) - 1000 * np.arange(10)
    assert np.allclose(c.dependent_variables[0].components, [out])

    c = b_test - a_test
    out = np.arange(10) - 1 / 1000 * np.arange(10)
    assert np.allclose(c.dependent_variables[0].components, [out])

    # add scalar
    c = a_test + cp.ScalarQuantity("2m")
    out = np.arange(10) + 2
    assert np.allclose(c.dependent_variables[0].components, [out])

    c = cp.ScalarQuantity("2m") + a_test
    assert np.allclose(c.dependent_variables[0].components, [out])

    a_t = cp.as_csdm(np.arange(10))
    c = a_t + 5.12
    out = np.arange(10) + 5.12
    assert np.allclose(c.dependent_variables[0].components, [out])

    c = 5.12 + a_t
    assert np.allclose(c.dependent_variables[0].components, [out])

    # add complex
    c = a_t + 5.12 - 4j
    out = np.arange(10) + 5.12 - 4j
    assert np.allclose(c.dependent_variables[0].components, [out])

    c = 5.12 - 4j + a_t
    assert np.allclose(c.dependent_variables[0].components, [out])

    c = a_test / cp.ScalarQuantity("m") + 3 + 4j
    out = np.arange(10) + 3 + 4j
    assert np.allclose(c.dependent_variables[0].components, [out])

    # subtract scalar
    c = a_test - cp.ScalarQuantity("2m")
    out = np.arange(10) - 2
    assert np.allclose(c.dependent_variables[0].components, [out])

    c = cp.ScalarQuantity("2m") - a_test
    assert np.allclose(c.dependent_variables[0].components, [-out])

    error = r"Cannot operate on CSDM objects with different dimensions."
    with pytest.raises(Exception, match=".*{0}.*".format(error)):
        c = a1_test + b_test

    error = r"Cannot operate on CSDM objects with differnet lengths of dependent"
    with pytest.raises(Exception, match=".*{0}.*".format(error)):
        c = a_test + b1_test


def test_iadd_isub():
    c = a_test.astype("float32")
    c += cp.ScalarQuantity("5.0cm")
    out = np.arange(10) + 0.05
    assert np.allclose(c.dependent_variables[0].components, [out])

    c = a_test.astype("float32")
    c -= cp.ScalarQuantity("5.0cm")
    out = np.arange(10) - 0.05
    assert np.allclose(c.dependent_variables[0].components, [out])

    c = a_test.astype("float32") / cp.ScalarQuantity("cm")
    c -= 0.05
    out = np.arange(10) - 0.05
    assert np.allclose(c.dependent_variables[0].components, [out])

    out, a_test_ = get_test(float)  # in units of m
    a_test_ += b_test
    out += 1000 * np.arange(10)
    assert np.allclose(a_test_.dependent_variables[0].components, [out])

    out, a_test_ = get_test(float)  # in units of m
    c = a_test_ / cp.ScalarQuantity("m")
    c += 2.0
    out += 2.0
    assert np.allclose(c.dependent_variables[0].components, [out])

    out, a_test_ = get_test(float)  # in units of m
    a_test_ -= b_test
    out -= 1000 * np.arange(10)
    assert np.allclose(a_test_.dependent_variables[0].components, [out])


def test_mul_truediv_pow():
    # mul
    c = a_test * 2
    out = a_test.dependent_variables[0].components
    assert np.allclose(c.dependent_variables[0].components, out * 2)
    assert id(a_test) != id(c)

    c = 2 * a_test
    assert np.allclose(c.dependent_variables[0].components, out * 2)

    c = b_test * 1.34
    out = b_test.dependent_variables[0].components
    assert np.allclose(c.dependent_variables[0].components, out * 1.34)
    assert id(b_test) != id(c)

    c = 1.34 * a_test
    assert np.allclose(c.dependent_variables[0].components, out * 1.34)

    c = b1_test * 1.423j
    out = b1_test.dependent_variables[0].components
    assert np.allclose(c.dependent_variables[0].components, out * 1.423j)
    assert id(b1_test) != id(c)

    c = 1.423j * b1_test
    assert np.allclose(c.dependent_variables[0].components, out * 1.423j)

    lst = np.random.rand(5).astype(np.complex128)
    c = a1_test * lst[2]
    out = b1_test.dependent_variables[0].components
    assert np.allclose(c.dependent_variables[0].components, out * lst[2])
    assert id(a1_test) != id(c)

    # c = lst[2] * a1_test
    # assert np.allclose(c.dependent_variables[0].components, out * lst[2])

    c = b1_test * cp.string_to_quantity("1.324 s")
    out = b1_test.dependent_variables[0].components
    assert np.allclose(c.dependent_variables[0].components, out * 1.324)
    assert str(c.dependent_variables[0].unit) == "km s"
    assert id(b1_test) != id(c)

    c = b1_test * cp.ScalarQuantity("1.324 s")
    out = b1_test.dependent_variables[0].components
    assert np.allclose(c.dependent_variables[0].components, out * 1.324)
    assert str(c.dependent_variables[0].unit) == "km s"
    assert id(b1_test) != id(c)

    c = cp.ScalarQuantity("1.324 s") * b1_test
    assert np.allclose(c.dependent_variables[0].components, out * 1.324)

    # div
    c = a_test / 2
    out = a_test.dependent_variables[0].components
    assert np.allclose(c.dependent_variables[0].components, out / 2)
    assert id(a_test) != id(c)

    c = 2.0 / a_test.astype(float)
    assert np.allclose(c.dependent_variables[0].components, 2 / out)

    c = b_test / 1.34
    out = b_test.dependent_variables[0].components
    assert np.allclose(c.dependent_variables[0].components, out / 1.34)
    assert id(b_test) != id(c)

    c = b1_test / 1.423j
    out = b1_test.dependent_variables[0].components
    assert np.allclose(c.dependent_variables[0].components, out / 1.423j)
    assert id(b1_test) != id(c)

    c = 1.423j / (b1_test + 1).astype(float)
    assert np.allclose(c.dependent_variables[0].components, 1.423j / (out + 1))

    lst = np.random.rand(5).astype(np.complex128)
    c = a1_test / lst[2]
    out = b1_test.dependent_variables[0].components
    assert np.allclose(c.dependent_variables[0].components, out / lst[2])
    assert id(a1_test) != id(c)

    c = b1_test / cp.string_to_quantity("1.324 s")
    out = b1_test.dependent_variables[0].components
    assert np.allclose(c.dependent_variables[0].components, out / 1.324)
    assert str(c.dependent_variables[0].unit) == "km / s"
    assert id(b1_test) != id(c)

    # c = cp.string_to_quantity("1.324 s") / (b1_test+1)
    # assert np.allclose(c.dependent_variables[0].components, 1.324 / (out+1))

    c = b1_test / cp.ScalarQuantity("1.324 s")
    out = b1_test.dependent_variables[0].components
    assert np.allclose(c.dependent_variables[0].components, out / 1.324)
    assert str(c.dependent_variables[0].unit) == "km / s"
    assert id(b1_test) != id(c)

    c = cp.ScalarQuantity("1.324 s") / (b_test + 1)
    assert np.allclose(c.dependent_variables[0].components, 1.324 / (out + 1))

    error = r"unsupported operand type\(s\) \*: 'CSDM' and 'str'."
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        c = a_test * "3"

    error = r"Only scalar multiplication or division is allowed."
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        c = a_test * np.asarray([1, 2])

    error = r"unsupported operand type\(s\) /: 'CSDM' and 'str'."
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        c = a_test / "3"

    error = r"Only scalar multiplication or division is allowed."
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        c = a_test / np.asarray([1, 2])

    # pow
    c = b1_test ** 2
    out = b1_test.dependent_variables[0].components
    assert np.allclose(c.dependent_variables[0].components, np.power(out, 2))
    assert str(c.dependent_variables[0].unit) == "km2"

    c **= 2
    assert np.allclose(c.dependent_variables[0].components, np.power(out, 4))
    assert str(c.dependent_variables[0].unit) == "km4"

    c **= 1 / 4
    assert np.allclose(c.dependent_variables[0].components, out)
    assert str(c.dependent_variables[0].unit) == "km"


def test_imul_itruediv():
    # imul
    out, a_test = get_test(int)
    b = a_test
    a_test *= 2
    out *= 2
    assert np.allclose(a_test.dependent_variables[0].components, [out])
    assert id(a_test) == id(b)

    out, a_test = get_test(float)
    b = a_test
    a_test *= 2.312
    out *= 2.312
    assert np.allclose(a_test.dependent_variables[0].components, [out])
    assert id(a_test) == id(b)

    out, a_test = get_test(complex)
    b = a_test
    a_test *= 2.12 + 1.1j
    out *= 2.12 + 1.1j
    assert np.allclose(a_test.dependent_variables[0].components, [out])
    assert id(a_test) == id(b)

    out, a_test = get_test(float)
    b = a_test
    a_test *= cp.string_to_quantity("3.12 s/km")
    out *= 3.12
    assert np.allclose(a_test.dependent_variables[0].components, [out])
    assert str(a_test.dependent_variables[0].unit) == "m s / km"
    assert id(a_test) == id(b)

    out, a_test = get_test(float)
    b = a_test
    a_test *= cp.ScalarQuantity("3.12 s/km")
    out *= 3.12
    assert np.allclose(a_test.dependent_variables[0].components, [out])
    assert str(a_test.dependent_variables[0].unit) == "m s / km"
    assert id(a_test) == id(b)

    # itruediv

    out, a_test = get_test(float)
    b = a_test
    a_test /= 2
    out /= 2
    assert np.allclose(a_test.dependent_variables[0].components, [out])
    assert id(a_test) == id(b)

    out, a_test = get_test(float)
    b = a_test
    a_test /= 2.312
    out /= 2.312
    assert np.allclose(a_test.dependent_variables[0].components, [out])
    assert id(a_test) == id(b)

    out, a_test = get_test(complex)
    b = a_test
    a_test /= 2.12 + 1.1j
    out /= 2.12 + 1.1j
    assert np.allclose(a_test.dependent_variables[0].components, [out])
    assert id(a_test) == id(b)

    out, a_test = get_test(float)
    b = a_test
    a_test /= cp.string_to_quantity("3.12 s/km")
    out /= 3.12
    assert np.allclose(a_test.dependent_variables[0].components, [out])
    assert str(a_test.dependent_variables[0].unit) == "km m / s"
    assert id(a_test) == id(b)

    out, a_test = get_test(float)
    b = a_test
    a_test /= cp.ScalarQuantity("3.12 s/km")
    out /= 3.12
    assert np.allclose(a_test.dependent_variables[0].components, [out])
    assert str(a_test.dependent_variables[0].unit) == "km m / s"
    assert id(a_test) == id(b)


def test_in_build():
    assert a_test == +a_test

    out = a_test.dependent_variables[0].components
    assert np.allclose(abs(a_test).dependent_variables[0].components[0], abs(out))


def test_max_min_clip():
    # max
    d0 = cp.LinearDimension(count=5, increment="1s")
    d1 = cp.LinearDimension(count=10, increment="1m")
    out, a_test = get_test_2d(float)
    assert out.max() == a_test.max().value
    assert str(a_test.max().unit) == "m"

    b = a_test.max(axis=1)
    assert np.allclose(out.max(0), b.dependent_variables[0].components[0])
    assert b.dimensions[0] == d0

    b = a_test.max(axis=0)
    assert np.allclose(out.max(1), b.dependent_variables[0].components[0])
    assert b.dimensions[0] == d1

    # min
    out, a_test = get_test_2d(float)
    assert out.min() == a_test.min().value
    assert str(a_test.min().unit) == "m"

    b = a_test.min(axis=1)
    assert np.allclose(out.min(0), b.dependent_variables[0].components[0])
    assert b.dimensions[0] == d0

    b = a_test.min(axis=0)
    assert np.allclose(out.min(1), b.dependent_variables[0].components[0])
    assert b.dimensions[0] == d1

    # clip
    b = a_test.clip(min=0)
    assert np.allclose(out.clip(min=0), b.dependent_variables[0].components[0])

    b = a_test.clip(max=0.5)
    assert np.allclose(out.clip(max=0.5), b.dependent_variables[0].components[0])


def test_real_imag_conj_angle():
    out, a_test = get_test_2d(complex)
    b = a_test.real
    assert b.dependent_variables[0].numeric_type == "float64"
    assert np.allclose(out.real, b.dependent_variables[0].components[0])

    b = np.real(a_test)
    assert b.dependent_variables[0].numeric_type == "float64"
    assert np.allclose(out.real, b.dependent_variables[0].components[0])

    b = a_test.imag
    assert b.dependent_variables[0].numeric_type == "float64"
    assert np.allclose(out.imag, b.dependent_variables[0].components[0])

    b = a_test.conj()
    assert b.dependent_variables[0].numeric_type == "complex128"
    assert np.allclose(out.conj(), b.dependent_variables[0].components[0])

    b = np.angle(a_test)
    assert b.dependent_variables[0].numeric_type == "float64"
    assert np.allclose(np.angle(out), b.dependent_variables[0].components[0])


def test_round_around():
    out, a_test = get_test_2d(float)
    b = a_test.round(1)
    assert np.allclose(out.round(1), b.dependent_variables[0].components[0])

    b = np.around(a_test, 1)
    assert np.allclose(np.around(out, 1), b.dependent_variables[0].components[0])


def test_not_implemented_error():
    fn = [np.argmax, np.argmin, np.ptp, np.trace, np.cumsum, np.cumprod]
    for fn_ in fn:
        with pytest.raises(NotImplementedError, match=""):
            fn_(a_test)

    with pytest.raises(NotImplementedError, match=""):
        a_test.argmax()

    with pytest.raises(NotImplementedError, match=""):
        a_test.argmin()

    with pytest.raises(NotImplementedError, match=""):
        a_test.ptp()

    with pytest.raises(NotImplementedError, match=""):
        a_test.trace()

    with pytest.raises(NotImplementedError, match=""):
        a_test.cumsum()

    with pytest.raises(NotImplementedError, match=""):
        a_test.cumprod()

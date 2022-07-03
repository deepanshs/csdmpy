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
    a_test.dimensions.append(cp.LinearDimension(count=10, increment="1s"))
    a_test.y.append(
        cp.DependentVariable(
            type="internal", quantity_type="scalar", unit="m", components=out
        )
    )

    return out, a_test


def get_test_2d(type):
    out = np.random.rand(50).astype(type).reshape(10, 5)

    d_0 = cp.LinearDimension(count=5, increment="1s")
    d_1 = cp.LinearDimension(count=10, increment="1m")
    dv_0 = cp.DependentVariable(
        type="internal",
        quantity_type="scalar",
        unit="m",
        components=out.ravel(),
    )
    obj = cp.CSDM(dimensions=[d_0, d_1], dependent_variables=[dv_0])
    return out, obj


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

    dm.dimensions.append(cp.LinearDimension(count=10, increment="1s"))

    assert dm != data


def test_split():
    a = cp.new()
    a.dimensions.append(cp.LinearDimension(count=10, increment="1m"))
    a.dependent_variables.append(
        {"type": "internal", "components": np.arange(10) + 1, "quantity_type": "scalar"}
    )

    b = cp.new()
    b.dimensions.append(cp.LinearDimension(count=10, increment="1m"))
    b.dependent_variables.append(
        {"type": "internal", "components": np.arange(10) + 2, "quantity_type": "scalar"}
    )

    c = cp.new()
    c.dimensions.append(cp.LinearDimension(count=10, increment="1m"))
    c.dependent_variables.append(
        {"type": "internal", "components": np.arange(10) + 1, "quantity_type": "scalar"}
    )
    c.dependent_variables.append(
        {"type": "internal", "components": np.arange(10) + 2, "quantity_type": "scalar"}
    )

    a_, b_ = c.split()

    assert a_ == a
    assert b_ == b


a_test = cp.new()
a_test.dimensions.append(cp.LinearDimension(count=10, increment="1s"))
a_test.add_dependent_variable(
    {
        "type": "internal",
        "quantity_type": "scalar",
        "unit": "m",
        "components": np.arange(10),
    }
)

a1_test = cp.new()
a1_test.dimensions.append(cp.LinearDimension(count=10, increment="1m"))
a1_test.add_dependent_variable(
    {
        "type": "internal",
        "quantity_type": "scalar",
        "unit": "m",
        "components": np.arange(10),
    }
)

b_test = cp.new()
b_test.dimensions.append(cp.LinearDimension(count=10, increment="1s"))
b_test.add_dependent_variable(
    {
        "type": "internal",
        "quantity_type": "scalar",
        "unit": "km",
        "components": np.arange(10, dtype=float),
    }
)

b1_test = cp.new()
b1_test.dimensions.append(cp.LinearDimension(count=10, increment="1s"))
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
    res = a_test + b_test
    out = np.arange(10) + 1000 * np.arange(10)
    assert np.allclose(res.y[0].components, [out])

    # sub
    res = a_test - b_test
    out = np.arange(10) - 1000 * np.arange(10)
    assert np.allclose(res.y[0].components, [out])

    res = b_test - a_test
    out = np.arange(10) - 1 / 1000 * np.arange(10)
    assert np.allclose(res.y[0].components, [out])

    # add scalar
    res = a_test + cp.ScalarQuantity("2m")
    out = np.arange(10) + 2
    assert np.allclose(res.y[0].components, [out])

    res = cp.ScalarQuantity("2m") + a_test
    assert np.allclose(res.y[0].components, [out])

    a_t = cp.as_csdm(np.arange(10))
    res = a_t + 5.12
    out = np.arange(10) + 5.12
    assert np.allclose(res.y[0].components, [out])

    res = 5.12 + a_t
    assert np.allclose(res.y[0].components, [out])

    # add complex
    res = a_t + 5.12 - 4j
    out = np.arange(10) + 5.12 - 4j
    assert np.allclose(res.y[0].components, [out])

    res = 5.12 - 4j + a_t
    assert np.allclose(res.y[0].components, [out])

    res = a_test / cp.ScalarQuantity("m") + 3 + 4j
    out = np.arange(10) + 3 + 4j
    assert np.allclose(res.y[0].components, [out])

    # subtract scalar
    res = a_test - cp.ScalarQuantity("2m")
    out = np.arange(10) - 2
    assert np.allclose(res.y[0].components, [out])

    res = cp.ScalarQuantity("2m") - a_test
    assert np.allclose(res.y[0].components, [-out])

    error = r"Cannot operate on CSDM objects with different dimensions."
    with pytest.raises(Exception, match=".*{0}.*".format(error)):
        res = a1_test + b_test

    error = r"Cannot operate on CSDM objects with different lengths of dependent"
    with pytest.raises(Exception, match=".*{0}.*".format(error)):
        res = a_test + b1_test


def test_iadd_isub():
    res = a_test.astype("float32")
    res += cp.ScalarQuantity("5.0cm")
    out = np.arange(10) + 0.05
    assert np.allclose(res.y[0].components, [out])

    res = a_test.astype("float32")
    res -= cp.ScalarQuantity("5.0cm")
    out = np.arange(10) - 0.05
    assert np.allclose(res.y[0].components, [out])

    res = a_test.astype("float32") / cp.ScalarQuantity("cm")
    res -= 0.05
    out = np.arange(10) - 0.05
    assert np.allclose(res.y[0].components, [out])

    out, new_test = get_test(float)  # in units of m
    new_test += b_test
    out += 1000 * np.arange(10)
    assert np.allclose(new_test.y[0].components, [out])

    out, new_test = get_test(float)  # in units of m
    res = new_test / cp.ScalarQuantity("m")
    res += 2.0
    out += 2.0
    assert np.allclose(res.y[0].components, [out])

    out, new_test = get_test(float)  # in units of m
    new_test -= b_test
    out -= 1000 * np.arange(10)
    assert np.allclose(new_test.y[0].components, [out])


def test_mul_truediv_pow():
    # mul
    res = a_test * 2
    out = a_test.y[0].components
    assert np.allclose(res.y[0].components, out * 2)
    assert id(a_test) != id(res)

    res = 2 * a_test
    assert np.allclose(res.y[0].components, out * 2)

    res = b_test * 1.34
    out = b_test.y[0].components
    assert np.allclose(res.y[0].components, out * 1.34)
    assert id(b_test) != id(res)

    res = 1.34 * a_test
    assert np.allclose(res.y[0].components, out * 1.34)

    res = b1_test * 1.423j
    out = b1_test.y[0].components
    assert np.allclose(res.y[0].components, out * 1.423j)
    assert id(b1_test) != id(res)

    res = 1.423j * b1_test
    assert np.allclose(res.y[0].components, out * 1.423j)

    lst = np.random.rand(5).astype(np.complex128)
    res = a1_test * lst[2]
    out = b1_test.y[0].components
    assert np.allclose(res.y[0].components, out * lst[2])
    assert id(a1_test) != id(res)

    # c = lst[2] * a1_test
    # assert np.allclose(c.y[0].components, out * lst[2])

    res = b1_test * cp.string_to_quantity("1.324 s")
    out = b1_test.y[0].components
    assert np.allclose(res.y[0].components, out * 1.324)
    assert str(res.y[0].unit) == "km s"
    assert id(b1_test) != id(res)

    res = b1_test * cp.ScalarQuantity("1.324 s")
    out = b1_test.y[0].components
    assert np.allclose(res.y[0].components, out * 1.324)
    assert str(res.y[0].unit) == "km s"
    assert id(b1_test) != id(res)

    res = cp.ScalarQuantity("1.324 s") * b1_test
    assert np.allclose(res.y[0].components, out * 1.324)

    # div
    res = a_test / 2
    out = a_test.y[0].components
    assert np.allclose(res.y[0].components, out / 2)
    assert id(a_test) != id(res)

    res = 2.0 / a_test.astype(float)
    assert np.allclose(res.y[0].components, 2 / out)

    res = b_test / 1.34
    out = b_test.y[0].components
    assert np.allclose(res.y[0].components, out / 1.34)
    assert id(b_test) != id(res)

    res = b1_test / 1.423j
    out = b1_test.y[0].components
    assert np.allclose(res.y[0].components, out / 1.423j)
    assert id(b1_test) != id(res)

    res = 1.423j / (b1_test + 1).astype(float)
    assert np.allclose(res.y[0].components, 1.423j / (out + 1))

    lst = np.random.rand(5).astype(np.complex128)
    res = a1_test / lst[2]
    out = b1_test.y[0].components
    assert np.allclose(res.y[0].components, out / lst[2])
    assert id(a1_test) != id(res)

    res = b1_test / cp.string_to_quantity("1.324 s")
    out = b1_test.y[0].components
    assert np.allclose(res.y[0].components, out / 1.324)
    assert str(res.y[0].unit) == "km / s"
    assert id(b1_test) != id(res)

    # c = cp.string_to_quantity("1.324 s") / (b1_test+1)
    # assert np.allclose(c.y[0].components, 1.324 / (out+1))

    res = b1_test / cp.ScalarQuantity("1.324 s")
    out = b1_test.y[0].components
    assert np.allclose(res.y[0].components, out / 1.324)
    assert str(res.y[0].unit) == "km / s"
    assert id(b1_test) != id(res)

    res = cp.ScalarQuantity("1.324 s") / (b_test + 1)
    assert np.allclose(res.y[0].components, 1.324 / (out + 1))

    error = r"unsupported operand type\(s\) \*: 'CSDM' and 'str'."
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        res = a_test * "3"

    error = r"Only scalar multiplication or division is allowed."
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        res = a_test * np.asarray([1, 2])

    error = r"unsupported operand type\(s\) /: 'CSDM' and 'str'."
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        res = a_test / "3"

    error = r"Only scalar multiplication or division is allowed."
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        res = a_test / np.asarray([1, 2])

    # pow
    res = b1_test ** 2
    out = b1_test.y[0].components
    assert np.allclose(res.y[0].components, np.power(out, 2))
    assert str(res.y[0].unit) == "km2"

    res **= 2
    assert np.allclose(res.y[0].components, np.power(out, 4))
    assert str(res.y[0].unit) == "km4"

    res **= 1 / 4
    assert np.allclose(res.y[0].components, out)
    assert str(res.y[0].unit) == "km"


def test_imul_itruediv():
    # imul
    out, new_test = get_test(int)
    res = new_test
    new_test *= 2
    out *= 2
    assert np.allclose(new_test.y[0].components, [out])
    assert id(new_test) == id(res)

    out, new_test = get_test(float)
    res = new_test
    new_test *= 2.312
    out *= 2.312
    assert np.allclose(new_test.y[0].components, [out])
    assert id(new_test) == id(res)

    out, new_test = get_test(complex)
    res = new_test
    new_test *= 2.12 + 1.1j
    out *= 2.12 + 1.1j
    assert np.allclose(new_test.y[0].components, [out])
    assert id(new_test) == id(res)

    out, new_test = get_test(float)
    res = new_test
    new_test *= cp.string_to_quantity("3.12 s/km")
    out *= 3.12
    assert np.allclose(new_test.y[0].components, [out])
    assert str(new_test.y[0].unit) == "m s / km"
    assert id(new_test) == id(res)

    out, new_test = get_test(float)
    res = new_test
    new_test *= cp.ScalarQuantity("3.12 s/km")
    out *= 3.12
    assert np.allclose(new_test.y[0].components, [out])
    assert str(new_test.y[0].unit) == "m s / km"
    assert id(new_test) == id(res)

    # itruediv

    out, new_test = get_test(float)
    res = new_test
    new_test /= 2
    out /= 2
    assert np.allclose(new_test.y[0].components, [out])
    assert id(new_test) == id(res)

    out, new_test = get_test(float)
    res = new_test
    new_test /= 2.312
    out /= 2.312
    assert np.allclose(new_test.y[0].components, [out])
    assert id(new_test) == id(res)

    out, new_test = get_test(complex)
    res = new_test
    new_test /= 2.12 + 1.1j
    out /= 2.12 + 1.1j
    assert np.allclose(new_test.y[0].components, [out])
    assert id(new_test) == id(res)

    out, new_test = get_test(float)
    res = new_test
    new_test /= cp.string_to_quantity("3.12 s/km")
    out /= 3.12
    assert np.allclose(new_test.y[0].components, [out])
    assert str(new_test.y[0].unit) == "km m / s"
    assert id(new_test) == id(res)

    out, new_test = get_test(float)
    res = new_test
    new_test /= cp.ScalarQuantity("3.12 s/km")
    out /= 3.12
    assert np.allclose(new_test.y[0].components, [out])
    assert str(new_test.y[0].unit) == "km m / s"
    assert id(new_test) == id(res)


def test_in_build():
    assert a_test == +a_test

    out = a_test.y[0].components
    assert np.allclose(abs(a_test).y[0].components[0], abs(out))


def test_max_min_clip():
    # max
    d_0 = cp.LinearDimension(count=5, increment="1s")
    d_1 = cp.LinearDimension(count=10, increment="1m")
    out, new_test = get_test_2d(float)
    assert out.max() == new_test.max().value
    assert str(new_test.max().unit) == "m"

    res = new_test.max(axis=1)
    assert np.allclose(out.max(0), res.y[0].components[0])
    assert res.dimensions[0] == d_0

    res = new_test.max(axis=0)
    assert np.allclose(out.max(1), res.y[0].components[0])
    assert res.dimensions[0] == d_1

    # min
    out, new_test = get_test_2d(float)
    assert out.min() == new_test.min().value
    assert str(new_test.min().unit) == "m"

    res = new_test.min(axis=1)
    assert np.allclose(out.min(0), res.y[0].components[0])
    assert res.dimensions[0] == d_0

    res = new_test.min(axis=0)
    assert np.allclose(out.min(1), res.y[0].components[0])
    assert res.dimensions[0] == d_1

    # clip
    res = new_test.clip(min=0)
    assert np.allclose(out.clip(min=0), res.y[0].components[0])

    res = new_test.clip(max=0.5)
    assert np.allclose(out.clip(max=0.5), res.y[0].components[0])


def test_real_imag_conj_angle():
    out, new_test = get_test_2d(complex)
    res = new_test.real
    assert res.y[0].numeric_type == "float64"
    assert np.allclose(out.real, res.y[0].components[0])

    res = np.real(new_test)
    assert res.y[0].numeric_type == "float64"
    assert np.allclose(out.real, res.y[0].components[0])

    res = new_test.imag
    assert res.y[0].numeric_type == "float64"
    assert np.allclose(out.imag, res.y[0].components[0])

    res = new_test.conj()
    assert res.y[0].numeric_type == "complex128"
    assert np.allclose(out.conj(), res.y[0].components[0])

    res = np.angle(new_test)
    assert res.y[0].numeric_type == "float64"
    assert np.allclose(np.angle(out), res.y[0].components[0])


def test_round_around():
    out, new_test = get_test_2d(float)
    res = new_test.round(1)
    assert np.allclose(out.round(1), res.y[0].components[0])

    res = np.around(new_test, 1)
    assert np.allclose(np.around(out, 1), res.y[0].components[0])


# def test_argmin_max():
#     out, new_test = get_test_2d(float)
#     assert np.allclose(np.argmax(out), np.argmax(new_test))
#     assert np.allclose(np.argmin(out), np.argmin(new_test))


def test_not_implemented_error():
    fn = [np.ptp, np.trace]
    for fn_ in fn:
        with pytest.raises(NotImplementedError, match=""):
            fn_(a_test)

"""Test for the csdm object
    1) sin, cos, tan, arcsin, arccos, arctan,
    2) sinh, cosh, tanh, arcsinh, arccosh, arctanh
    3) exp, exp2, expm1, log, log2, log10, log1p
    4) negative, positive, absolute, fabs, rint, sign, conj, conjugate
    5) sqrt, square, cbrt, reciprocal, power
"""
import numpy as np
import pytest

import csdmpy as cp

data = np.random.rand(15, 5, 10)
dim_1 = {"type": "linear", "count": 10, "increment": "1"}
dim_2 = {"type": "linear", "count": 5, "increment": "1"}
dim_3 = {"type": "linear", "count": 15, "increment": "1"}
d_v = {"type": "internal", "components": [data.ravel()], "quantity_type": "scalar"}
test_1 = cp.CSDM(dimensions=[dim_1, dim_2, dim_3], dependent_variables=[d_v])

data1 = np.random.rand(15 * 5 * 10).reshape(15, 5, 10) * 1e3 + 10
d_v = {"type": "internal", "components": [data1.ravel()], "quantity_type": "scalar"}
test_2 = cp.CSDM(dimensions=[dim_1, dim_2, dim_3], dependent_variables=[d_v])

# ---------------------------------------------------------------
# test for ufunc that apply to dimensionless dependent variables.
# __ufunc_list_dimensionless_unit__


def test_sin():
    res = np.sin(test_1)
    assert np.allclose(res.y[0].components[0], np.sin(data))


def test_cos():
    res = np.cos(test_1)
    assert np.allclose(res.y[0].components[0], np.cos(data))


def test_tan():
    res = np.tan(test_1)
    assert np.allclose(res.y[0].components[0], np.tan(data))


def test_arcsin():
    res = np.arcsin(test_1)
    assert np.allclose(res.y[0].components[0], np.arcsin(data))


def test_arccos():
    res = np.arccos(test_1)
    assert np.allclose(res.y[0].components[0], np.arccos(data))


def test_arctan():
    res = np.arctan(test_1)
    assert np.allclose(res.y[0].components[0], np.arctan(data))


def test_sinh():
    res = np.sinh(test_2)
    assert np.allclose(res.y[0].components[0], np.sinh(data1))


def test_cosh():
    res = np.cosh(test_2 + 2)
    assert np.allclose(res.y[0].components[0], np.cosh(data1 + 2))


def test_tanh():
    res = np.tanh(test_2)
    assert np.allclose(res.y[0].components[0], np.tanh(data1))


def test_arcsinh():
    res = np.arcsinh(test_1)
    assert np.allclose(res.y[0].components[0], np.arcsinh(data))


def test_arccosh():
    res = np.arccosh(test_2)
    assert np.allclose(res.y[0].components[0], np.arccosh(data1))


def test_arctanh():
    res = np.arctanh(test_1)
    assert np.allclose(res.y[0].components[0], np.arctanh(data))


def test_exp():
    res = np.exp(test_1)
    assert np.allclose(res.y[0].components[0], np.exp(data))


def test_exp2():
    res = np.exp2(test_1)
    assert np.allclose(res.y[0].components[0], np.exp2(data))


def test_expm1():
    res = np.expm1(test_1)
    assert np.allclose(res.y[0].components[0], np.expm1(data))


def test_log():
    res = np.log(test_1)
    assert np.allclose(res.y[0].components[0], np.log(data))


def test_log2():
    res = np.log2(test_1)
    assert np.allclose(res.y[0].components[0], np.log2(data))


def test_log10():
    res = np.log10(test_1)
    assert np.allclose(res.y[0].components[0], np.log10(data))


def test_log1p():
    res = np.log1p(test_1)
    assert np.allclose(res.y[0].components[0], np.log1p(data))


# test unit of components

data2 = np.random.rand(15 * 5 * 10).reshape(15, 5, 10) - 0.5

d_v = {
    "type": "internal",
    "components": [data2.ravel()],
    "quantity_type": "scalar",
    "unit": "m",
}
test_3 = cp.CSDM(dimensions=[dim_1, dim_2, dim_3], dependent_variables=[d_v])


def test_unsupported_unit():
    error = r"Cannot apply `sin` to quantity with physical type `length`"
    with pytest.raises(ValueError, match=error):
        np.sin(test_3)


# ------------------------------------------------------------------------------
# test for ufunc that are independent of the dependent variables dimensionality.
# __ufunc_list_unit_independent__


def test_negative():
    res = np.negative(test_3)
    assert np.allclose(res.y[0].components[0], np.negative(data2))


def test_positive():
    res = np.positive(test_3)
    assert np.allclose(res.y[0].components[0], np.positive(data2))


def test_absolute():
    res = np.absolute(test_3)
    assert np.allclose(res.y[0].components[0], np.absolute(data2))


def test_fabs():
    res = np.fabs(test_3)
    assert np.allclose(res.y[0].components[0], np.fabs(data2))


def test_rint():
    res = np.rint(test_3)
    assert np.allclose(res.y[0].components[0], np.rint(data2))


def test_sign():
    res = np.sign(test_3)
    assert np.allclose(res.y[0].components[0], np.sign(data2))


def test_conj():
    res = np.conj(test_3)
    assert np.allclose(res.y[0].components[0], np.conj(data2))


def test_conjugate():
    res = np.conjugate(test_3)
    assert np.allclose(res.y[0].components[0], np.conjugate(data2))


# -----------------------------------------------------------------
# test for ufunc that also apply to the unit of dependent variables.
# __ufunc_list_applies_to_unit__


def test_sqrt():
    res = np.sqrt(np.abs(test_3))
    assert np.allclose(res.y[0].components[0], np.sqrt(np.abs(data2)), equal_nan=True)
    assert str(res.y[0].unit) == "m(1/2)"


def test_square():
    res = np.square(test_3)
    assert np.allclose(res.y[0].components[0], np.square(data2))
    assert str(res.y[0].unit) == "m2"


def test_cbrt():
    res = np.cbrt(test_3)
    assert np.allclose(res.y[0].components[0], np.cbrt(data2), equal_nan=True)
    assert str(res.y[0].unit) == "m(1/3)"


def test_reciprocal():
    res = np.reciprocal(test_3)
    assert np.allclose(res.y[0].components[0], np.reciprocal(data2), equal_nan=True)
    assert str(res.y[0].unit) == "1 / m"


def test_power():
    res = np.power(np.abs(test_3), 5.3)
    assert np.allclose(
        res.y[0].components[0], np.power(np.abs(data2), 5.3), equal_nan=True
    )
    assert str(res.y[0].unit) == "m(53/10)"

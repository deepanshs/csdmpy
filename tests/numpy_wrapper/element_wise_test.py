# -*- coding: utf-8 -*-
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
a = cp.new()
dim1 = {"type": "linear", "count": 10, "increment": "1"}
dim2 = {"type": "linear", "count": 5, "increment": "1"}
dim3 = {"type": "linear", "count": 15, "increment": "1"}
dv = {"type": "internal", "components": [data.ravel()], "quantity_type": "scalar"}

a.add_dimension(dim1)
a.add_dimension(dim2)
a.add_dimension(dim3)
a.add_dependent_variable(dv)

data1 = np.random.rand(15 * 5 * 10).reshape(15, 5, 10) * 1e3 + 10
a1 = cp.new()
dv = {"type": "internal", "components": [data1.ravel()], "quantity_type": "scalar"}

a1.add_dimension(dim1)
a1.add_dimension(dim2)
a1.add_dimension(dim3)
a1.add_dependent_variable(dv)

# ---------------------------------------------------------------
# test for ufunc that apply to dimensionless dependent variables.
# __ufunc_list_dimensionless_unit__


def test_sin():
    b = np.sin(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.sin(data))


def test_cos():
    b = np.cos(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.cos(data))


def test_tan():
    b = np.tan(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.tan(data))


def test_arcsin():
    b = np.arcsin(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.arcsin(data))


def test_arccos():
    b = np.arccos(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.arccos(data))


def test_arctan():
    b = np.arctan(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.arctan(data))


def test_sinh():
    b = np.sinh(a1)
    assert np.allclose(b.dependent_variables[0].components[0], np.sinh(data1))


def test_cosh():
    b = np.cosh(a1)
    assert np.allclose(b.dependent_variables[0].components[0], np.cosh(data1))


def test_tanh():
    b = np.tanh(a1)
    assert np.allclose(b.dependent_variables[0].components[0], np.tanh(data1))


def test_arcsinh():
    b = np.arcsinh(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.arcsinh(data))


def test_arccosh():
    b = np.arccosh(a1)
    assert np.allclose(b.dependent_variables[0].components[0], np.arccosh(data1))


def test_arctanh():
    b = np.arctanh(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.arctanh(data))


def test_exp():
    b = np.exp(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.exp(data))


def test_exp2():
    b = np.exp2(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.exp2(data))


def test_expm1():
    b = np.expm1(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.expm1(data))


def test_log():
    b = np.log(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.log(data))


def test_log2():
    b = np.log2(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.log2(data))


def test_log10():
    b = np.log10(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.log10(data))


def test_log1p():
    b = np.log1p(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.log1p(data))


# test unit of components

data2 = np.random.rand(15 * 5 * 10).reshape(15, 5, 10) - 0.5
a2 = cp.new()
dv = {
    "type": "internal",
    "components": [data2.ravel()],
    "quantity_type": "scalar",
    "unit": "m",
}

a2.add_dimension(dim1)
a2.add_dimension(dim2)
a2.add_dimension(dim3)
a2.add_dependent_variable(dv)


def test_unsupported_unit():
    error = r"Cannot apply `sin` to quantity with physical type `length`"
    with pytest.raises(ValueError, match=error):
        np.sin(a2)


# ------------------------------------------------------------------------------
# test for ufunc that are independent of the dependent variables dimensionality.
# __ufunc_list_unit_independent__


def test_negative():
    b = np.negative(a2)
    assert np.allclose(b.dependent_variables[0].components[0], np.negative(data2))


def test_positive():
    b = np.positive(a2)
    assert np.allclose(b.dependent_variables[0].components[0], np.positive(data2))


def test_absolute():
    b = np.absolute(a2)
    assert np.allclose(b.dependent_variables[0].components[0], np.absolute(data2))


def test_fabs():
    b = np.fabs(a2)
    assert np.allclose(b.dependent_variables[0].components[0], np.fabs(data2))


def test_rint():
    b = np.rint(a2)
    assert np.allclose(b.dependent_variables[0].components[0], np.rint(data2))


def test_sign():
    b = np.sign(a2)
    assert np.allclose(b.dependent_variables[0].components[0], np.sign(data2))


def test_conj():
    b = np.conj(a2)
    assert np.allclose(b.dependent_variables[0].components[0], np.conj(data2))


def test_conjugate():
    b = np.conjugate(a2)
    assert np.allclose(b.dependent_variables[0].components[0], np.conjugate(data2))


# -----------------------------------------------------------------
# test for ufunc that also apply to the unit of dependent variables.
# __ufunc_list_applies_to_unit__


def test_sqrt():
    b = np.sqrt(a2)
    assert np.allclose(
        b.dependent_variables[0].components[0], np.sqrt(data2), equal_nan=True
    )
    assert str(b.dependent_variables[0].unit) == "m(1/2)"


def test_square():
    b = np.square(a2)
    assert np.allclose(b.dependent_variables[0].components[0], np.square(data2))
    assert str(b.dependent_variables[0].unit) == "m2"


def test_cbrt():
    b = np.cbrt(a2)
    assert np.allclose(
        b.dependent_variables[0].components[0], np.cbrt(data2), equal_nan=True
    )
    assert str(b.dependent_variables[0].unit) == "m(1/3)"


def test_reciprocal():
    b = np.reciprocal(a2)
    assert np.allclose(
        b.dependent_variables[0].components[0], np.reciprocal(data2), equal_nan=True
    )
    assert str(b.dependent_variables[0].unit) == "1 / m"


def test_power():
    b = np.power(a2, 5.3)
    assert np.allclose(
        b.dependent_variables[0].components[0], np.power(data2, 5.3), equal_nan=True
    )
    assert str(b.dependent_variables[0].unit) == "m(53/10)"

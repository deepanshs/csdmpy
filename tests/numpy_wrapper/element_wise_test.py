# -*- coding: utf-8 -*-
import numpy as np

import csdmpy as cp

data = np.random.rand(15, 5, 10)
a = cp.new()
dim1 = {"type": "linear", "count": 10, "increment": "1"}
dim2 = {"type": "linear", "count": 5, "increment": "1"}
dim3 = {"type": "linear", "count": 15, "increment": "1"}
dv = {"type": "internal", "components": [data], "quantity_type": "scalar"}


a.add_dimension(dim1)
a.add_dimension(dim2)
a.add_dependent_variable(dv)


def test_sin():
    b = cp.sin(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.sin(data))


def test_cos():
    b = cp.cos(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.cos(data))


def test_tan():
    b = cp.tan(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.tan(data))


def test_arcsin():
    b = cp.arcsin(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.arcsin(data))


def test_arccos():
    b = cp.arccos(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.arccos(data))


def test_arctan():
    b = cp.arctan(a)
    assert np.allclose(b.dependent_variables[0].components[0], np.arctan(data))

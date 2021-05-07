# -*- coding: utf-8 -*-
"""Test for the csdm object"""
from os import remove

import numpy as np

import csdmpy as cp

data = np.random.rand(15, 5, 10)
a = cp.new()
dim1 = {"type": "linear", "count": 10, "increment": "1"}
dim2 = {"type": "linear", "count": 5, "increment": "1"}
dim3 = {"type": "linear", "count": 15, "increment": "1"}
dv = {"type": "internal", "components": [data.ravel()], "quantity_type": "scalar"}

a.dimensions += [dim1, dim2, dim3]
a.add_dependent_variable(dv)

data1 = np.random.rand(15 * 5 * 10).reshape(15, 5, 10) * 1e3 + 10
a1 = cp.new()
dv = {"type": "internal", "components": [data1.ravel()], "quantity_type": "scalar"}

a1.dimensions += [dim1, dim2, dim3]
a1.add_dependent_variable(dv)

# ---------------------------------------------------------------
# test for ufunc that apply to dimensionless dependent variables.
# __ufunc_list_dimensionless_unit__


def test_T():
    b = a.T
    out = a.dependent_variables[0].components[0]
    assert np.allclose(b.dependent_variables[0].components[0], out.T)
    b.save("test_abc.csdf")

    b_ = cp.load("test_abc.csdf")
    assert b == b_
    remove("test_abc.csdf")

# -*- coding: utf-8 -*-
"""Test for the csdm object"""
from os import remove

import numpy as np

import csdmpy as cp

data = np.random.rand(4, 3, 2)
dim1 = {"type": "linear", "count": 2, "increment": "1"}
dim2 = {"type": "linear", "count": 3, "increment": "1"}
dim3 = {"type": "linear", "count": 4, "increment": "1"}
dv = {"type": "internal", "components": [data.ravel()], "quantity_type": "scalar"}
obj_1 = cp.CSDM(dimensions=[dim1, dim2, dim3], dependent_variables=[dv])

# data1 = np.random.rand(15 * 5 * 10).reshape(15, 5, 10) * 1e3 + 10
# dv = {"type": "internal", "components": [data1.ravel()], "quantity_type": "scalar"}
# obj_2 = cp.CSDM(dimensions=[dim1, dim2, dim3], dependent_variables=[dv])

# ---------------------------------------------------------------
# test for ufunc that apply to dimensionless dependent variables.
# __ufunc_list_dimensionless_unit__


def test_00():
    """shape test"""
    test1 = obj_1.T
    out = obj_1.y[0].components[0]
    assert np.allclose(test1.y[0].components[0], out.T)
    test1.save("test_abc.csdf")

    test2 = cp.load("test_abc.csdf")
    assert test1 == test2
    remove("test_abc.csdf")

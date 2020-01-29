# -*- coding: utf-8 -*-
import numpy as np

import csdmpy as cp

data = np.random.rand(50 * 15).reshape(15, 5, 10)
a = cp.new()
dim1 = {"type": "linear", "count": 10, "increment": "1"}
dim2 = {"type": "linear", "count": 5, "increment": "1"}
dim3 = {"type": "linear", "count": 15, "increment": "1"}
dv = {"type": "internal", "components": [data], "quantity_type": "scalar"}


a.add_dimension(dim1)
a.add_dimension(dim2)
a.add_dimension(dim3)
a.add_dependent_variable(dv)


def test_sum():
    dimensions = [0, 1, 2]
    for dimension in dimensions:
        b = cp.sum(a, dimension=dimension)
        components = b.dependent_variables[0].components[0]
        assert np.allclose(components, data.sum(axis=-dimension - 1))

    dimensions = [(0, 1), [0, 2], (1, 2)]
    for dimension in dimensions:
        b = cp.sum(a, dimension=dimension)
        components = b.dependent_variables[0].components[0]
        dim_ = tuple(-i - 1 for i in dimension)
        assert np.allclose(components, data.sum(axis=dim_))


def test_prod():
    dimensions = [0, 1, 2]
    for dimension in dimensions:
        b = cp.prod(a, dimension=dimension)
        components = b.dependent_variables[0].components[0]
        assert np.allclose(components, data.prod(axis=-dimension - 1))

    dimensions = [(0, 1), (0, 2), [1, 2]]
    for dimension in dimensions:
        b = cp.prod(a, dimension=dimension)
        components = b.dependent_variables[0].components[0]
        dim_ = tuple(-i - 1 for i in dimension)
        assert np.allclose(components, data.prod(axis=dim_))

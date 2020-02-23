# -*- coding: utf-8 -*-
"""Test for the csdm object
    1) sum, mean, var, std, prod.
"""
import numpy as np
import pytest

import csdmpy as cp

data = np.random.rand(50 * 15).reshape(15, 5, 10)
a = cp.new()
dim = []
dim.append({"type": "linear", "count": 10, "increment": "1"})
dim.append({"type": "linear", "count": 5, "increment": "1"})
dim.append({"type": "linear", "count": 15, "increment": "1"})
dv = {"type": "internal", "components": [data.ravel()], "quantity_type": "scalar"}


a.add_dimension(dim[0])
a.add_dimension(dim[1])
a.add_dimension(dim[2])
a.add_dependent_variable(dv)


def test_exceptions():
    error = r"Index/Indices are expected as integer"
    with pytest.raises(TypeError, match=error):
        a.sum(axis=0.2)

    error = r"Index/Indices are expected as integer"
    with pytest.raises(TypeError, match=error):
        a.sum(axis=(1, 0.2))

    error = r"The `index` 4 cannot be greater than the total number of dimensions - 1"
    with pytest.raises(IndexError, match=error):
        a.sum(axis=4)


def test_sum():
    dimensions = [0, 1, 2]
    i = [[1, 2], [0, 2], [0, 1]]
    assert np.allclose(
        np.sum(a=a, axis=0).dependent_variables[0].components, data.sum(axis=-1)
    )
    assert np.allclose(
        np.sum(a, 0).dependent_variables[0].components, data.sum(axis=-1)
    )
    assert np.allclose(
        np.sum(a, 1).dependent_variables[0].components, data.sum(axis=-2)
    )
    for i_, dimension in zip(i, dimensions):
        b = a.sum(axis=dimension)
        components = b.dependent_variables[0].components[0]
        assert np.allclose(components, data.sum(axis=-dimension - 1))
        assert b.dimensions[0] == a.dimensions[i_[0]]
        assert b.dimensions[1] == a.dimensions[i_[1]]

    dimensions = [(0, 1), [0, 2], (1, 2)]
    i = [2, 1, 0]
    for i_, dimension in zip(i, dimensions):
        b = a.sum(axis=dimension)
        components = b.dependent_variables[0].components[0]
        dim_ = tuple(-i - 1 for i in dimension)
        assert np.allclose(components, data.sum(axis=dim_))
        assert b.dimensions[0] == a.dimensions[i_]

    b = a.sum()
    assert np.allclose(b, data.sum())

    assert np.allclose(a.sum(-1).dependent_variables[0].components, data.sum(axis=0))


def test_mean():
    dimensions = [0, 1, 2]
    i = [[1, 2], [0, 2], [0, 1]]
    for i_, dimension in zip(i, dimensions):
        b = a.mean(axis=dimension)
        components = b.dependent_variables[0].components[0]
        assert np.allclose(components, data.mean(axis=-dimension - 1))
        assert b.dimensions[0] == a.dimensions[i_[0]]
        assert b.dimensions[1] == a.dimensions[i_[1]]

    dimensions = [(0, 1), [0, 2], (1, 2)]
    i = [2, 1, 0]
    for i_, dimension in zip(i, dimensions):
        b = a.mean(axis=dimension)
        components = b.dependent_variables[0].components[0]
        dim_ = tuple(-i - 1 for i in dimension)
        assert np.allclose(components, data.mean(axis=dim_))
        assert b.dimensions[0] == a.dimensions[i_]

    b = a.mean()
    assert np.allclose(b, data.mean())


def test_var():
    dimensions = [0, 1, 2]
    i = [[1, 2], [0, 2], [0, 1]]
    for i_, dimension in zip(i, dimensions):
        b = a.var(axis=dimension)
        components = b.dependent_variables[0].components[0]
        assert np.allclose(components, data.var(axis=-dimension - 1))
        assert b.dimensions[0] == a.dimensions[i_[0]]
        assert b.dimensions[1] == a.dimensions[i_[1]]

    dimensions = [(0, 1), [0, 2], (1, 2)]
    i = [2, 1, 0]
    for i_, dimension in zip(i, dimensions):
        b = a.var(axis=dimension)
        components = b.dependent_variables[0].components[0]
        dim_ = tuple(-i - 1 for i in dimension)
        assert np.allclose(components, data.var(axis=dim_))
        assert b.dimensions[0] == a.dimensions[i_]

    b = a.var()
    assert np.allclose(b, data.var())


def test_std():
    dimensions = [0, 1, 2]
    i = [[1, 2], [0, 2], [0, 1]]
    for i_, dimension in zip(i, dimensions):
        b = a.std(axis=dimension)
        components = b.dependent_variables[0].components[0]
        assert np.allclose(components, data.std(axis=-dimension - 1))
        assert b.dimensions[0] == a.dimensions[i_[0]]
        assert b.dimensions[1] == a.dimensions[i_[1]]

    dimensions = [(0, 1), [0, 2], (1, 2)]
    i = [2, 1, 0]
    for i_, dimension in zip(i, dimensions):
        b = a.std(axis=dimension)
        components = b.dependent_variables[0].components[0]
        dim_ = tuple(-i - 1 for i in dimension)
        assert np.allclose(components, data.std(axis=dim_))
        assert b.dimensions[0] == a.dimensions[i_]

    b = a.std()
    assert np.allclose(b, data.std())


def test_prod():
    dimensions = [0, 1, 2]
    i = [[1, 2], [0, 2], [0, 1]]
    for i_, dimension in zip(i, dimensions):
        b = a.prod(axis=dimension)
        components = b.dependent_variables[0].components[0]
        assert np.allclose(components, data.prod(axis=-dimension - 1))
        assert b.dimensions[0] == a.dimensions[i_[0]]
        assert b.dimensions[1] == a.dimensions[i_[1]]

    dimensions = [(0, 1), [0, 2], (1, 2)]
    i = [2, 1, 0]
    for i_, dimension in zip(i, dimensions):
        b = a.prod(axis=dimension)
        components = b.dependent_variables[0].components[0]
        dim_ = tuple(-i - 1 for i in dimension)
        assert np.allclose(components, data.prod(axis=dim_))
        assert b.dimensions[0] == a.dimensions[i_]

    b = a.prod()
    assert np.allclose(b, data.prod())

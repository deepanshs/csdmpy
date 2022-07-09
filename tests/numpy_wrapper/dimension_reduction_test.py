"""Test for the csdm object
    1) sum, mean, var, std, prod.
"""
import numpy as np
import pytest

import csdmpy as cp

data = np.random.rand(50 * 15).reshape(15, 5, 10)
dim = [
    {"type": "linear", "count": 10, "increment": "1"},
    {"type": "linear", "count": 5, "increment": "1"},
    {"type": "linear", "count": 15, "increment": "1"},
]
dv = {"type": "internal", "components": [data.ravel()], "quantity_type": "scalar"}
test_1 = cp.CSDM(dimensions=dim, dependent_variables=[dv])


def test_exceptions():
    error = r"Index/Indices are expected as integer"
    with pytest.raises(TypeError, match=error):
        test_1.sum(axis=0.2)

    error = r"Index/Indices are expected as integer"
    with pytest.raises(TypeError, match=error):
        test_1.sum(axis=(1, 0.2))

    error = r"The `index` 4 cannot be greater than the total number of dimensions - 1"
    with pytest.raises(IndexError, match=error):
        test_1.sum(axis=4)


def test_sum_cumsum():
    dimensions = [0, 1, 2]
    i = [[1, 2], [0, 2], [0, 1]]
    for np_fn in [np.sum, np.cumsum]:
        assert np.allclose(
            np_fn(a=test_1, axis=0).y[0].components, np_fn(data, axis=-1)
        )
        assert np.allclose(np_fn(test_1, 0).y[0].components, np_fn(data, axis=-1))
        assert np.allclose(np_fn(test_1, 1).y[0].components, np_fn(data, axis=-2))
        for index, dimension in zip(i, dimensions):
            res = np_fn(test_1, axis=dimension)
            components = res.y[0].components[0]
            assert np.allclose(components, np_fn(data, axis=-dimension - 1))
            assert res.dimensions[0] == test_1.dimensions[index[0]]
            assert res.dimensions[1] == test_1.dimensions[index[1]]

    dimensions = [(0, 1), [0, 2], (1, 2)]
    i = [2, 1, 0]
    for index, dimension in zip(i, dimensions):
        res = np.sum(test_1, axis=dimension)
        components = res.y[0].components[0]
        dim_ = tuple(-i - 1 for i in dimension)
        assert np.allclose(components, np.sum(data, axis=dim_))
        assert res.dimensions[0] == test_1.dimensions[index]

    res = test_1.sum()
    assert np.allclose(res, data.sum())

    assert np.allclose(test_1.sum(-1).y[0].components, data.sum(axis=0))


def test_reduction_multi_axis():
    cp_fn = ["prod", "sum", "mean", "var", "std"]
    np_fn = [np.prod, np.sum, np.mean, np.var, np.std]
    for fn_np, fn_cp in zip(np_fn, cp_fn):
        dimensions = [0, 1, 2]
        i = [[1, 2], [0, 2], [0, 1]]
        for index, dimension in zip(i, dimensions):
            res = fn_np(test_1, axis=dimension)
            components = res.y[0].components[0]
            print(dimension)
            assert np.allclose(components, fn_np(data, axis=-dimension - 1))
            assert res.dimensions[0] == test_1.dimensions[index[0]]
            assert res.dimensions[1] == test_1.dimensions[index[1]]

        dimensions = [(0, 1), [0, 2], (1, 2)]
        i = [2, 1, 0]
        for index, dimension in zip(i, dimensions):
            res = test_1.__getattribute__(fn_cp)(axis=dimension)
            components = res.y[0].components[0]
            dim_ = tuple(-i - 1 for i in dimension)
            assert np.allclose(components, fn_np(data, axis=dim_))
            assert res.dimensions[0] == test_1.dimensions[index]

        res = test_1.__getattribute__(fn_cp)()
        assert np.allclose(res, fn_np(data))


def test_reduction_single_axis():
    dimensions = [0, 1, 2]
    i = [[1, 2], [0, 2], [0, 1]]
    cp_fn = ["cumprod", "cumsum", "argmin", "argmax"]
    np_fn = [np.cumprod, np.cumsum, np.argmin, np.argmax]
    for fn_np, fn_cp in zip(np_fn, cp_fn):
        for index, dimension in zip(i, dimensions):
            res = fn_np(test_1, axis=dimension)
            components = res.y[0].components[0]
            assert np.allclose(components, fn_np(data, axis=-dimension - 1))
            assert res.dimensions[0] == test_1.dimensions[index[0]]
            assert res.dimensions[1] == test_1.dimensions[index[1]]

        res = test_1.__getattribute__(fn_cp)()
        assert np.allclose(res, fn_np(data))

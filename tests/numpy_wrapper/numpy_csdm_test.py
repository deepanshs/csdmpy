import numpy as np
import pytest

import csdmpy as cp

data = np.random.rand(15, 5, 10)
dim_1 = {"type": "linear", "count": 10, "increment": "1"}
dim_2 = {"type": "linear", "count": 5, "increment": "1"}
dim_3 = {"type": "linear", "count": 15, "increment": "1"}
d_v = {"type": "internal", "components": [data.ravel()], "quantity_type": "scalar"}
test_1 = cp.CSDM(dimensions=[dim_1, dim_2, dim_3], dependent_variables=[d_v])

test_2 = cp.CSDM(
    dimensions=[dim_1], dependent_variables=[cp.as_dependent_variable(np.ones(10) * 2)]
)


def test_mult():
    res = np.ones(10) * 2
    data_new = test_1 * res[:, None, None]
    assert np.allclose(data_new.y[0].components[0], data * res[None, None, :])

    data_new = res[:, None, None] * test_1
    assert np.allclose(data_new.y[0].components[0], res[None, None, :] * data)

    test_a = test_1.copy()
    test_a *= res[:, None, None]
    assert np.allclose(test_a.y[0].components[0], data * res[None, None, :])

    data_new = test_1 * test_2
    assert np.allclose(data_new.y[0].components[0], data * res[None, None, :])


def test_div():
    res = np.ones(10) * 2
    data_new = test_1 / res[:, None, None]
    assert np.allclose(data_new.y[0].components[0], data / res[None, None, :])

    data_new = res[:, None, None] / test_1
    assert np.allclose(data_new.y[0].components[0], res[None, None, :] / data)

    test_a = test_1.copy()
    test_a /= res[:, None, None]
    assert np.allclose(test_a.y[0].components[0], data / res[None, None, :])

    data_new = test_1 / test_2
    assert np.allclose(data_new.y[0].components[0], data / res[None, None, :])


def test_raise():
    test_dvs = cp.CSDM(dimensions=[dim_1], dependent_variables=[d_v, d_v])
    error = "'CSDM' and multi dependent variable CSDM"
    with pytest.raises(TypeError, match=f".*{error}.*"):
        _ = test_1 * test_dvs

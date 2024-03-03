import numpy as np

import csdmpy as cp


def test_1_linear():
    dim1 = cp.as_dimension(np.arange(4))
    dim2 = cp.as_dimension(np.arange(10))
    dv = cp.as_dependent_variable(np.arange(40))
    dataset = cp.CSDM(dimensions=[dim1, dim2], dependent_variables=[dv])

    new_dim1 = cp.LinearDimension(count=5, increment="2 Hz")
    new_dim2 = cp.LinearDimension(count=20, increment="1 s")

    ds1 = np.tile(dataset, (1, new_dim2, new_dim1))
    ds2 = np.tile(dataset, (1, 2, new_dim1))

    assert ds1.shape == (4, 20, 5)
    assert ds2.shape == (4, 20, 5)

    tiled = np.tile(dv.components[0], (new_dim1.count, 2, 1))
    np.allclose(ds1.y[0].components[0], tiled)
    np.allclose(ds2.y[0].components[0], tiled)

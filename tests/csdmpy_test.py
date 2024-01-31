import numpy as np

import csdmpy as cp


def test_append():
    out = (np.random.rand(50).reshape(10, 5) * 10000).astype(int)
    out1 = np.random.rand(50).astype(float).reshape(10, 5)
    out2 = np.random.rand(50).astype(complex).reshape(10, 5)

    d_0 = cp.LinearDimension(count=5, increment="1s")
    d_1 = cp.LinearDimension(count=10, increment="1m")
    units = ["m", "s", "t"]
    dv = [
        cp.DependentVariable(
            type="internal",
            quantity_type="scalar",
            unit=unit,
            components=item.ravel(),
        )
        for unit, item in zip(units, [out, out1, out2])
    ]

    obj = cp.CSDM(dimensions=[d_0, d_1], dependent_variables=[dv[0]])
    obj1 = cp.CSDM(dimensions=[d_0, d_1], dependent_variables=dv[1:])
    obj2 = cp.CSDM(dimensions=[d_0, d_1], dependent_variables=[dv[1]])
    obj3 = cp.CSDM(dimensions=[d_0, d_1], dependent_variables=[dv[2]])
    obj4 = cp.CSDM(dimensions=[d_0, d_1], dependent_variables=dv[::-1])

    new = cp.join([obj, obj1, obj2, obj3, obj4])

    assert len(new.y) == 8
    assert list(new.y) == [dv[0], dv[1], dv[2], dv[1], dv[2], dv[2], dv[1], dv[0]]

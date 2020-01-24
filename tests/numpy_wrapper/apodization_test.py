import csdmpy as cp
import numpy as np

a = cp.new()
data = np.ones(5 * 10).reshape(10, 5)
dim1 = {"type": "linear", "count": 5, "increment": "1 s"}
dim2 = {"type": "linear", "count": 10, "increment": "1 m"}
dv = {"type": "internal", "components": [data], "quantity_type": "scalar"}

a.add_dimension(dim1)
a.add_dimension(dim2)
a.add_dependent_variable(dv)


def test_sin():
    b = cp.apodize.sin(a, "(2*3.1415*0.1) s^-1", dimension=(0))
    s = np.sin(2 * 3.1415 * 0.1 * np.arange(5)) * data[0, :]
    assert np.allclose(s, b.dependent_variables[0].components[0][0, :])

    b = cp.apodize.sin(a, "(2*3.1415*0.1) m^-1", dimension=1)
    s = np.sin(2 * 3.1415 * 0.1 * np.arange(10)) * data[:, 0]
    assert np.allclose(s, b.dependent_variables[0].components[0][:, 0])


def test_cos():
    b = cp.apodize.cos(a, "(2*3.1415*0.1) s^-1", dimension=(0))
    s = np.cos(2 * 3.1415 * 0.1 * np.arange(5)) * data[0, :]
    assert np.allclose(s, b.dependent_variables[0].components[0][0, :])

    b = cp.apodize.cos(a, "(2*3.1415*0.1) m^-1", dimension=1)
    s = np.cos(2 * 3.1415 * 0.1 * np.arange(10)) * data[:, 0]
    assert np.allclose(s, b.dependent_variables[0].components[0][:, 0])

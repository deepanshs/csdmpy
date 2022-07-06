"""Apodization module"""
import numpy as np

import csdmpy as cp

data = np.ones(5 * 10).reshape(10, 5)
dim1 = {"type": "linear", "count": 5, "increment": "1 s"}
dim2 = {"type": "linear", "count": 10, "increment": "1 m"}
dv = {"type": "internal", "components": [data.ravel()], "quantity_type": "scalar"}
obj = cp.CSDM(dimensions=[dim1, dim2], dependent_variables=[dv])


def test_sin():
    """sin test"""
    test_cp = cp.apodize.sin(obj, "(2*3.1415*0.1) s^-1", dimension=(0))
    test_np = np.sin(2 * 3.1415 * 0.1 * np.arange(5)) * data[0, :]
    assert np.allclose(test_np, test_cp.y[0].components[0][0, :])

    test_cp = cp.apodize.sin(obj, "(2*3.1415*0.1) m^-1", dimension=1)
    test_np = np.sin(2 * 3.1415 * 0.1 * np.arange(10)) * data[:, 0]
    assert np.allclose(test_np, test_cp.y[0].components[0][:, 0])


def test_cos():
    """cos test"""
    test_cp = cp.apodize.cos(obj, "(2*3.1415*0.1) s^-1", dimension=(0))
    test_np = np.cos(2 * 3.1415 * 0.1 * np.arange(5)) * data[0, :]
    assert np.allclose(test_np, test_cp.y[0].components[0][0, :])

    test_cp = cp.apodize.cos(obj, "(2*3.1415*0.1) m^-1", dimension=1)
    test_np = np.cos(2 * 3.1415 * 0.1 * np.arange(10)) * data[:, 0]
    assert np.allclose(test_np, test_cp.y[0].components[0][:, 0])


def test_tan():
    """tan test"""
    test_cp = cp.apodize.tan(obj, "(2*3.1415*0.1) s^-1", dimension=(0))
    test_np = np.tan(2 * 3.1415 * 0.1 * np.arange(5)) * data[0, :]
    assert np.allclose(test_np, test_cp.y[0].components[0][0, :])

    test_cp = cp.apodize.tan(obj, "(2*3.1415*0.1) m^-1", dimension=1)
    test_np = np.tan(2 * 3.1415 * 0.1 * np.arange(10)) * data[:, 0]
    assert np.allclose(test_np, test_cp.y[0].components[0][:, 0])


def test_arcsin():
    """arc sin test"""
    test_cp = cp.apodize.arcsin(obj, "(1/(2*3.1415*10)) s^-1", dimension=(0))
    test_np = np.arcsin(1 / (2 * 3.1415 * 10) * np.arange(5)) * data[0, :]
    assert np.allclose(test_np, test_cp.y[0].components[0][0, :])

    test_cp = cp.apodize.arcsin(obj, "(1/(2*3.1415*10)) m^-1", dimension=1)
    test_np = np.arcsin(1 / (2 * 3.1415 * 10) * np.arange(10)) * data[:, 0]
    assert np.allclose(test_np, test_cp.y[0].components[0][:, 0])


def test_arccos():
    """arc cos test"""
    test_cp = cp.apodize.arccos(obj, "(1/(2*3.1415*10)) s^-1", dimension=(0))
    test_np = np.arccos(1 / (2 * 3.1415 * 10) * np.arange(5)) * data[0, :]
    assert np.allclose(test_np, test_cp.y[0].components[0][0, :])

    test_cp = cp.apodize.arccos(obj, "(1/(2*3.1415*10)) m^-1", dimension=1)
    test_np = np.arccos(1 / (2 * 3.1415 * 10) * np.arange(10)) * data[:, 0]
    assert np.allclose(test_np, test_cp.y[0].components[0][:, 0])


def test_arctan():
    """arc tan test"""
    test_cp = cp.apodize.arctan(obj, "(2*3.1415*10) s^-1", dimension=(0))
    test_np = np.arctan(2 * 3.1415 * 10 * np.arange(5)) * data[0, :]
    assert np.allclose(test_np, test_cp.y[0].components[0][0, :])

    test_cp = cp.apodize.arctan(obj, "(2*3.1415*10) m^-1", dimension=1)
    test_np = np.arctan(2 * 3.1415 * 10 * np.arange(10)) * data[:, 0]
    assert np.allclose(test_np, test_cp.y[0].components[0][:, 0])


def test_exp():
    """exp test"""
    test_cp = cp.apodize.exp(obj, "-0.1 s^-1", dimension=(0))
    test_np = np.exp(-0.1 * np.arange(5)) * data[0, :]
    assert np.allclose(test_np, test_cp.y[0].components[0][0, :])

    test_cp = cp.apodize.exp(obj, "-0.1 m^-1", dimension=1)
    test_np = np.exp(-0.1 * np.arange(10)) * data[:, 0]
    assert np.allclose(test_np, test_cp.y[0].components[0][:, 0])

# -*- coding: utf-8 -*-
import numpy as np

import csdmpy as cp
import csdmpy.statistics as stat


def get_gaussian(x, b, c):
    return np.exp(-((x - b) ** 2) / (2 * c ** 2))


def test_01():
    x = np.arange(100) * 2 - 100.0
    gauss = get_gaussian(x, 5.0, 4.0)
    csdm = cp.as_csdm(gauss, unit="T")
    csdm.dimensions[0] = cp.as_dimension(x, unit="µm")

    gauss_integral = 4.0 * np.sqrt(2 * np.pi)

    # integration
    int_csdm = stat.integral(csdm)
    assert np.allclose(int_csdm.value, gauss_integral)
    assert str(int_csdm.unit) == "T um"

    # mean
    mean_csdm = stat.mean(csdm)[0]
    assert np.allclose(mean_csdm.value, 5.0)
    assert str(mean_csdm.unit) == "um"

    # variance
    var_csdm = stat.var(csdm)[0]
    assert np.allclose(var_csdm.value, 16.0)
    assert str(var_csdm.unit) == "um2"

    # standard deviation
    std_csdm = stat.std(csdm)[0]
    assert np.allclose(std_csdm.value, 4.0)
    assert str(std_csdm.unit) == "um"


def test_02():
    x = np.arange(100) - 50.0
    y = np.arange(500) * 0.1 - 25.0
    gauss1 = get_gaussian(x, 5.0, 4.0)[np.newaxis, :]
    gauss2 = get_gaussian(y, 0.50, 0.40)[:, np.newaxis]
    csdm = cp.as_csdm(gauss1 * gauss2, unit="K")
    csdm.dimensions[1] = cp.as_dimension(y, unit="s")
    csdm.dimensions[0] = cp.as_dimension(x, unit="deg")

    gauss_integral = 4.0 * 2 * np.pi * 0.4

    # integration
    int_csdm = stat.integral(csdm)
    assert np.allclose(int_csdm.value, gauss_integral)
    assert str(int_csdm.unit) == "deg K s"

    # mean
    mean_csdm = stat.mean(csdm)
    assert np.allclose(mean_csdm[0].value, 5.0)
    assert np.allclose(mean_csdm[1].value, 0.5)
    assert str(mean_csdm[0].unit) == "deg"
    assert str(mean_csdm[1].unit) == "s"

    # variance
    var_csdm = stat.var(csdm)
    assert np.allclose(var_csdm[0].value, 16.0)
    assert np.allclose(var_csdm[1].value, 0.16)
    assert str(var_csdm[0].unit) == "deg2"
    assert str(var_csdm[1].unit) == "s2"

    # standard deviation
    std_csdm = stat.std(csdm)
    assert np.allclose(std_csdm[0].value, 4.0)
    assert np.allclose(std_csdm[1].value, 0.4)
    assert str(std_csdm[0].unit) == "deg"
    assert str(std_csdm[1].unit) == "s"

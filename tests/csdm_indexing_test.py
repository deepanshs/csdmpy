# -*- coding: utf-8 -*-
"""Test for the csdm object
    1) indexing and slicing test
"""
import numpy as np
import pytest

import csdmpy as cp


array = np.arange(6000).reshape(30, 20, 10)
a_obj = cp.as_csdm(array, unit="A", quantity_type="scalar")
d2 = cp.LinearDimension(
    count=30,
    increment="2.4 ms",
    coordinates_offset="-5ms",
    label="t3",
    application={"blah": "blah"},
)

arr = 10 ** (np.arange(20) / 10)
d1 = cp.as_dimension(arr, unit="m/s", label="d2")

d0 = cp.Dimension(type="labeled", labels=list("abcdefghij"), label="l1")

a_obj.dimensions[0] = d0
a_obj.dimensions[1] = d1
a_obj.dimensions[2] = d2


def test_shape():
    assert a_obj.shape == (10, 20, 30)
    assert a_obj.dependent_variables[0].components[0].shape == (30, 20, 10)


def test_index_0():
    l_test = a_obj[:, 0, 0]
    assert l_test.shape == (10,)
    assert l_test.dimensions[0] == d0
    assert np.allclose(l_test.dependent_variables[0].components, array[0, 0, :])
    assert str(l_test.dependent_variables[0].unit) == "A"


def test_index_1():
    l_test = a_obj[1:9:2, 0, 0]
    assert l_test.shape == (4,)
    assert l_test.dimensions[0].count == 4
    assert np.all(l_test.dimensions[0].coordinates == np.asarray(list("bdfh")))
    assert np.allclose(l_test.dependent_variables[0].components, array[0, 0, 1:9:2])
    assert str(l_test.dependent_variables[0].unit) == "A"


def test_index_2():
    l_test = a_obj[:, :, 0]
    assert l_test.shape == (10, 20)
    assert l_test.dimensions[0] == d0
    assert l_test.dimensions[1] == d1
    assert np.allclose(l_test.dependent_variables[0].components, array[0, :, :])
    assert str(l_test.dependent_variables[0].unit) == "A"


def test_index_3():
    l_test = a_obj[:, 4:19:4, 0]
    assert l_test.shape == (10, 4)
    assert l_test.dimensions[0] == d0
    assert np.allclose(l_test.dimensions[1].coordinates.value, arr[4:19:4])
    assert l_test.dimensions[1].label == "d2"
    assert np.allclose(l_test.dependent_variables[0].components, array[0, 4:19:4, :])
    assert str(l_test.dependent_variables[0].unit) == "A"


def test_index_4():
    l_test = a_obj[:, 4:19:2, :]
    assert l_test.shape == (10, 8, 30)
    assert l_test.dimensions[0] == d0
    assert l_test.dimensions[2] == d2
    assert np.allclose(l_test.dimensions[1].coordinates.value, arr[4:19:2])
    assert l_test.dimensions[1].label == "d2"
    assert np.allclose(l_test.dependent_variables[0].components, array[:, 4:19:2, :])
    assert str(l_test.dependent_variables[0].unit) == "A"


def test_index_5():
    l_test = a_obj[0, :, :]
    assert l_test.shape == (20, 30)
    assert l_test.dimensions[0] == d1
    assert l_test.dimensions[1] == d2
    assert np.allclose(l_test.dependent_variables[0].components, array[:, :, 0])
    assert str(l_test.dependent_variables[0].unit) == "A"


def test_index_6():
    l_test = a_obj[3]
    assert l_test.shape == (20, 30)
    assert l_test.dimensions[0] == d1
    assert l_test.dimensions[1] == d2
    assert np.allclose(l_test.dependent_variables[0].components, array[:, :, 3])
    assert str(l_test.dependent_variables[0].unit) == "A"


def test_index_7():
    l_test = a_obj[1, 3, 9]
    assert l_test.shape == ()
    assert np.allclose(l_test.dependent_variables[0].components[0], array[9, 3, 1])
    assert str(l_test.dependent_variables[0].unit) == "A"

    l_test = a_obj[(1, 3, 19)]
    assert l_test.shape == ()
    assert np.allclose(l_test.dependent_variables[0].components[0], array[19, 3, 1])
    assert str(l_test.dependent_variables[0].unit) == "A"


def test_index_8():
    error = "Fancy indexing using tuples or lists may result in"
    with pytest.raises(NotImplementedError, match=".*{0}.*".format(error)):
        a_obj[(1, 3, 9), 10]

# -*- coding: utf-8 -*-
from os.path import split

import numpy as np
import pytest

import csdmpy as cp


def test_load_files():
    assert split(cp.tests.test01)[1] == "yis83dhuj1q7v2srw2b1hjnb66d1rw1h.csdf"
    assert split(cp.tests.test02)[1] == "0jsvs9bmme8vf6yn76bctkhfxm4vkcc8.csdf"


def test00():
    error = "Missing the value for the required `filename` attribute."
    with pytest.raises(Exception, match=".*{0}.*".format(error)):
        cp.load()


def test01():
    dataset = cp.load(cp.tests.test01)

    assert dataset.dependent_variables[0].type == "internal"

    # encoding is always set to 'base64' after import
    assert dataset.dependent_variables[0].encoding == "base64"

    assert dataset.dependent_variables[0].numeric_type == "float32"

    assert dataset.dependent_variables[0].components.dtype == np.float32

    assert dataset.description == "A simulated sine curve."

    assert len(dataset.dependent_variables) == 1

    assert len(dataset.dimensions) == 1

    assert dataset.dimensions[0].type == "linear"

    assert str(dataset.dimensions[0].increment) == "0.1 s"

    assert str(dataset.dimensions[0].origin_offset) == "0.0 s"

    assert dataset.dimensions[0].count == 10

    assert dataset.dimensions[0].quantity_name == "time"

    assert np.all(dataset.dimensions[0].coordinates.value == np.arange(10) * 0.1)


def test02():
    dataset = cp.load(cp.tests.test02)

    assert dataset.dependent_variables[0].type == "internal"

    # encoding is always set to 'base64' after import
    assert dataset.dependent_variables[0].encoding == "base64"

    assert dataset.dependent_variables[0].numeric_type == "float64"

    assert dataset.dependent_variables[0].components.dtype == np.float64

    assert dataset.description == "Base64 encoding test"

    assert len(dataset.dependent_variables) == 4

    assert len(dataset.dimensions) == 1

    assert dataset.dimensions[0].type == "monotonic"

    assert str(dataset.dimensions[0].origin_offset) == "0.0 cm"

    assert dataset.dimensions[0].count == 10

    assert dataset.dimensions[0].quantity_name == "length"

    assert dataset.size == dataset.dependent_variables[0].components[0].size


# def test03():
#     dataset1 = cp.load(cp.tests.test03, sort_fft_order=False)
#     dataset2 = cp.load(cp.tests.test03, sort_fft_order=True)

#     dat1 = dataset1.dependent_variables[0].components[0]
#     dat2 = dataset2.dependent_variables[0].components[0]
#     assert np.all(np.fft.fftshift(dat1) == dat2)


def test04():
    data1 = cp.load(cp.tests.test04)
    data2 = data1.copy()
    assert data1.data_structure == data2.data_structure

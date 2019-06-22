# -*- coding: utf-8 -*-
from os.path import join
from os.path import split

import numpy as np

import csdfpy as cp


def test00():
    test_path = join(split(cp.__file__)[0], "tests")
    test01_file = join(test_path, "test01.csdf")
    dataset1 = cp.load(test01_file)

    assert dataset1.dependent_variables[0].type == "internal"

    # encoding is always set to 'base64' after import
    assert dataset1.dependent_variables[0].encoding == "base64"

    assert dataset1.dependent_variables[0].numeric_type == "float32"

    assert dataset1.dependent_variables[0].components.dtype == np.float32

    assert dataset1.description == "Just another test"

    assert len(dataset1.dependent_variables) == 1

    assert len(dataset1.dimensions) == 1

    assert dataset1.dimensions[0].type == "linear"

    assert str(dataset1.dimensions[0].increment) == "0.1 s"

    assert str(dataset1.dimensions[0].origin_offset) == "0.0 s"

    assert dataset1.dimensions[0].count == 10

    assert dataset1.dimensions[0].quantity_name == "time"

    assert np.all(
        dataset1.dimensions[0].coordinates.value == np.arange(10) * 0.1
    )


def test01():
    test_path = join(split(cp.__file__)[0], "tests")
    test02_file = join(test_path, "test02.csdf")
    dataset1 = cp.load(test02_file)

    assert dataset1.dependent_variables[0].type == "internal"

    # encoding is always set to 'base64' after import
    assert dataset1.dependent_variables[0].encoding == "base64"

    assert dataset1.dependent_variables[0].numeric_type == "float64"

    assert dataset1.dependent_variables[0].components.dtype == np.float64

    assert dataset1.description == "Base64 encoding test"

    assert len(dataset1.dependent_variables) == 1

    assert len(dataset1.dimensions) == 1

    assert dataset1.dimensions[0].type == "monotonic"

    assert str(dataset1.dimensions[0].origin_offset) == "0.0 cm"

    assert dataset1.dimensions[0].count == 10

    assert dataset1.dimensions[0].quantity_name == "length"

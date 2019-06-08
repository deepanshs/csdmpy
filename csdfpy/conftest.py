# -*- coding: utf-8 -*-
from os.path import join
from os.path import split

import numpy as np
import pytest

import csdfpy as cp
from csdfpy import DependentVariable
from csdfpy import Dimension


@pytest.fixture(autouse=True)
def add_cp_dimension(doctest_namespace):
    doctest_namespace["cp"] = cp
    doctest_namespace["np"] = np
    doctest_namespace["Dimension"] = Dimension
    doctest_namespace["DependentVariable"] = DependentVariable
    doctest_namespace["x"] = Dimension(
        type="linear",
        description="This is a test",
        number_of_points=10,
        increment="5 G",
        index_zero_value="10 mT",
        origin_offset="10 T",
        label="field strength",
    )

    doctest_namespace["dimension_dictionary"] = {
        "type": "linear",
        "description": "This is a test",
        "number_of_points": 10,
        "increment": "5 G",
        "index_zero_value": "10 mT",
        "origin_offset": "10 T",
        "label": "field strength",
    }

    numpy_array = np.arange(30).reshape(3, 10).astype(np.float32)
    doctest_namespace["y"] = DependentVariable(
        type="internal",
        description="A test image",
        name="star",
        unit="W s",
        quantity="energy",
        quantity_type="RGB",
        components=numpy_array,
    )

    doctest_namespace["dependent_variable_dictionary"] = {
        "type": "internal",
        "description": "A test image",
        "name": "star",
        "unit": "W s",
        "quantity": "energy",
        "quantity_type": "RGB",
        "components": numpy_array,
    }

    test_path = join(split(cp.__file__)[0], "tests")
    test01_file = join(test_path, "test01.csdf")
    doctest_namespace["data"] = cp.load(test01_file)

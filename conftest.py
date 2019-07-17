# -*- coding: utf-8 -*-
import numpy as np
import pytest

import csdfpy as cp
from csdfpy.dependent_variables import DependentVariable
from csdfpy.dimensions import Dimension

__all__ = []


@pytest.fixture(autouse=True)
def add_cp_dimension(doctest_namespace):
    doctest_namespace["cp"] = cp
    doctest_namespace["np"] = np
    doctest_namespace["Dimension"] = Dimension
    doctest_namespace["DependentVariable"] = DependentVariable
    doctest_namespace["x"] = Dimension(
        type="linear",
        description="This is a test",
        count=10,
        increment="5 G",
        coordinates_offset="10 mT",
        origin_offset="10 T",
        label="field strength",
    )

    doctest_namespace["dimension_dictionary"] = {
        "type": "linear",
        "description": "This is a test",
        "count": 10,
        "increment": "5 G",
        "coordinates_offset": "10 mT",
        "origin_offset": "10 T",
        "label": "field strength",
    }

    numpy_array = np.arange(30).reshape(3, 10).astype(np.float32)
    doctest_namespace["y"] = DependentVariable(
        type="internal",
        description="A test image",
        name="star",
        unit="W s",
        quantity_name="energy",
        quantity_type="pixel_3",
        components=numpy_array,
    )

    doctest_namespace["dependent_variable_dictionary"] = {
        "type": "internal",
        "description": "A test image",
        "name": "star",
        "unit": "W s",
        "quantity_name": "energy",
        "quantity_type": "pixel_3",
        "components": numpy_array,
    }

    doctest_namespace["data"] = cp.load(cp.tests.test01)

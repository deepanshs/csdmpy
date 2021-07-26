# -*- coding: utf-8 -*-
import numpy as np
import pytest

import csdmpy as cp
import csdmpy.statistics as stat
from csdmpy.dependent_variable import DependentVariable
from csdmpy.dimension import Dimension

__all__ = []


@pytest.fixture(autouse=True)
def add_cp_dimension(doctest_namespace):
    doctest_namespace["cp"] = cp
    doctest_namespace["np"] = np
    doctest_namespace["stat"] = stat
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
        reciprocal={"quantity_name": "electrical mobility"},
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
    doctest_namespace["my_data"] = cp.load(cp.tests.test02)

    x = np.arange(100) * 2 - 100.0
    gauss = np.exp(-((x - 5.0) ** 2) / (2 * 4.0 ** 2))
    csdm = cp.as_csdm(gauss, unit="T")
    csdm.dimensions[0] = cp.as_dimension(x, unit="m")
    doctest_namespace["csdm"] = csdm

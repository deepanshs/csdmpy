# -*- coding: utf-8 -*-
import pytest

import csdmpy as cp
from csdmpy.utils import check_and_assign_bool
from csdmpy.utils import check_encoding
from csdmpy.utils import NumericType
from csdmpy.utils import QuantityType


def setup():
    data = cp.new(description="An emoji dataset")

    x = dict(type="labeled", labels=["🍈", "🍉", "🍋", "🍌", "🥑", "🍍"])
    data.add_dimension(x)

    y = dict(
        type="internal",
        numeric_type="float32",
        quantity_type="scalar",
        components=[[0.5, 0.25, 1, 2, 1, 0.25]],
    )
    data.add_dependent_variable(y)
    return data


def test_csdf_base64():
    data = setup()
    data.save("my_file_base64.csdf")


def test_csdf_none():
    data = setup()
    data.dependent_variables[0].encoding = "none"
    data.save("my_file_none.csdf")


def test_csdfe():
    data = setup()
    data.dependent_variables[0].encoding = "raw"
    data.save("my_file_raw.csdfe")

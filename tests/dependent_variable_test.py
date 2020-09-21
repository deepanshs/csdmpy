# -*- coding: utf-8 -*-
import json

import numpy as np
import pytest

import csdmpy as cp


def test_internal_new():
    data = cp.new()
    test_array = np.arange(20).reshape(2, 10)
    dim = {
        "type": "internal",
        "numeric_type": "float32",
        "quantity_type": "vector_2",
        "components": test_array,
    }
    data.add_dependent_variable(dim)

    assert data.dependent_variables == data.y
    assert data.dimensions == data.x

    # check type
    assert data.dependent_variables[0].type == "internal"
    data.dependent_variables[0].type = "external"
    assert data.dependent_variables[0].type == "external"
    error = "is invalid for the `type` attribute of the DependentVariable object."
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].type = "celestial"

    # check components
    assert np.all(data.dependent_variables[0].components == test_array)
    assert data.dependent_variables[0].numeric_type == "float32"

    # assign and check components
    data.dependent_variables[0].components = test_array.astype("int32") + 100

    assert np.all(data.dependent_variables[0].components == test_array + 100.0)
    assert data.dependent_variables[0].numeric_type == "int32"

    # check name
    assert data.dependent_variables[0].name == ""
    data.dependent_variables[0].name = "happy days"
    assert data.dependent_variables[0].name == "happy days"

    # check unit
    assert data.dependent_variables[0].unit == ""
    error = r"`unit` attribute cannot be modified"
    with pytest.raises(AttributeError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].unit = "m/s"

    # check component_url
    error = r"DependentVariable' object has no attribute 'component_url"
    with pytest.raises(AttributeError, match=error):
        _ = data.dependent_variables[0].component_url

    # component names
    assert data.dependent_variables[0].component_labels == ["", ""]
    data.dependent_variables[0].component_labels = [":)"]
    assert data.dependent_variables[0].component_labels == [":)", ""]

    data.dependent_variables[0].component_labels = []
    assert data.dependent_variables[0].component_labels == ["", ""]

    data.dependent_variables[0].component_labels = ["1", "2", "3"]
    assert data.dependent_variables[0].component_labels == ["1", "2"]

    data.dependent_variables[0].component_labels[0] = ":("
    assert data.dependent_variables[0].component_labels == [":(", "2"]

    # quantity type
    assert data.dependent_variables[0].quantity_type == "vector_2"

    # Need to fix this
    data.dependent_variables[0].quantity_type = "vector_2"

    # encoding
    assert data.dependent_variables[0].encoding == "base64"
    data.dependent_variables[0].encoding = "none"
    assert data.dependent_variables[0].encoding == "none"
    error = "is an invalid `encoding` enumeration literal. The allowed values are"
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].encoding = "base16"
    data.dependent_variables[0].encoding = "raw"
    assert data.dependent_variables[0].encoding == "raw"

    # numeric_type
    assert data.dependent_variables[0].numeric_type == "int32"
    data.dependent_variables[0].numeric_type = "complex64"
    assert data.dependent_variables[0].numeric_type == "complex64"
    assert np.all(data.dependent_variables[0].components == test_array + 100.0)
    error = "is an invalid `numeric_type` enumeration literal. The allowed values are"
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].numeric_type = "complex32"

    # quantity_name
    assert data.dependent_variables[0].quantity_name == "dimensionless"
    error = "`quantity_name` attribute cannot be modified."
    with pytest.raises(NotImplementedError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].quantity_name = "time"

    # description
    assert data.dependent_variables[0].description == ""
    data.dependent_variables[0].description = "This is a test"
    assert data.dependent_variables[0].description == "This is a test"
    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].description = {}

    # application
    assert data.dependent_variables[0].application == {}
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].application = ""

    dependent_variables_dict_1 = [
        {
            "type": "internal",
            "description": "This is a test",
            "name": "happy days",
            "numeric_type": "complex64",
            "quantity_type": "vector_2",
            "component_labels": [":(", "2"],
            "components": [
                ["(100+0j), (101+0j), ..., (108+0j), (109+0j)"],
                ["(110+0j), (111+0j), ..., (118+0j), (119+0j)"],
            ],
        }
    ]
    dict1 = {
        "csdm": {
            "version": "1.0",
            "dimensions": [],
            "dependent_variables": dependent_variables_dict_1,
        }
    }

    assert data.data_structure == str(
        json.dumps(dict1, ensure_ascii=False, sort_keys=False, indent=2)
    )

    data.dependent_variables[0].encoding = "base64"
    dependent_variables_dict_2 = {
        "type": "internal",
        "description": "This is a test",
        "name": "happy days",
        "numeric_type": "complex64",
        "quantity_type": "vector_2",
        "component_labels": [":(", "2"],
        "encoding": "base64",
        "components": [
            (
                "AADIQgAAAAAAAMpCAAAAAAAAzEIAAAAAAADOQgAAAAAAANBCAAAAAA"
                "AA0kIAAAAAAADUQgAAAAAAANZCAAAAAAAA2EIAAAAAAADaQgAAAAA="
            ),
            (
                "AADcQgAAAAAAAN5CAAAAAAAA4EIAAAAAAADiQgAAAAAAAORCAAAAAA"
                "AA5kIAAAAAAADoQgAAAAAAAOpCAAAAAAAA7EIAAAAAAADuQgAAAAA="
            ),
        ],
    }
    assert data.dependent_variables[0].dict() == dependent_variables_dict_2

    # data = cp.new()
    # test_array = np.arange(20).reshape(2, 10)
    # dim = {
    #     "type": "internal",
    #     "numeric_type": "float32",
    #     "quantity_type": "vector_1",
    #     "components": test_array,
    # }
    # error = "The quantity_type, 'vector_1', requires exactly 1 component"
    # with pytest.raises(Exception, match=".*{0}.*".format(error)):
    #     data.add_dependent_variable(dim)

    # check equality
    dim1 = data.dependent_variables[0].copy()
    assert data.dependent_variables[0] == dim1

    dim1.quantity_type = "pixel_2"
    assert data.dependent_variables[0] != dim1

    assert dim1 != 21


def test_external_new():
    data = cp.new()
    dim = {
        "type": "external",
        "components_url": (
            "https://osu.box.com/shared/static/b967zfl7efcvf471wm9a7tqb74kqomuh.dat"
        ),
        "component_labels": ["monotonic"],
        "name": "Headspace from cinnamon stick",
        "numeric_type": "float32",
        "quantity_type": "scalar",
    }
    data.add_dependent_variable(dim)
    data.add_y(dim)

    for dv in data.dependent_variables:
        # check type
        assert dv.type == "internal"
        dv.type = "external"
        assert dv.type == "external"

        # check components
        assert dv.numeric_type == "float32"

        # assign and check components
        dv.numeric_type = "int32"
        assert dv.numeric_type == "int32"
        assert dv.components.dtype == "int32"

        # check name
        assert dv.name == "Headspace from cinnamon stick"

        # check unit
        assert dv.unit == ""

        # check component_url
        assert dv.components_url == (
            "https://osu.box.com/shared/static/b967zfl7efcvf471wm9a7tqb74kqomuh.dat"
        )

        # component names
        assert dv.component_labels == ["monotonic"]

        # quantity type
        assert dv.quantity_type == "scalar"

        # encoding
        assert dv.encoding == "base64"
        dv.encoding = "raw"
        assert dv.encoding == "raw"

        # description
        assert dv.description == ""
        dv.description = "This is also a test"
        assert dv.description == "This is also a test"

        # application
        assert dv.application == {}

    dict1 = {
        "csdm": {
            "version": "1.0",
            "dimensions": [],
            "dependent_variables": [
                {
                    "type": "internal",
                    "description": "This is also a test",
                    "name": "Headspace from cinnamon stick",
                    "numeric_type": "int32",
                    "quantity_type": "scalar",
                    "component_labels": ["monotonic"],
                    "components": [["48453, 48444, ..., 48040, 48040"]],
                },
                {
                    "type": "internal",
                    "description": "This is also a test",
                    "name": "Headspace from cinnamon stick",
                    "numeric_type": "int32",
                    "quantity_type": "scalar",
                    "component_labels": ["monotonic"],
                    "components": [["48453, 48444, ..., 48040, 48040"]],
                },
            ],
        }
    }

    assert data.data_structure == json.dumps(
        dict1, ensure_ascii=False, sort_keys=False, indent=2
    )

    # check equality
    dim1 = data.dependent_variables[0].copy()
    assert data.dependent_variables[0] == dim1

    dim1.numeric_type = "int64"
    assert data.dependent_variables[0] != dim1

    assert dim1 != 21


def test_missing_type():
    data = cp.new()
    dim = {
        "numeric_type": "float32",
        "quantity_type": "scalar",
        "components": [np.arange(10)],
    }
    error = "Missing a required `type` key from the DependentVariable object."
    with pytest.raises(KeyError, match=".*{0}.*".format(error)):
        data.add_dependent_variable(dim)


def test_wrong_type():
    data = cp.new()
    dim = {
        "type": "",
        "numeric_type": "float32",
        "quantity_type": "scalar",
        "components": [np.arange(10)],
    }
    error = "is an invalid `type` for the DependentVariable"
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        data.add_dependent_variable(dim)


def test_missing_component():
    data = cp.new()
    dim = {"type": "internal", "numeric_type": "float32", "quantity_type": "scalar"}
    error = "Missing a required `components` key"
    with pytest.raises(KeyError, match=".*{0}.*".format(error)):
        data.add_dependent_variable(dim)


def test_missing_component_url():
    data = cp.new()
    dim = {"type": "external", "numeric_type": "float32", "quantity_type": "scalar"}
    error = "Missing a required `components_url` key"
    with pytest.raises(KeyError, match=".*{0}.*".format(error)):
        data.add_dependent_variable(dim)

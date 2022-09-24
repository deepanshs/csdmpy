import json

import numpy as np
import pytest

import csdmpy as cp


def test_internal_new():
    test_array = np.arange(20).reshape(2, 10)
    data = cp.CSDM(
        dependent_variables=[
            cp.DependentVariable(
                type="internal",
                numeric_type="float32",
                quantity_type="vector_2",
                components=test_array,
            )
        ]
    )

    assert data.dependent_variables == data.y
    assert data.dimensions == data.x

    # check type
    assert data.dependent_variables[0].type == "internal"
    data.y[0].type = "external"
    assert data.y[0].type == "external"
    error = "is invalid for the `type` attribute of the DependentVariable object."
    with pytest.raises(ValueError, match=f".*{error}.*"):
        data.y[0].type = "celestial"

    # check components
    assert np.all(data.y[0].components == test_array)
    assert data.y[0].numeric_type == "float32"

    # assign and check components
    data.y[0].components = test_array.astype("int32") + 100

    assert np.all(data.y[0].components == test_array + 100.0)
    assert data.y[0].numeric_type == "int32"

    # check name
    assert data.y[0].name == ""
    data.y[0].name = "happy days"
    assert data.y[0].name == "happy days"

    # check unit
    assert data.y[0].unit == ""
    error = r"`unit` attribute cannot be modified"
    with pytest.raises(AttributeError, match=f".*{error}.*"):
        data.y[0].unit = "m/s"

    # check component_url
    error = r"DependentVariable' object has no attribute 'component_url"
    with pytest.raises(AttributeError, match=error):
        _ = data.y[0].component_url

    # component names
    assert data.y[0].component_labels == ["", ""]
    data.y[0].component_labels = [":)"]
    assert data.y[0].component_labels == [":)", ""]

    data.y[0].component_labels = []
    assert data.y[0].component_labels == ["", ""]

    data.y[0].component_labels = ["1", "2", "3"]
    assert data.y[0].component_labels == ["1", "2"]

    data.y[0].component_labels[0] = ":("
    assert data.y[0].component_labels == [":(", "2"]

    # quantity type
    assert data.y[0].quantity_type == "vector_2"

    # Need to fix this
    data.y[0].quantity_type = "vector_2"

    # encoding
    assert data.y[0].encoding == "base64"
    data.y[0].encoding = "none"
    assert data.y[0].encoding == "none"
    error = "is an invalid `encoding` enumeration literal. The allowed values are"
    with pytest.raises(ValueError, match=f".*{error}.*"):
        data.y[0].encoding = "base16"
    data.y[0].encoding = "raw"
    assert data.y[0].encoding == "raw"

    # numeric_type
    assert data.y[0].numeric_type == "int32"
    data.y[0].numeric_type = "complex64"
    assert data.y[0].numeric_type == "complex64"
    assert np.all(data.y[0].components == test_array + 100.0)
    error = "is an invalid `numeric_type` enumeration literal. The allowed values are"
    with pytest.raises(ValueError, match=f".*{error}.*"):
        data.y[0].numeric_type = "complex32"

    # quantity_name
    assert data.y[0].quantity_name == "dimensionless"
    error = "`quantity_name` attribute cannot be modified."
    with pytest.raises(NotImplementedError, match=f".*{error}.*"):
        data.y[0].quantity_name = "time"

    # description
    assert data.y[0].description == ""
    data.y[0].description = "This is a test"
    assert data.y[0].description == "This is a test"
    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=f".*{error}.*"):
        data.y[0].description = {}

    # application
    assert data.y[0].application is None
    with pytest.raises(TypeError, match=f".*{error}.*"):
        data.y[0].application = ""

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
        "csdm": {"version": "1.0", "dependent_variables": dependent_variables_dict_1}
    }

    assert data.data_structure == str(
        json.dumps(dict1, ensure_ascii=False, sort_keys=False, indent=2)
    )

    data.y[0].encoding = "base64"
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
    assert data.y[0].dict() == dependent_variables_dict_2

    # check equality
    dim1 = data.y[0].copy()
    assert data.y[0] == dim1

    dim1.quantity_type = "pixel_2"
    assert data.y[0] != dim1

    assert dim1 != 21


def test_external_new():
    domain = "https://www.ssnmr.org/sites/default/files/CSDM"

    dv_obj = cp.DependentVariable(
        type="external",
        components_url=f"{domain}/GC/cinnamon_raw_cinnamon stick.dat",
        component_labels=["monotonic"],
        name="Headspace from cinnamon stick",
        numeric_type="float32",
        quantity_type="scalar",
    )
    data = cp.CSDM(dependent_variables=[dv_obj, dv_obj.copy()])

    for dv_obj in data.y:
        # check type
        assert dv_obj.type == "internal"
        dv_obj.type = "external"
        assert dv_obj.type == "external"

        # check components
        assert dv_obj.numeric_type == "float32"

        # assign and check components
        dv_obj.numeric_type = "int32"
        assert dv_obj.numeric_type == "int32"
        assert dv_obj.components.dtype == "int32"

        # check name
        assert dv_obj.name == "Headspace from cinnamon stick"

        # check unit
        assert dv_obj.unit == ""

        # check component_url
        assert dv_obj.components_url == f"{domain}/GC/cinnamon_raw_cinnamon stick.dat"

        # component names
        assert dv_obj.component_labels == ["monotonic"]

        # quantity type
        assert dv_obj.quantity_type == "scalar"

        # encoding
        assert dv_obj.encoding == "base64"
        dv_obj.encoding = "raw"
        assert dv_obj.encoding == "raw"

        # description
        assert dv_obj.description == ""
        dv_obj.description = "This is also a test"
        assert dv_obj.description == "This is also a test"

        # application
        assert dv_obj.application is None

    dict_1 = {
        "type": "internal",
        "description": "This is also a test",
        "name": "Headspace from cinnamon stick",
        "numeric_type": "int32",
        "quantity_type": "scalar",
        "component_labels": ["monotonic"],
        "components": [["48453, 48444, ..., 48040, 48040"]],
    }
    dict1 = {"csdm": {"version": "1.0", "dependent_variables": [dict_1, dict_1]}}

    assert data.data_structure == json.dumps(
        dict1, ensure_ascii=False, sort_keys=False, indent=2
    )

    # check equality
    dim1 = data.y[0].copy()
    assert data.y[0] == dim1

    dim1.numeric_type = "int64"
    assert data.y[0] != dim1

    assert dim1 != 21


def test_missing_type():
    d_v = {
        "numeric_type": "float32",
        "quantity_type": "scalar",
        "components": [np.arange(10)],
    }
    error = "Missing a required `type` key from the DependentVariable object."
    with pytest.raises(KeyError, match=f".*{error}.*"):
        _ = cp.CSDM(dependent_variables=[d_v])


def test_wrong_type():
    d_v = {
        "type": "",
        "numeric_type": "float32",
        "quantity_type": "scalar",
        "components": [np.arange(10)],
    }
    error = "is an invalid `type` for the DependentVariable"
    with pytest.raises(ValueError, match=f".*{error}.*"):
        _ = cp.CSDM(dependent_variables=[d_v])


def test_missing_component():
    d_v = {"type": "internal", "numeric_type": "float32", "quantity_type": "scalar"}
    error = "Missing a required `components` key"
    with pytest.raises(KeyError, match=f".*{error}.*"):
        _ = cp.CSDM(dependent_variables=[d_v])


def test_missing_component_url():
    d_v = {"type": "external", "numeric_type": "float32", "quantity_type": "scalar"}
    error = "Missing a required `components_url` key"
    with pytest.raises(KeyError, match=f".*{error}.*"):
        _ = cp.CSDM(dependent_variables=[d_v])


def test_c_f_contiguous_array():
    arr_c = np.random.rand(1028 * 1028).reshape(1028, 1028)
    arr_f = np.asfortranarray(arr_c.copy())

    assert arr_c.flags["C_CONTIGUOUS"] is True
    assert arr_c.flags["F_CONTIGUOUS"] is False
    assert arr_f.flags["C_CONTIGUOUS"] is False
    assert arr_f.flags["F_CONTIGUOUS"] is True

    dv_c = cp.as_dependent_variable(arr_c)
    dv_f = cp.as_dependent_variable(arr_f)

    assert np.allclose(dv_c.components, dv_f.components)

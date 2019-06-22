# -*- coding: utf-8 -*-
import numpy as np
import pytest

import csdfpy as cp


def test_internal_new_data():
    data = cp.new()
    dim = {
        "type": "internal",
        "numeric_type": "float32",
        "components": [np.arange(10)],
    }
    data.add_dependent_variable(dim)

    # check type
    assert data.dependent_variables[0].type == "internal"
    data.dependent_variables[0].type = "external"
    assert data.dependent_variables[0].type == "external"

    # check components
    assert np.all(
        data.dependent_variables[0].components
        == [np.arange(10).astype(np.float32)]
    )
    assert data.dependent_variables[0].numeric_type == "float32"

    # assign and check components
    data.dependent_variables[0].components = [
        np.arange(10, dtype="int32") + 100
    ]
    assert np.all(
        data.dependent_variables[0].components
        == [np.arange(10).astype(np.int32) + 100.0]
    )
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
        data.dependent_variables[0].component_url

    # component labels
    assert data.dependent_variables[0].component_labels == [""]
    data.dependent_variables[0].component_labels = [":)"]
    assert data.dependent_variables[0].component_labels == [":)"]
    data.dependent_variables[0].component_labels[0] = ":("
    assert data.dependent_variables[0].component_labels == [":("]

    # quantity type
    assert data.dependent_variables[0].quantity_type == "scalar"

    # Need to fix this
    data.dependent_variables[0].quantity_type = "vector"

    # encoding
    assert data.dependent_variables[0].encoding == "base64"
    data.dependent_variables[0].encoding = "none"
    assert data.dependent_variables[0].encoding == "none"
    error = (
        "is not a valid `encoding` enumeration literal. "
        "The allowed values are"
    )
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].encoding = "base16"
    data.dependent_variables[0].encoding = "raw"
    assert data.dependent_variables[0].encoding == "raw"

    # numeric_type
    assert data.dependent_variables[0].numeric_type == "int32"
    data.dependent_variables[0].numeric_type = "complex64"
    assert data.dependent_variables[0].numeric_type == "complex64"
    assert np.all(
        data.dependent_variables[0].components
        == [np.arange(10).astype(np.complex64) + 100.0]
    )
    error = (
        "is not a valid `numeric_type` enumeration literal. "
        "The allowed values are"
    )
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].numeric_type = "complex32"

    # quantity_name
    assert data.dependent_variables[0].quantity_name == "dimensionless"
    error = "The `quantity_name` attribute cannot be modified."
    with pytest.raises(NotImplementedError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].quantity_name = "time"

    # description
    assert data.dependent_variables[0].description == ""
    data.dependent_variables[0].description = "This is a test"
    assert data.dependent_variables[0].description == "This is a test"
    error = "Description requires a string"
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].description = {}

    # application
    assert data.dependent_variables[0].application == {}
    error = "A dict value is required"
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        data.dependent_variables[0].application = ""


# dict1 = {
#     "csdm": {
#         "version": "0.0.12",
#         "dimensions": [],
#         "dependent_variables": [
#             {
#                 "type": "internal",
#                 "description": "This is a test",
#                 "name": "happy days",
#                 "numeric_type": "complex64",
#                 "quantity_type": "vector",
#                 "component_labels": [
#                     ":("
#                 ],
#                 "components": ("[(100+0j), (100+0j), ...... "
#                                "(108+0j), (108+0j)])"
#             }
#         ]
#     }
# }

# assert data.data_structure == str(json.dumps(
#     dict1, ensure_ascii=False, sort_keys=False, indent=2))


def test_external_new_data():
    data = cp.new()
    dim = {
        "type": "external",
        "components_url": (
            "https://www.grandinetti.org/resources/CSDM/"
            "cinnamon_raw_cinnamon stick.dat"
        ),
        "component_labels": ["monotonic"],
        "name": "Headspace from cinnamon stick",
        "numeric_type": "float32",
        "encoding": "raw",
    }
    data.add_dependent_variable(dim)

    # check type
    assert data.dependent_variables[0].type == "internal"
    data.dependent_variables[0].type = "external"
    assert data.dependent_variables[0].type == "external"

    # check components
    assert data.dependent_variables[0].numeric_type == "float32"

    # assign and check components
    data.dependent_variables[0].numeric_type = "int32"
    assert data.dependent_variables[0].numeric_type == "int32"
    assert data.dependent_variables[0].components.dtype == "int32"

    # check name
    assert data.dependent_variables[0].name == "Headspace from cinnamon stick"

    # check unit
    assert data.dependent_variables[0].unit == ""

    # check component_url
    assert data.dependent_variables[0].components_url == (
        "https://www.grandinetti.org/resources/CSDM/cinnamon_raw_cinnamon "
        "stick.dat"
    )

    # component labels
    assert data.dependent_variables[0].component_labels == ["monotonic"]

    # quantity type
    assert data.dependent_variables[0].quantity_type == "scalar"

    # encoding
    assert data.dependent_variables[0].encoding == "base64"
    data.dependent_variables[0].encoding = "raw"
    assert data.dependent_variables[0].encoding == "raw"

    # description
    assert data.dependent_variables[0].description == ""
    data.dependent_variables[0].description = "This is also a test"
    assert data.dependent_variables[0].description == "This is also a test"

    # application
    assert data.dependent_variables[0].application == {}

    # print(data.data_structure)
    # dict1 = {
    #     "csdm": {
    #         "version": "0.0.12",
    #         "dimensions": [],
    #         "dependent_variables": [
    #             {
    #                 "type": "internal",
    #                 "description": "This is also a test",
    #                 "name": "Headspace from cinnamon stick",
    #                 "numeric_type": "int32",
    #                 "component_labels": [
    #                     "monotonic"
    #                 ],
    #                 "components": "[48453, 48453, ...... 48040, 48040]"
    #             }
    #         ]
    #     }
    # }

    # assert data.data_structure == json.dumps(
    #     dict1, ensure_ascii=False, sort_keys=False, indent=2)


if __name__ == "__main__":
    test_internal_new_data()
    test_external_new_data()

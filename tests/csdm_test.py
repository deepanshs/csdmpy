# -*- coding: utf-8 -*-
import json

import pytest

import csdfpy as cp


def test_csdm():
    data = cp.new(description="This is a test")

    # read_only
    assert data.read_only is False
    data.read_only = True
    assert data.read_only is True
    error = "Expecting an instance of type,"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.read_only = "True"

    # tags
    assert data.tags == []
    data.tags = ["1", "2", "3"]
    assert data.tags == ["1", "2", "3"]
    error = "Expecting an instance of type,"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.tags = "23"

    # version
    assert data.version == cp.__version__

    # geographic_coordinate
    assert data.geographic_coordinate == {}
    error = "can't set attribute"
    with pytest.raises(AttributeError, match=".*{0}.*".format(error)):
        data.geographic_coordinate = {}

    # description
    assert data.description == "This is a test"
    data.description = "Enough with the tests"
    assert data.description == "Enough with the tests"
    error = "Expecting an instance of type,"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.description = {}

    # application
    assert data.application == {}
    data.application = {"csdfpy": "Some day"}
    assert data.application == {"csdfpy": "Some day"}
    error = "Expecting an instance of type,"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.application = "Some other day"

    # filename
    assert data.filename == ""

    # data_structure
    structure = {
        "csdm": {
            "version": "0.0.12",
            "read_only": True,
            "tags": ["1", "2", "3"],
            "description": "Enough with the tests",
            "dimensions": [],
            "dependent_variables": [],
        }
    }
    assert data.data_structure == str(
        json.dumps(structure, ensure_ascii=False, sort_keys=False, indent=2)
    )

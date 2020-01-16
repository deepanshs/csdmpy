# -*- coding: utf-8 -*-
import json

import numpy as np
import pytest
from astropy import units as u

import csdmpy as cp
from csdmpy.units import ScalarQuantity


# linear dimension
def test_linear_new():
    data = cp.new()
    dim = {
        "type": "linear",
        "increment": "10 m/s",
        "count": 10,
        "coordinates_offset": "5 m/s",
    }
    data.add_dimension(dim)

    assert data.dimensions[0].type == "linear"

    error = "can't set attribute"
    with pytest.raises(AttributeError, match=".*{0}.*".format(error)):
        data.dimensions[0].type = "monotonic"

    assert str(data.dimensions[0].increment) == "10.0 m / s"
    data.dimensions[0].increment = ScalarQuantity("20.0 m / s")
    assert str(data.dimensions[0].increment) == "20.0 m / s"
    data.dimensions[0].increment = 20.0 * u.Unit("m / s")
    assert str(data.dimensions[0].increment) == "20.0 m / s"

    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.dimensions[0].increment = 10

    data.dimensions[0].increment = "20/2 m / s"
    assert str(data.dimensions[0].increment) == "10.0 m / s"

    assert data.dimensions[0].count == 10

    assert data.dimensions[0].application == {}
    data.dimensions[0].application = {"my_application": {}}
    assert data.dimensions[0].application == {"my_application": {}}
    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.dimensions[0].application = "my_application"

    assert str(data.dimensions[0].coordinates_offset) == "5.0 m / s"

    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.dimensions[0].coordinates_offset = 50

    data.dimensions[0].coordinates_offset = ScalarQuantity("5.0 m / s")
    assert str(data.dimensions[0].coordinates_offset) == "5.0 m / s"

    assert str(data.dimensions[0].origin_offset) == "0.0 m / s"
    assert data.dimensions[0].quantity_name == "speed"
    assert str(data.dimensions[0].period) == "inf m / s"
    assert data.dimensions[0].complex_fft is False
    assert np.all(data.dimensions[0].coordinates.value == np.arange(10) * 10.0 + 5.0)

    data.dimensions[0].count = 12
    assert data.dimensions[0].count == 12
    assert np.all(data.dimensions[0].coordinates.value == np.arange(12) * 10.0 + 5.0)
    assert np.all(
        data.dimensions[0].absolute_coordinates.value == np.arange(12) * 10.0 + 5.0
    )

    data.dimensions[0].origin_offset = "1 km/s"
    assert str(data.dimensions[0].origin_offset) == "1.0 km / s"
    assert np.all(data.dimensions[0].coordinates.value == np.arange(12) * 10.0 + 5.0)

    test_with = np.arange(12) * 10.0 + 5.0 + 1000.0
    assert np.all(data.dimensions[0].absolute_coordinates.value == test_with)

    data.dimensions[0].increment = "20 m/s"
    assert str(data.dimensions[0].increment) == "20.0 m / s"
    assert np.all(data.dimensions[0].coordinates.value == np.arange(12) * 20.0 + 5.0)

    test_with = np.arange(12) * 20.0 + 5.0 + 1000.0
    assert np.all(data.dimensions[0].absolute_coordinates.value == test_with)

    data.dimensions[0].complex_fft = True
    assert data.dimensions[0].complex_fft is True
    assert np.all(
        data.dimensions[0].coordinates.value == (np.arange(12) - 6) * 20.0 + 5.0
    )

    test_with = (np.arange(12) - 6) * 20.0 + 5.0 + 1000.0
    assert np.all(data.dimensions[0].absolute_coordinates.value == test_with)

    dict1 = {
        "csdm": {
            "version": "1.0",
            "dimensions": [
                {
                    "type": "linear",
                    "count": 12,
                    "increment": "20.0 m * s^-1",
                    "coordinates_offset": "5.0 m * s^-1",
                    "origin_offset": "1.0 km * s^-1",
                    "quantity_name": "speed",
                    "application": {"my_application": {}},
                    "complex_fft": True,
                }
            ],
            "dependent_variables": [],
        }
    }
    assert data.data_structure == json.dumps(
        dict1, ensure_ascii=False, sort_keys=False, indent=2
    )
    assert data.dimensions[0].to_dict() == dict1["csdm"]["dimensions"][0]


# monotonic dimension
def test_monotonic_new():
    data = cp.new()
    dim = {
        "type": "monotonic",
        "description": "Far far away.",
        "coordinates": ["1 m", "100 m", "1 km", "1 Gm", "0.25 lyr"],
    }
    data.add_dimension(dim)

    # description
    assert data.dimensions[0].description == "Far far away."
    data.dimensions[0].description = "A galaxy far far away."
    assert data.dimensions[0].description == "A galaxy far far away."

    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.dimensions[0].description = 12

    # dimension type
    assert data.dimensions[0].type == "monotonic"

    # values
    assert data.dimensions[0].subtype._values == [
        "1 m",
        "100 m",
        "1 km",
        "1 Gm",
        "0.25 lyr",
    ]

    # increment
    error = "'MonotonicDimension' object has no attribute 'increment'"
    with pytest.raises(AttributeError, match=".*{0}.*".format(error)):
        data.dimensions[0].increment

    # label
    assert data.dimensions[0].label == ""
    data.dimensions[0].label = "some string"
    assert data.dimensions[0].label == "some string"

    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.dimensions[0].label = {}

    # count
    assert data.dimensions[0].count == 5
    error = "Cannot set the count,"
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        data.dimensions[0].count = 12

    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.dimensions[0].count = "12"

    # coordinates_offset
    error = "`MonotonicDimension` has no attribute `coordinates_offset`."
    with pytest.raises(AttributeError, match=".*{0}.*".format(error)):
        data.dimensions[0].coordinates_offset

    # origin offset
    assert str(data.dimensions[0].origin_offset) == "0.0 m"

    data.dimensions[0].origin_offset = ScalarQuantity("3.1415 m")
    assert str(data.dimensions[0].origin_offset) == "3.1415 m"

    data.dimensions[0].origin_offset = "1 lyr"
    assert str(data.dimensions[0].origin_offset) == "1.0 lyr"

    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=".*{0}.*".format(error)):
        data.dimensions[0].origin_offset = {"12 m"}

    # quantity_name
    assert data.dimensions[0].quantity_name == "length"

    error = "This attribute is not yet implemented"
    with pytest.raises(NotImplementedError, match=".*{0}.*".format(error)):
        data.dimensions[0].quantity_name = "area/length"

    # period
    assert str(data.dimensions[0].period) == "inf m"
    data.dimensions[0].period = "Infinity m"
    assert str(data.dimensions[0].period) == "inf m"
    data.dimensions[0].period = "20 m^2/m"
    assert str(data.dimensions[0].period) == "20.0 m"
    data.dimensions[0].period = "(1/0) m^5/m^4"
    assert str(data.dimensions[0].period) == "inf m"

    # fft output order
    error = "'MonotonicDimension' object has no attribute 'complex_fft'"
    with pytest.raises(AttributeError, match=".*{0}.*".format(error)):
        data.dimensions[0].complex_fft

    # coordinates
    assert np.allclose(
        data.dimensions[0].coordinates.value,
        np.asarray(
            [1.00000000e00, 1.00000000e02, 1.00000000e03, 1.00000000e09, 2.36518262e15]
        ),
    )

    # coordinates
    assert np.allclose(
        data.dimensions[0].absolute_coordinates.value,
        np.asarray(
            [9.46073047e15, 9.46073047e15, 9.46073047e15, 9.46073147e15, 1.18259131e16]
        ),
    )

    dict1 = {
        "csdm": {
            "version": "1.0",
            "dimensions": [
                {
                    "type": "monotonic",
                    "description": "A galaxy far far away.",
                    "coordinates": ["1 m", "100 m", "1 km", "1 Gm", "0.25 lyr"],
                    "origin_offset": "1.0 lyr",
                    "quantity_name": "length",
                    "label": "some string",
                    "reciprocal": {"quantity_name": "wavenumber"},
                }
            ],
            "dependent_variables": [],
        }
    }
    assert data.data_structure == json.dumps(
        dict1, ensure_ascii=False, sort_keys=False, indent=2
    )
    assert data.dimensions[0].to_dict() == dict1["csdm"]["dimensions"][0]


# labeled dimension
def test_labeled_new():
    pass


# if __name__ == "__main__":
#     test_linear_new()
#     test_monotonic_new()

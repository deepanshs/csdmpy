# -*- coding: utf-8 -*-
# import json
import numpy as np
import pytest
from numpy.fft import fftshift

import csdfpy as cp


# linear dimension
def test_linear_new():
    data = cp.new()
    dim = {
        "type": "linear",
        "increment": "10 m/s",
        "count": 10,
        "index_zero_coordinate": "5 m/s",
    }
    data.add_dimension(dim)

    assert data.dimensions[0].type == "linear"
    assert str(data.dimensions[0].increment) == "10.0 m / s"
    assert data.dimensions[0].count == 10
    assert str(data.dimensions[0].index_zero_coordinate) == "5.0 m / s"
    assert str(data.dimensions[0].origin_offset) == "0.0 m / s"
    assert data.dimensions[0].quantity_name == "speed"
    assert str(data.dimensions[0].period) == "inf m / s"
    assert data.dimensions[0].fft_output_order is False
    assert np.all(
        data.dimensions[0].coordinates.value == np.arange(10) * 10.0 + 5.0
    )

    data.dimensions[0].count = 12
    assert data.dimensions[0].count == 12
    assert np.all(
        data.dimensions[0].coordinates.value == np.arange(12) * 10.0 + 5.0
    )
    assert np.all(
        data.dimensions[0].absolute_coordinates.value
        == np.arange(12) * 10.0 + 5.0
    )

    data.dimensions[0].origin_offset = "1 km/s"
    assert str(data.dimensions[0].origin_offset) == "1.0 km / s"
    assert np.all(
        data.dimensions[0].coordinates.value == np.arange(12) * 10.0 + 5.0
    )
    assert np.all(
        data.dimensions[0].absolute_coordinates.value
        == np.arange(12) * 10.0 + 5.0 + 1000.0
    )

    data.dimensions[0].increment = "20 m/s"
    assert str(data.dimensions[0].increment) == "20.0 m / s"
    assert np.all(
        data.dimensions[0].coordinates.value == np.arange(12) * 20.0 + 5.0
    )
    assert np.all(
        data.dimensions[0].absolute_coordinates.value
        == np.arange(12) * 20.0 + 5.0 + 1000.0
    )

    data.dimensions[0].fft_output_order = True
    assert data.dimensions[0].fft_output_order is True
    assert np.all(
        data.dimensions[0].coordinates.value
        == fftshift((np.arange(12) - 6) * 20.0 + 5.0)
    )
    assert np.all(
        data.dimensions[0].absolute_coordinates.value
        == fftshift((np.arange(12) - 6) * 20.0 + 5.0 + 1000.0)
    )


# # monotonic dimension
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

    # count
    assert data.dimensions[0].count == 5
    error = "Cannot set count,"
    with pytest.raises(ValueError, match=".*{0}.*".format(error)):
        data.dimensions[0].count = 12

    # index_zero_coordinate
    error = "`MonotonicDimension` has no attribute `index_zero_coordinate`."
    with pytest.raises(AttributeError, match=".*{0}.*".format(error)):
        data.dimensions[0].index_zero_coordinate

    # origin offset
    assert str(data.dimensions[0].origin_offset) == "0.0 m"
    data.dimensions[0].origin_offset = "1 lyr"
    assert str(data.dimensions[0].origin_offset) == "1.0 lyr"

    # quantity_name
    assert data.dimensions[0].quantity_name == "length"

    # period
    assert str(data.dimensions[0].period) == "inf m"

    # fft output order
    error = "'MonotonicDimension' object has no attribute 'fft_output_order'"
    with pytest.raises(AttributeError, match=".*{0}.*".format(error)):
        data.dimensions[0].fft_output_order

    # coordinates
    assert np.allclose(
        data.dimensions[0].coordinates.value,
        np.asarray(
            [
                1.00000000e00,
                1.00000000e02,
                1.00000000e03,
                1.00000000e09,
                2.36518262e15,
            ]
        ),
    )

    # coordinates
    assert np.allclose(
        data.dimensions[0].absolute_coordinates.value,
        np.asarray(
            [
                9.46073047e15,
                9.46073047e15,
                9.46073047e15,
                9.46073147e15,
                1.18259131e16,
            ]
        ),
    )

    # dict1 = {
    #     "csdm": {
    #         "version": "0.0.12",
    #         "dimensions": [
    #             {
    #                 "type": "monotonic",
    #                 "description": "A galaxy far far away.",
    #                 "coordinates": [
    #                     "1 m",
    #                     "100 m",
    #                     "1 km",
    #                     "1 Gm",
    #                     "0.25 lyr"
    #                 ],
    #                 "origin_offset": "1.0 lyr",
    #                 "quantity_name": "length",
    #                 "label": "some string",
    #                 "reciprocal": {
    #                     "quantity_name": "wavenumber"
    #                 }
    #             }
    #         ],
    #         "dependent_variables": []
    #     }
    # }
    # assert data.data_structure == json.dumps(
    #     dict1, ensure_ascii=False, sort_keys=False, indent=2)


if __name__ == "__main__":
    test_linear_new()
    test_monotonic_new()

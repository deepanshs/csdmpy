import json

import numpy as np
import pytest
from astropy import units as u

import csdmpy as cp
from csdmpy.units import ScalarQuantity


# linear dimension
def test_linear_new():
    dim = {
        "type": "linear",
        "increment": "10 m/s",
        "count": 10,
        "coordinates_offset": "5 m/s",
    }
    data = cp.CSDM(dimensions=[dim])

    assert data.dimensions[0].is_quantitative() is True

    # test for attributes
    assert data.dependent_variables == data.y
    assert data.dimensions == data.x

    # type
    assert data.dimensions[0].type == "linear"

    error = "can't set attribute"
    with pytest.raises(AttributeError, match=f".*{error}.*"):
        data.dimensions[0].type = "monotonic"

    # increment
    assert str(data.dimensions[0].increment) == "10.0 m / s"
    data.dimensions[0].increment = ScalarQuantity("20.0 m / s")
    assert str(data.dimensions[0].increment) == "20.0 m / s"
    data.dimensions[0].increment = 20.0 * u.Unit("m / s")
    assert str(data.dimensions[0].increment) == "20.0 m / s"

    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=f".*{error}.*"):
        data.dimensions[0].increment = 10

    data.dimensions[0].increment = "20/2 m / s"
    assert str(data.dimensions[0].increment) == "10.0 m / s"

    # application
    assert data.dimensions[0].application is None
    data.dimensions[0].application = {"my_application": {}}
    assert data.dimensions[0].application == {"my_application": {}}
    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=f".*{error}.*"):
        data.dimensions[0].application = "my_application"

    # coordinates offset
    assert str(data.dimensions[0].coordinates_offset) == "5.0 m / s"

    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=f".*{error}.*"):
        data.dimensions[0].coordinates_offset = 50

    data.dimensions[0].coordinates_offset = ScalarQuantity("5.0 m / s")
    assert str(data.dimensions[0].coordinates_offset) == "5.0 m / s"

    # quantity name, period, complex fft
    assert data.dimensions[0].quantity_name == "speed"
    assert str(data.dimensions[0].period) == "inf m / s"
    assert data.dimensions[0].complex_fft is False
    assert np.all(data.dimensions[0].coordinates.value == np.arange(10) * 10.0 + 5.0)
    assert np.all(data.x[0].coords.value == np.arange(10) * 10.0 + 5.0)

    # count
    assert data.dimensions[0].count == 10
    data.dimensions[0].count = 12
    assert data.dimensions[0].count == 12
    assert np.all(data.dimensions[0].coordinates.value == np.arange(12) * 10.0 + 5.0)
    assert np.all(data.x[0].coords.value == np.arange(12) * 10.0 + 5.0)
    assert np.all(
        data.dimensions[0].absolute_coordinates.value == np.arange(12) * 10.0 + 5.0
    )

    # origin offset
    assert str(data.dimensions[0].origin_offset) == "0.0 m / s"
    data.dimensions[0].origin_offset = "1 km/s"
    assert str(data.dimensions[0].origin_offset) == "1.0 km / s"
    assert np.all(data.dimensions[0].coordinates.value == np.arange(12) * 10.0 + 5.0)
    assert np.all(data.x[0].coords.value == np.arange(12) * 10.0 + 5.0)

    test_with = np.arange(12) * 10.0 + 5.0 + 1000.0
    assert np.all(data.dimensions[0].absolute_coordinates.value == test_with)

    data.dimensions[0].increment = "20 m/s"
    assert str(data.dimensions[0].increment) == "20.0 m / s"
    assert np.all(data.dimensions[0].coordinates.value == np.arange(12) * 20.0 + 5.0)
    assert np.all(data.x[0].coords.value == np.arange(12) * 20.0 + 5.0)

    test_with = np.arange(12) * 20.0 + 5.0 + 1000.0
    assert np.all(data.dimensions[0].absolute_coordinates.value == test_with)

    # fft complex
    data.dimensions[0].complex_fft = True
    assert data.dimensions[0].complex_fft is True
    assert np.all(
        data.dimensions[0].coordinates.value == (np.arange(12) - 6) * 20.0 + 5.0
    )
    assert np.all(data.x[0].coords.value == (np.arange(12) - 6) * 20.0 + 5.0)

    test_with = (np.arange(12) - 6) * 20.0 + 5.0 + 1000.0
    assert np.all(data.dimensions[0].absolute_coordinates.value == test_with)

    error = "The attribute cannot be modified for Dimension objects with"
    with pytest.raises(AttributeError, match=f".*{error}.*"):
        data.dimensions[0].coordinates = [1, 3]

    with pytest.raises(AttributeError, match=f".*{error}.*"):
        data.x[0].coords = [1, 3]

    data.dimensions[0].reciprocal.description = "blah blah"

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
                    "reciprocal": {"description": "blah blah"},
                }
            ],
        }
    }
    assert data.data_structure == json.dumps(
        dict1, ensure_ascii=False, sort_keys=False, indent=2
    )
    assert data.dimensions[0].dict() == dict1["csdm"]["dimensions"][0]

    # reduced dict
    data.dimensions[0].reciprocal.description = ""
    data.dimensions[0].description = "blah blah"
    data.dimensions[0].application = {}

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
                    "description": "blah blah",
                    "complex_fft": True,
                }
            ],
        }
    }
    assert data.data_structure == json.dumps(
        dict1, ensure_ascii=False, sort_keys=False, indent=2
    )
    assert data.dimensions[0].dict() == dict1["csdm"]["dimensions"][0]

    assert data.dimensions[0].data_structure == json.dumps(
        dict1["csdm"]["dimensions"][0], ensure_ascii=False, sort_keys=False, indent=2
    )

    # check equality
    dim1 = data.dimensions[0].copy()
    assert data.dimensions[0] == dim1

    dim1.coordinates_offset = "0 m * s^-1"
    assert data.dimensions[0] != dim1

    assert dim1 != 21

    # axis label
    assert data.dimensions[0].axis_label == "speed / (m / s)"
    data.dimensions[0].label = "velocity"
    assert data.dimensions[0].axis_label == "velocity / (m / s)"


def test_linearDimension():
    dim_1 = cp.LinearDimension(count=3, increment="2s")
    dim_2 = cp.Dimension(type="linear", count=3, increment="2s")

    message = "LinearDimension([0. 2. 4.] s)"
    assert dim_1.__str__() == message
    assert dim_2.__str__() == message

    message = (
        "LinearDimension(count=3, increment=2.0 s, "
        "quantity_name=time, reciprocal={'quantity_name': 'frequency'})"
    )
    assert dim_1.__repr__() == message
    assert dim_2.__repr__() == message

    assert dim_1 != 2
    assert dim_1.is_quantitative() is True

    dim_3 = cp.as_dimension(np.arange(3) * 2)
    assert dim_1 / cp.ScalarQuantity("1s") == dim_3
    assert dim_1 * cp.ScalarQuantity("s^-1") == dim_3
    assert dim_2 / cp.ScalarQuantity("1s") == dim_3
    assert dim_2 * cp.ScalarQuantity("s^-1") == dim_3

    dim_3 *= cp.ScalarQuantity("1s")
    assert dim_1 == dim_3
    assert dim_2 == dim_3

    dim_3 /= cp.ScalarQuantity("s")
    dim_1 *= cp.ScalarQuantity("s^-1")
    dim_2 *= cp.ScalarQuantity("s^-1")
    assert dim_1 == dim_3
    assert dim_2 == dim_3

    dim_2 = cp.Dimension(type="linear", count=3, increment="2s")
    dim_2 /= cp.ScalarQuantity("s")
    assert dim_2 == cp.as_dimension(np.arange(3) * 2)

    assert dim_1.count == 3

    freq = cp.LinearDimension(
        count=10, increment="100 Hz", origin_offset="1 MHz", coordinates_offset="1kHz"
    )

    freq.to("kHz")
    assert np.allclose(freq.coordinates.value, (np.arange(10) * 0.1 + 1))
    assert np.allclose(freq.coords.value, (np.arange(10) * 0.1 + 1))

    freq.to("ppm", "nmr_frequency_ratio")
    values = (np.arange(10) * 100 + 1000) / (1 - (0.001 + 0.0005))
    assert np.allclose(freq.coordinates.value, values)
    assert np.allclose(freq.coords.value, values)

    freq.origin_offset = "0 Hz"
    assert str(freq.origin_offset) == "0.0 Hz"

    freq.coordinates_offset = "0 Hz"
    assert str(freq.coordinates_offset) == "0.0 Hz"

    assert (freq.origin_offset - freq.coordinates_offset).value == 0

    freq.complex_fft = True
    freq.to("ppm", "nmr_frequency_ratio")
    error = "Cannot convert the coordinates to ppm."
    with pytest.raises(ZeroDivisionError, match=error):
        _ = freq.coordinates

    with pytest.raises(ZeroDivisionError, match=error):
        _ = freq.coords


# monotonic dimension
def test_monotonic_new():
    dim_x = cp.Dimension(
        type="monotonic",
        description="Far far away.",
        coordinates=["1 m", "100 m", "1 km", "1 Gm", "0.25 lyr"],
    )
    data = cp.CSDM(dimensions=[dim_x, dim_x.copy()])

    for dim in data.dimensions:
        assert dim.is_quantitative() is True

        # description
        assert dim.description == "Far far away."
        dim.description = "A galaxy far far away."
        assert dim.description == "A galaxy far far away."

        error = "Expecting an instance of type"
        with pytest.raises(TypeError, match=f".*{error}.*"):
            dim.description = 12

        # dimension type
        assert dim.type == "monotonic"

        # values
        assert dim.subtype._values == [
            "1 m",
            "100 m",
            "1 km",
            "1 Gm",
            "0.25 lyr",
        ]

        # increment
        error = "'MonotonicDimension' object has no attribute 'increment'"
        with pytest.raises(AttributeError, match=f".*{error}.*"):
            _ = dim.increment

        # label
        assert dim.label == ""
        dim.label = "some string"
        assert dim.label == "some string"

        error = "Expecting an instance of type"
        with pytest.raises(TypeError, match=f".*{error}.*"):
            dim.label = {}

        # count
        assert dim.count == 5
        error = "Cannot set the count,"
        with pytest.raises(ValueError, match=f".*{error}.*"):
            dim.count = 12

        error = "Expecting an instance of type"
        with pytest.raises(TypeError, match=f".*{error}.*"):
            dim.count = "12"

        # coordinates_offset
        error = "`MonotonicDimension` has no attribute `coordinates_offset`."
        with pytest.raises(AttributeError, match=f".*{error}.*"):
            _ = dim.coordinates_offset

        error = "can't set attribute"
        with pytest.raises(AttributeError, match=f".*{error}.*"):
            dim.coordinates_offset = "1"

        # origin offset
        assert str(dim.origin_offset) == "0.0 m"

        dim.origin_offset = ScalarQuantity("3.1415 m")
        assert str(dim.origin_offset) == "3.1415 m"

        dim.origin_offset = "1 lyr"
        assert str(dim.origin_offset) == "1.0 lyr"

        error = "Expecting an instance of type"
        with pytest.raises(TypeError, match=f".*{error}.*"):
            dim.origin_offset = {"12 m"}

        # quantity_name
        assert dim.quantity_name == "length"

        error = "This attribute is not yet implemented"
        with pytest.raises(NotImplementedError, match=f".*{error}.*"):
            dim.quantity_name = "area/length"

        # period
        assert str(dim.period) == "inf m"
        dim.period = "Infinity m"
        assert str(dim.period) == "inf m"
        dim.period = "20 m^2/m"
        assert str(dim.period) == "20.0 m"
        dim.period = "(1/0) m^5/m^4"
        assert str(dim.period) == "inf m"
        dim.period = 1 * u.Unit("m^5/m^4")
        assert str(dim.period) == "1.0 m"

        error = "Expecting an instance of type `str` for period, got `int`."
        with pytest.raises(TypeError, match=f".*{error}.*"):
            dim.period = 1

        # fft output order
        error = "'MonotonicDimension' object has no attribute 'complex_fft'"
        with pytest.raises(AttributeError, match=f".*{error}.*"):
            _ = dim.complex_fft

    # coordinates
    assert np.allclose(
        data.dimensions[0].coordinates.value,
        np.asarray(
            [1.00000000e00, 1.00000000e02, 1.00000000e03, 1.00000000e09, 2.36518262e15]
        ),
    )

    # coords
    assert np.allclose(
        data.x[0].coords.value,
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

    data.dimensions[0].application = {"go": "in"}
    data.dimensions[1].application = {"go": "out"}
    data.dimensions[0].reciprocal.description = "blah"
    data.dimensions[1].reciprocal.description = "1/blah"

    assert data.dimensions[0].reciprocal.description == "blah"

    kwargs = {
        "type": "monotonic",
        "coordinates": ["1 m", "100 m", "1 km", "1 Gm", "0.25 lyr"],
        "origin_offset": "1.0 lyr",
        "quantity_name": "length",
        "period": "1.0 m",
        "label": "some string",
        "description": "A galaxy far far away.",
    }
    dim1 = {
        **kwargs,
        "application": {"go": "in"},
        "reciprocal": {"quantity_name": "wavenumber", "description": "blah"},
    }
    dim2 = {
        **kwargs,
        "application": {"go": "out"},
        "reciprocal": {"quantity_name": "wavenumber", "description": "1/blah"},
    }
    dict1 = {"csdm": {"version": "1.0", "dimensions": [dim1, dim2]}}
    assert data.data_structure == json.dumps(
        dict1, ensure_ascii=False, sort_keys=False, indent=2
    )

    assert data.dimensions[0].data_structure == json.dumps(
        dict1["csdm"]["dimensions"][0], ensure_ascii=False, sort_keys=False, indent=2
    )

    assert data.dimensions[0].dict() == dict1["csdm"]["dimensions"][0]
    assert data.dimensions[0].to_dict() == dict1["csdm"]["dimensions"][0]

    error = r"The unit 's' \(time\) is inconsistent with the unit 'm' \(length\)"
    with pytest.raises(Exception, match=f".*{error}.*"):
        data.dimensions[0].coordinates = ["1s", "2s"]
    with pytest.raises(Exception, match=f".*{error}.*"):
        data.x[0].coords = ["1s", "2s"]

    data.dimensions[0].coordinates = ["1m", "2m"]
    assert np.allclose(data.dimensions[0].coordinates.value, np.asarray([1, 2]))
    assert np.allclose(data.x[0].coords.value, np.asarray([1, 2]))

    # check equality
    dim1 = data.dimensions[0].copy()
    assert data.dimensions[0] == dim1

    dim1.origin_offset = "1 m"
    assert data.dimensions[0] != dim1

    dim2 = dim1.copy()
    dim2.origin_offset = "100 cm"
    assert dim1 == dim2

    assert dim1 != 21


def test_monotonicDimension():
    dim_1 = cp.MonotonicDimension(coordinates=10 ** (np.arange(2)))
    assert dim_1.__str__() == "MonotonicDimension([ 1. 10.])"

    assert dim_1.__repr__() == ("MonotonicDimension(coordinates=[ 1. 10.])")

    assert dim_1 != 2
    assert dim_1.is_quantitative() is True

    dim_2 = cp.as_dimension([1, 10], type="monotonic") * cp.ScalarQuantity("s")
    assert dim_2 / cp.ScalarQuantity("1s") == cp.as_dimension([1, 10], type="monotonic")
    assert dim_1 * cp.ScalarQuantity("s") == dim_2

    dim_2 /= cp.ScalarQuantity("s")
    dim_1 *= cp.ScalarQuantity("s^-1")
    assert dim_1 * cp.ScalarQuantity("1s") == dim_2

    dim_2.count = 1
    assert dim_2.coordinates.value == [1]
    assert dim_2.coords.value == [1]

    ratio = cp.as_dimension([1, 10], type="monotonic") * cp.ScalarQuantity("Hz")
    ratio.origin_offset = "1 MHz"
    assert str(ratio.origin_offset) == "1.0 MHz"

    ratio.to("ppm", "nmr_frequency_ratio")

    assert np.allclose(ratio.coordinates.value, np.asarray([1.0, 10.0]) / (1.0 - 1e-6))
    assert np.allclose(ratio.coords.value, np.asarray([1.0, 10.0]) / (1.0 - 1e-6))

    ratio.coordinates = ["0 Hz", "10 Hz"]
    ratio.coords = ["0 Hz", "10 Hz"]

    assert np.allclose(ratio.coordinates.value, [0.0, 10])
    assert np.allclose(ratio.coords.value, [0.0, 10])

    error = r"The unit '' \(dimensionless\) is inconsistent with the unit 'Hz'"
    with pytest.raises(Exception, match=f".*{error}.*"):
        ratio.coordinates = ["0 ", "10 "]
    with pytest.raises(Exception, match=f".*{error}.*"):
        ratio.coords = ["0 ", "10 "]

    ratio.origin_offset = "0 Hz"
    error = "Cannot convert the coordinates to ppm."
    with pytest.raises(ZeroDivisionError, match=f".*{error}.*"):
        _ = ratio.coordinates
    with pytest.raises(ZeroDivisionError, match=f".*{error}.*"):
        _ = ratio.coords

    assert ratio.axis_label == "frequency / (ppm)"

    ratio.label = "shift"
    assert ratio.axis_label == "shift / (ppm)"

    ratio.to("Hz", "nmr_frequency_ratio")
    assert ratio.axis_label == "shift / (Hz)"

    ratio.to("MHz")
    assert np.allclose(ratio.coordinates.value, np.asarray([0.0, 10.0e-6]))
    assert np.allclose(ratio.coords.value, np.asarray([0.0, 10.0e-6]))

    assert ratio.axis_label == "shift / (MHz)"


# labeled dimension
def test_labeled_new():
    data = cp.new()
    dim = {
        "type": "labeled",
        "description": "Far far away.",
        "labels": ["m", "s", "t", "a"],
    }
    data.dimensions.append(dim)

    assert data.dimensions[0].is_quantitative() is False

    # description
    assert data.dimensions[0].description == "Far far away."
    data.dimensions[0].description = "A galaxy far far away."
    assert data.dimensions[0].description == "A galaxy far far away."

    error = "Expecting an instance of type"
    with pytest.raises(TypeError, match=f".*{error}.*"):
        data.dimensions[0].description = 12

    assert data.dimensions[0].labels[0] == "m"
    assert data.dimensions[0].coordinates[-1] == "a"
    assert data.x[0].coords[-1] == "a"

    error = "A list of labels is required"
    with pytest.raises(ValueError, match=f".*{error}.*"):
        data.dimensions[0].labels = 12

    error = "A list of string labels are required"
    with pytest.raises(ValueError, match=f".*{error}.*"):
        data.dimensions[0].labels = ["12", "1", 4]

    data.dimensions[0].label = "labeled dimension"
    assert data.dimensions[0].label == "labeled dimension"

    data.dimensions[0].application = {"this is it": "period"}
    assert data.dimensions[0].application == {"this is it": "period"}

    data.dimensions[0].coordinates = ["a", "b", "c"]
    assert data.dimensions[0].coordinates[-1] == "c"
    assert data.x[0].coords[-1] == "c"

    dict1 = {
        "csdm": {
            "version": "1.0",
            "dimensions": [
                {
                    "type": "labeled",
                    "labels": ["a", "b", "c"],
                    "label": "labeled dimension",
                    "description": "A galaxy far far away.",
                    "application": {"this is it": "period"},
                }
            ],
        }
    }
    assert data.data_structure == json.dumps(
        dict1, ensure_ascii=False, sort_keys=False, indent=2
    )
    assert data.dimensions[0].dict() == dict1["csdm"]["dimensions"][0]

    assert data.dimensions[0].data_structure == json.dumps(
        dict1["csdm"]["dimensions"][0], ensure_ascii=False, sort_keys=False, indent=2
    )

    # check equality
    dim1 = data.dimensions[0].copy()
    assert data.dimensions[0] == dim1

    dim1.labels[1] = "Skywalker"
    assert data.dimensions[0] != dim1

    assert dim1 != 21
    assert dim1.axis_label == "labeled dimension"


def test_labeledDimension():
    dim_1 = cp.as_dimension(["1", "a", "c"])

    assert dim_1.__str__() == "LabeledDimension(['1' 'a' 'c'])"

    assert dim_1.__repr__() == ("LabeledDimension(labels=['1', 'a', 'c'])")

    assert dim_1.type == "labeled"
    assert dim_1 != 1
    assert dim_1.is_quantitative() is False
    assert dim_1.count == 3

    error = "Cannot set the count, 4, more than the number of coordinates"
    with pytest.raises(ValueError, match=f".*{error}.*"):
        dim_1.count = 4

    dim_1.count = 2
    assert dim_1.count == 2

    assert dim_1 == dim_1.copy()


def test_as_dimension():
    array = np.arange(10)
    one = np.ones(10)
    rand = np.random.rand(10)
    monotonic = 10**array / 10

    dim = cp.as_dimension(array, unit="s")
    assert np.allclose(dim.coordinates.value, array)
    assert np.allclose(dim.coords.value, array)

    # linear
    error = "Invalid array for Dimension object."
    with pytest.raises(ValueError, match=f".*{error}.*"):
        cp.as_dimension(one, unit="s")

    dim = cp.as_dimension(array, unit="s", type="linear")
    assert np.allclose(dim.coordinates.value, array)

    # linear with type
    error = "Invalid array for LinearDimension object."
    with pytest.raises(ValueError, match=f".*{error}.*"):
        cp.as_dimension(one, unit="s", type="linear")

    error = "Invalid array for LinearDimension object."
    with pytest.raises(ValueError, match=f".*{error}.*"):
        cp.as_dimension(one, unit="s", type="linear")

    # monotonic

    dim = cp.as_dimension(monotonic, unit="s")
    assert np.allclose(dim.coordinates.value, monotonic)
    assert np.allclose(dim.coords.value, monotonic)

    dim = cp.as_dimension(monotonic, unit="s", type="monotonic")
    assert np.allclose(dim.coordinates.value, monotonic)
    assert np.allclose(dim.coords.value, monotonic)

    error = "Invalid array for Dimension object."
    with pytest.raises(ValueError, match=f".*{error}.*"):
        cp.as_dimension(rand, unit="s")

    error = "Invalid array for MonotonicDimension object."
    with pytest.raises(ValueError, match=f".*{error}.*"):
        cp.as_dimension(rand, unit="s", type="monotonic")

    # labeled

    dim = cp.as_dimension(list("abcd"))
    assert np.all(dim.coordinates == list("abcd"))
    assert np.all(dim.coords == list("abcd"))

    dim = cp.as_dimension(list("abcd"), type="labeled")
    assert np.all(dim.coordinates == list("abcd"))
    assert np.all(dim.coords == list("abcd"))

    # error
    error = "Invalid value for `type`. Allowed values are"
    with pytest.raises(ValueError, match=f".*{error}.*"):
        cp.as_dimension(array, type="log-linear")

    error = "to a Dimension object."
    with pytest.raises(ValueError, match=f".*{error}.*"):
        cp.as_dimension({"a": [1, 2, 3]})

    error = "Cannot convert a 2 dimensional array to a Dimension object."
    with pytest.raises(ValueError, match=f".*{error}.*"):
        cp.as_dimension(np.arange(100).reshape(10, 10))


def test_dimension_scale():
    """Test for unit physical type in astropy>=4.0"""
    dim = cp.LinearDimension(count=10, increment="1m")
    dim2 = dim / 2.4
    assert np.allclose(dim2.coordinates.value, np.arange(10) / 2.4)
    assert dim2.quantity_name == "length"
    assert type(dim2.quantity_name) == str

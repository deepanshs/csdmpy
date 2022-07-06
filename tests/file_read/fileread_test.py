from os import path

import pytest

import csdmpy as cp

COMMON_PATH = path.join("tests", "file_read", "test_files")


def file_testing(file_, error, error_type):
    with pytest.raises(error_type, match=f".*{error}.*"):
        cp.load(file_)


def test_01():
    file_ = path.join(COMMON_PATH, "1.csdfe")
    error = "'CSDM' is not a valid keyword for the CSD model."
    file_testing(file_, error, KeyError)


def test_02():
    file_ = path.join(COMMON_PATH, "2.csdfe")
    error = "Missing a required `version` key from the CSDM object."
    file_testing(file_, error, KeyError)


def test_03():
    file_ = path.join(COMMON_PATH, "3.csdfe")
    error = "Expecting an instance of type `int` for count, got `str`."
    file_testing(file_, error, TypeError)


def test_04():
    file_ = path.join(COMMON_PATH, "4.csdfe")
    error = "The value, `tensor`, is an invalid `quantity_type`"
    file_testing(file_, error, ValueError)


def test_05():
    file_ = path.join(COMMON_PATH, "5.csdfe")
    error = "The quantity_type, 'vector_2', requires exactly 2 component"
    file_testing(file_, error, Exception)


def test_06():
    file_ = path.join(COMMON_PATH, "6.csdfe")
    error = "The value, `float16`, is an invalid `numeric_type`"
    file_testing(file_, error, ValueError)


def test_07():
    file_ = path.join(COMMON_PATH, "7.csdfe")
    error = "Missing a required `coordinates` key from the MonotonicDimension"
    file_testing(file_, error, KeyError)


def test_08():
    file_ = path.join(COMMON_PATH, "8.csdfe")
    error = "A list of string labels are required, found int"
    file_testing(file_, error, ValueError)


def test_09():
    file_ = path.join(COMMON_PATH, "9.csdfe")
    error = "Missing a required `quantity_type` key from the DependentVariable"
    file_testing(file_, error, KeyError)


def test_10():
    file_ = path.join(COMMON_PATH, "10.csdfe")
    error = "Missing a required `numeric_type` key from the DependentVariable"
    file_testing(file_, error, KeyError)


def test_11():
    file_ = path.join(COMMON_PATH, "11.csdfe")
    error = "The `encoding` key is invalid for DependentVariable objects"
    file_testing(file_, error, KeyError)


def test_12():
    file_ = path.join(COMMON_PATH, "12.csdfe")
    error = "Missing a required 'type' key from the Dimension object."
    file_testing(file_, error, KeyError)


def test_13():
    file_ = path.join(COMMON_PATH, "13.csdfe")
    error = "Missing a required `count` key from the LinearDimension."
    file_testing(file_, error, KeyError)


def test_14():
    file_ = path.join(COMMON_PATH, "14.csdfe")
    error = "Missing a required `type` key from the DependentVariable."
    file_testing(file_, error, KeyError)


def test_15():
    file_ = path.join(COMMON_PATH, "15.csdfe")
    error = "The value, 'blah', is invalid for the `type` attribute"
    file_testing(file_, error, ValueError)


def test_16():
    file_ = path.join(COMMON_PATH, "16.csdfe")
    error = "Missing a required `labels` key from the LabeledDimension object."
    file_testing(file_, error, KeyError)

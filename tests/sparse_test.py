import numpy as np
import pytest

from csdmpy.dependent_variable.sparse import check_sparse_sampling_key_value
from csdmpy.dependent_variable.sparse import SparseSampling

sparse_sampling = {
    "dimension_indexes": [0],
    "sparse_grid_vertexes": [0, 5, 10, 15, 20, 25],
    "unsigned_integer_type": "uint16",
}


def test_01():
    s_p = SparseSampling(**sparse_sampling)
    assert s_p.dimension_indexes == [0]

    assert np.all(s_p.sparse_grid_vertexes == [0, 5, 10, 15, 20, 25])

    assert s_p.description == ""
    assert s_p.encoding == "none"
    assert s_p.unsigned_integer_type.value == "uint16"
    assert s_p.application is None


def test_02():
    sparse_sampling = {
        "dimension_indexes": [0],
    }

    error = "Missing a required `sparse_grid_vertexes`"
    with pytest.raises(KeyError, match=f".*{error}.*"):
        check_sparse_sampling_key_value(sparse_sampling)


def test_03():
    sparse_sampling = {
        "sparse_grid_vertexes": [0, 5, 10, 15, 20, 25],
    }

    error = "Missing a required `dimension_indexes`"
    with pytest.raises(KeyError, match=f".*{error}.*"):
        check_sparse_sampling_key_value(sparse_sampling)


def test_04():
    sparse_sampling = {
        "encoding": "base64",
        "dimension_indexes": [0],
        "sparse_grid_vertexes": [0, 5, 10, 15, 20, 25],
    }
    error = "Missing a required `unsigned_integer_type`"
    with pytest.raises(KeyError, match=f".*{error}.*"):
        check_sparse_sampling_key_value(sparse_sampling)


def test_05():
    sparse_sampling = {
        "encoding": "base64",
        "unsigned_integer_type": "float32",
        "dimension_indexes": [0],
        "sparse_grid_vertexes": [0, 5, 10, 15, 20, 25],
    }
    error = "float32 is an invalid `unsigned_integer_type` enumeration"
    with pytest.raises(ValueError, match=f".*{error}.*"):
        check_sparse_sampling_key_value(sparse_sampling)


def test_06():
    sp1 = SparseSampling(**sparse_sampling)
    sp2 = SparseSampling(**sparse_sampling)

    assert sp1 == sp2

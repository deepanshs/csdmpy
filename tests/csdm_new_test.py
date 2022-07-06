import numpy as np
import pytest

import csdmpy as cp


def test_csdm_new():
    a = cp.CSDM(dimensions=[cp.as_dimension(np.arange(10))])

    error = "Expecting a Dimension object"
    with pytest.raises(ValueError, match=f".*{error}.*"):
        a.dimensions.append(np.arange(5))

    with pytest.raises(ValueError, match=f".*{error}.*"):
        a.dimensions[0] = np.arange(5)

    error = "Deleting items is not allowed"
    with pytest.raises(LookupError, match=f".*{error}.*"):
        del a.dimensions[0]

    assert a.dimensions[0] != np.arange(5)
    assert a.ndim == 1
    assert a.to_dict() == {
        "csdm": {
            "dimensions": [{"count": 10, "increment": "1.0", "type": "linear"}],
            "version": "1.0",
        }
    }


def test_bad_csdm():
    error = "A list of valid Dimension or equivalent dictionary objects"
    with pytest.raises(ValueError, match=f".*{error}.*"):
        cp.CSDM(dimensions="blah")

    error = "A list of valid DependentVariable or equivalent dictionary objects"
    with pytest.raises(ValueError, match=f".*{error}.*"):
        cp.CSDM(dependent_variables="blah")

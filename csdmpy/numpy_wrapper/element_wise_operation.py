"""
A wrapper to the Numpy functions which result in a element-wise operation.

The list of supported functions are:
    - sin
    - cos
    - ...
"""

import numpy as np
from csdmpy.numpy_wrapper import _get_new_csdm_object_after_applying_func


def sin(csdm):
    """Return a CSDM object after applying sine to the dependent variable
    components."""
    func = np.sin
    return _get_new_csdm_object_after_applying_func(csdm, func)


def cos(csdm):
    """Return a CSDM object after applying cosine to the dependent variable
    components."""
    func = np.cos
    return _get_new_csdm_object_after_applying_func(csdm, func)

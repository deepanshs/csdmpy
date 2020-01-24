"""
A wrapper to the Numpy functions which result in a dimension collapse.

The list of supported functions are:
    - sum
    - prod
    - ...
"""

import numpy as np
from csdmpy.numpy_wrapper import _get_new_csdm_object_after_applying_func


def sum(csdm, dimension=0):
    """
    Sum of the components over a given `dimension`.

    Args:
        csdm: A CSDM object.
        dimension: An integer or tuple of `m` integers cooresponding to the
                   index/indices of dimensions along which the sum of the
                   dependent variable components is performed.

    Return:
        A CSDM object with `d-m` dimensions where `d` is the total
        number of dimensions from the original csdm data.
    """
    func = np.sum
    return _get_new_csdm_object_after_applying_func(csdm, func, dimension)


def prod(csdm, dimension=0):
    """
    Product of the components over a given `dimension`.

    Args:
        csdm: A CSDM object.
        dimension: An integer or tuple of `m` integers cooresponding to the
                   index/indices of dimensions along which the product of the
                   dependent variable components is performed.

    Return:
        A CSDM object with `d-m` dimensions where `d` is the total number of
        dimensions from the original csdm dataset.
    """
    func = np.prod
    return _get_new_csdm_object_after_applying_func(csdm, func, dimension)

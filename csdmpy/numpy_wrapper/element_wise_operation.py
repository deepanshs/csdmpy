# -*- coding: utf-8 -*-
"""
A wrapper to the Numpy functions which result in a element-wise operation.

The list of supported functions are:
    - sin
    - cos
    - ...
"""
import numpy as np

from csdmpy.numpy_wrapper import _get_new_csdm_object_after_applying_func

__all__ = ("sin", "cos", "tan", "arcsin", "arccos", "arctan")


# Trigonometric functions
def sin(csdm):
    """Return a CSDM object with the sine of the dependent variables."""
    return _get_new_csdm_object_after_applying_func(csdm, np.sin)


def cos(csdm):
    """Return a CSDM object with the cosine of the dependent variables."""
    return _get_new_csdm_object_after_applying_func(csdm, np.cos)


def tan(csdm):
    """Return a CSDM object with the tangent of the dependent variables."""
    return _get_new_csdm_object_after_applying_func(csdm, np.tan)


def arcsin(csdm):
    """Return a CSDM object with the inverse sine of the dependent variables."""
    return _get_new_csdm_object_after_applying_func(csdm, np.arcsin)


def arccos(csdm):
    """Return a CSDM object with the inverse cosine of the dependent variables."""
    return _get_new_csdm_object_after_applying_func(csdm, np.arccos)


def arctan(csdm):
    """Return a CSDM object with the inverse tangent of the dependent variables."""
    return _get_new_csdm_object_after_applying_func(csdm, np.arctan)

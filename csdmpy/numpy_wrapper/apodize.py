# -*- coding: utf-8 -*-
"""
A wrapper to the Numpy functions used to apodize the components along a given
dimension. If :math:`x` is  the coordinates along the dimension, the apodization
function follows,

.. math::
        y = function(a x),

where :math:`a` is the argument of the function. The dimensionality of :math:`a`
must be reciprocal of that of :math:`x`.

The list of supported functions are:
    - sin
    - cos
    - ...
"""
import numpy as np

from csdmpy.csdm import _get_new_csdm_object_after_apodization

__all__ = ("sin", "cos", "tan", "arcsin", "arccos", "arctan", "exp")


# Trigonometric functions


def sin(csdm, arg, dimension=0):
    r"""
    Apodize the components along the `dimension` with :math:`\sin(a x)`.

    Args:
        csdm: A CSDM object.
        arg: String or Quantity object. The function argument :math:`a`.
        dimension: An integer or tuple of `m` integers cooresponding to the
                   index/indices of the dimensions along which the sine of the
                   dependent variable components is performed.
    Return:
        A CSDM object with `d-m` dimensions, where `d` is the total
        number of dimensions from the original `csdm` object.
    """
    return _get_new_csdm_object_after_apodization(csdm, np.sin, arg, dimension)


def cos(csdm, arg, dimension=0):
    r"""
    Apodize the components along the `dimension` with :math:`\cos(a x)`.

    Args:
        csdm: A CSDM object.
        arg: String or Quantity object. The function argument :math:`a`.
        dimension: An integer or tuple of `m` integers cooresponding to the
                   index/indices of the dimensions along which the cosine of the
                   dependent variable components is performed.
    Return:
        A CSDM object with `d-m` dimensions, where `d` is the total
        number of dimensions from the original `csdm` object.
    """
    return _get_new_csdm_object_after_apodization(csdm, np.cos, arg, dimension)


def tan(csdm, arg, dimension=0):
    r"""
    Apodize the components along the `dimension` with :math:`\tan(a x)`.

    Args:
        csdm: A CSDM object.
        arg: String or Quantity object. The function argument :math:`a`.
        dimension: An integer or tuple of `m` integers cooresponding to the
                   index/indices of the dimensions along which the tangent of the
                   dependent variable components is performed.
    Return:
        A CSDM object with `d-m` dimensions, where `d` is the total
        number of dimensions from the original `csdm` object.
    """
    return _get_new_csdm_object_after_apodization(csdm, np.tan, arg, dimension)


def arcsin(csdm, arg, dimension=0):
    r"""
    Apodize the components along the `dimension` with :math:`\arcsin(a x)`.

    Args:
        csdm: A CSDM object.
        arg: String or Quantity object. The function argument :math:`a`.
        dimension: An integer or tuple of `m` integers cooresponding to the
                   index/indices of the dimensions along which the inverse sine of the
                   dependent variable components is performed.
    Return:
        A CSDM object with `d-m` dimensions, where `d` is the total
        number of dimensions from the original `csdm` object.
    """
    return _get_new_csdm_object_after_apodization(csdm, np.arcsin, arg, dimension)


def arccos(csdm, arg, dimension=0):
    r"""
    Apodize the components along the `dimension` with :math:`\arccos(a x)`.

    Args:
        csdm: A CSDM object.
        arg: String or Quantity object. The function argument :math:`a`.
        dimension: An integer or tuple of `m` integers cooresponding to the
                   index/indices of the dimensions along which the inverse cosine of
                   the dependent variable components is performed.
    Return:
        A CSDM object with `d-m` dimensions, where `d` is the total
        number of dimensions from the original `csdm` object.
    """
    return _get_new_csdm_object_after_apodization(csdm, np.arccos, arg, dimension)


def arctan(csdm, arg, dimension=0):
    r"""
    Apodize the components along the `dimension` with :math:`\arctan(a x)`.

    Args:
        csdm: A CSDM object.
        arg: String or Quantity object. The function argument :math:`a`.
        dimension: An integer or tuple of `m` integers cooresponding to the
                   index/indices of the dimensions along which the inverse tangent of
                   the dependent variable components is performed.
    Return:
        A CSDM object with `d-m` dimensions, where `d` is the total
        number of dimensions from the original `csdm` object.
    """
    return _get_new_csdm_object_after_apodization(csdm, np.arctan, arg, dimension)


def exp(csdm, arg, dimension=0):
    r"""
    Apodize the components along the `dimension` with :math:`\exp(a x)`.

    Args:
        csdm: A CSDM object.
        arg: String or Quantity object. The function argument :math:`a`.
        dimension: An integer or tuple of `m` integers cooresponding to the
                   index/indices of the dimensions along which the exp of the
                   dependent variable components is performed.
    Return:
        A CSDM object with `d-m` dimensions, where `d` is the total
        number of dimensions from the original `csdm` object.
    """
    return _get_new_csdm_object_after_apodization(csdm, np.exp, arg, dimension)

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
from csdmpy.numpy_wrapper import _get_new_csdm_object_after_apodization


def sin(csdm, arg, dimension=0):
    r"""
    Apodize the components along the `dimension` by :math:`\sin(a x)`.

    Args:
        csdm: A CSDM object.
        arg: The function argument :math:`a`.
        dimension: An integer or tuple of `m` integers cooresponding to the
                   index/indices of dimensions along which the sin of the
                   dependent variable components is performed.
    Return:
        A CSDM object with `d-m` dimensions where `d` is the total
        number of dimensions from the original csdm data.
    """
    func = np.sin
    return _get_new_csdm_object_after_apodization(csdm, func, arg, dimension)


def cos(csdm, arg, dimension=0):
    r"""
    Apodize the components along the `dimension` by :math:`\cos(a x)`.

    Args:
        csdm: A CSDM object.
        arg: The function argument :math:`a`.
        dimension: An integer or tuple of `m` integers cooresponding to the
                   index/indices of dimensions along which the cosine of the
                   dependent variable components is performed.
    Return:
        A CSDM object with `d-m` dimensions where `d` is the total
        number of dimensions from the original csdm data.
    """
    func = np.cos
    return _get_new_csdm_object_after_apodization(csdm, func, arg, dimension)

# -*- coding: utf-8 -*-
import numpy as np

from csdmpy.utils import _get_broadcast_shape


def _check_dimension_type(csdm):
    check = [item.type == "linear" for item in csdm.dimensions]
    if not np.all(check):
        raise NotImplementedError(
            "Statistics is currently only available for linear dimensions."
        )


def integral(csdm):
    """Evaluate the integral of the dependent variables over all dimensions.

    Args:
        csdm: A csdm object.

    Return:
        A list of integrals corresponding to the list of the dependent variables. If
        only one dependent variable is present, return a quantity instead.

    Example:
        >>> import csdmpy.statistics as stat
        >>> x = np.arange(100) * 2 - 100.0
        >>> gauss = np.exp(-((x - 5.) ** 2) / (2 * 4. ** 2))
        >>> csdm = cp.as_csdm(gauss, unit='T')
        >>> csdm.dimensions[0] = cp.as_dimension(x, unit="m")
        >>> stat.integral(csdm)
        <Quantity 10.0265131 m T>
    """
    dim_l = len(csdm.dimensions)
    _check_dimension_type(csdm)

    intervals = [item.coordinates[1] - item.coordinates[0] for item in csdm.dimensions]
    i = 1.0
    for _ in range(dim_l):
        i = i * intervals[_]

    csdm_sum = csdm.sum()
    if isinstance(csdm_sum, list):
        return [sum_ * i for sum_ in csdm_sum]
    return csdm_sum * i


def mean(csdm):
    """Evaluate the mean coordinate of a dependent variable along each dimension.

    Args:
        csdm: A csdm object.

    Return:
        A list of tuples, where each tuple represents the mean coordinates of the
        dependent variables. If only one dependent variable is present, return a tuple
        of coordinates instead.

    Example:
        >>> stat.mean(csdm)
        (<Quantity 5. m>,)
    """
    dim_l = len(csdm.dimensions)
    _check_dimension_type(csdm)

    dims = [
        _get_broadcast_shape(item.coordinates, dim_l, -i - 1)
        for i, item in enumerate(csdm.dimensions)
    ]

    sum_csdm = csdm.sum()
    if not isinstance(sum_csdm, list):
        sum_csdm = [sum_csdm]
    y = []
    for i, variable in enumerate(csdm.dependent_variables):
        y_ = []
        for dim in dims:
            unit = dim.unit * variable.unit
            y_.append(np.sum(variable.components * dim.value) / sum_csdm[i] * unit)
        y.append(tuple(y_))

    if len(y) > 1:
        return y
    return y[0]


def var(csdm):
    """Evaluate the variance of the dependent variables along each dimension.

    Args:
        csdm: A csdm object.

    Return:
        A list of tuples, where each tuple is the variance along the dimensions of the
        dependent variables. If only one dependent variable is present, return a tuple
        instead.

    Example:
        >>> stat.var(csdm)
        (<Quantity 16. m2>,)
    """
    dim_l = len(csdm.dimensions)
    _check_dimension_type(csdm)

    dims = [
        _get_broadcast_shape(item.coordinates, dim_l, -i - 1)
        for i, item in enumerate(csdm.dimensions)
    ]

    mean_csdm = mean(csdm)
    if not isinstance(mean_csdm, list):
        mean_csdm = [mean_csdm]

    sum_csdm = csdm.sum()
    if not isinstance(sum_csdm, list):
        sum_csdm = [sum_csdm]

    y = []
    for i, variable in enumerate(csdm.dependent_variables):
        y_ = []
        for j, dim in enumerate(dims):
            d = (dim - mean_csdm[i][j]) ** 2
            unit = d.unit * variable.unit
            y_.append(np.sum(variable.components * d.value) / sum_csdm[i] * unit)
        y.append(tuple(y_))

    if len(y) > 1:
        return y
    return y[0]


def std(csdm):
    """Evaluate the standard deviation of the dependent variables along each dimension.

    Args:
        csdm: A csdm object.

    Return:
        A list of tuples, where each tuple is the standard deviation along the
        dimensions of the dependent variables. If only one dependent variable is
        present, return a tuple instead.

    Example:
        >>> stat.std(csdm)
        (<Quantity 4. m>,)
    """
    var_ = var(csdm)
    if isinstance(var_, list):
        return [tuple([np.sqrt(value) for value in items]) for items in var_]
    return tuple([np.sqrt(value) for value in var_])

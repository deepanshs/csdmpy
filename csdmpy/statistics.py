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
    dim_l = len(csdm.dimensions)
    _check_dimension_type(csdm)

    intervals = [item.coordinates[1] - item.coordinates[0] for item in csdm.dimensions]
    i = 1.0
    for _ in range(dim_l):
        i = i * intervals[_]

    csdm_sum = csdm.sum()
    return [sum_ * i for sum_ in csdm_sum]


def mean(csdm):
    dim_l = len(csdm.dimensions)
    _check_dimension_type(csdm)

    dims = [
        _get_broadcast_shape(item.coordinates, dim_l, -i - 1)
        for i, item in enumerate(csdm.dimensions)
    ]

    sum_csdm = csdm.sum()
    y = []
    for i, variable in enumerate(csdm.dependent_variables):
        y_ = []
        for dim in dims:
            unit = dim.unit * variable.unit
            y_.append(np.sum(variable.components * dim.value) / sum_csdm[i] * unit)
        y.append(y_)

    return y


def std(csdm):
    pass


# def var(csdm):
#     return _base(csdm, np.mean) / np.asarray(csdm.sum())[:, np.newaxis]

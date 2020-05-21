# -*- coding: utf-8 -*-
import numpy as np

import csdmpy as cp
from csdmpy.utils import _check_dimension_indices  # lgtm [py/import-own-module]
from csdmpy.utils import _get_broadcast_shape  # lgtm [py/import-own-module]


def fft(csdm, axis=0):
    """Perform a FFT along the given `dimension=axis`."""
    index = _check_dimension_indices(len(csdm.dimensions), axis)[0]
    # for index in indexes:
    if csdm.dimensions[index].type != "linear":
        raise NotImplementedError(
            f"The FFT method is not available for Dimension objects with "
            f"subtype, {csdm.dimensions[index].type}."
        )

    csdm_new = csdm.astype(np.complex128)
    dimension_object = csdm_new.dimensions[index]
    if not isinstance(dimension_object, cp.LinearDimension):
        dimension_object = dimension_object.subtype

    unit_in = dimension_object._unit
    coordinates = dimension_object._coordinates.to(unit_in).value
    coordinates_offset = dimension_object._coordinates_offset.to(unit_in).value

    unit_out = (1 / unit_in).unit
    coordinates_res = dimension_object.reciprocal_coordinates().to(unit_out).value
    coordinates_offset_res = dimension_object.reciprocal._coordinates_offset.to(
        unit_out
    ).value

    ndim = len(csdm_new.dimensions)

    if dimension_object._complex_fft:
        phase = np.exp(2j * np.pi * coordinates_offset_res * coordinates)
        phase_grid = _get_broadcast_shape(phase, ndim, axis=index)
        for item in csdm_new.dependent_variables:
            phased_signal = item.subtype._components * phase_grid
            ft_shift = np.fft.ifftshift(phased_signal, axes=index)
            signal_ft = np.fft.ifft(ft_shift, axis=index)

            item.subtype._components = signal_ft
        dimension_object._complex_fft = False
    else:  # FFT is false
        phase = np.exp(-2j * np.pi * coordinates_offset * coordinates_res)
        phase_grid = _get_broadcast_shape(phase, ndim, axis=index)
        for item in csdm_new.dependent_variables:
            ft = np.fft.fft(item.subtype._components, axis=index)
            ft_shift = np.fft.fftshift(ft, axes=index)
            signal_ft = ft_shift * phase_grid

            item.subtype._components = signal_ft
        dimension_object._complex_fft = True

    # get the coordinates of the reciprocal dimension.
    dimension_object._swap()
    dimension_object._increment = dimension_object.reciprocal_increment()
    dimension_object._get_coordinates()
    return csdm_new


#
# def _compare_cv_object(cv1, cv2):
#     if cv1.gcv._getparams == cv2.gcv._getparams:
#         return True
#     return False
#
# def _compare_cv_objects(object1, object2):
#     dim1 = len(object1.dimensions)
#     dim2 = len(object2.dimensions)
#     message = (
#         "{0} and {1} do not have the same set of "
#         "controlled variables."
#     ).format(object1.__name__, object2.__name__)
#     if dim1 != dim2:
#         raise Exception(message)
#     for i in range(dim1):
#         if not _compare_cv_object(
#             object1.dimensions[i],
#             object2.dimensions[i]
#         ):
#             raise Exception(message)
#     return True
#
# def _compare_uv(uv1, uv2):
#     # a = {
#     #     'unit': True,
#     #     'quantity_name': True,
#     #     'quantity_type': True
#     # }
#     a = True
#     if uv1.unit.physical_type != uv2.unit.physical_type:
#         a = False
#     if uv1.quantity_name != uv2.quantity_name:
#         raise Exception(
#             (
#                 "Binary operates are not supported for "
#                 "objects with different quantity."
#             )
#         )
#     if uv1.quantity_type != uv2.quantity_type:
#         raise Exception(
#             (
#                 "Binary operates are not supported for "
#                 "objects with different quantity_type."
#             )
#         )
#     return a
#
# def _compare_uv_objects(object1, object2):
#     dim1 = len(object1.dependent_variables)
#     dim2 = len(object2.dependent_variables)
#     for j in range(dim1):
#         for i in range(dim2):
#             a = _compare_uv(
#                 object1.dependent_variables[i],
#                 object2.dependent_variables[j]
#             )

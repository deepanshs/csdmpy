import numpy as np
import scipy as sp

import csdmpy as cp
from csdmpy.utils import _check_dimension_indices
from csdmpy.utils import _get_broadcast_shape


__ufunc_list_dimensionless_unit__ = [
    np.sin,
    np.cos,
    np.tan,
    np.arcsin,
    np.arccos,
    np.arctan,
    np.sinh,
    np.cosh,
    np.tanh,
    np.arcsinh,
    np.arccosh,
    np.arctanh,
    np.exp,
    np.exp2,
    np.log,
    np.log2,
    np.log10,
    np.expm1,
    np.log1p,
]

__ufunc_list_unit_independent__ = [
    np.negative,
    np.positive,
    np.absolute,
    np.fabs,
    np.rint,
    np.sign,
    np.conj,
    np.conjugate,
]

__ufunc_list_applies_to_unit__ = [np.sqrt, np.square, np.cbrt, np.reciprocal, np.power]

__function_reduction_list__ = [
    np.max,
    np.min,
    np.sum,
    np.mean,
    np.var,
    np.std,
    np.prod,
    np.cumsum,
    np.cumprod,
    np.argmin,
    np.argmax,
]

__other_functions__ = [np.round, np.real, np.imag, np.clip, np.around, np.angle]

__shape_manipulation_functions__ = [np.transpose]
__array_manipulation__ = [np.flip]


def fft(csdm, axis=0):
    """Perform a FFT along the given `dimension=axis`."""
    index = _check_dimension_indices(len(csdm.dimensions), axis)
    index = index if isinstance(index, int) else index[0]
    # for index in indexes:
    if csdm.dimensions[axis].type != "linear":
        raise NotImplementedError(
            f"The FFT method is not available for Dimension objects with "
            f"subtype, {csdm.dimensions[axis].type}."
        )

    csdm_new = csdm.astype(np.complex128)
    dimension_object = csdm_new.dimensions[axis]
    if not isinstance(dimension_object, cp.LinearDimension):
        dimension_object = dimension_object.subtype

    unit_in = dimension_object._unit
    # the following coordinates does not include the coordinates offset and have are
    # given in the base unit of the dimension.
    coordinates = dimension_object._coordinates.to(unit_in).value
    coordinates_offset = dimension_object._coordinates_offset.to(unit_in).value

    unit_out = (1 / unit_in).unit
    # the following coordinates does not include the coordinates offset and have are
    # given in the vase unit of the dimension.
    coordinates_res = dimension_object._reciprocal_coordinates().to(unit_out).value
    coordinates_offset_res = dimension_object.reciprocal._coordinates_offset
    coordinates_offset_res = coordinates_offset_res.to(unit_out).value

    ndim = len(csdm_new.dimensions)

    if dimension_object._complex_fft:
        scale_factor = 1.0 if np.isfinite(dimension_object.reciprocal.period) else 2.0
        phase = np.exp(2j * np.pi * coordinates_offset_res * coordinates)
        phase_grid = _get_broadcast_shape(phase, ndim, axis=index)
        for item in csdm_new.dependent_variables:
            comp_shape_len = len(item.subtype._components.shape)
            slice_ = get_cross_section_slice(index, comp_shape_len)

            phased_signal = item.subtype._components * phase_grid
            ft_shift = sp.fft.ifftshift(phased_signal, axes=index)
            signal_ft = sp.fft.ifft(ft_shift, axis=index)
            signal_ft[slice_] *= scale_factor

            item.subtype._components = signal_ft
        dimension_object._complex_fft = False

    else:  # FFT is false
        scale_factor = 1.0 if np.isfinite(dimension_object.period) else 2.0
        phase = np.exp(-2j * np.pi * coordinates_offset * coordinates_res)
        phase_grid = _get_broadcast_shape(phase, ndim, axis=index)
        for item in csdm_new.dependent_variables:
            comp_shape_len = len(item.subtype._components.shape)
            slice_ = get_cross_section_slice(index, comp_shape_len)

            item.subtype._components[slice_] /= scale_factor

            ft = sp.fft.fft(item.subtype._components, axis=index)
            ft_shift = sp.fft.fftshift(ft, axes=index)
            signal_ft = ft_shift * phase_grid

            item.subtype._components = signal_ft
        dimension_object._complex_fft = True

    # get the coordinates of the reciprocal dimension.
    dimension_object._swap()
    dimension_object._increment = dimension_object.reciprocal_increment()
    dimension_object._get_coordinates()
    return csdm_new


def get_cross_section_slice(index, size):
    """Return a slice object for a size dimensional dataset at index `index`."""
    slc = [
        slice(None, 1, None) if i == -index - 1 else slice(None) for i in range(size)
    ]
    return tuple(slc[::-1])


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

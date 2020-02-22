# -*- coding: utf-8 -*-
# import numpy as np
# def _get_broadcast_shape(array, ndim, axis):
#     """Return the broadcast array for numpy ndarray operations."""
#     s = [None for i in range(ndim)]
#     s[axis] = slice(None, None, None)
#     return array[tuple(s)]
#
# def _check_dimension_indices(d, index=-1):
#     """
#         Check the list of indexes to ensure that each index is an integer
#         and within the counts of dimensions.
#     """
#     index = deepcopy(index)
#     def _correct_index(i, d):
#         if not isinstance(i, int):
#             raise TypeError(f"{message}, found {type(i)}")
#         if i < 0:
#             i += d
#         if i > d:
#             raise IndexError(
#                 f"The `index` {index} cannot be greater than the total number of "
#                 f"dimensions, {d}."
#             )
#         return -1 - i
#     message = "Index/Indices are expected as integer(s)"
#     if isinstance(index, tuple):
#         index = list(index)
#     if isinstance(index, (list, np.ndarray)):
#         for i, item in enumerate(index):
#             index[i] = _correct_index(item, d)
#         return tuple(index)
#     elif isinstance(index, int):
#         return tuple([_correct_index(index, d)])
#     else:
#         raise TypeError(f"{message}, found {type(i)}")
#
# def fft(self, dimension=0):
#     """
#     Perform a FFT along the along the given dimension `dimensions`.
#     Needs debugging.
#     """
#     index = self._check_dimension_indices(len(self.dimensions), dimension)[0]
#     # for index in indexes:
#     if self.dimensions[index].type != "linear":
#         raise NotImplementedError(
#             f"The FFT method is not available for Dimension objects with "
#             f"subtype, {self.dimensions[index].type}."
#         )
#     dimension_object = self.dimensions[index].subtype
#     unit_in = dimension_object._unit
#     # compute the reciprocal increment using Nyquist-shannan theorem.
#     _reciprocal_increment = 1.0 / (
#         dimension_object._count * dimension_object._increment
#     )
#     # swap the values of object with the respective reciprocal object.
#     dimension_object._swap()
#     unit = dimension_object._unit
#     dimension_object._increment = _reciprocal_increment.to(unit)
#     ndim = len(self.dimensions)
#     # calculate the phase that will be applied to the fft amplitudes.
#     reciprocal_coordinates = dimension_object.reciprocal._coordinates_offset.to(
#         unit_in
#     ).value
#     coordinates = dimension_object._coordinates.to(unit).value
#     phase = np.exp(2j * np.pi * reciprocal_coordinates * coordinates)
#     phase_grid = _get_broadcast_shape(phase, ndim, axis=index)
#     # phase_grid = 1
#     # toggle the value of the complex_fft attribute
#     if dimension_object._complex_fft:
#         for item in self.dependent_variables:
#             signal_ft = np.fft.ifft(
#                 np.fft.ifftshift(item.subtype._components, axes=index) * phase_grid,
#                 axis=index,
#             )
#             item.subtype._components = signal_ft
#         dimension_object._complex_fft = False
#     else:  # FFT is false
#         for item in self.dependent_variables:
#             signal_ft = np.fft.fftshift(
#                 np.fft.fft(item.subtype._components, axis=index) * phase_grid,
#                 axes=index,
#             )
#             item.subtype._components = signal_ft
#         dimension_object._complex_fft = True
#     # for item in self.dependent_variables:
#     #     signal_ft = fftshift(
#     #         fft(item.subtype._components, axis=index) * phase_grid, axes=-index - 1
#     #     )
#     #     item.subtype._components = signal_ft
#     # get the coordinates of the reciprocal dimension.
#     dimension_object._get_coordinates()
#     # self.dimensions[index].gcv._reciprocal()
#     # self._toggle_complex_fft(self.dimensions[index])
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

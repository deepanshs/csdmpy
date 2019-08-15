# -*- coding: utf-8 -*-
"""CSDM."""
from __future__ import division
from __future__ import print_function

import datetime
import json
import warnings
from copy import deepcopy

import numpy as np
from numpy.fft import fft
from numpy.fft import fftshift
from numpy.fft import ifft
from numpy.fft import ifftshift

from csdmpy.dependent_variables import DependentVariable
from csdmpy.dimensions import Dimension
from csdmpy.utils import validate
from csdmpy.version import __version__


__all__ = ["CSDM"]


class CSDM:
    r"""
    Create an instance of a CSDM class.

    This class is based on the root CSDM object of the core scientific dataset
    (CSD) model. The class is a composition of the :ref:`dv_api` and
    :ref:`dim_api` instances, where an instance of the :ref:`dv_api` class
    describes a :math:`p`-component dependent variable, and an instance of the
    :ref:`dim_api` class describes a dimension of a :math:`d`-dimensional
    space. Additional attributes of this class is listed below.
    """

    __latest_CSDM_version__ = "1.0"  # __version__
    _old_compatible_versions = ()
    _old_incompatible_versions = ("0.0.9", "0.0.10", "0.0.11")

    __slots__ = [
        "_dimensions",
        "_dependent_variables",
        "_tags",
        "_read_only",
        "_version",
        "_timestamp",
        "_geographic_coordinate",
        "_description",
        "_application",
        "_filename",
    ]

    def __init__(self, filename="", version=None, description=""):
        """Python module from reading and writing csdm files."""
        if version is None:
            version = self.__latest_CSDM_version__
        elif version in self._old_incompatible_versions:
            raise Exception(
                (
                    "Files created with version {0} of the CSD Model "
                    "are no longer supported."
                ).format(version)
            )

        self._dependent_variables = ()
        self._dimensions = ()
        self._tags = []
        self._read_only = False
        self._version = version
        self._timestamp = ""
        self._geographic_coordinate = {}
        self._description = description
        self._application = {}
        self._filename = filename

    # ----------------------------------------------------------------------- #
    #                                Attributes                               #
    # ----------------------------------------------------------------------- #
    @property
    def dependent_variables(self):
        """Tuple of :ref:`dv_api` instances."""
        return self._dependent_variables

    @property
    def dimensions(self):
        """Tuple of :ref:`dim_api` instances."""
        return self._dimensions

    @property
    def tags(self):
        """List of tags attached to the dataset."""
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = validate(value, "tags", list)

    @property
    def read_only(self):
        """
        If True, the data-file is serialized as read only, otherwise, False.

        By default, the :ref:`csdm_api` object loads a copy of the .csdf(e)
        file, irrespective of the value of the `read_only` attribute.
        The value of this attribute may be toggled at any time after the file
        import.
        When serializing the `.csdf(e)` file, if the value of the `read_only`
        attribute is found True, the file will be serialized as read only.
        """
        return deepcopy(self._read_only)

    @read_only.setter
    def read_only(self, value):
        self._read_only = validate(value, "read_only", bool)

    @property
    def version(self):
        """Version number of the CSD model on file."""
        return deepcopy(self._version)

    @property
    def timestamp(self):
        """
        Timestamp from when the file was last serialized.

        The timestamp stamp is a string representation of the Coordinated
        Universal Time (UTC) formatted according to the iso-8601 standard.

        Raises:
            AttributeError: When the attribute is modified.
        """
        return deepcopy(self._timestamp)

    @property
    def geographic_coordinate(self):
        """
        Geographic coordinate, if present, from where the file was last serialized.

        The geographic coordinates correspond to the location where the file was last
        serialized. If present, the geographic coordinates are described with three
        attributes, the required latitude and longitude, and an optional altitude.

        Raises:
            AttributeError: When the attribute is modified.
        """
        return deepcopy(self._geographic_coordinate)

    @property
    def description(self):
        """Description of the dataset.

        The default value is an empty string, ''.

        Example:
            >>> print(data.description)
            A simulated sine curve.

        Returns:
            A string of UTF-8 allows characters describing the dataset.

        Raises:
            TypeError: When the assigned value is not a string.
        """
        return self._description

    @description.setter
    def description(self, value):
        self._description = validate(value, "description", str)

    @property
    def application(self):
        """
        Application metadata dictionary of the CSDM object.

        .. doctest::

            >>> print(data.application)
            {}

        By default, the application attribute is an empty dictionary, that is,
        the application metadata stored by the previous application is ignored
        upon file import.

        The application metadata may, however, be retained with a request via
        the :meth:`~csdmpy.load` method. This feature may be useful to related
        applications where application metadata might contain additional information.
        The attribute may be updated with a python dictionary.

        The application attribute is where an application can place its own
        metadata as a python dictionary object containing application specific
        metadata, using a reverse domain name notation string as the attribute
        key, for example,

        Example:
            >>> data.application = {
            ...     "com.example.myApp" : {
            ...         "myApp_key": "myApp_metadata"
            ...      }
            ... }
            >>> print(data.application)
            {'com.example.myApp': {'myApp_key': 'myApp_metadata'}}

        Returns:
            Python dictionary object with the application metadata.
        """
        return deepcopy(self._application)

    @application.setter
    def application(self, value):
        self._application = validate(value, "application", dict)

    @property
    def filename(self):
        """Local file address of the current file. """
        return self._filename

    @property
    def data_structure(self):
        r"""
        Json serialized string describing the CSDM class instance.

        The data_structure attribute is only intended for a quick preview of
        the dataset. This JSON serialized string from this attribute avoids
        displaying large datasets. Do not use the value of this attribute to
        save the data to a file, instead use the :meth:`~csdmpy.CSDM.save`
        methods of the instance.

        Raises:
            AttributeError: When modified.
        """
        dictionary = self._get_python_dictionary(self.filename, print_function=True)

        return json.dumps(dictionary, ensure_ascii=False, sort_keys=False, indent=2)

    # ----------------------------------------------------------------------- #
    #                                  Methods                                #
    # ----------------------------------------------------------------------- #

    def _reshape(self, shape):
        r"""
        Reshapes the components array.

        The array is reshaped to :math:`(p \times N_{d-1} \times ... N_1 \times N_0)`
        where :math:`p` is the number of components and :math:`N_k` is the number of
        points along the :math:`k^\mathrm{th}` dimension.
        """
        for item in self.dependent_variables:
            item = item.subtype
            sub_shape = (item.quantity_type.p,) + tuple(shape)
            dtype = item.numeric_type.dtype

            grid_points = np.asarray(sub_shape).prod()
            components_size = item._components.size

            if grid_points != components_size and item._sparse_sampling == {}:
                warnings.warn(
                    (
                        f"The number of elements in the components array, "
                        f"{components_size}, is not consistent with the total "
                        f"number of grid points, {grid_points}."
                    )
                )
            if item._sparse_sampling == {}:
                item._components = np.asarray(
                    item._components[:, :grid_points].reshape(sub_shape), dtype=dtype
                )
            else:
                item._components = self.fill_sparse_space(item, sub_shape, dtype)

    def fill_sparse_space(self, item, shape, dtype):
        """Fill sparse grid using numpy broadcasting."""
        components = np.zeros(shape, dtype=dtype)
        sparse_dimensions_indexes = item._sparse_sampling._sparse_dimensions_indexes
        sgs = item._sparse_sampling._sparse_grid_vertexes.size
        grid_vertexes = item._sparse_sampling._sparse_grid_vertexes.reshape(
            int(sgs / len(sparse_dimensions_indexes)), len(sparse_dimensions_indexes)
        ).T

        vertexes = [slice(None) for i in range(len(shape))]
        for i, sparse_index in enumerate(sparse_dimensions_indexes):
            vertexes[sparse_index] = grid_vertexes[i]

        vertexes = tuple(vertexes[::-1])
        _new_shape = components[vertexes].shape

        components[vertexes] = item.components.reshape(_new_shape)
        return components

    def add_dimension(self, *args, **kwargs):
        """
        Add a new :ref:`dim_api` instance to the :ref:`csdm_api` instance.

        There are three ways to add a new independent variable.

        *From a python dictionary containing valid keywords.*

        .. doctest::

            >>> import csdmpy as cp
            >>> datamodel = cp.new()
            >>> py_dictionary = {
            ...     'type': 'linear',
            ...     'increment': '5 G',
            ...     'count': 50,
            ...     'coordinates_offset': '-10 mT'
            ... }
            >>> datamodel.add_dimension(py_dictionary)

        *From a list of valid keyword arguments.*

        .. doctest::

            >>> datamodel.add_dimension(
            ...     type = 'linear',
            ...     increment = '5 G',
            ...     count = 50,
            ...     coordinates_offset = '-10 mT'
            ... )

        *From an* :ref:`dim_api` *instance.*

        .. doctest::

            >>> from csdmpy import Dimension
            >>> datamodel = cp.new()
            >>> var1 = Dimension(type = 'linear',
            ...                  increment = '5 G',
            ...                  count = 50,
            ...                  coordinates_offset = '-10 mT')
            >>> datamodel.add_dimension(var1)
            >>> print(datamodel.data_structure)
            {
              "csdm": {
                "version": "1.0",
                "dimensions": [
                  {
                    "type": "linear",
                    "count": 50,
                    "increment": "5.0 G",
                    "coordinates_offset": "-10.0 mT",
                    "quantity_name": "magnetic flux density"
                  }
                ],
                "dependent_variables": []
              }
            }

        For the last method, the instance ``var1`` is added to the
        ``datamodel`` as a reference, `i.e.`, if the instance ``var1`` is
        destroyed, the ``datamodel`` instance will become corrupt. As a
        recommendation always pass a copy of the :ref:`dim_api` instance to the
        :meth:`~csdmpy.csdm.CSDM.add_dimension` method. We provide
        the later alternative for it is useful for copying an :ref:`dim_api`
        instance from one :ref:`csdm_api` instance to another.
        """
        if args != () and isinstance(args[0], Dimension):
            self._dimensions += (args[0],)
        else:
            self._dimensions += (Dimension(*args, **kwargs),)

    def add_dependent_variable(self, *args, **kwargs):
        """
        Add a new :ref:`dv_api` instance to the :ref:`csdm_api` instance.

        There are again three ways to add a new dependent variable instance.

        *From a python dictionary containing valid keywords.*

        .. doctest::

            >>> import numpy as np

            >>> datamodel = cp.new()

            >>> numpy_array = (100*np.random.rand(3,50)).astype(np.uint8)
            >>> py_dictionary = {
            ...     'type': 'internal',
            ...     'components': numpy_array,
            ...     'name': 'star',
            ...     'unit': 'W s',
            ...     'quantity_name': 'energy',
            ...     'quantity_type': 'pixel_3'
            ... }
            >>> datamodel.add_dependent_variable(py_dictionary)

        *From a list of valid keyword arguments.*

        .. doctest::

            >>> datamodel.add_dependent_variable(type='internal',
            ...                                  name='star',
            ...                                  unit='W s',
            ...                                  quantity_type='pixel_3',
            ...                                  components=numpy_array)

        *From a* :ref:`dv_api` *instance.*

        .. doctest::

            >>> from csdmpy import DependentVariable
            >>> var1 = DependentVariable(type='internal',
            ...                          name='star',
            ...                          unit='W s',
            ...                          quantity_type='pixel_3',
            ...                          components=numpy_array)
            >>> datamodel.add_dependent_variable(var1)

        If passing a :ref:`dv_api` instance, as a general recommendation,
        always pass a copy of the DependentVariable instance to the
        :meth:`~csdmpy.csdm.CSDM.add_dependent_variable` method. We provide
        the later alternative as it is useful for copying a DependentVariable
        instance from one :ref:`csdm_api` instance to another.
        """
        if args != () and isinstance(args[0], DependentVariable):
            self._dependent_variables += (args[0],)
        else:
            self._dependent_variables += (
                DependentVariable(filename=self.filename, *args, **kwargs),
            )
        self._dependent_variables[-1].encoding = "base64"
        self._dependent_variables[-1].type = "internal"

    def _get_python_dictionary(
        self, filename, print_function=False, version=__latest_CSDM_version__
    ):
        """Return the CSDM instance as a python dictionary."""
        dictionary = {}

        dictionary["version"] = self.version

        if self.read_only:
            dictionary["read_only"] = self.read_only

        if self.timestamp != "":
            dictionary["timestamp"] = self.timestamp

        if self.geographic_coordinate != {}:
            dictionary["geographic_coordinate"] = self.geographic_coordinate

        if self.tags != []:
            dictionary["tags"] = self.tags

        if self.description.strip() != "":
            dictionary["description"] = self.description
        dictionary["dimensions"] = []
        dictionary["dependent_variables"] = []

        for i in range(len(self.dimensions)):
            dictionary["dimensions"].append(self.dimensions[i]._get_python_dictionary())

        _length_of_dependent_variables = len(self.dependent_variables)
        for i in range(_length_of_dependent_variables):
            dictionary["dependent_variables"].append(
                self.dependent_variables[i]._get_python_dictionary(
                    filename=filename,
                    dataset_index=i,
                    for_display=print_function,
                    version=self.__latest_CSDM_version__,
                )
            )

        csdm = {}
        csdm["csdm"] = dictionary
        return csdm

    def save(
        self,
        filename="",
        read_only=False,
        version=__latest_CSDM_version__,
        output_device=None,
    ):
        """
        Serialize the :ref:`CSDM_api` instance as a JSON data-exchange file.

        The serialized file is saved with two file extensions.
        When every instance of the DependentVariable class from the CSDM
        instance has an `internal` subtype, the corresponding CSDM instance is
        serialized with a `.csdf` file extension.
        If any single DependentVariable instance has an `external` subtype, the
        CSDM instance is serialized with a `.csdfe` file extension.
        We use the two different file extensions to alert the end use of the
        possible deserialization error associated with the `.csdfe` file
        extensions when the external data file is inaccessible.

        .. Important::
            Irrespective of the subtypes from the serialized JSON file, by default,
            all instances of DependentVariable class are assigned an `internal`
            subtype upon import with `base64` as the value of the `encoding` attribute.
            The user may, however, change these attribute at any time after the
            file import and before serializing to a file.

        Args:
            filename (str): The filename of the serialized file.
            read_only (bool): If true, the file is serialized as read_only.
            version (str): The file is serialized with the given CSD model version.
            output_device(object): Object where the data is written.

        Example:
            >>> data.save('my_file.csdf')

        .. testcleanup::
            import os
            os.remove('my_file.csdf')
        """
        dictionary = self._get_python_dictionary(filename, version=version)

        timestamp = datetime.datetime.utcnow().isoformat()[:-7] + "Z"
        dictionary["csdm"]["timestamp"] = timestamp

        if read_only:
            dictionary["csdm"]["read_only"] = read_only

        if output_device is None:
            with open(filename, "w", encoding="utf8") as outfile:
                json.dump(
                    dictionary,
                    outfile,
                    ensure_ascii=False,
                    sort_keys=False,
                    indent=2,
                    allow_nan=False,
                )
        else:
            json.dump(
                dictionary,
                output_device,
                ensure_ascii=False,
                sort_keys=False,
                indent=2,
                allow_nan=False,
            )

    def copy(self):
        """
        Create a copy of the current CSDM instance.

        Returns:
            A CSDM instance.
        """
        return deepcopy(self)

    # def replace(self,
    #             controlled_variable=None,
    #             cv_index=-1,
    #             uncontrolled_variable=None,
    #             uv_index=-1):
    #     """
    #     Replace the controlled or the uncontrolled variable at the index.

    #     :params: controlled_variable: A new ControlledVariable object or a
    #         python dictionary corresponding to a new ControlledVariable
    #         object.
    #     :params: cv_index: An integer corresponding to the
    #         UncontrolledVariable object to the updated.
    #     :params: uncontrolled_variable: A new UncontrolledVariable object or
    #         a python dictionary corresponding to a new UncontrolledVariable
    #         object.
    #     :params: uv_index: An integer corresponding to the
    #         UncontrolledVariable object to the updated.

    #     .. todo::
    #         Well, write the method.
    #     """
    #     pass

    def _check_dimension_indices(self, index=-1):
        def _correct_index(i):
            if not isinstance(i, int):
                raise TypeError(message)
            if i < 0:
                i += d
            if i > d - 1:
                raise ValueError(
                    (
                        "`index` {0} cannot be greater than the number of "
                        "independent variables, {1}."
                    ).format(index, d)
                )
            return -1 - i

        message = "Index/Indices are expected as integer(s)."

        d = len(self.dimensions)

        if isinstance(index, (tuple, list, np.ndarray)):
            for i, item in enumerate(index):
                index[i] = _correct_index(item)
            return index

        elif isinstance(index, int):
            return [_correct_index(index)]

        else:
            raise TypeError(message)

    def _get_new_csdmodel_object(self, func, index):
        index = self._check_dimension_indices(index)
        new = CSDM()
        for variable in self.dependent_variables:
            y = func(variable.components, axis=index)
            new.add_dependent_variable(
                components=y,
                name=variable.name,
                quantity_name=variable.quantity_name,
                encoding=variable.encoding,
                numeric_type=variable.numeric_type,
                quantity_type=variable.quantity_type,
                component_labels=variable.component_labels,
                components_uri=variable.components_uri,
            )
        for i, variable in enumerate(self.dimensions):
            if i not in index[0]:
                new.add_dimension(variable)
        return new

    def sum(self, dimensions=0):
        """
        Sum of the component values along the given dimension `dimensions`.

        Args:
            dimensions: An integer or tuple of `m` integers cooresponding to the
                        index/indices of dimensions along which the sum of the
                        dependent variables component values are performed.

        Return:
            A CSDM object with `d-m` dimensions where `d` is the
            number of dimensions in the original csdm data.
        """
        func = np.sum
        return self._get_new_csdmodel_object(func, dimensions)

    def prod(self, dimensions=0):
        """
        Product of the component values along the given dimension `dimensions`.

        Args:
            dimensions: An integer or tuple of `m` integers cooresponding to the
                        index/indices of dimensions along which the product of the
                        dependent variables component values are performed.

        Return:
            A CSDM object with `d-m` dimensions where `d` is the number of
            dimensions in the original csdm dataset.
        """
        func = np.prod
        return self._get_new_csdmodel_object(func, dimensions)

    def fft(self, dimensions=0):
        """
        Perform a FFT along the along the given dimension `dimensions`.

        Needs debugging.
        """
        indexes = self._check_dimension_indices(dimensions)

        for index in indexes:
            if self.dimensions[index].type != "linear":
                raise NotImplementedError(
                    "FFT is available for dimensions with type 'linear'."
                )

            dimension_object = self.dimensions[index].subtype
            unit_in = dimension_object._unit
            # swap the values of object with the respective reciprocal object.
            dimension_object._swap()

            # compute the reciprocal increment using Nyquist-shannan theorem.
            _reciprocal_increment = 1.0 / (
                dimension_object._count * dimension_object._increment
            )

            unit = dimension_object._unit
            dimension_object._increment = _reciprocal_increment.to(unit)

            # get the coordinates of the reciprocal dimension.
            dimension_object._get_coordinates()

        ndim = len(self.dimensions)

        # toggle the value of the complex_fft attribute
        if dimension_object._complex_fft:
            phase = np.exp(
                2j
                * np.pi
                * dimension_object.reciprocal._coordinates_offset.to(unit_in).value
                * dimension_object._coordinates.to(unit).value
            )
            for i in range(len(self.dependent_variables)):
                signal_ft = ifft(
                    ifftshift(
                        self.dependent_variables[i].subtype._components, axes=index
                    )
                    * get_broadcase_shape(phase, ndim, axis=index),
                    axis=index,
                )
                self.dependent_variables[i].subtype._components = signal_ft
            dimension_object._complex_fft = False
        else:  # FFT is false
            # calculate the phase that will be applied to the fft amplitudes.
            phase = np.exp(
                2j
                * np.pi
                * dimension_object.reciprocal._coordinates_offset.to(unit_in).value
                * dimension_object._coordinates.to(unit).value
            )
            for i in range(len(self.dependent_variables)):
                signal_ft = fftshift(
                    fft(self.dependent_variables[i].subtype._components, axis=index)
                    * get_broadcase_shape(phase, ndim, axis=index),
                    axes=index,
                )
                self.dependent_variables[i].subtype._components = signal_ft
            dimension_object._complex_fft = True

        for i in range(len(self.dependent_variables)):
            signal_ft = fftshift(
                fft(self.dependent_variables[i].subtype._components, axis=index)
                * get_broadcase_shape(phase, ndim, axis=index),
                axes=-index - 1,
            )

            self.dependent_variables[i].subtype._components = signal_ft

        # self.dimensions[index].gcv._reciprocal()
        # self._toggle_complex_fft(self.dimensions[index])


#     def __add__(self, other):
#         """
#         Add two CSDM instances.

#         We follow a safe rule---the addition of two CSDM instances
#         will only be successfull when the attributes of the corresponding
#         ControlledVariable instances are identical.
#         """
#         if not _compare_cv_objects(self, other):
#             raise Exception("Cannot add")

#         dim1 = len(self.dependent_variables)
#         dim2 = len(other.dependent_variables)

#         if dim1 != dim2:
#             raise Exception(
#                 (
#                     "Cannot add {0} and {1}. They have differnet "
#                     "number of uncontrolled variables."
#                 ).format(self.__class__.__name__, other.__class__.__name__)
#             )

#         d1 = deepcopy(self)
#         for i in range(dim1):
#             if _compare_uv(
#                 self.dependent_variables[i],
#                 other.dependent_variables[i]
#             ):
#                 d1.dependent_variables[i].components += \
#                     other.dependent_variables[i].components

#         return d1

#     def __sub__(self, other):
#         """
#         Subtract two CSDM instances.

#         We follow a safe rule---the subtraction of two CSDM instances
#         will only be successfull when the attributes of the corresponding
#         ControlledVariable instances are identical.
#         """
#         pass

#     def __mul__(self, other):
#         """
#         Multiply two CSDM instances.

#         We follow a safe rule---the multiplication of two CSDM instances
#         will only be successfull when the attributes of the corresponding
#         ControlledVariable instances are identical.
#         """
#         pass

#     def __div__(self, other):
#         """
#         Divide two CSDM instances.

#         We follow a safe rule---the division of two CSDM instances
#         will only be successfull when the attributes of the corresponding
#         ControlledVariable instances are identical.
#         """
#         pass


def get_broadcase_shape(array, ndim, axis):
    """Return the broadcast array for numpy ndarray operations."""
    s = [None for i in range(ndim)]
    s[axis] = slice(None, None, None)
    return array[tuple(s)]


# def _compare_cv_object(cv1, cv2):
#     if cv1.gcv._getparams == cv2.gcv._getparams:
#         return True
#     return False


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


# def _compare_uv_objects(object1, object2):
#     dim1 = len(object1.dependent_variables)
#     dim2 = len(object2.dependent_variables)

#     for j in range(dim1):
#         for i in range(dim2):
#             a = _compare_uv(
#                 object1.dependent_variables[i],
#                 object2.dependent_variables[j]
#             )

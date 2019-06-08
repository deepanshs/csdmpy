# -*- coding: utf-8 -*-
"""CSDModel."""
from __future__ import division
from __future__ import print_function

import json
from copy import deepcopy
from os import listdir
from os.path import isdir
from urllib.parse import urlparse

import numpy as np
from numpy.fft import fft
from numpy.fft import fftshift

from ._utils_download_file import _download_file_from_url
from ._version import __version__
from .dependent_variable import DependentVariable
from .dimensions import Dimension


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__version__ = __version__


def _import_json(filename):
    res = urlparse(filename)
    if res[0] not in ["file", ""]:
        filename = _download_file_from_url(filename)
    with open(filename, "rb") as f:
        content = f.read()
        return json.loads(str(content, encoding="UTF-8"))


def load(filename=None, application=False):
    r"""
    Load a .csdf/.csdfe file and return an instance of :ref:`csdm_api` class.

    The file must be a JSON serialization of the CSD Model.

    .. doctest::

        >>> data1 = cp.load('local_address/file.csdf') # doctest: +SKIP
        >>> data2 = cp.load('url_address/file.csdf') # doctest: +SKIP

    :params: filename: A local or remote address to the `.csdf or
                        `.csdfe` file.
    :returns: A ``CSDModel`` instance.
    """
    if filename is None:
        raise Exception("'open' method requires a data file address.")

    if isdir(filename) and filename.endswith(".csdm"):
        csdm_files = [
            f
            for f in listdir(filename)
            if f.endswith(".csdf") or f.endswith(".csdfe")
        ]
        if len(csdm_files) != 1:
            raise Exception(
                ("More that one csdf(e) files encountered in the .csdm folder")
            )
        csd_file = csdm_files[0]
    else:
        csd_file = filename

    return _load(csd_file, application=application)
    # csdm_objects = []
    # for file_ in csdm_files:
    #     csdm_objects.append(_load(file_, application=application))
    #     return csdm_objects


def _load(filename, application=False):
    try:
        dictionary = _import_json(filename)
    except Exception as e:
        raise Exception(e)

    key_list_root = dictionary.keys()

    # ----------------------------------------------------------------------- #
    # Create the CSDModel and populate the attributes
    # ----------------------------------------------------------------------- #

    if "CSDM" in key_list_root:
        raise KeyError("'CSDM' is not a valid keyword. Dit you mean 'csdm'?")

    if "csdm" not in key_list_root:
        raise KeyError("'csdm' key is not present.")

    _version = dictionary["csdm"]["version"]
    # is version required?

    key_list_CSDM = dictionary["csdm"].keys()

    csdm = CSDModel(filename, _version)

    if "dimensions" in key_list_CSDM:
        for dim in dictionary["csdm"]["dimensions"]:
            csdm.add_dimension(dim)

    if "dependent_variables" in key_list_CSDM:
        for dat in dictionary["csdm"]["dependent_variables"]:
            csdm.add_dependent_variable(dat)

    if "description" in key_list_CSDM:
        csdm.description = dictionary["csdm"]["description"].strip()

    npts = [item.number_of_points for item in csdm.dimensions]
    if npts != []:
        csdm._reshape(npts[::-1])

    # Create the augmentation layer model #
    if "read_only" in key_list_root:
        csdm._read_only = dictionary["read_only"]

    if "timestamp" in key_list_root:
        csdm._timestamp = dictionary["timestamp"]

    if "geographic_coordinate" in key_list_root:
        csdm._geographic_coordinate = dictionary["geographic_coordinate"]

    if application:
        if "application" in key_list_root:
            csdm._application = dictionary["application"]
    else:
        csdm._application = {}

    return csdm


def new(description=""):
    r"""
    Return a new instance of :ref:`csdm_api` class containing a 0D{0} dataset.

    Optionally, a description may be provided as an argument to this method,
    for example,

    .. doctest::

        >>> import csdfpy as cp
        >>> emptydata = cp.new(description='Testing Testing 1 2 3')
        >>> print(emptydata.data_structure)
        {
          "csdm": {
            "version": "0.0.11",
            "description": "Testing Testing 1 2 3",
            "dimensions": [],
            "dependent_variables": []
          }
        }

    :returns: A ``CSDModel`` instance
    """
    return CSDModel(description=description)


class CSDModel:
    r"""
    Instantiate a CSDModel class.

    The CSDModel class is based on the core scientific dataset (CSD) model.
    This class is a composition of the :ref:`dv_api` and :ref:`iv_api`
    instances,
    where every instance of the :ref:`dv_api` class is a :math:`p`-component
    independent variable, :math:`y` and every instance of :ref:`iv_api` class
    is a dimension of a :math:`d`-dimensional independent variable space
    :math:`(x_0, x_1, ... x_k, ... x_{d-1})`.

    :returns: A ``CSDModel`` instance.
    """

    __file_version__ = "0.0.11"
    _old_compatible_versions = ()
    _old_incompatible_versions = ("0.0.9", "0.0.10")

    __slots__ = [
        "_dimensions",
        "_dependent_variables",
        "_read_only",
        "_version",
        "_timestamp",
        "_geographic_coordinate",
        "_description",
        "_application",
        "_filename",
        "_persistent",
    ]

    def __init__(self, filename="", version=None, description=""):
        """Python module from reading and writing csdm files."""
        if version is None:
            version = self.__file_version__
        elif version in self._old_incompatible_versions:
            raise Exception(
                (
                    "Files created with version {0} of the CSDModel "
                    "are no longer supported."
                ).format(version)
            )

        self._dependent_variables = ()
        self._dimensions = ()
        self._read_only = False
        self._version = version
        self._timestamp = ""
        self._description = description
        self._geographic_coordinate = ""
        self._application = {}

        self._filename = filename
        self._persistent = {}

    # ----------------------------------------------------------------------- #
    #                                Attributes                               #
    # ----------------------------------------------------------------------- #

    # dependent variables
    @property
    def dependent_variables(self):
        """Return a tuple of the :ref:`dv_api` instances."""
        return self._dependent_variables

    # dimensions
    @property
    def dimensions(self):
        """Return a tuple of the :ref:`iv_api` instances."""
        return self._dimensions

    # read only
    @property
    def read_only(self):
        """
        Return True, if the file is set to read only, otherwise, False.

        By default, the :ref:`csdm` object loads a copy of the csdf/csdfe
        file, and therefore, the default value of the `read_only` attribute is
        always False. This flag may be set to True, at any later time.
        If the value of the `read_only` attribute is True when saving
        the csdf file, the file will be serialized as read only. Alternatively,
        the `read_only` flag may be provided to the :meth:`~csdfpy.save`
        method.
        """
        return deepcopy(self._read_only)

    @read_only.setter
    def read_only(self, value):
        if isinstance(value, bool):
            self._read_only = value
        else:
            raise ValueError(
                (
                    "Expecting a boolean value for the `read_only` attribute,"
                    " found {0}."
                ).format(type(value))
            )

    # version
    @property
    def version(self):
        """
        Return the version number of the :ref:`csdm_api` on file.

        The attribute cannot be modified.
        """
        return deepcopy(self._version)

    # timestamp
    @property
    def timestamp(self):
        """
        Return the timestamp when the CSDM file was last serialized.

        The timestamp stamp is a string representation of the Coordinated
        Universal Time (UTC) formatted according to the iso-8601 standard.

        The attribute cannot be modified.
        """
        return deepcopy(self._timestamp)

    # geographic coordinate
    @property
    def geographic_coordinate(self):
        """
        Return the geographic coordinate, if present.

        The geographic coordinates correspond to the location where the CSDM
        file was last serialized.
        The geographic coordinates are described with three attributes,
        the required latitude and longitude, and an optional altitude.


        The attribute cannot be modified.
        """
        return deepcopy(self._geographic_coordinate)

    # description
    @property
    def description(self):
        """
        Return a string with the description of the datasets.

        The default value is an empty string, ''.

        .. doctest::

            >>> print(data.description)
            Just another test


        :returns: A ``string`` with UTF-8 allows characters.
        :raises ValueError: When the non-string value is assigned.
        """
        return self._description

    @description.setter
    def description(self, value):
        if isinstance(value, str):
            self._description = value
        else:
            raise ValueError(
                (
                    "Expecting a string value for the `description` attribute"
                    " found {0}."
                ).format(type(value))
            )

    @property
    def application(self):
        """
        Return an application dictionary, if present.

        By default, the application attribute is an empty dictionary, that is,
        the application metadata stored by the previous application is ignored
        upon file import.

        The application metadata may, however, be retained with a request via
        the :meth:`~csdfpy.load` method. This feature may be useful
        to related applications where application metadata might
        contain additional information.

        This attribute may be updated with a python dictionary, for example,

        .. doctest::

            >>> data.application = {
            ...     "com.reverse.domain": {
            ...         "my_key": "my_metadata"
            ...     }
            ... }
        """
        return deepcopy(self._application)

    @application.setter
    def application(self, value):
        if isinstance(value, dict):
            self._application = value
        else:
            raise ValueError(
                (
                    "Expecting a dictionary object for the `application` "
                    "attribute, found {0}."
                ).format(type(value))
            )

    # filename of the current file
    @property
    def filename(self):
        """
        Return the local file address of the current JSON file.

        The file extensions includes the `.csdf` and the `.csdfe` files.
        """
        return self._filename

    # data structure
    @property
    def data_structure(self):
        r"""
        Return the :ref:`csdm_api` instance as a JSON serialization.

        The data_structure attribute is only intended for a quick preview of
        the dataset. This JSON serialized output from this attribute avoids
        displaying large datasets. Do not use the value of this attribute to
        save the data to a file, instead use the :meth:`~csdfpy.CSDModel.save`
        methods of the instance.

        The attribute cannot be modified.

        :raises AttributeError: When modified.
        """
        dictionary = self._get_python_dictionary(
            self.filename, print_function=True
        )

        return json.dumps(
            dictionary, ensure_ascii=False, sort_keys=False, indent=2
        )

    # ----------------------------------------------------------------------- #
    #                              Private methods                            #
    # ----------------------------------------------------------------------- #

    def _reshape(self, shape):
        r"""
        Reshapes the components array.

        The array is reshaped to
        :math:`(p \times N_{d-1} \times ... N_1 \times N_0)` where :math:`p`
        is the number of components and :math:`N_k` is the number of points
        sampled along the :math:`k^\mathrm{th}` independent variable.
        """
        for item in self.dependent_variables:
            _item = item.subtype
            _shape = (_item.quantity_type._p,) + tuple(shape)
            _nptype = _item.numeric_type._nptype

            # print(_item._sparse_sampling)
            if _item._sparse_sampling == {}:
                _item._components = np.asarray(
                    _item._components.reshape(_shape), dtype=_nptype
                )
            else:
                _item._components = self.fill_sparse_space(
                    _item, _shape, _nptype
                )

    def fill_sparse_space(self, _item, _shape, _nptype):
        """Fill sparse grid using numpy broadcasting."""
        _components = np.zeros(_shape, dtype=_nptype)
        _sparse_dimensions = _item._sparse_sampling._sparse_dimensions
        sgs = _item._sparse_sampling._sparse_grid_vertexes.size
        _grid_vertexes = _item._sparse_sampling._sparse_grid_vertexes.reshape(
            int(sgs / len(_sparse_dimensions)), len(_sparse_dimensions)
        ).T

        vertexes = [slice(None) for i in range(len(_shape))]
        for i, sparse_index in enumerate(_sparse_dimensions):
            vertexes[sparse_index] = _grid_vertexes[i]

        vertexes = tuple(vertexes[::-1])
        _new_shape = _components[vertexes].shape

        _components[vertexes] = _item.components.reshape(_new_shape)
        return _components

    # ----------------------------------------------------------------------- #
    #                              Public methods                             #
    # ----------------------------------------------------------------------- #

    def add_dimension(self, *arg, **kwargs):
        """
        Add a new :ref:`iv_api` instance to the :ref:`csdm_api` instance.

        There are three ways to add a new independent variable.

        *From a python dictionary containing valid keywords.*

        .. doctest::

            >>> import csdfpy as cp

            >>> datamodel = cp.new()
            >>> py_dictionary = {
            ...     'type': 'linear',
            ...     'increment': '5 G',
            ...     'number_of_points': 50,
            ...     'index_zero_value': '-10 mT'
            ... }
            >>> datamodel.add_dimension(py_dictionary)

        *From a list of valid keyword arguments.*

        .. doctest::

            >>> datamodel.add_dimension(
            ...     type = 'linear',
            ...     increment = '5 G',
            ...     number_of_points = 50,
            ...     index_zero_value = '-10 mT'
            ... )

        *From an* :ref:`iv_api` *instance.*

        .. doctest::

            >>> from csdfpy import Dimension
            >>> datamodel = cp.new()
            >>> var1 = Dimension(type = 'linear',
            ...                  increment = '5 G',
            ...                  number_of_points = 50,
            ...                  index_zero_value = '-10 mT')
            >>> datamodel.add_dimension(var1)
            >>> print(datamodel.data_structure)
            {
              "csdm": {
                "version": "0.0.11",
                "dimensions": [
                  {
                    "type": "linear",
                    "number_of_points": 50,
                    "increment": "5.0 G",
                    "index_zero_value": "-10.0 mT",
                    "quantity": "magnetic flux density"
                  }
                ],
                "dependent_variables": []
              }
            }

        For the last method, the instance ``var1`` is added to the
        ``datamodel`` as a reference, `i.e.`, if the instance ``var1`` is
        destroyed, the ``datamodel`` instance will become corrupt. As a
        recommendation always pass a copy of the :ref:`iv_api` instance to the
        :meth:`~csdfpy.CSDModel.add_dimension` method. We provide
        the later alternative for it is useful for copying an :ref:`iv_api`
        instance from one :ref:`csdm_api` instance to another.
        """
        if arg != () and isinstance(arg[0], Dimension):
            self._dimensions += (arg[0],)

        else:
            self._dimensions += (Dimension(*arg, **kwargs),)

    def add_dependent_variable(self, *arg, **kwargs):
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
            ...     'quantity': 'energy',
            ...     'quantity_type': 'RGB'
            ... }
            >>> datamodel.add_dependent_variable(py_dictionary)

        *From a list of valid keyword arguments.*

        .. doctest::

            >>> datamodel.add_dependent_variable(type='internal',
            ...                                  name='star',
            ...                                  unit='W s',
            ...                                  quantity_type='RGB',
            ...                                  components=numpy_array)

        *From a* :ref:`dv_api` *instance.*

        .. doctest::

            >>> from csdfpy import DependentVariable
            >>> var1 = DependentVariable(type='internal',
            ...                          name='star',
            ...                          unit='W s',
            ...                          quantity_type='RGB',
            ...                          components=numpy_array)
            >>> datamodel.add_dependent_variable(var1)

        If passing a :ref:`dv_api` instance, as a general recommendation,
        always pass a copy of the DependentVariable instance to the
        :meth:`~csdfpy.CSDModel.add_dependent_variable` method. We provide
        the later alternative as it is useful for copying a DependentVariable
        instance from one :ref:`csdm_api` instance to another.
        """
        if arg != () and isinstance(arg[0], DependentVariable):
            self._dependent_variables += (arg[0],)

        else:
            self._dependent_variables += (
                DependentVariable(filename=self.filename, *arg, **kwargs),
            )
        self._dependent_variables[-1].encoding = "base64"
        self._dependent_variables[-1].type = "internal"

    def _get_python_dictionary(
        self, filename, print_function=False, version=__file_version__
    ):
        """Return the CSDModel instance as a python dictionary."""
        dictionary = {}

        dictionary["version"] = version
        if self.description.strip() != "":
            dictionary["description"] = self.description
        dictionary["dimensions"] = []
        dictionary["dependent_variables"] = []

        for i in range(len(self.dimensions)):
            dictionary["dimensions"].append(
                self.dimensions[i]._get_python_dictionary()
            )

        _length_of_dependent_variables = len(self.dependent_variables)

        for i in range(_length_of_dependent_variables):
            dictionary["dependent_variables"].append(
                self.dependent_variables[i]._get_python_dictionary(
                    filename=filename,
                    dataset_index=i,
                    for_display=print_function,
                    version=self.__file_version__,
                )
            )

        csdm = {}
        csdm["csdm"] = dictionary

        if self._persistent != {}:
            csdm["persistent"] = self._persistent

        return csdm

    def save(self, filename, version=__file_version__):
        """
        Serialize the :ref:`CSDM_api` instance as a JSON data-exchange file.

        The serialized file is saved with two file extensions.
        When every instance of the DependentVariable class from the CSDModel
        instance has
        an `internal` subtype, the corresponding CSDModel instance is
        serialized with a `.csdf` file extension.
        If any single DependentVariable instance has an `external` subtype, the
        CSDModel instance is serialized with a `.csdfe` file extension.
        We use the two different file extensions to alert the end use of the
        possible deserialization error associated with the `.csdfe` file
        extensions when the external data file is inaccessible.

        Irrespective of the subtypes from the serialized JSON file, by default,
        all instances of DependentVariable class are assigned an `internal`
        subtype with `base64` as the value of the `encoding` attribute upon
        the import.
        The user may, however, change these attribute at any time after the
        file import and before serializing to a file. The syntax follows,

        .. doctest::

            >>> data.save('myfile.csdf')

        .. testcleanup::

            import os
            os.remove('myfile.csdf')

        where ``datamodel`` is an instance of the CSDModel class.
        """
        dictionary = self._get_python_dictionary(filename, version=version)
        with open(filename, "w", encoding="utf8") as outfile:
            json.dump(
                dictionary,
                outfile,
                ensure_ascii=False,
                sort_keys=False,
                indent=2,
                allow_nan=False,
            )

    def copy(self):
        """Return a copy of the current CSDModel instance."""
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

        if (
            isinstance(index, tuple)
            or isinstance(index, list)
            or isinstance(index, np.ndarray)
        ):
            for i, item in enumerate(index):
                index[i] = _correct_index(item)
            return index, "list"

        elif isinstance(index, int):
            return _correct_index(index), "number"

        else:
            raise TypeError(message)

    def _get_new_csdmodel_object(self, func, index):
        index = self._check_dimension_indices(index)
        new = CSDModel()
        for variable in self.dependent_variables:
            y = func(variable.components, axis=index)
            new.add_dependent_variable(
                components=y,
                name=variable.name,
                quantity=variable.quantity,
                encoding=variable.encoding,
                numeric_type=variable.numeric_type,
                quantity_type=variable.quantity_type,
                component_labels=variable.component_labels,
                components_uri=variable.components_uri,
            )
        for i, variable in enumerate(self.dimensions):
            if index[1] == "number":
                if i != index[0]:
                    new.add_dimension(variable)
            else:
                if i not in index[0]:
                    new.add_dimension(variable)
        return new

    # def split_dependent_variables(self):
    #     for y in self.dependent_variables
    #     new = CSDModel()

    def sum(self, index=0):
        """
        Sum of data values along the independent variable indices.

        Sum the dependent variable data values along the independent variable
        at indices given by `index`. The default value is index 0. The index
        can be an interger or a tuple of intergers.

        :params: index: An integer or tuple of integers cooresponding to the
                index/indices of the independent variable along which the sum
                of data values is performed .
        :returns: A ``CSDModel`` object.
        """
        func = np.sum
        return self._get_new_csdmodel_object(func, index)

    def prod(self, index=0):
        """
        Product of data values along the independent variable indices.

        The default value is index 0. The `index` is either an integer or a
        tuple of intergers.

        :params: index: An integer or tuple of integers cooresponding to the
                index/indices of the independent variable along which the
                product of data values is performed.
        :returns: A ``CSDModel`` object.
        """
        func = np.prod
        return self._get_new_csdmodel_object(func, index)

    def fft(self, index=0):
        """
        Perform a FFT along the specified control variable (cv).

        Needs debugging.
        """
        if self.dimensions[index].dimension_type != "linear":
            raise NotImplementedError(
                "FFT is available for dimensions with type 'linear'."
            )

        object_id = self.dimensions[index].subtype
        # swap the values of object with the respective reciprocal object.
        object_id._swap()

        # compute the reciprocal increment using Nyquist shannan theorem.
        _reciprocal_increment = 1.0 / (
            object_id._number_of_points * object_id._increment.value
        )
        object_id._increment = _reciprocal_increment * object_id._unit

        # toggle the value of the FFT_output_order attribute
        # if object_id._fft_output_order:
        #     object_id._fft_output_order = False
        # else:
        #     object_id._fft_output_order = True

        # get the coordinates of the reciprocal dimension.
        object_id._get_coordinates()

        # calculate the phase that will be applied to the fft amplitudes.
        phase = np.exp(
            1j
            * 2
            * np.pi
            * object_id.reciprocal._reference_offset
            * object_id._coordinates
        )

        ndim = len(self.dimensions)

        for i in range(len(self.dependent_variables)):
            signal_ft = fftshift(
                fft(
                    self.dependent_variables[i].subtype._components,
                    axis=-index - 1,
                )
                * get_broadcase_shape(phase, ndim, axis=-index - 1),
                axes=-index - 1,
            )

            self.dependent_variables[i].subtype._components = signal_ft

        # self.dimensions[index].gcv._reciprocal()
        # self._toggle_fft_output_order(self.dimensions[index])


#     def __add__(self, other):
#         """
#         Add two CSDModel instances.

#         We follow a safe rule---the addition of two CSDModel instances
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
#         Subtract two CSDModel instances.

#         We follow a safe rule---the subtraction of two CSDModel instances
#         will only be successfull when the attributes of the corresponding
#         ControlledVariable instances are identical.
#         """
#         pass

#     def __mul__(self, other):
#         """
#         Multiply two CSDModel instances.

#         We follow a safe rule---the multiplication of two CSDModel instances
#         will only be successfull when the attributes of the corresponding
#         ControlledVariable instances are identical.
#         """
#         pass

#     def __div__(self, other):
#         """
#         Divide two CSDModel instances.

#         We follow a safe rule---the division of two CSDModel instances
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
#     #     'quantity': True,
#     #     'quantity_type': True
#     # }
#     a = True
#     if uv1.unit.physical_type != uv2.unit.physical_type:
#         a = False
#     if uv1.quantity != uv2.quantity:
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

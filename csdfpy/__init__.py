
"""CSDModel."""

from __future__ import print_function, division
from .independent_variable import IndependentVariable
from .dependent_variable import DependentVariable
from ._version import __version__
import numpy as np
import json
from scipy.fftpack import fft, fftshift

from copy import deepcopy
from ._utils_download_file import _download_file_from_url

from urllib.parse import urlparse
from os import path


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
# __version__ = "0.0.10dev0"


script_path = path.dirname(path.abspath(__file__))


test_file = {
    "test01": path.normpath(script_path+'/../tests/test01.csdf'),
    "test02": path.normpath(script_path+'/../tests/test02.csdf')
    }


def _import_json(filename):
    res = urlparse(filename)
    if res[0] not in ['file', '']:
        filename = _download_file_from_url(filename)
    with open(filename, "rb") as f:
        content = f.read()
        return (json.loads(str(content, encoding="UTF-8")))


def load(filename=None):
    r"""
    Open a `.csdf` or `.csdfe` file and returns an instance of the :ref:`csdm_api` class.

    The file must be a JSON serialization of the CSD Model.

    .. doctest::

        >>> import csdfpy as cp
        >>> data1 = cp.load('local_address/file.csdf')  # doctest: +SKIP
        >>> data2 = cp.load('url_address/file.csdf')  # doctest: +SKIP

    :params: filename: A local or remote address to the `.csdf or
                        `.csdfe` file.
    :returns: A ``CSDModel`` instance.
    """
    if filename is None:
        raise Exception("'open' method requires a data file address.")

    try:
        dictionary = _import_json(filename)
    except Exception as e:
        raise Exception(e)

    # Create the CSDModel and populate the attribures
    _version = dictionary['CSDM']['version']

    csdm = CSDModel(filename, _version)

    for dim in dictionary['CSDM']['independent_variables']:
        csdm.add_independent_variable(dim)

    for dat in dictionary['CSDM']['dependent_variables']:
        csdm.add_dependent_variable(dat)    # filename)

    csdm.description = dictionary['CSDM']['description'].strip()
    # if np.all(_type):
    npts = [item.number_of_points for item in csdm.independent_variables]
    if npts != []:
        csdm._reshape(npts[::-1])

# Create the augmentation layer model #

    return csdm


def new():
    r"""
    Return an instance of the CSDModel class corresponding a :math:`0\mathrm{D}\{0\}` dataset.

    .. doctest::

        >>> import csdfpy as cp
        >>> emptydata = cp.new()
        >>> print(emptydata.data_structure)
        {
          "CSDM": {
            "version": "0.0.9",
            "independent_variables": [],
            "dependent_variables": []
          }
        }

    :returns: A ``CSDModel`` instance
    """
    return CSDModel()


class CSDModel:
    r"""
    Instantiate a CSDModel class.

    The CSDModel class is based on the core scientific dataset (CSD) model.
    The class is a composition of the :ref:`dv_api` and :ref:`iv_api`
    instances,
    where every instance of the :ref:`dv_api` class is a :math:`p`-component
    independent variable, :math:`y` and every instance of :ref:`iv_api` class
    is a dimension of a :math:`d`-dimensional independent variable space
    :math:`(x_0, x_1, ... x_k, ... x_{d-1})`.

    :returns: A ``CSDModel`` instance.
    """

    __file_version__ = "0.0.10"
    _old_compatible_versions = ()
    _old_incompatible_versions = ('0.0.9')

    __slots__ = [
            '_independent_variables',
            '_dependent_variables',
            '_version',
            '_description',
            '_filename',
        ]

    def __init__(self, filename='', version=None):
        """Python module from reading and writing CSDM files."""
        if version is None:
            version = self.__file_version__
        elif version in self._old_incompatible_versions:
            raise Exception(
                (
                    "Files created with version {0} of the CSDModel "
                    "are no longer supported."
                ).format(version)
            )

        self._independent_variables = ()
        self._dependent_variables = ()
        self._description = ''
        self._version = version
        self._filename = filename

# ---- Attribute ----#
# controlled variables
    @property
    def independent_variables(self):
        """Return a tuple of the :ref:`iv_api` instances."""
        return self._independent_variables

# uncontrolled variables
    @property
    def dependent_variables(self):
        """Return a tuple of the :ref:`dv_api` instances."""
        return self._dependent_variables

# CSD model version on file
    @property
    def version(self):
        """
        Return the version number of the :ref:`csdm_api` on file.
        
        The attribute cannot be modified.
        """
        return self._version

# CSD model description
    @property
    def description(self):
        """
        Return a string with the description of the datasets within the CSD model.
        
        The default value is an empty string, ''.

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
                ("Description requires a string, {0} given".format(type(value)))
            )

# CSD model version on file
    @property
    def filename(self):
        """
        Return the local file address of the current JSON file.

        The file extensions includes the `.csdf` and the `.csdfe` files.
        """
        return self._filename

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

        return (json.dumps(dictionary, ensure_ascii=False,
                           sort_keys=False, indent=2))

# private method

    def _reshape(self, shape):
        r"""
        Reshapes the components array.

        The array is reshaped to
        :math:`(p \times N_{d-1} \times ... N_1 \times N_0)` where :math:`p`
        is the number of components and :math:`N_k` is the number of points
        sampled along the :math:`k^\mathrm{th}` independent variable.
        """
        for item in self.dependent_variables:
            item1 = item.subtype
            _shape = (item1.quantity_type._p,) + tuple(shape)
            _nptype = item1.numeric_type._nptype

            item1._components = np.asarray(
                item1._components.reshape(_shape), dtype=_nptype
            )

# ----------- Public Methods -------------- #

    def add_independent_variable(self, *arg, **kwargs):
        """
        Add a new :ref:`iv_api` instance to the :ref:`csdm_api` instance.

        There are three ways to add a new independent variable.

        *From a python dictionary containing valid keywords.*

        .. doctest::

            >>> import csdfpy as cp

            >>> datamodel = cp.new()
            >>> py_dictionary = {
            ...     'type': 'linearly_sampled',
            ...     'increment': '5 G',
            ...     'number_of_points': 50,
            ...     'reference_offset': '-10 mT'
            ... }
            >>> datamodel.add_independent_variable(py_dictionary)

        *From a list of valid keyword arguaments.*

        .. doctest::

            >>> datamodel.add_independent_variable(
            ...     type = 'linearly_sampled',
            ...     increment = '5 G',
            ...     number_of_points = 50,
            ...     reference_offset = '-10 mT'
            ... )

        *From an* :ref:`iv_api` *instance.*

        .. doctest::

            >>> from csdfpy import IndependentVariable
            >>> datamodel = cp.new()
            >>> var1 = IndependentVariable(type = 'linearly_sampled',
            ...                            increment = '5 G',
            ...                            number_of_points = 50,
            ...                            reference_offset = '-10 mT')
            >>> datamodel.add_independent_variable(var1)
            >>> print(datamodel.data_structure)
            {
              "CSDM": {
                "version": "0.0.9",
                "independent_variables": [
                  {
                    "type": "linearly_sampled",
                    "number_of_points": 50,
                    "increment": "5.0 G",
                    "reference_offset": "-10.0 mT",
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
        :meth:`~csdfpy.CSDModel.add_independent_variable` method. We provide
        the later alternative for it is useful for copying an :ref:`iv_api`
        instance from one :ref:`csdm_api` instance to another.
        """
        if arg != () and isinstance(arg[0], IndependentVariable):
            self._independent_variables += (arg[0], )

        else:
            self._independent_variables += (
                    IndependentVariable(*arg, **kwargs),
                    )

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
            ...     'components': numpy_array,
            ...     'name': 'star',
            ...     'unit': 'W s',
            ...     'quantity': 'energy',
            ...     'quantity_type': 'RGB'
            ... }
            >>> datamodel.add_dependent_variable(py_dictionary)

        *From a lsit of valid keyword arguaments.*

        .. doctest::

            >>> datamodel.add_dependent_variable(name='star',
            ...                                  unit='W s',
            ...                                  quantity_type='RGB',
            ...                                  components=numpy_array)

        *From a* :ref:`dv_api` *instance.*

        .. doctest::

            >>> from csdfpy import DependentVariable
            >>> var1 = DependentVariable(name='star',
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
            self._dependent_variables += (arg[0], )

        else:
            self._dependent_variables += (
                    DependentVariable(
                        filename=self.filename, *arg, **kwargs
                        ),
                    )
        self._dependent_variables[-1].encoding = 'base64'
        self._dependent_variables[-1].type = 'internal'

    def _get_python_dictionary(self, filename, print_function=False,
                               version=__file_version__):
        """Return the CSDModel instance as a python dictionary."""
        dictionary = {}

        dictionary["version"] = version
        dictionary["description"] = self.description
        dictionary["independent_variables"] = []
        dictionary["dependent_variables"] = []

        for i in range(len(self.independent_variables)):
            dictionary["independent_variables"].append(
                self.independent_variables[i]._get_python_dictionary()
            )

        _length_of_dependent_variables = len(self.dependent_variables)

        for i in range(_length_of_dependent_variables):
            dictionary["dependent_variables"].append(
                self.dependent_variables[i]._get_python_dictionary(
                    filename=filename,
                    dataset_index=i,
                    for_display=print_function,
                    version=self.__file_version__)
                )

        csdm = {}
        csdm['CSDM'] = dictionary
        return csdm

    def save(self, filename, version=__file_version__):
        """
        Serialize the :ref:`CSDM_api` instance as a JSON data-exchange data file.

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

            >>> datamodel.save('myfile.csdf')

        .. testcleanup::

            import os
            os.remove('myfile.csdf')

        where ``datamodel`` is an instance of the CSDModel class.
        """
        dictionary = self._get_python_dictionary(filename, version=version)
        with open(filename, 'w', encoding='utf8') as outfile:
            json.dump(dictionary, outfile, ensure_ascii=False,
                      sort_keys=False, indent=2, allow_nan=False)

    def copy(self):
        """Return a copy of the current CSDModel instance."""
        return deepcopy(self)

#     def replace(self,
#                 controlled_variable=None,
#                 cv_index=-1,
#                 uncontrolled_variable=None,
#                 uv_index=-1):
#         """
#         Repalce the controlled or the uncontrolled variable at the index.

#         :params: controlled_variable: A new ControlledVariable object or a
#             python dictionary corresponding to a new ControlledVariable object.
#         :params: cv_index: An integer corresponding to the
#             UncontrolledVariable object to the updated.
#         :params: uncontrolled_variable: A new UncontrolledVariable object or a
#             python dictionary corresponding to a new UncontrolledVariable
#             object.
#         :params: uv_index: An integer corresponding to the
#             UncontrolledVariable object to the updated.

#         .. todo::
#             Well, write the method.
#         """
#         pass

    def _check_independent_variable_indicies(self, index=-1):

        def _correct_index(i):
            if not isinstance(i, int):
                raise TypeError(message)
            if i < 0:
                i += d
            if i > d-1:
                raise ValueError((
                    "`index` {0} cannot be greater than the number of "
                    "independent variables, {1}."
                    ).format(index, d)
                )
            return -1-i

        message = "Index/Indicies are expected as integer(s)."

        d = len(self.independent_variables)

        if isinstance(index, tuple) or \
                isinstance(index, list) or \
                isinstance(index, np.ndarray):
            for i, item in enumerate(index):
                index[i] = _correct_index(item)
            return index, 'list'

        elif isinstance(index, int):
            return _correct_index(index), 'number'

        else:
            raise TypeError(message)

    def _get_new_csdmodel_object(self, func, index):
        index = self._check_independent_variable_indicies(index)
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
        for i, variable in enumerate(self.independent_variables):
            if index[1] == 'number':
                if i != index[0]:
                    new.add_independent_variable(variable)
            else:
                if i not in index[0]:
                    new.add_independent_variable(variable)
        return new

    # def split_dependent_variables(self):
    #     for y in self.dependent_variables
    #     new = CSDModel()

    def sum(self, index=0):
        """
        Sum of data values along the independent variable indicies.

        Sum the dependent variable data values along the independent variable
        at indicies given by `index`. The default value is index 0. The index
        can be an interger or a tuple of intergers.

        :params: index: An integer or tuple of imtegers cooresponding to the
                index/indicies of the independent variable along which the sum
                of data values is performed .
        :returns: A ``CSDModel`` object.
        """
        func = np.sum
        return self._get_new_csdmodel_object(func, index)

    def prod(self, index=0):
        """
        Product of data values along the independent variable indicies.

        The default value is index 0. The `index` is either an integer or a
        tuple of intergers.

        :params: index: An integer or tuple of integers cooresponding to the
                index/indicies of the independent variable along which the
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
        if self.independent_variables[index].dimension_type != 'linear_spacing':
            raise NotImplementedError(
                "FFT is available for dimensions with type 'linear_spacing'."
            )

        object_id = self.independent_variables[index].subtype
        # swap the values of object with the respective reciprocal object.
        object_id._swap()

        # compute the reciprocal increment using Nyquist shannan theorm.
        _reciprocal_increment = 1.0/(
            object_id._number_of_points * object_id._increment.value
        )
        object_id._increment = _reciprocal_increment * object_id._unit

        # toggle the value of the fft_output_order attribute
        # if object_id._fft_output_order:
        #     object_id._fft_output_order = False
        # else:
        #     object_id._fft_output_order = True

        # get the coordinates of the reciprocal dimension.
        object_id._get_coordinates()

        # calculate the phase that will be applied to the fft amplitudes.
        phase = np.exp(
            1j * 2*np.pi *
            object_id.reciprocal._reference_offset * object_id._coordinates
        )

        ndim = len(self.independent_variables)

        for i in range(len(self.dependent_variables)):
            signal_ft = fftshift(
                fft(self.dependent_variables[i].subtype._components,
                    axis=-index-1) * get_broadcase_shape(
                        phase, ndim, axis=-index-1
                        ), axes=-index-1
                )

            self.dependent_variables[i].subtype._components = signal_ft

        # self.independent_variables[index].gcv._reciprocal()
        # self._toggle_fft_output_order(self.independent_variables[index])

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
#     dim1 = len(object1.independent_variables)
#     dim2 = len(object2.independent_variables)

#     message = (
#         "{0} and {1} do not have the same set of "
#         "controlled variables."
#     ).format(object1.__name__, object2.__name__)

#     if dim1 != dim2:
#         raise Exception(message)

#     for i in range(dim1):
#         if not _compare_cv_object(
#             object1.independent_variables[i],
#             object2.independent_variables[i]
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

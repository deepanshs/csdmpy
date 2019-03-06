
"""Uncontrolled variable object: attributes and methods."""

from __future__ import print_function, division
import base64
import json
import warnings
from os import path
import numpy as np

from ._utils import (
    _assign_and_check_unit_consistency,
    # _check_unit_consistency,
    _check_quantity,
    _check_encoding,
    _check_numeric_type,
    _check_dataset_type,
    numpy_dtype_to_numeric_type,
    _type_message,
    _axis_label,
    _get_dictionary
)
from copy import deepcopy

from .unit import (
    value_object_format,
    # string_to_unit
)

from urllib.request import urlopen
from urllib.parse import urlparse


def _get_absolute_data_address(data_path, file):
    """
    Return the absolute path address of a local data file.

    :params: data_path:
    """
    _file_abs_path = path.abspath(file)
    _path, _file = path.split(_file_abs_path)
    _join = path.join(_path, data_path)
    _join = path.normpath(_join)

    return 'file:'+_join


def _get_relative_data_address(data_absolute_uri, file):
    res = urlparse(data_absolute_uri)
    _data_abs_path = path.abspath(res.path)
    _file_abs_path = path.split(path.abspath(file))[0]
    _data_rel_path = path.relpath(_data_abs_path, start=_file_abs_path)
    return 'file:./'+_data_rel_path


def _get_absolute_uri_path(uri, file):
    res = urlparse(uri)
    path = uri
    # print(res)
    if res.scheme in ['file', '']:
        if res.netloc == '':
            path = _get_absolute_data_address(res.path, file)
    return path


class UncontrolledVariable:
    r"""
    The base UncontrolledVariable class.

    This class returns an object which represents an uncontrol variable.
    The uncontrol variable, :math:`y_\alpha`, resides in a
    :math:`p_\alpha`-dimensional space. For example, a scalar resides in a
    one-dimensional space (:math:`p_\alpha=1`), a vector resides in an
    `n`-dimensional vector space (:math:`p_\alpha=n`), and a second rank
    symmetric tensor resides in a six-dimensional space (:math:`p_\alpha=6`).
    We refer the coordinates of a data value from this
    :math:`p_\alpha`-dimensional space as the components of the
    data value. For example, if the coordinates of a magnetic field vector is
    ("1 T", "25 mT"), then "1 T" and "25 mT" are the components of the
    magnetic field vector.

    **Creating a new uncontrol variable.**

    There are two ways to create a new uncontrolled variable from the
    UncontrolledVariable class.

    `From a python dictionary containing valid keywords.` ::

        >>> from csdfpy import UncontrolledVariable
        >>> import numpy as np
        >>> numpy_array = np.arange(30).reshape(3,10).astype(np.uint8)
        >>> py_dictionary = {
        ...     'components': numpy_array,
        ...     'name': 'star',
        ...     'unit': 'W s',
        ...     'quantity': 'energy',
        ...     'dataset_type': 'RGB'
        ... }
        >>> y = UncontrolledVariable(py_dictionary)

    `From valid keyword arguaments.` ::

        >>> y = UncontrolledVariable(name='star',
        ...                          unit='W s',
        ...                          dataset_type='RGB',
        ...                          components=numpy_array)
    """

    __slots__ = ['uv']

    def __new__(cls, *args, **kwargs):
        """Create a new instance of UncontrolVariable object."""
        # if args != () and isinstance(args[0], ControlledVariable):
        #     print('inside __new__. arg')
        #     return args[0]
        # else:
        instance = super(UncontrolledVariable, cls).__new__(cls)
        # instance.__init__(*args, **kwargs)
        return instance

    def __init__(self, *args, **kwargs):
        """Initialize an instance of UncontrolVariable object."""
        dictionary = {
            'name': '',
            'unit': '',
            'quantity': None,
            'component_labels': None,
            'encoding': None,
            'numeric_type': None,
            'dataset_type': 'scalar',
            'components': None,
            'components_URI': None,
            'sampling_schedule': None,
            'filename': __file__
        }

        default_keys = dictionary.keys()
        input_dict = _get_dictionary(*args, **kwargs)
        input_keys = input_dict.keys()

        for key in input_keys:
            if key in default_keys:
                dictionary[key] = input_dict[key]
        if 'filename' in kwargs.keys():
            dictionary['filename'] = kwargs['filename']

        _uv_object = _UnControlledVariable(
                    _name=dictionary['name'],
                    _unit=dictionary['unit'],
                    _quantity=dictionary['quantity'],
                    _encoding=dictionary['encoding'],
                    _numeric_type=dictionary['numeric_type'],
                    _dataset_type=dictionary['dataset_type'],
                    _component_labels=dictionary['component_labels'],
                    _components=dictionary['components'],
                    _components_uri=dictionary['components_URI'],
                    _sampling_schedule=dictionary['sampling_schedule'],
                    _filename=dictionary['filename']
                )

        super(UncontrolledVariable, self).__setattr__('uv', _uv_object)

# =========================================================================== #
#                                 Attributes                                  #
# =========================================================================== #

    @property
    def name(self):
        r"""
        Return a string containing the name of the uncontrolled variable.

        The attribute is editable. For example, ::

            >>> y.name
            'star'
            >>> y.name = 'rock star'

        In the above example, ``y`` is an instance of the UncontrolledVariable
        class.

        :returns: A ``String``.
        :raises TypeError: When the assigned value is not a string.
        """
        return deepcopy(self.uv._name)

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))
        self.uv.set_attribute('_name', value)

# Unit #
    @property
    def unit(self):
        r"""
        Return the unit associated the uncontrolled variable.

        The attribute cannot be modified. To convert the unit, use the
        :py:meth:`~csdfpy.UncontrolledVariable.to` method of the class. ::

            >>> y.unit
            Unit("s W")

        :returns: A ``Unit`` object.
        :raises AttributeError: When assigned a value.
        """
        return deepcopy(self.uv._unit)

    @unit.setter
    def unit(self, value):
        raise AttributeError(
            "`unit` attribute cannot be modified. Use ``to`` method for unit "
            "conversion."
        )

    @property
    def quantity(self):
        """
        Return a string with a `quantity name` of the uncontrolled variable.

        ::

            >>> y.quantity
            'energy'

        :returns: A ``String``.
        :raises NotImplementedError: When assigning a value.
        """
        return deepcopy(self.uv._quantity)

    @quantity.setter
    def quantity(self, value=''):
        raise NotImplementedError(
            (
                'The feature to modify the `quantity` attribute is not yet '
                'implemented.'
            )
        )

    @property
    def encoding(self):
        r"""
        Return a string describing the encoding method.

        The attribute holds the value that determines the method used when
        storing the data values to a file. Currently, there are
        three valid encoding methods:

        | ``raw``
        | ``base64``
        | ``none``

        A value, `raw`, indicates that the data values are stored as binary.
        The value, `base64`, implies that the data values are stored as
        base64 strings, while, the value `none` refers to text-based storage.
        The attribute is *only* relevant when storing the dataset to a file.
        The value is specified as a string containing a *valid* encoding
        method, for example, ::

            >>> y.encoding = 'base64'

        :returns: A ``String``.
        :raises ValueError: If an invalid value is assigned.
        :raises TypeError: When the assigned value is not a string.
        """
        return deepcopy(self.uv._encoding)

    @encoding.setter
    def encoding(self, value):
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))
        value = _check_encoding(value)
        self.uv.set_attribute('_encoding', value)

    @property
    def numeric_type(self):
        r"""
        Return a string describing the numeric type of data values.

        There are currently thirteen valid numeric types which are:

        ==============   ============   ============   ============
        ``uint8``        ``int8``       ``float16``    ``complex64``
        ``uint16``       ``int16``      ``float32``    ``complex128``
        ``uint32``       ``int32``      ``float64``
        ``uint64``       ``int64``
        ==============   ============   ============   ============

        When assigned a value, this attribute updates the `numeric type` as
        well as the `dtype` of the Numpy array from the corresponding
        :py:attr:`~csdfpy.UncontrolledVariable.components` attribute. We
        recommended the use of the numeric type attribute for updating
        the `dtype` of the Numpy array. For example, ::

            >>> print(y.components)
            [[ 0  1  2  3  4  5  6  7  8  9]
             [10 11 12 13 14 15 16 17 18 19]
             [20 21 22 23 24 25 26 27 28 29]]
            >>> y.numeric_type
            'uint8'
            >>> y.numeric_type = 'complex64'
            >>> print(y.components)
            [[ 0.+0.j  1.+0.j  2.+0.j  3.+0.j  4.+0.j  5.+0.j  6.+0.j  7.+0.j  8.+0.j
               9.+0.j]
             [10.+0.j 11.+0.j 12.+0.j 13.+0.j 14.+0.j 15.+0.j 16.+0.j 17.+0.j 18.+0.j
              19.+0.j]
             [20.+0.j 21.+0.j 22.+0.j 23.+0.j 24.+0.j 25.+0.j 26.+0.j 27.+0.j 28.+0.j
              29.+0.j]]

        :returns: A ``String``.
        :raises ValueError: If an invalid value is assigned.
        :raises TypeError: When the assigned value is not a string.
        """
        return deepcopy(self.uv._numeric_type)

    @numeric_type.setter
    def numeric_type(self, value):
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))
        _va, npType = _check_numeric_type(value)
        self.uv.set_attribute('_numeric_type', value)
        self.uv.set_attribute('_npType', npType)
        self.uv.set_attribute(
            '_components', np.asarray(self.components, dtype=npType)
        )

    @property
    def dataset_type(self):
        r"""
        Return a string describing the dataset type of data values.

        There are currently six dataset types,

        | ``RGB``
        | ``RGBA``
        | ``scalar``
        | ``vector_n``
        | ``matrix_n_m``
        | ``symmetric_matrix_n``

        where `n` and `m` are integers. The attribute can also be used
        to assign a `dataset type` to the dataset. ::

            >>> y.dataset_type
            'RGB'
            >>> y.dataset_type = 'vector_3'

        :returs: A ``String``.
        :raise ValueError: If an invalid value is assigned.
        :raises TypeError: When the assigned value is not a string.
        """
        return deepcopy(self.uv._dataset_type)

    @dataset_type.setter
    def dataset_type(self, value):
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))
        value, component = _check_dataset_type(value)
        self.uv.set_attribute('_dataset_type', value)

    @property
    def component_labels(self):
        r"""
        Return an ordered array of labels relative to the order of the :py:attr:`~csdfpy.UncontrolledVariable.components`. ::

            >>> y.component_labels
            ['', '', '']

        When assigning a value, simply assign an array with same size ::

            >>> y.component_labels = ['x', 'y', 'z']

        The individual labels are accessed with proper indexing,
        for example, ::

            >>> y.component_labels[2]
            'z'

        .. todo::
            Check the component labels.

        :raises TypeError: When the assigned value is not a string.
        """
        return deepcopy(self.uv._component_labels)

    @component_labels.setter
    def component_labels(self, value):
        self.uv.set_compnents_label(value)

    @property
    def axis_label(self):
        r"""
        Return a formatted array of strings for displaying the label.

        This supplementary attribute is convenient for labeling axes.
        For uncontrolled variables, this attributes returns an array of strings
        where every string is formatted as, 'label / unit',  if the
        corresponding index of the `component_labels` array is not an empty
        string, otherwise, 'quantity / unit’. Here
        `quantity`, `component_labels`, and `unit` are the attributes of the
        :ref:`uv_api` instances described before.
        For example, consider a diffusion tensor uncontrolled variable where ::

            >>> y.component_labels[1]
            'y'
            >>> y.axis_label[1]
            'y / ( s * W)'

        :returns: A ``String``.
        :raises AttributeError: When assigned a value.
        """
        labels = []
        for i, label in enumerate(self.component_labels):
            if label.strip() == '':
                label = self.quantity
            labels.append(_axis_label(label, self.uv._unit))
        return labels

    @property
    def components(self):
        r"""
        Return the components of data values.

        The value of the components attribute of the uncontrolled variables
        :math:`y_\alpha` is a Numpy array of shape
        :math:`(p_\alpha \times N_{d-1} \times ... N_1 \times N_0)` where
        :math:`p_\alpha` is the number of components, and :math:`N_k` is the
        number of points sampled along the :math:`k^\mathrm{th}` controlled
        variable. The total number of dimensions from this array is :math:`d+1`
        where :math:`d` is the number of controlled variables. Note, the
        shape of the Numpy array follows a reverse order based on the ordered
        list of controlled variables, that is, the :math:`k^\mathrm{th}`
        controlled variable lies along the :math:`(d-k)^\mathrm{th}` axis of
        the Numpy array. Thus, the first controlled variable :math:`x_0`
        with :math:`N_0` points is the last axis, and the last
        controlled variable :math:`x_{d-1}` with :math:`N_{d-1}` points is
        the first axis of the Numpy array. The zeroth axis with
        :math:`p_\alpha` points is the number of components.

        This attribute can only be updated when the shape of the new array is
        the same as the shape of the components array.

        For example, ::

            >>> print(y.components.shape)
            (3, 10)
            >>> y.numeric_type
            'complex64'

        be a single-component uncontrolled variable with five data values. The
        numeric type of data values, in this example, is `float16`. To update
        the components array, assign an array of shape (1,5) to the components
        attribute. In the following example, we assign a Numpy
        array of random numbers. ::

            >>> y.components = np.linspace(0,256,30, dtype='u1').reshape(3,10)
            >>> y.numeric_type
            'uint8'

        Notice, the value of the `numeric_type` attribute is automatically
        updated based on the `dtype` of the Numpy array. In this case, from a
        *complex64* to *uint8*.
        In this other example, ::

            >>> y.components = np.random.rand(1,10).astype('u1')
            Traceback (most recent call last):
              File "<stdin>", line 1, in <module>
              File "/Users/deepansh/Dropbox/NMRgit/MRData/csdfpy/csdfpy/uv.py", line 491, in components
                self.uv._set_components(value)
              ValueError: The shape of `ndarray`, `(1, 10)`, is not consistent with the shape of the components array, `(3, 10)`.

        a `ValueError` is raised because the shape of the input array (1,10) is
        not consistent with the shape of the components array, (1,5).

        :returns: A ``Numpy array``.
        :raises ValueError: When assigning an array whose shape is
            not consistent with the shape of the components array.
        """
        return self.uv._components

    @components.setter
    def components(self, value):
        value = np.asarray(value)
        if value.shape == self.components.shape:
            self.uv._set_components(value)
        else:
            raise ValueError(
                (
                    "The shape of `{0}`, `{1}`, is not consistent with the "
                    "shape of the components array, `{2}`."
                ).format(
                    value.__class__.__name__,
                    value.shape,
                    self.components.shape
                )
            )

    @property
    def components_uri(self):
        r"""
        Return the URI of the data file where data components are stored.

        The attribute is only informative and cannot be modified. Its value is
        a string containing the local or remote address of a file where the
        data values are stored.

        :returns: A ``String``.
        :raises AttributeError: When assigining a value.
        """
        return self.uv._components_uri

    @property
    def schedule(self):
        r"""NotImplemented."""
        return self.uv._sampling_schedule

    @property
    def data_structure(self):
        r"""
        Return the UncontrolledVariable object as a json object.

        This attribute is useful for a quick view of the data structure. Note,
        the JSON object from this attribute is not the same as the one written
        to the file. For convenience, the values from the `components`
        attribute are truncated to the first and the last two numbers per
        component. Also, the `encoding` keyword is hidden from this view.
        The attribute cannot be modified. ::

            >>> print(y.data_structure)
            {
              "name": "rock star",
              "unit": " s * W",
              "quantity": "energy",
              "component_labels": [
                "x",
                "y",
                "z"
              ],
              "numeric_type": "uint8",
              "dataset_type": "vector_3",
              "components": "[0, 0, ...... 70, 70], [88, 88, ...... 158, 158], [176, 176, ...... 247, 247]"
            }

        :raises AttributeError: When modified.
        """
        dictionary = self.get_python_dictionary()
        return (json.dumps(dictionary, ensure_ascii=False,
                           sort_keys=False, indent=2))

# =========================================================================== #
#                                  Methods                                    #
# =========================================================================== #

    def scale(self, value):
        r"""NotImplemented."""
        value = _assign_and_check_unit_consistency(value, None)
        self.uv.set_attribute('_unit', self.unit*value.unit)
        value = self.unit*value.value
        self.uv.set_attribute('_components', self.components*value)

    def to(self, unit):
        r"""
        Convert the unit of the uncontrolled variable components to `unit`.

        This method is a wrapper of the `to` method from the
        `Quantity <http://docs.astropy.org/en/stable/api/\
        astropy.units.Quantity.html#astropy.units.Quantity.to>`_ class. ::

            >>> y.unit
            Unit("s W")
            >>> y.to('J')
            >>> y.unit
            Unit(" J")

        """
        factor = (1.0*self.unit).to(unit)
        self.uv.set_attribute('_components', self.components*factor.value)
        self.uv.set_attribute('_unit', factor.unit)

    def reshape(self, shape):
        r"""
        Reshape the components array.

        The array id reshaped relative to the number of points in controlled
        variables. Let :math:`N_k` be the number of points sampled along the
        :math:`k^\mathrm{th}` control variable, then the shape of the
        ``component`` array is
        :math:`(p_\alpha \times N_{d-1} \times ... N_1 \times N_0)` where
        :math:`p_\alpha` is the number of components.
        """
        shape = (self.uv._total_components,) + tuple(shape)
        nptype = self.uv._npType

        self.uv.set_attribute(
            '_components', np.asarray(self.components.reshape(shape),
                                      dtype=nptype)
        )

    def get_python_dictionary(self, filename=None, dataset_index=None,
                              for_display=True, version=None):
        """Return the UnontrolledVariable object as a python dictionary."""
        return self.uv._get_python_dictionary(filename,
                                              dataset_index,
                                              for_display,
                                              version)


class _UnControlledVariable:
    """
    An uncontrolled variable core object.

        keywork aruament :
          name : any string
          format : either 'binary' or 'text'.
          data_type : one of 'float32', 'float64', 'comple64' or 'complex128'.
          unit : unit associated with the dataset.
          quantity : the physical qunatity associated with the dataset.
          values : ordered array in format specified at keywords 'format'
                   and 'data_type'.
    """

    __slots__ = ['_name',
                 '_unit',
                 '_quantity',
                 '_encoding',
                 '_numeric_type',
                 '_dataset_type',
                 '_component_labels',
                 '_components',
                 '_components_uri',
                 '_sampling_schedule',

                 '_npType',
                 '_total_components',
                 '_filename']

    def __init__(
            self,
            _name='',
            _unit='',
            _quantity=None,
            _encoding=None,
            _numeric_type=None,
            _dataset_type='scalar',
            _component_labels=None,
            _components=None,
            _components_uri=None,
            _sampling_schedule=None,
            _filename=''):

        if _components is None and _components_uri is None:
            raise ValueError(
                (
                    "Either '{0}' or '{1}' is not present."
                ).format('components', 'components_URI')
            )

        # unit, name, and quantity
        _va = _assign_and_check_unit_consistency(_unit, None)
        self.set_attribute('_unit', _va.unit)
        self.set_attribute('_name', str(_name))
        self.set_attribute('_quantity', _check_quantity(_quantity, self._unit))

        # dataset_tpye
        _va, total_components = _check_dataset_type(_dataset_type)
        self.set_attribute('_dataset_type', _va)
        self.set_attribute('_total_components', total_components)

        # components label
        self.set_compnents_label(_component_labels)

        # if components is a python list
        if isinstance(_components, list):
            if _encoding not in ['none', 'raw', 'base64']:
                _components = np.asarray(_components)

        # if components is numpy array
        if isinstance(_components, np.ndarray):
            # encoding
            _encoding = 'base64'
            self.set_attribute('_encoding', _check_encoding(_encoding))

            self._set_components(_components, _numeric_type)

            self.set_attribute('_components_uri', _components_uri)

        else:
            # encoding
            if _encoding is None:
                raise ValueError("`encoding` type not specified.")
            self.set_attribute('_encoding', _check_encoding(_encoding))

            # numeric type and numpy types
            if _numeric_type is None:
                raise ValueError("`numeric_type` type not specified.")
            _va, npType = _check_numeric_type(_numeric_type)
            self.set_attribute('_numeric_type', _va)
            self.set_attribute('_npType', npType)

            # components and components URI
            if _components is not None:
                _components = self._decode_components(_components)

            elif _components_uri is not None:
                _absolute_URI = _get_absolute_uri_path(
                    _components_uri, _filename
                )
                _components = urlopen(_absolute_URI).read()
                _components = self._decode_components(_components)

            self.set_attribute('_components', _components)
            self.set_attribute('_components_uri', _components_uri)

            # sampling schedule
            """
            .. todo::
                Support for under sampled orthogonal grid based datasets
            """
            self.set_attribute('_sampling_schedule', _sampling_schedule)

    def set_attribute(self, name, value):
        super(_UnControlledVariable, self).__setattr__(name, value)

    def set_compnents_label(self, component_labels):
        """
        Assign an array of strings, based on the number of components.

        If no label is provided, a default values,
        :math:`['', '', N_k]`, is assigned. If the number of component labels
        does not match the total number of components, a warning is raised and
        the inconsistency is resolved by appropriate truncating or additing the
        required number of strings.
        """
        if component_labels is None:
            self.set_attribute(
                '_component_labels',
                ['' for i in range(self._total_components)]
            )
            return

        if not isinstance(component_labels, list):
            raise ValueError(
                (
                    "A list of string labels is required, "
                    "{0} provided."
                ).format(type(component_labels))
            )

        if len(component_labels) != self._total_components:
            warnings.warn(
                (
                    "The number of component labels, {0}, "
                    "is not equal to the number of components, "
                    "{1}. The inconsistency is resolved by "
                    "appropriate truncation or addition of "
                    "strings padding."
                ).format(len(component_labels), self._total_components)
            )

            _lables = ['' for i in range(self._total_components)]
            for i, item in enumerate(component_labels):
                _lables[i] = item
            self.set_attribute('_component_labels', _lables)

        else:
            self.set_attribute('_component_labels', component_labels)

# =========================================================================== #
#                                Private Methods                              #
# =========================================================================== #

    @classmethod
    def __delattr__(cls, name):
        """Delete attribute."""
        if name in cls.__slots__:
            raise AttributeError(
                "Attribute '{0}' cannot be deleted.".format(name)
            )

    def __setattr__(self, name, value):
        """Set attributes."""
        if name in self.__class__.__slots__:
            raise AttributeError(
                "Attribute '{0}' cannot be modified.".format(name)
            )

        elif name in self.__class__.__dict__.keys():
            return self.set_attribute(name, value)

        else:
            raise AttributeError(
                (
                    "The '{0}' object has no attribute '{1}'."
                ).format(self.__class__.__name__, name)
            )

    def _download_file_contents_from_url(self, filename):
        pass

    def _check_number_of_components_and_encoding_key(self, length):
        """Verify the consistency of encoding wrt the number of components."""
        if length != self._total_components:
            raise Exception(
                (
                    "dataset_type '{0}' is non consistent with"
                    "total number of components, {1}"
                ).format(self._dataset_type, length)
            )

    def _set_components(self, _components, _numeric_type=None):
        # numeric type
        if _numeric_type is None:
            _numeric_type = numpy_dtype_to_numeric_type(
                str(_components.dtype)
            )
        _va, npType = _check_numeric_type(_numeric_type)
        self.set_attribute('_numeric_type', _va)
        self.set_attribute('_npType', npType)

        # components
        self.set_attribute(
            '_components', np.asarray(_components, self._npType)
        )

    def _decode_components(self, _components):
        """
        Decode the components based on the encoding key value.

        The valid encodings are 'base64', 'none' (text), and 'raw' (binary).
        """
        _val_len = len(_components)

        if self._encoding == 'base64':
            self._check_number_of_components_and_encoding_key(_val_len)
            _components = np.asarray([np.fromstring(base64.b64decode(item),
                                     dtype=self._npType)
                                     for item in _components])

            _components.setflags(write=1)
            return _components

        if self._encoding == 'none':
            self._check_number_of_components_and_encoding_key(_val_len)
            if self._npType in ['<c8', '<c16']:
                _components = np.asarray(
                    [np.asarray(item[0::2]) + 1j*np.asarray(item[1::2])
                        for item in _components], dtype=self._npType
                )
            else:
                _components = np.asarray(
                    [np.asarray(item) for item in _components],
                    dtype=self._npType
                )

            _components.setflags(write=1)
            return _components

        if self._encoding == 'raw':
            _components = np.frombuffer(_components, dtype=self._npType)

            _components = _components.reshape(
                self._total_components, int(
                    _components.size/self._total_components
                )
            )

            _components.setflags(write=1)
            return _components

        if self._encoding == 'ndarray':
            _components = np.asarray(_components, dtype=self._npType)
            return _components

        raise Exception(
            "'{0}' is an invalid data 'encoding'.".format(self._encoding)
        )

    def _getparams(self):
        lst = [
            '_unit',
            '_quantity',
            '_numeric_type',
            '_dataset_type',
            '_sampling_schedule',
            '_npType'
        ]
        return np.asarray([getattr(self, item) for item in lst])

    def _info(self):
        _response = [
            self._components_uri,
            self._name,
            str(self._unit),
            self._quantity,
            self._component_labels,
            self._encoding,
            self._numeric_type,
            self._dataset_type
        ]
        return _response

    def _get_python_dictionary(self, filename=None, dataset_index=None,
                               for_display=True, version=None):
        """Return the UnontrolledVariable object as a python dictionary."""
        dictionary = {}
        if self._name.strip() != '' and self._name is not None:
            dictionary['name'] = self._name

        if str(self._unit) != '':
            dictionary['unit'] = value_object_format(
                1.0*self._unit, numerical_value=False
            )

        if self._quantity not in ['dimensionless', 'unknown', None]:
            dictionary['quantity'] = self._quantity

        print_label = False
        for label in self._component_labels:
            if label.strip() != '':
                print_label = True
                break

        if print_label:
            dictionary['component_labels'] = self._component_labels

        dictionary['numeric_type'] = str(self._numeric_type)

        if self._dataset_type != 'scalar':
            dictionary['dataset_type'] = self._dataset_type

        if for_display:
            _str = ''
            for i in range(len(self._components)):
                temp = self._components[i].ravel()
                lst = [str(temp[0]), str(temp[0]),
                       str(temp[-2]), str(temp[-2])]
                _string = (
                    "[{0}, {1}, ...... {2}, {3}], "
                ).format(*lst)
                # ''.join(
                #     [
                #         '[ ', str(temp[0]), ',  ', str(temp[1]),
                #         ' ...... ', str(temp[-2]), ',  ',
                #         str(temp[-1]), ' ], '
                #     ]
                # )
                _str = _str + _string
            temp = None
            dictionary['components'] = _str[:-2]

        if not for_display:
            dictionary['encoding'] = str(self._encoding)

            size = self._components[0].size
            if self._numeric_type[:7] == 'complex':
                if self._numeric_type == 'complex64':
                    c = np.empty(
                        (self._total_components, size*2), dtype=np.float32
                    )
                if self._numeric_type == 'complex128':
                    c = np.empty(
                        (self._total_components, size*2), dtype=np.float64
                    )

                for i in range(self._total_components):
                    c[i, 0::2] = self._components.real[i].ravel()
                    c[i, 1::2] = self._components.imag[i].ravel()
            else:
                c = np.empty(
                    (self._total_components, size), dtype=self._npType
                )
                for i in range(self._total_components):
                    c[i] = self._components[i].ravel()

            if self._encoding == 'none':
                dictionary['components'] = c.tolist()
            if self._encoding == 'base64':
                dictionary['components'] = [base64.b64encode(
                    item).decode("utf-8") for item in c]

            # print ('before raw')
            if self._encoding == 'raw':
                # print ('in raw')
                index = str(dataset_index)
                file_save_path_abs = _get_absolute_uri_path('', filename)

                print('abs URI', self._components_uri)
                print('rel filename', filename)
                data_path_relative = path.join(
                    'file:.', path.splitext(
                        path.split(filename)[1]
                    )[0] + '_' + index + '.dat'
                )

                print('relative path', data_path_relative)
                dictionary['components_URI'] = data_path_relative

                data_path_absolute = path.abspath(
                    urlparse(path.join(
                        file_save_path_abs, urlparse(data_path_relative).path
                    )).path
                )

                print(data_path_absolute)
                c.ravel().tofile(data_path_absolute)

            c = None
            del c
        return dictionary

# ------------- Public Methods ------------------ #

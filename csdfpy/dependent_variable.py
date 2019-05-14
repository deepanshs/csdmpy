
"""Dependent variable object: attributes and methods."""

from __future__ import print_function, division

import json
from ._dependent_variables import InternalDataset, ExternalDataset

from copy import deepcopy

from ._utils import (
    _assign_and_check_unit_consistency,
    _type_message,
    _check_quantity,
    _get_dictionary,
    _axis_label
)

from .unit import (
    value_object_format,
)

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


class DependentVariable:
    r"""
    Instantiate a DependentVariable class.

    The instance of this class represents a dependent variable,
    :math:`y`. A dependent variable holds :math:`p`-component data values,
    where :math:`p>0` is an integer.
    For example, a scalar is single-component (:math:`p=1`),
    a vector can have up to `n`-components (:math:`p=n`),
    while a second rank symmetric tensor has six-component (:math:`p=6`).

    **Creating a new dependent variable.**

    There are two ways to create a new dependent variable from the
    DependentVariable class.

    `From a python dictionary containing valid keywords.`

    .. doctest::

        >>> from csdfpy import DependentVariable
        >>> import numpy as np
        >>> numpy_array = np.arange(30).reshape(3,10).astype(np.uint8)

        >>> py_dictionary = {
        ...     'type': 'internal',
        ...     'components': numpy_array,
        ...     'name': 'star',
        ...     'unit': 'W s',
        ...     'quantity': 'energy',
        ...     'quantity_type': 'RGB'
        ... }
        >>> y = DependentVariable(py_dictionary)

    Here, ``py_dictionary`` is the python dictionary.

    *From valid keyword arguaments.*

    .. doctest::

        >>> y = DependentVariable(type='internal',
        ...                       name='star',
        ...                       unit='W s',
        ...                       quantity_type='RGB',
        ...                       components=numpy_array)
    """

    __slots__ = (
        'subtype',
        '_type',
        '_name',
        '_unit',
        '_quantity',
        '_component_labels',
        '_description'
    )

    _immutable_objects_ = ()

    def __init__(self, *args, **kwargs):
        """Initialize an instance of DependentVariable class."""
        dictionary = {
            'type': 'internal',
            'description': '',
            'name': '',
            'unit': '',
            'quantity': None,
            'component_labels': None,
            'encoding': 'base64',
            'numeric_type': None,
            'quantity_type': 'scalar',
            'components': None,
            'components_URI': None,
            'sampling_schedule': None,
            'filename': __file__
        }

        default_keys = dictionary.keys()
        input_dict = _get_dictionary(*args, **kwargs)
        input_keys = input_dict.keys()

        for item in self.__class__._immutable_objects_:
            if item in input_keys:
                dictionary[item] = input_dict[item]

        if 'type' not in input_keys:
            raise ValueError("Missing a required 'type' key in the dependent variable object.")

        for key in input_keys:
            if key in default_keys:
                dictionary[key] = input_dict[key]
        if 'filename' in kwargs.keys():
            dictionary['filename'] = kwargs['filename']

        if dictionary['type'] not in ['internal', 'external']:
            raise ValueError((
                "'{0}' is an invalid DependentVariable 'type'. The allowed values "
                "are 'internal', 'external'.".format(dictionary['type'])
            ))

        # unit
        _va = _assign_and_check_unit_consistency(dictionary['unit'], None)
        self._unit = _va.unit

        # name
        self._name = dictionary['name']

        # quantity
        self._quantity = _check_quantity(dictionary['quantity'], self._unit)

        if dictionary['type'] == 'internal':
            self._type = 'internal'
            _uv_object = InternalDataset(
                    _name=dictionary['name'],
                    _unit=dictionary['unit'],
                    _quantity=dictionary['quantity'],
                    _encoding=dictionary['encoding'],
                    _numeric_type=dictionary['numeric_type'],
                    _quantity_type=dictionary['quantity_type'],
                    _component_labels=dictionary['component_labels'],
                    _components=dictionary['components']
                )

        if dictionary['type'] == 'external':
            self._type = 'external'
            _uv_object = ExternalDataset(
                    _name=dictionary['name'],
                    _unit=dictionary['unit'],
                    _quantity=dictionary['quantity'],
                    _encoding=dictionary['encoding'],
                    _numeric_type=dictionary['numeric_type'],
                    _quantity_type=dictionary['quantity_type'],
                    _component_labels=dictionary['component_labels'],
                    _components_uri=dictionary['components_URI'],
                    _filename=dictionary['filename']
                )
        self.subtype = _uv_object
        self._description = dictionary['description']

# =========================================================================== #
#                                 Attributes                                  #
# =========================================================================== #
    @property
    def description(self):
        """
        A description for the instance of the DependentVariable class.

        The default value is an empty string, ''. The attribute can be
        modified, for example
        
        .. doctest::

            >>> print(y.description)
            ''

            >>> y.description = 'The variable is a simulation.'

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

    @property
    def type(self):
        """
        Return the subtype of the :ref:`dv_api` instance.

        By default, all DependentVariable instances are assiged an `internal`
        subtype upon import. The user can update this arrtritue at ant time.

        .. doctest::

            >>> print(y.type)
            internal

            >>> y.type = 'external'

        When `type` is external, the data values from the corresponding
        DependentVariable instance are store in an external file within
        the same directory as the `.csdfe` file.

        :returns: A ``String``.
        :raises ValueError: When an invalid value is assigned
        """
        return self._type

    @type.setter
    def type(self, value):
        if value in ['internal', 'external']:
            self._type = value
        else:
            raise ValueError((
                "{0} is not a valid value. The allowed values are "
                "'internal' and 'external'.".format(value)
            ))

    @property
    def name(self):
        r"""
        Return a string containing the name of the dependent variable.

        The attribute is editable. For example,

        .. doctest::

            >>> y.name
            'star'
            >>> y.name = 'rock star'

        In the above example, ``y`` is an instance of the DependentVariable
        class.

        :returns: A ``String``.
        :raises TypeError: When the assigned value is not a string.
        """
        return deepcopy(self._name)

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))
        self._name = value

# Unit #
    @property
    def unit(self):
        r"""
        Return the unit associated with the dependent variable.

        The attribute cannot be modified. To convert the unit, use the
        :py:meth:`~csdfpy.DependentVariable.to` method of the class instance.

        .. doctest::

            >>> y.unit
            Unit("s W")

        :returns: A ``Unit`` object.
        :raises AttributeError: When assigned a value.
        """
        return deepcopy(self._unit)

    @unit.setter
    def unit(self, value):
        raise AttributeError(
            "`unit` attribute cannot be modified. Use the ``to`` method of "
            "the instance for the unit conversion."
        )

    @property
    def quantity(self):
        """
        Return a string with the `quantity name` of the dependent variable.

        .. doctest::

            >>> y.quantity
            'energy'

        :returns: A ``String``.
        :raises NotImplementedError: When assigning a value.
        """
        return deepcopy(self._quantity)

    @quantity.setter
    def quantity(self, value=''):
        raise NotImplementedError((
            'The `quantity` attribute is not yet mutable.'
        ))

    @property
    def encoding(self):
        r"""
        Return a string describing the encoding method for the data value.

        The value of the attribute determines the method used when
        serializing/deserializing the data values to/from a file.
        Currently, there are three `valid` encoding methods:

        | ``raw``
        | ``base64``
        | ``none``

        A value, `raw`, means that the data values are serialized as binary
        data. The value, `base64`, implies that the data values are serialized
        as base64 strings, while, the value `none` refers to text-based
        serialization.
        The attribute value can be modified with a string containing a *valid*
        encoding method, for example,

        .. doctest::

            >>> y.encoding = 'base64'

        :returns: A ``String``.
        :raises ValueError: If an invalid value is assigned.
        :raises TypeError: When the assigned value is not a string.
        """
        return self.subtype.encoding

    @encoding.setter
    def encoding(self, value):
        self.subtype.encoding = value

    @property
    def numeric_type(self):
        r"""
        Return a string describing the numeric type of the data values.

        There are currently thirteen valid numeric types:

        ==============   ============   ============   ============
        ``uint8``        ``int8``       ``float16``    ``complex64``
        ``uint16``       ``int16``      ``float32``    ``complex128``
        ``uint32``       ``int32``      ``float64``
        ``uint64``       ``int64``
        ==============   ============   ============   ============

        When assigning a value, this attribute updates the `numeric type` as
        well as the `dtype` of the Numpy array from the corresponding
        :py:attr:`~csdfpy.DependentVariable.components` attribute. We
        recommended the use of the numeric type attribute for updating
        the `dtype` of the Numpy array. For example,

        .. doctest::

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
        return self.subtype._numeric_type._value

    @numeric_type.setter
    def numeric_type(self, value):
        self.subtype._numeric_type._update(value)

    @property
    def quantity_type(self):
        r"""
        Return a string describing the quantity type of the data values.

        There are currently six *valid* quantity types,

        | ``RGB``
        | ``RGBA``
        | ``scalar``
        | ``vector_n``
        | ``matrix_n_m``
        | ``symmetric_matrix_n``

        where `n` and `m` are integers. The value of the attribute can be
        modified with a string containing a *valid* quantity type.

        .. doctest::

            >>> y.quantity_type
            'RGB'
            >>> y.quantity_type = 'vector_3'

        :returs: A ``String``.
        :raise ValueError: If an invalid value is assigned.
        :raises TypeError: When the assigned value is not a string.
        """
        return self.subtype._quantity_type._value

    @quantity_type.setter
    def quantity_type(self, value):
        self.subtype._quantity_type._update(value)

    @property
    def component_labels(self):
        r"""
        Return an ordered array of labels.

        The order of the labels are relative to the order of the array
        from the :py:attr:`~csdfpy.DependentVariable.components` attribute.

        .. doctest::

            >>> y.component_labels
            ['', '', '']

        When assigning a value, simply assign an array with same number of
        elements.

        .. doctest::

            >>> y.component_labels = ['x', 'y', 'z']

        The individual labels are accessed with proper indexing, for example,

        .. doctest::

            >>> y.component_labels[2]
            'z'

        .. todo::
            Check the component labels.

        :raises TypeError: When the assigned value is not an array of strings.
        """
        return self.subtype.component_labels

    @component_labels.setter
    def component_labels(self, value):
        self.subtype.component_labels = value

    @property
    def axis_label(self):
        r"""
        Return a formatted array of strings for displaying the label.

        This supplementary attribute is convenient for labeling axes.
        It returns an array of strings where every string at a given index
        is formatted as 'label / unit'  if the corresponding index of the
        `component_labels` array is not an empty string, otherwise,
        'quantity / unit’. Here, the `quantity`, `component_labels`, and `unit`
        are the attributes of the :ref:`dv_api` instance.
        For example,

        .. doctest::

            >>> y.component_labels[1]
            'y'
            >>> y.axis_label[1]
            'y / (s * W)'

        :returns: A ``String``.
        :raises AttributeError: When assigned a value.
        """
        labels = []
        for label in self.component_labels:
            if label.strip() == '':
                label = self.quantity
            labels.append(_axis_label(label, self._unit))
        return labels

    @property
    def components(self):
        r"""
        Return the components of the data values.

        The value of the components attribute of the dependent variable,
        :math:`y`, is a Numpy array of shape
        :math:`(p \times N_{d-1} \times ... N_1 \times N_0)` where :math:`p` is
        the number of components, and :math:`N_k` is the number of points
        from the :math:`k^\mathrm{th}` :ref:`iv_api` instance. The number
        of dimensions of this Numpy array is :math:`d+1` where :math:`d` is the
        number of independent variables or equivalently the number of
        :ref:`iv_api` instances. Note, the shape of the Numpy array follows a
        reverse order based on the ordered list of IndependentVariable
        instances,
        that is, the :math:`k^\mathrm{th}` independent variable lies along the
        :math:`(d-k)^\mathrm{th}` axis of the Numpy array. Thus, the first
        independent variable :math:`x_0` with :math:`N_0` points is the last
        axis, and the last independent variable :math:`x_{d-1}` with
        :math:`N_{d-1}` points is the first axis of the Numpy array. The
        zeroth axis with :math:`p` points is the number of components.

        This attribute can only be modified when the shape of the new array is
        the same as the shape of the components array.

        For example,

        .. doctest::

            >>> print(y.components.shape)
            (3, 10)
            >>> y.numeric_type
            'complex64'

        is a three-component dependent variable with ten data values per
        component. The numeric type of data values, in this example, is
        `complex64`. To update the components array, assign a array of
        shape (3, 10) to the `components` attribute. In the following example,
        we assign a Numpy array,

        .. doctest::

            >>> y.components = np.linspace(0,256,30, dtype='u1').reshape(3,10)
            >>> y.numeric_type
            'uint8'

        Notice, the value of the `numeric_type` attribute is automatically
        updated based on the `dtype` of the Numpy array. In this case, from a
        *complex64* to *uint8*.
        In this other example,

        .. doctest::

            >>> y.components = np.random.rand(1,10).astype('u1')
            Traceback (most recent call last):
              File "<stdin>", line 1, in <module>
              File "/Users/deepansh/Dropbox/NMRgit/MRData/csdfpy/csdfpy/dependent_variable.py", line 486, in components
                self.subtype.components = value
              File "/Users/deepansh/Dropbox/NMRgit/MRData/csdfpy/csdfpy/_dependent_variables.py", line 497, in components
                self.components.shape
            ValueError: The shape of `ndarray`, `(1, 10)`, is not consistent with the shape of the components array, `(3, 10)`.

        a `ValueError` is raised because the shape of the input array (1, 10)
        is not consistent with the shape of the components array, (3, 10).

        :returns: A ``Numpy array``.
        :raises ValueError: When assigning an array whose shape is
            not consistent with the shape of the components array.
        """
        return self.subtype.components

    @components.setter
    def components(self, value):
        self.subtype.components = value

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
        return self.subtype.components_uri

    # @property
    # def schedule(self):
    #     r"""NotImplemented."""
    #     return self.subtype._sampling_schedule

    @property
    def data_structure(self):
        r"""
        Return an instance of the DependentVariable as a JSON object instance.

        This attribute is useful for a quick view of the data structure. Note,
        the JSON object from this attribute is not the same as the one
        serialized to a file. For convenience, the values from the `components`
        attribute are truncated to the first and the last two numbers per
        component. Also, the `encoding` keyword is hidden from this view.
        The attribute cannot be modified.

        .. doctest::

            >>> print(y.data_structure)
            {
              "description": "The variable is a simulation.",
              "name": "rock star",
              "unit": "s * W",
              "quantity": "energy",
              "numeric_type": "uint8",
              "quantity_type": "vector_3",
              "component_labels": [
                "x",
                "y",
                "z"
              ],
              "components": "[0, 0, ...... 70, 70], [88, 88, ...... 158, 158], [176, 176, ...... 247, 247]"
            }

        :raises AttributeError: When modified.
        """
        dictionary = self._get_python_dictionary()
        return (json.dumps(dictionary, ensure_ascii=False,
                           sort_keys=False, indent=2))

# =========================================================================== #
#                                  Methods                                    #
# =========================================================================== #

    # def scale(self, value):
    #     r"""NotImplemented."""
    #     value = _assign_and_check_unit_consistency(value, None)
    #     self._unit = self.unit*value.unit
    #     # self.subtype.set_attribute('_unit', self.unit*value.unit)
    #     value = self.unit*value.value
    #     self.subtype.set_attribute('_components', self.components*value)

    def to(self, unit):
        r"""
        Convert the unit of the dependent variable to the `unit`.

        This method is a wrapper of the `to` method from the
        `Quantity <http://docs.astropy.org/en/stable/api/\
        astropy.units.Quantity.html#astropy.units.Quantity.to>`_ class.

        .. doctest::

            >>> y.unit
            Unit("s W")
            >>> y.to('J')
            >>> y.unit
            Unit("J")

        """
        factor = (1.0*self.unit).to(unit)
        self.subtype._components = self.subtype._components*factor.value
        self._unit = factor.unit

        # factor = (1.0*self.unit).to(unit)
        # self._components = self.components*factor.value
        # self._unit = factor.unit
        # self.subtype.set_attribute('_components', self.components*factor.value)
        # self.subtype.set_attribute('_unit', factor.unit)

    def _get_python_dictionary(self, filename=None, dataset_index=None,
                               for_display=True, version=None):
        """Return the DependentVariable instance as a python dictionary."""
        dictionary = {}

        if self.description.strip() != '':
            dictionary['description'] = self.description

        if self._name.strip() != '':
            dictionary['name'] = self._name

        if str(self._unit) != '':
            dictionary['unit'] = value_object_format(
                1.0*self._unit, numerical_value=False
            )

        if self._quantity not in ['dimensionless', 'unknown', None]:
            dictionary['quantity'] = self._quantity

        dictionary.update(
            self.subtype._get_python_dictionary(
                filename,
                dataset_index,
                for_display,
                version
            )
        )
        return dictionary

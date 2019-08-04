# -*- coding: utf-8 -*-
"""Dependent variable object: attributes and methods."""
from __future__ import division
from __future__ import print_function

import json

from csdmpy.dependent_variables.external import ExternalDataset
from csdmpy.dependent_variables.internal import InternalDataset
from csdmpy.utils import _axis_label
from csdmpy.utils import _get_dictionary


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["DependentVariable"]


class DependentVariable:
    r"""
    Create an instance of the DependentVariable class.

    The instance of this class represents a dependent variable, :math:`\mathbf{U}`.
    A dependent variable holds :math:`p`-component data values, where :math:`p>0`
    is an integer. For example, a scalar is single-component (:math:`p=1`),
    a vector may have up to `n`-components (:math:`p=n`),
    while a second rank symmetric tensor have six unique component (:math:`p=6`).

    **Creating a new dependent variable.**

    There are two ways of creating a new instance of a DependentVariable class.

    *From a python dictionary containing valid keywords.*

    .. doctest::

        >>> from csdmpy import DependentVariable
        >>> import numpy as np
        >>> numpy_array = np.arange(30).reshape(3,10).astype(np.float32)

        >>> dependent_variable_dictionary = {
        ...     'type': 'internal',
        ...     'components': numpy_array,
        ...     'name': 'star',
        ...     'unit': 'W s',
        ...     'quantity_name': 'energy',
        ...     'quantity_type': 'pixel_3'
        ... }
        >>> y = DependentVariable(dependent_variable_dictionary)

    Here, `dependent_variable_dictionary` is the python dictionary.

    *From valid keyword arguments.*

    .. doctest::

        >>> y = DependentVariable(
        ...         type='internal',
        ...         name='star',
        ...         unit='W s',
        ...         quantity_type='pixel_3',
        ...         components=numpy_array
        ...     )
    """

    __slots__ = ("subtype", "_type")

    _immutable_objects_ = ()

    def __init__(self, *args, **kwargs):
        """Initialize an instance of a DependentVariable class."""
        dictionary = {
            "type": "internal",
            "description": "",
            "name": "",
            "unit": "",
            "quantity_name": None,
            "component_labels": None,
            "encoding": "none",
            "numeric_type": None,
            "quantity_type": "scalar",
            "components": None,
            "components_url": None,
            "filename": __file__,
            "application": {},
            "sparse_sampling": {
                "dimensions": None,
                "sparse_grid_vertexes": None,
                "encoding": "none",
                "numeric_type": "int64",
                "application": {},
                "description": "",
            },
        }
        default_keys = dictionary.keys()
        input_dict = _get_dictionary(*args, **kwargs)
        input_keys = input_dict.keys()

        if "type" not in input_keys:
            raise ValueError(
                "Missing a required `type` key from the dependent variable."
            )

        if input_dict["type"] not in ["internal", "external"]:
            raise ValueError(
                (
                    "'{0}' is an invalid DependentVariable 'type'. The "
                    "allowed values are 'internal', 'external'."
                ).format(input_dict["type"])
            )

        if "quantity_type" not in input_keys:
            raise ValueError(
                "Missing a required `quantity_type` key from the dependent variable."
            )

        if input_dict["type"] == "external" and "encoding" in input_dict:
            raise ValueError(
                "The key `encoding` is invalid for dependent variables of subtype `external`."
            )

        def message(item, subtype):
            return (
                f"Missing a required `{item}` key from the dependent "
                "variable of type `{subtype}`."
            )

        if input_dict["type"] == "internal" and "components" not in input_keys:
            raise ValueError(message("components", "internal"))

        if input_dict["type"] == "external":
            if "components_url" not in input_keys:
                raise ValueError(message("components_url", "external"))

        if "filename" in kwargs.keys():
            dictionary["filename"] = kwargs["filename"]

        for key in input_keys:
            if key in default_keys and key != "sparse_sampling":
                dictionary[key] = input_dict[key]

        if "sparse_sampling" in input_keys:
            for key in input_dict["sparse_sampling"].keys():
                dictionary["sparse_sampling"][key] = input_dict["sparse_sampling"][key]
        else:
            dictionary["sparse_sampling"] = {}

        if dictionary["type"] == "internal":
            self._type = "internal"
            self.subtype = InternalDataset(**dictionary)

        if dictionary["type"] == "external":
            self._type = "external"
            self.subtype = ExternalDataset(**dictionary)

    # ======================================================================= #
    #                      DependentVariable  Attributes                      #
    # ======================================================================= #
    @property
    def application(self):
        """
        Application metadata of the DependentVariable object.

        .. doctest::

            >>> print(y.application)
            {}

        The application attribute is where an application can place its own
        metadata as a python dictionary object containing the application specific
        metadata, using a reverse domain name notation string as the attribute
        key, for example,

        .. doctest::

            >>> y.application = {
            ...     "com.example.myApp" : {
            ...         "myApp_key": "myApp_metadata"
            ...      }
            ... }
            >>> print(y.application)
            {'com.example.myApp': {'myApp_key': 'myApp_metadata'}}

        Please refer to the Core Scientific Dataset Model article for details.

        Returns:
            A python dictionary containing dependent variable application metadata.
        """
        return self.subtype.application

    @application.setter
    def application(self, value):
        self.subtype.application = value

    @property
    def axis_label(self):
        r"""
        List of formatted string labels for each component of the dependent variable.

        This attribute is not a part of the original core scientific dataset
        model, however, it is a convenient supplementary attribute that provides
        formated string ready for labeling the components of the dependent variable.
        The string at index `i` is formatted as `component_labels[i] / unit` if
        `component_labels[i]` is a non-empty string, otherwise, `quantity_name / unit`.
        Here, `quantity_name`, `component_labels`, and `unit`are the attributes of the
        :ref:`dv_api` instance. For example,

        .. doctest::

            >>> y.axis_label
            ['energy / (s * W)', 'energy / (s * W)', 'energy / (s * W)']

        Returns:
            A list of formated component label strings.

        Raises:
            AttributeError: When assigned a value.
        """
        labels = []
        for label in self.component_labels:
            if label.strip() == "":
                label = self.quantity_name
            labels.append(_axis_label(label, self.unit))
        return labels

    @property
    def component_labels(self):
        r"""
        List of labels corresponding to the components of the dependent variable.

        .. doctest::

            >>> y.component_labels
            ['', '', '']

        To update the `component_labels`, assign an array of strings with same
        number of elements as the number of components.

        .. doctest::

            >>> y.component_labels = ['channel 0', 'channel 1', 'channel 2']

        The individual labels are accessed with proper indexing, for example,

        .. doctest::

            >>> y.component_labels[2]
            'channel 2'

        .. todo::
            Check the component labels.

        Returns:
            A list of component label strings.

        Raises:
            TypeError: When the assigned value is not an array of strings.
        """
        return self.subtype.component_labels

    @component_labels.setter
    def component_labels(self, value):
        self.subtype.component_labels = value

    @property
    def components(self):
        r"""
        Component array of the dependent variable.

        The value of this attribute, :math:`\mathbb{U}`, is a Numpy array of
        shape :math:`(p \times N_{d-1} \times ... N_1 \times N_0)` where
        :math:`p` is the number of components, and :math:`N_k` is the number
        of points from the :math:`k^\mathrm{th}` :ref:`dim_api` object.

        .. note::
            The shape of the components Numpy array,
            :math:`(p \times N_{d-1} \times ... N_1 \times N_0)`, is reverse the
            shape of the components array,
            :math:`(N_0 \times N_1 \times ... N_{d-1} \times p)`, from the CSD model.
            This is because CSD model utilizes a column-major order to shape the
            components array relative to the order of the dimension while Numpy
            utilizes a row-major order.

        The dimensionality of this Numpy array is :math:`d+1` where :math:`d`
        is the number of dimension objects. The zeroth axis with :math:`p` points
        is the number of components.

        This attribute can only be updated when the shape of the new array is
        the same as the shape of the components array.

        For example,

        .. doctest::

            >>> print(y.components.shape)
            (3, 10)
            >>> y.numeric_type
            'float32'

        is a three-component dependent variable with ten data values per
        component. The numeric type of the data values, in this example, is
        `float32`. To update the components array, assign an array of
        shape (3, 10) to the `components` attribute. In the following example,
        we assign a Numpy array,

        .. doctest::

            >>> y.components = np.linspace(0,256,30, dtype='u1').reshape(3,10)
            >>> y.numeric_type
            'uint8'

        Notice, the value of the `numeric_type` attribute is automatically
        updated based on the `dtype` of the Numpy array. In this case, from a
        *float32* to *uint8*.
        In this other example,

        .. doctest::

            >>> try:
            ...     y.components = np.random.rand(1,10).astype('u1')
            ... except ValueError as e:
            ...     print(e)
            The shape of `ndarray`, `(1, 10)`, is inconsistent
            with the shape of the components array, `(3, 10)`.

        a `ValueError` is raised because the shape of the input array (1, 10)
        is not consistent with the shape of the components array, (3, 10).

        Returns:
            A Numpy array of components.

        Raises:
            ValueError: When assigning an array whose shape is not consistent with
                        the shape of the components array.
        """
        return self.subtype.components

    @components.setter
    def components(self, value):
        self.subtype.components = value

    @property
    def components_url(self):
        r"""
        URL where the data components of the dependent variable are stored.

        This attribute is only informative and cannot be modified. Its value is a
        string containing the local or remote address of the file where the data values
        are stored. The attribute is only valid for dependent variable with type,
        `external`.

        Returns:
            A string containing the URL.

        Raises:
            AttributeError: When assigned a value.
        """
        return self.subtype.components_url

    @property
    def data_structure(self):
        r"""
        Json serialized string describing the DependentVariable class instance.

        This supplementary attribute is useful for a quick preview of the dependent
        variable object. For convenience, the values from the `components` attribute
        are truncated to the first and the last two numbers per component.
        The `encoding` keyword is also hidden from this view.

        .. doctest::

            >>> print(y.data_structure)
            {
              "type": "internal",
              "description": "A test image",
              "name": "star",
              "unit": "s * W",
              "quantity_name": "energy",
              "numeric_type": "float32",
              "quantity_type": "pixel_3",
              "components": [
                [
                  "0.0, 1.0, ..., 8.0, 9.0"
                ],
                [
                  "10.0, 11.0, ..., 18.0, 19.0"
                ],
                [
                  "20.0, 21.0, ..., 28.0, 29.0"
                ]
              ]
            }

        Returns:
            A json serialized string of the dependent variable object.

        Raises:
            AttributeError: When modified.
        """
        dictionary = self._get_python_dictionary()
        return json.dumps(dictionary, ensure_ascii=False, sort_keys=False, indent=2)

    @property
    def description(self):
        """
        Brief description of the dependent variables.

        The default value is an empty string, ''.

        .. doctest::

            >>> print(y.description)
            A test image
            >>> y.description = 'A test pixel_3 image'
            >>> print(y.description)
            A test pixel_3 image

        Returns:
            A string of UTF-8 allowed characters describing the dependent variable.

        Raises:
            TypeError: When the assigned value is not a string.
        """
        return self.subtype.description

    @description.setter
    def description(self, value):
        self.subtype.description = value

    @property
    def encoding(self):
        r"""
        The encoding method used in representing the dependent variable.

        The value of this attribute determines the method used when serializing or
        deserializing the data values to and from the file. Currently, there are three
        `valid` encoding methods:

        | ``raw``
        | ``base64``
        | ``none``

        A value, `raw`, means that the data values are serialized as binary data.
        The value, `base64`, implies that the data values are serialized as base64
        strings, while, the value `none` refers to text-based serialization.

        By default, the encoding attribute of all dependent variable object are set to
        `base64` after import. The user may update this attribute, at any time, with a
        string containing a *valid* encoding literal, for example,

        .. doctest::

            >>> y.encoding = 'base64'

        The value of this attribute will be used in serializing the data to the file,
        when using the :meth:`~csdmpy.csdm.CSDM.save` method.

        Returns:
            A string with a `valid` encoding type.

        Raises:
            ValueError: If an invalid encoding value is assigned.
        """
        return self.subtype.encoding

    @encoding.setter
    def encoding(self, value):
        self.subtype.encoding = value

    @property
    def name(self):
        r"""
        Name of the dependent variable.

        .. doctest::

            >>> y.name
            'star'
            >>> y.name = 'rock star'

        Returns:
            A string containing the name of the dependent variable.

        Raises:
            TypeError: When the assigned value is not a string.
        """
        return self.subtype.name

    @name.setter
    def name(self, value):
        self.subtype.name = value

    @property
    def numeric_type(self):
        r"""
        The numeric type of the data values from the dependent variable.

        There are currently twelve *valid* numeric types:

        ==============   ============   ============   ============
        ``uint8``        ``int8``       ``float32``    ``complex64``
        ``uint16``       ``int16``      ``float64``    ``complex128``
        ``uint32``       ``int32``
        ``uint64``       ``int64``
        ==============   ============   ============   ============

        When assigning a valid value, this attribute updates the `dtype` of the
        Numpy array from the corresponding
        :attr:`~csdmpy.dependent_variables.DependentVariable.components`
        attribute. We recommended the use of the numeric type attribute for
        updating the `dtype` of the Numpy array. For example,

        .. doctest::

            >>> y.numeric_type
            'float32'

            >>> print(y.components)
            [[ 0.  1.  2.  3.  4.  5.  6.  7.  8.  9.]
             [10. 11. 12. 13. 14. 15. 16. 17. 18. 19.]
             [20. 21. 22. 23. 24. 25. 26. 27. 28. 29.]]

            >>> y.numeric_type = 'complex64'

            >>> print(y.components[:,:5])
            [[ 0.+0.j  1.+0.j  2.+0.j  3.+0.j  4.+0.j]
             [10.+0.j 11.+0.j 12.+0.j 13.+0.j 14.+0.j]
             [20.+0.j 21.+0.j 22.+0.j 23.+0.j 24.+0.j]]

        Returns:
            A string with a `valid` numeric type.

        Raises:
            ValueError: If an invalid numeric type value is assigned.
        """
        return self.subtype.numeric_type.value

    @numeric_type.setter
    def numeric_type(self, value):
        self.subtype.numeric_type = value

    @property
    def quantity_name(self):
        """
        Quantity name of the physical quantities associated with the dependent variable.

        .. doctest::

            >>> y.quantity_name
            'energy'

        Returns:
            A string with the quantity name associated with the dependent variable
            physical quantities .

        Raises:
            NotImplementedError: When assigning a value.
        """
        return self.subtype.quantity_name

    @quantity_name.setter
    def quantity_name(self, value=""):
        self.subtype.quantity_name = value

    @property
    def quantity_type(self):
        r"""
        Quantity type of the dependent variable.

        There are currently six *valid* quantity types,

        | ``scalar``
        | ``vector_n``
        | ``pixel_n``
        | ``matrix_n_m``
        | ``symmetric_matrix_n``

        where `n` and `m` are integers. The value of the attribute is modified with a
        string containing a *valid* quantity type.

        .. doctest::

            >>> y.quantity_type
            'pixel_3'
            >>> y.quantity_type = 'vector_3'

        Returns:
            A string with a `valid` quantity type.

        Raises:
            ValueError: If an invalid value is assigned.
        """
        return self.subtype.quantity_type.value

    @quantity_type.setter
    def quantity_type(self, value):
        self.subtype.quantity_type = value

    @property
    def type(self):
        """
        The dependent variable subtype.

        There are two *valid* subtypes of DependentVariable class with the following
        enumeration literals,

        | ``internal``
        | ``external``

        corresponding to Internal and External sub class. By default, all instances of
        the DependentVariable class are assigned as  `internal` upon import. The user
        may update the value of this attribute, at any time, with a string containing a
        valid `type` literal, for example,

        .. doctest::

            >>> print(y.type)
            internal

            >>> y.type = 'external'

        When `type` is external, the data values from the corresponding dependent
        variable are serialized to an external file within the same directory as the
        `.csdfe` file.

        Returns:
             A string with a `valid` dependent variable subtype.

        Raises:
            ValueError: When an invalid value is assigned.
        """
        return self._type

    @type.setter
    def type(self, value):
        if value in ["internal", "external"]:
            self._type = value
            return
        raise ValueError(
            (
                "{0} is not a valid value. The allowed values are "
                "'internal' and 'external'.".format(value)
            )
        )

    @property
    def unit(self):
        r"""
        Unit associated with the dependent variable.

        .. note::
            The attribute cannot be modified. To convert the unit, use the
            :meth:`~csdmpy.dependent_variables.DependentVariable.to` method of
            the class instance.

        .. doctest::

            >>> y.unit
            Unit("s W")

        Returns:
            A `Unit` object from astropy.unit package.

        Raises:
            AttributeError: When assigned a value.
        """
        return self.subtype.unit

    @unit.setter
    def unit(self, value):
        raise AttributeError(
            "`unit` attribute cannot be modified. Use the ``to`` method of "
            "the instance for the unit conversion."
        )

    # ======================================================================= #
    #                                  Methods                                #
    # ======================================================================= #

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

        Args:
            unit: A string containing a unit with the same dimensionality as the
                  components of the dependent variable.

        .. doctest::

            >>> y.unit
            Unit("s W")
            >>> print(y.components[0,5])
            5.0
            >>> y.to('mJ')
            >>> y.unit
            Unit("mJ")
            >>> print(y.components[0,5])
            5000.0

        .. note::
                This method is a wrapper of the `to` method from the `Quantity <http://
                docs.astropy.org/en/stable/api/\astropy.units.Quantity.html#astropy.
                units.Quantity.to>`_ class.

        """
        factor = (1.0 * self.unit).to(unit)
        self.subtype._components = self.subtype._components * factor.value
        self.subtype._unit = factor.unit

        # factor = (1.0*self.unit).to(unit)
        # self._components = self.components*factor.value
        # self._unit = factor.unit
        # self.subtype.set_attribute(
        #       '_components', self.components*factor.value
        # )
        # self.subtype.set_attribute('_unit', factor.unit)

    def _get_python_dictionary(
        self, filename=None, dataset_index=None, for_display=True, version=None
    ):
        """Return the DependentVariable instance as a python dictionary."""
        dictionary = self.subtype._get_python_dictionary(
            filename, dataset_index, for_display, version
        )
        return dictionary

# -*- coding: utf-8 -*-
"""The Dimension object: attributes and methods."""
import warnings
from copy import deepcopy

import numpy as np

from .labeled import LabeledDimension  # lgtm [py/import-own-module]
from .linear import LinearDimension  # lgtm [py/import-own-module]
from .monotonic import MonotonicDimension  # lgtm [py/import-own-module]
from csdmpy.units import string_to_quantity  # lgtm [py/import-own-module]
from csdmpy.utils import _get_dictionary  # lgtm [py/import-own-module]
from csdmpy.utils import validate  # lgtm [py/import-own-module]

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["Dimension"]


functional_dimension = ["linear"]


class Dimension:
    r"""
    Create an instance of the Dimension class.

    An instance of this class describes a dimension of a multi-dimensional system.
    In version 1.0 of the CSD model, there are three subtypes of the Dimension class:

    - :ref:`linearDimension_uml`,
    - :ref:`monotonicDimension_uml`, and
    - :ref:`labeledDimension_uml`.

    **Creating an instance of a dimension object**

    There are two ways of creating a new instance of a Dimension class.

    *From a python dictionary containing valid keywords.*

    .. doctest::

        >>> from csdmpy import Dimension
        >>> dimension_dictionary = {
        ...     'type': 'linear',
        ...     'description': 'test',
        ...     'increment': '5 G',
        ...     'count': 10,
        ...     'coordinates_offset': '10 mT',
        ...     'origin_offset': '10 T'
        ... }
        >>> x = Dimension(dimension_dictionary)

    Here, `dimension_dictionary` is the python dictionary.

    *From valid keyword arguments.*

    .. doctest::

        >>> x = Dimension(type = 'linear',
        ...               description = 'test',
        ...               increment = '5 G',
        ...               count = 10,
        ...               coordinates_offset = '10 mT',
        ...               origin_offset = '10 T')

    """

    __slots__ = ("subtype",)

    _immutable_objects_ = ()

    def __init__(self, *args, **kwargs):
        """Initialize an instance of Dimension object."""
        default = {
            "type": None,  # valid for all dimension subtypes
            "description": "",  # valid for all dimension subtypes
            "count": None,  # valid for linear subtype
            "increment": None,  # valid for linear subtype
            "labels": None,  # valid for labeled subtype
            "coordinates": None,  # valid for monotonic subtype
            "coordinates_offset": None,  # valid for linear subtype
            "origin_offset": None,  # valid for linear subtype
            "complex_fft": False,  # valid for linear subtype
            "period": None,  # valid for monotonic and linear subtypes
            "quantity_name": None,  # valid for monotonic and linear subtypes
            "label": "",  # valid for all dimension subtypes
            "application": {},  # valid for all dimension subtypes
            "reciprocal": {  # valid for monotonic and linear subtypes
                "increment": None,  # valid for monotonic and linear subtypes
                "coordinates_offset": None,  # valid for monotonic and linear subtypes
                "origin_offset": None,  # valid for monotonic and linear subtypes
                "period": None,  # valid for monotonic and linear subtypes
                "quantity_name": None,  # valid for monotonic and linear subtypes
                "label": "",  # valid for monotonic and linear subtypes
                "description": "",  # valid for monotonic and linear subtypes
                "application": {},  # valid for monotonic and linear subtypes
            },
        }

        default_keys = default.keys()
        input_dict = _get_dictionary(*args, **kwargs)
        input_keys = input_dict.keys()

        if "type" not in input_keys:
            raise KeyError("Missing a required 'type' key from the Dimension object.")

        if "reciprocal" in input_keys:
            input_subkeys = input_dict["reciprocal"].keys()
        for key in input_keys:
            if key in default_keys:
                if key == "reciprocal":
                    for subkey in input_subkeys:
                        default[key][subkey] = input_dict[key][subkey]
                else:
                    default[key] = input_dict[key]

        _valid_types = ["monotonic", "linear", "labeled"]

        type_ = default["type"]
        message = (
            f"The value, '{type_}', is invalid for the `type` attribute of the "
            "Dimension object. The allowed values are 'monotonic', 'linear' and "
            "'labeled'."
        )

        if default["type"] not in _valid_types:
            raise ValueError(message)

        if default["type"] == "labeled" and default["labels"] is None:
            raise KeyError(
                "Missing a required `labels` key from the LabeledDimension object."
            )

        if default["type"] == "labeled":
            self.subtype = LabeledDimension(**default)

        if default["type"] == "monotonic" and default["coordinates"] is None:
            raise KeyError(
                "Missing a required `coordinates` key from the MonotonicDimension "
                "object."
            )
        if default["type"] == "monotonic":
            self.subtype = MonotonicDimension(values=default["coordinates"], **default)

        if default["type"] == "linear":
            self.subtype = self._linear(default)

    def _linear(self, default):
        """Create and assign a linear dimension."""
        missing_key = ["increment", "count"]

        for item in missing_key:
            if default[item] is None:
                raise KeyError(
                    f"Missing a required `{item}` key from the LinearDimension object."
                )

        validate(default["count"], "count", int)

        return LinearDimension(**default)

    def __repr__(self):
        """String representation of object."""
        return self.subtype.__repr__()

    def __str__(self):
        """String representation of object."""
        return self.subtype.__str__()

    def __eq__(self, other):
        """Overrides the default implementation."""
        if isinstance(other, Dimension):
            if self.subtype == other.subtype:
                return True
            return False
        if isinstance(other, (LinearDimension, LabeledDimension, MonotonicDimension)):
            if self.subtype == other:
                return True
            return False
        return False

    def __mul__(self, other):
        """Multiply the Dimension object by a scalar."""
        return self.subtype.__mul__(other)

    def __imul__(self, other):
        """Multiply the Dimension object by a scalar, in-place."""
        return self.subtype.__imul__(other)

    def __truediv__(self, other):
        """Divide the Dimension object by a scalar."""
        return self.subtype.__truediv__(other)

    def __itruediv__(self, other):
        """Divide the Dimension object by a scalar, in-place."""
        return self.subtype.__itruediv__(other)

    # ======================================================================= #
    #                          Dimension Attributes                           #
    # ======================================================================= #
    @property
    def absolute_coordinates(self):
        r"""
        Absolute coordinates, :math:`\bf X_k^{\rm{abs}}`, along the dimension.

        This attribute is only *valid* for quantitative dimensions, that is,
        `linear` and `monotonic` dimensions. The absolute coordinates are given as

        .. math::

            \mathbf{X}_k^\mathrm{abs} = \mathbf{X}_k + o_k \mathbf{1}

        where :math:`\mathbf{X}_k` are the coordinates along the dimension and
        :math:`o_k` is the :attr:`~csdmpy.Dimension.origin_offset`.
        For example, consider

        .. doctest::

            >>> print(x.origin_offset)
            10.0 T
            >>> print(x.coordinates[:5])
            [100. 105. 110. 115. 120.] G

        then the absolute coordinates are

        .. doctest::

            >>> print(x.absolute_coordinates[:5])
            [100100. 100105. 100110. 100115. 100120.] G

        For `linear` dimensions, the order of the `absolute_coordinates`
        further depend on the value of the
        :attr:`~csdmpy.Dimension.complex_fft` attributes. For
        examples, when the value of the `complex_fft` attribute is True,
        the absolute coordinates are

        .. doctest::

            >>> x.complex_fft = True
            >>> print(x.absolute_coordinates[:5])
            [100075. 100080. 100085. 100090. 100095.] G

        .. testsetup::

            >>> x.complex_fft = False

        Returns:
            A Quantity array of absolute coordinates for quantitative dimensions, `i.e`
            `linear` and `monotonic`.

        Raises:
            AttributeError: For labeled dimensions.
        """
        return self.subtype.absolute_coordinates

    @property
    def application(self):
        """
        Application metadata dictionary of the dimension object.

        .. doctest::

            >>> print(x.application)
            {}

        The application attribute is where an application can place its own
        metadata as a python dictionary object containing application specific
        metadata, using a reverse domain name notation string as the attribute
        key, for example,

        .. doctest::

            >>> x.application = {
            ...     "com.example.myApp" : {
            ...         "myApp_key": "myApp_metadata"
            ...      }
            ... }
            >>> print(x.application)
            {'com.example.myApp': {'myApp_key': 'myApp_metadata'}}

        Returns:
            A python dictionary containing dimension application metadata.
        """
        return self.subtype.application

    @application.setter
    def application(self, value):
        self.subtype.application = value

    @property
    def axis_label(self):
        r"""
        Formatted string for displaying label along the dimension axis.

        This attribute is not a part of the original core scientific dataset
        model, however, it is a convenient supplementary attribute that provides
        a formated string ready for labeling dimension axes.
        For quantitative dimensions, this attributes returns a string,
        `label / unit`,  if the `label` is a non-empty string, otherwise,
        `quantity_name / unit`. Here
        :attr:`~csdmpy.Dimension.quantity_name` and
        :attr:`~csdmpy.Dimension.label` are the attributes of the
        :ref:`dim_api` instances, and `unit` is the unit associated with the
        coordinates along the dimension. For examples,

        .. doctest::

            >>> x.label
            'field strength'
            >>> x.axis_label
            'field strength / (G)'

        For `labeled` dimensions, this attribute returns `label`.

        Returns:
            A formated string of label.

        Raises:
            AttributeError: When assigned a value.
        """
        return self.subtype.axis_label

    @property
    def coordinates(self):
        r"""
        Coordinates, :math:`{\bf X}_k`, along the dimension.

        Example:
            >>> print(x.coordinates)
            [100. 105. 110. 115. 120. 125. 130. 135. 140. 145.] G

        For `linear` dimensions, the order of the `coordinates` also depend on the
        value of the :attr:`~csdmpy.Dimension.complex_fft` attributes.
        For examples, when the value of the `complex_fft` attribute is True,
        the coordinates are

        .. doctest::

            >>> x.complex_fft = True
            >>> print(x.coordinates)
            [ 75.  80.  85.  90.  95. 100. 105. 110. 115. 120.] G

        .. testsetup::

            >>> x.complex_fft = False

        Returns:
            A Quantity array of coordinates for quantitative dimensions, `i.e.` `linear`
            and `monotonic`.

        Returns:
            A Numpy array for labeled dimensions.

        Raises:
            AttributeError: For dimensions with subtype `linear`.
        """
        return self.subtype.coordinates

    @coordinates.setter
    def coordinates(self, value):
        self.subtype.coordinates = value

    @property
    def data_structure(self):
        r"""
        Json serialized string describing the Dimension class instance.

        This supplementary attribute is useful for a quick preview of the dimension
        object. The attribute cannot be modified.

        .. doctest::

            >>> print(x.data_structure)
            {
              "type": "linear",
              "description": "This is a test",
              "count": 10,
              "increment": "5.0 G",
              "coordinates_offset": "10.0 mT",
              "origin_offset": "10.0 T",
              "quantity_name": "magnetic flux density",
              "label": "field strength"
            }

        Returns:
            A json serialized string of the dimension object.
        Raises:
            AttributeError: When modified.
        """
        return self.subtype.data_structure

    @property
    def description(self):
        """
        Brief description of the dimension object.

        The default value is an empty string, ''. The attribute may be
        modified, for example,

        .. doctest::

            >>> print(x.description)
            This is a test

            >>> x.description = 'This is a test dimension.'

        Returns:
            A string of UTF-8 allows characters describing the dimension.

        Raises:
            TypeError: When the assigned value is not a string.
        """
        return self.subtype.description

    @description.setter
    def description(self, value):
        self.subtype.description = value

    @property
    def complex_fft(self):
        r"""
        If true, the coordinates are the ordered as the output of a complex fft.

        This attribute is only `valid` for the Dimension instances with `linear`
        subtype.
        The value of this attribute is a boolean specifying if the coordinates along
        the dimension are evaluated as the output of a complex fast Fourier transform
        (FFT) routine.
        For example, consider the following Dimension object,

        .. doctest::

            >>> test = Dimension(
            ...            type='linear',
            ...	           increment = '1',
            ...            count = 10
            ...        )

            >>> test.complex_fft
            False
            >>> print(test.coordinates)
            [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]

            >>> test.complex_fft = True
            >>> print(test.coordinates)
            [-5. -4. -3. -2. -1.  0.  1.  2.  3.  4.]

        Returns:
            A Boolean.

        Raises:
            TypeError: When the assigned value is not a boolean.
        """
        return self.subtype.complex_fft

    @complex_fft.setter
    def complex_fft(self, value):
        self.subtype.complex_fft = value

    @property
    def increment(self):
        r"""
        Increment along a `linear` dimension.

        The attribute is only `valid` for Dimension instances with the subtype
        `linear`. When assigning a value, the dimensionality of the value must
        be consistent with the dimensionality of other members specifying the
        dimension.

        Example:
            >>> print(x.increment)
            5.0 G
            >>> x.increment = "0.1 G"
            >>> print(x.coordinates)
            [100.  100.1 100.2 100.3 100.4 100.5 100.6 100.7 100.8 100.9] G

        Returns:
            A Quantity instance with the increment along the dimension.

        Raises:
            AttributeError: For dimension with subtypes other than `linear`.
            TypeError: When the assigned value is not a string containing a quantity
                       or a Quantity object.
        """
        # .. note:: The sampling interval along a grid dimension and the
        #     respective reciprocal grid dimension follow the Nyquist–Shannon
        #     sampling theorem. Therefore, updating the ``increment``
        #     will automatically trigger an update on its reciprocal
        #     counterpart.
        return self.subtype.increment

    @increment.setter
    def increment(self, value):
        self.subtype.increment = value

    @property
    def coordinates_offset(self):
        r"""
        Offset corresponding to the zero of the indexes array, :math:`\mathbf{J}_k`.

        When assigning a value, the dimensionality of the value must be consistent with
        the dimensionality of the other members specifying the dimension.

        Example:
            >>> print(x.coordinates_offset)
            10.0 mT
            >>> x.coordinates_offset = "0 T"
            >>> print(x.coordinates)
            [ 0.  5. 10. 15. 20. 25. 30. 35. 40. 45.] G

        The attribute is `invalid` for `labeled` dimensions.

        Returns:
            A Quantity instance with the coordinates offset.

        Raises:
            AttributeError: For `labeled` dimensions.
            TypeError: When the assigned value is not a string containing a quantity
                       or a Quantity object.
        """
        return self.subtype.coordinates_offset

    @coordinates_offset.setter
    def coordinates_offset(self, value):
        self.subtype.coordinates_offset = value

    @property
    def label(self):
        r"""
        Label associated with the dimension.

        Example:
            >>> print(x.label)
            field strength
            >>> x.label = 'magnetic field strength'

        Returns:
            A string containing the label.
        Raises:
            TypeError: When the assigned value is not a string.
        """
        return self.subtype.label

    @label.setter
    def label(self, label=""):
        self.subtype.label = label

    @property
    def count(self):
        r"""
        Number of coordinates, :math:`N_k \ge 1`, along the dimension.

        Example:
            >>> print(x.count)
            10
            >>> x.count = 5

        Returns:
            An Integer specifying the number of coordinates along the dimension.

        Raises:
            TypeError: When the assigned value is not an integer.
        """
        return self.subtype._count

    @count.setter
    def count(self, value):
        self.subtype.count = value

    @property
    def origin_offset(self):
        r"""
        Origin offset, :math:`o_k`, along the dimension.

        When assigning a value, the dimensionality of the value must be consistent
        with the dimensionality of other members specifying the dimension.

        Example:
            >>> print(x.origin_offset)
            10.0 T
            >>> x.origin_offset = "1e5 G"

        The origin offset only affect the absolute_coordinates along the dimension.
        This attribute is `invalid` for `labeled` dimensions.

        Returns:
            A Quantity instance with the origin offset.

        Raises:
            AttributeError: For `labeled` dimensions.
            TypeError: When the assigned value is not a string containing a quantity
                       or a Quantity object.
        """
        return self.subtype.origin_offset

    @origin_offset.setter
    def origin_offset(self, value):
        self.subtype.origin_offset = value

    @property
    def period(self):
        r"""
        Period of the dimension.

        The default value of the period is infinity, i.e., the dimension is
        non-periodic.

        Example:
            >>> print(x.period)
            inf G
            >>> x.period = '1 T'

        To assign a dimension as non-periodic, one of the following may be
        used,

        .. doctest::

            >>> x.period = '1/0 T'
            >>> x.period = 'infinity µT'
            >>> x.period = '∞ G'

        .. Attention::
            The physical quantity of the period must be consistent with other
            physical quantities specifying the dimension.

        Returns:
            A Quantity instance with the period of the dimension.

        Raises:
            AttributeError: For `labeled` dimensions.
            TypeError: When the assigned value is not a string containing a quantity
                       or a Quantity object.
        """
        return self.subtype.period

    @period.setter
    def period(self, value=None):
        self.subtype.period = value

    @property
    def quantity_name(self):
        r"""
        Quantity name associated with the physical quantities specifying the dimension.

        The attribute is `invalid` for the labeled dimension.

        .. doctest::

            >>> print(x.quantity_name)
            magnetic flux density

        Returns:
            A string with the `quantity name`.

        Raises:
            AttributeError: For `labeled` dimensions.
            NotImplementedError: When assigning a value.
        """
        return self.subtype.quantity_name

    @quantity_name.setter
    def quantity_name(self, value):
        self.subtype.quantity_name = value

    @property
    def type(self):
        r"""
        The dimension subtype.

        There are three *valid* subtypes of Dimension class. The valid
        literals are given by the :ref:`dimObjectSubtype_uml` enumeration.

        .. doctest::

            >>> print(x.type)
            linear

        Returns:
            A string with a valid dimension subtype.

        Raises:
            AttributeError: When the attribute is modified.
        """
        return self.subtype.type

    @property
    def labels(self):
        r"""
        Ordered list of labels along the `Labeled` dimension.

        Consider the following labeled dimension,

        .. doctest::

            >>> x2 = Dimension(
            ...         type='labeled',
            ...         labels=['Cu', 'Ag', 'Au']
            ...      )

        then the lables along the labeled dimension are

        .. doctest::

            >>> print(x2.labels)
            ['Cu' 'Ag' 'Au']

        .. note::
            For Labeled dimension, the :attr:`~csdmpy.Dimension.coordinates`
            attribute is an alias of :attr:`~csdmpy.Dimension.labels`
            attribute. For example,

            .. doctest::

                >>> np.all(x2.coordinates == x2.labels)
                True

        In the above example, ``x2`` is an instance of the :ref:`dim_api` class with
        `labeled` subtype.

        Returns:
             A Numpy array with labels along the dimension.

        Raises:
            AttributeError: For dimensions with subtype other than `labeled`.
        """
        return self.coordinates

    @labels.setter
    def labels(self, array):
        self.subtype.labels = array

    @property
    def reciprocal(self):
        r"""
        An instance of the ReciprocalDimension class.

        The attributes of ReciprocalDimension class are:
            - coordinates_offset
            - origin_offset
            - period
            - quantity_name
            - label
        where the definition of each attribute is the same as the corresponding
        attribute from the Dimension instance.
        """
        return self.subtype.reciprocal

    # ======================================================================= #
    #                           Dimension Methods                             #
    # ======================================================================= #

    def _copy_metadata(self, obj, copy=False):
        """Copy Dimension metadata"""
        self.subtype._type = obj.subtype._type
        self.subtype._copy_metadata(obj)

    def to_dict(self):
        r"""
        Return Dimension object as a python dictionary.

        Example:
            >>> x.to_dict() # doctest: +SKIP
            {'type': 'linear', 'description': 'This is a test', 'count': 10,
            'increment': '5.0 G', 'coordinates_offset': '10.0 mT',
            'origin_offset': '10.0 T', 'quantity_name': 'magnetic flux density',
            'label': 'field strength'}
        """
        return self.subtype.to_dict()

    def is_quantitative(self):
        r"""
        Return True if the dependent variable is quantitative.

        Example:
            >>> x.is_quantitative()
            True
        """
        return self.subtype.is_quantitative()

    def to(self, unit="", equivalencies=None):
        r"""
        Convert the coordinates along the dimension to the unit, `unit`.

        This method is a wrapper of the `to` method from the
        `Quantity <http://docs.astropy.org/en/stable/api/\
        astropy.units.Quantity.html#astropy.units.Quantity.to>`_ class
        and is only `valid` for physical dimensions.

        Example:
            >>> print(x.coordinates)
            [100. 105. 110. 115. 120. 125. 130. 135. 140. 145.] G
            >>> x.to('mT')
            >>> print(x.coordinates)
            [10.  10.5 11.  11.5 12.  12.5 13.  13.5 14.  14.5] mT

        Args:
            `unit` : A string containing a unit with the same dimensionality as the
                     coordinates along the dimension.

        Raises:
            AttributeError: For `labeled` dimensions.
        """
        self.subtype.to(unit, equivalencies)

    def copy(self):
        """Return a copy of the Dimension object."""
        return deepcopy(self)


def as_dimension(array, unit="", type=None, label="", description="", application={}):
    """Generate and return a Dimension object from a 1D numpy array.

    Args:
        array: A 1D numpy array.
        unit: The unit of the coordinates along the dimension.
        type: The dimension type. Valid values are linear, monotonic, labeled, or
                None. If the value is None, let us decide. The default value is None.
        label: The label along the dimension. The default value is an empty string.
        description: A description of the dimension. The default value is an empty
                string.
        application: An application dictionary. The default is an empty dictionary.

    Example:
        >>> array = np.arange(15)*0.5
        >>> dim_object = cp.as_dimension(array)
        >>> print(dim_object)
        LinearDimension([0.  0.5 1.  1.5 2.  2.5 3.  3.5 4.  4.5 5.  5.5 6.  6.5 7. ])

        >>> array = ['The', 'great', 'circle']
        >>> dim_object = cp.as_dimension(array, label='in the sky')
        >>> print(dim_object)
        LabeledDimension(['The' 'great' 'circle'])
    """
    options = [None, "linear", "monotonic", "labeled"]
    if type not in options:
        raise ValueError(f"Invalid value for `type`. Allowed values are {options}.")

    if not isinstance(array, (list, np.ndarray)):
        raise ValueError(
            f"Cannot convert {array.__class__.__name__} to a Dimension object."
        )
    if isinstance(array, list):
        array = np.asarray(array)
    if array.ndim != 1:
        raise ValueError(
            f"Cannot convert a {array.ndim} dimensional array to a Dimension object."
        )

    kwargs = {"label": label, "description": description, "application": application}

    if type is None:
        # labeled
        if str(array.dtype)[:2] in [">U", "<U"]:
            if unit != "":
                warnings.warn("Ignoring unit argument for LabeledDimension.")
            return LabeledDimension(labels=array.tolist(), **kwargs)

        # linear
        increment = array[1] - array[0]
        if increment == 0:
            raise ValueError("Invalid array for Dimension object.")

        if np.allclose(np.diff(array, 1), increment):
            return LinearDimension(
                count=array.size,
                increment=f"{increment} {unit}",
                coordinates_offset=f"{array[0]} {unit}",
                **kwargs,
            )

        # monotonic
        if np.all(np.diff(array, 1) > 0) or np.all(np.diff(array, 1) < 0):
            return MonotonicDimension(
                coordinates=array * string_to_quantity(unit), **kwargs
            )

        raise ValueError("Invalid array for Dimension object.")

    if type == "linear":
        increment = array[1] - array[0]
        if increment == 0:
            raise ValueError("Invalid array for LinearDimension object.")

        if np.all(np.diff(array, 1) == increment):
            return LinearDimension(
                count=array.size,
                increment=f"{increment} {unit}",
                coordinates_offset=f"{array[0]} {unit}",
                **kwargs,
            )

    if type == "monotonic":
        if np.all(np.diff(array, 1) > 0) or np.all(np.diff(array, 1) < 0):
            return MonotonicDimension(
                coordinates=array * string_to_quantity(unit), **kwargs
            )
        raise ValueError("Invalid array for MonotonicDimension object.")

    if type == "labeled":
        if unit != "":
            warnings.warn("Ignoring unit argument for LabeledDimension object.")
        return LabeledDimension(labels=array.tolist(), **kwargs)

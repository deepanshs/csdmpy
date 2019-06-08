# -*- coding: utf-8 -*-
"""The base ControlledVariable object: attributes and methods."""
import json
import warnings

from ._dimensions import LabeledDimension
from ._dimensions import LinearDimension
from ._dimensions import MonotonicDimension
from ._utils import _axis_label
from ._utils import _get_dictionary
from ._utils import _type_message

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


_dimension_generators = ["linear"]


class Dimension:
    r"""
    Instantiate a Dimension class.

    The instance of this class represents an independent variable, :math:`x_k`.
    There are three subtypes of the independent variables based on the
    three types of dimensions: LinearlySampledDimension,
    ArbitrarilySampledDimension, and the
    LabeledDimension, respectively.

    **A linearly sampled independent variable**

    Let :math:`m_k` be the sampling interval, :math:`N_k \ge 1` be the
    number of points, :math:`c_k` be the reference offset, and
    :math:`o_k` be the origin offset along the :math:`k^{th}`
    independent variable dimension, then the corresponding coordinates along
    the dimension are given as,

    .. math ::
        \begin{align}
        \mathbf{X}_k &= [m_k j ]_{j=0}^{N_k-1} - c_k \mathbf{1}, \\
        \mathbf{X}_k^\mathrm{abs} &= \mathbf{X}_k + o_k \mathbf{1}.
        \end{align}
        :label: eq_linear_gcv

    Here :math:`\mathbf{X}_k` and :math:`\mathbf{X}_k^\mathrm{abs}` are the
    ordered arrays of the reference and absolute independent variable
    coordinates, respectively, and :math:`\mathbf{1}` is an array of ones.

    **An monotonically sampled independent variable**

    Let :math:`\mathbf{A}_k` be an ordered array of ascending
    quantities, :math:`c_k` be the reference offset, and
    :math:`o_k` be the origin offset along the :math:`k^{th}`
    independent variable dimension, then the coordinates along this dimension
    are given as,

    .. math ::
        \begin{align}
        \mathbf{X}_k = \mathbf{A}_k - c_k \mathbf{1},\\
        \mathbf{X}_k^\mathrm{abs} = \mathbf{X}_k + o_k \mathbf{1},
        \end{align}

    where :math:`\mathbf{X}_k`, :math:`\mathbf{X}_k^\mathrm{abs}`,
    and :math:`\mathbf{1}` are the same as described in :eq:`eq_linear_gcv`.


    **A labeled independent variable**

    For labeled dimensions, the coordinates along the dimension are given as

    .. math ::
        \mathbf{X}_k = \mathbf{A}_k.

    where :math:`\mathbf{A}_k` is an array of labeled entries.

    **Creating a new independent variable.**

    There are two ways to create a new instance of an independent variable
    using this class.

    `From a python dictionary containing valid keywords.`

    .. doctest::

        >>> from csdfpy import Dimension
        >>> dimension_dictionary = {
        ...     'type': 'linear',
        ...     'description': 'test',
        ...     'increment': '5 G',
        ...     'number_of_points': 10,
        ...     'index_zero_value': '10 mT',
        ...     'origin_offset': '10 T'
        ... }
        >>> x = Dimension(dimension_dictionary)

    Here, ``dimension_dictionary`` is the python dictionary.

    `From valid keyword arguaments.`

    .. doctest::

        >>> x = Dimension(type = 'linear',
        ...               description = 'test',
        ...               increment = '5 G',
        ...               number_of_points = 10,
        ...               index_zero_value = '10 mT',
        ...               origin_offset = '10 T')

    """

    __slots__ = ("subtype",)

    _immutable_objects_ = ()

    def __init__(self, *args, **kwargs):
        """Initialize an instance of Dimension object."""
        dictionary = {
            "type": None,
            "description": "",
            "number_of_points": None,
            "increment": None,
            "values": None,
            "index_zero_value": None,
            "origin_offset": None,
            "fft_output_order": False,
            "period": None,
            "quantity": None,
            "label": "",
            "application": {},
            "reciprocal": {
                "increment": None,
                "index_zero_value": None,
                "origin_offset": None,
                "period": None,
                "quantity": None,
                "label": "",
                "description": "",
                "application": {},
            },
        }

        default_keys = dictionary.keys()
        input_dict = _get_dictionary(*args, **kwargs)
        input_keys = input_dict.keys()

        for item in self.__class__._immutable_objects_:
            if item in input_keys:
                dictionary[item] = input_dict[item]

        if "type" not in input_keys:
            raise ValueError(
                "Missing a required 'type' key in the dimension object."
            )

        if "reciprocal" in input_keys:
            input_subkeys = input_dict["reciprocal"].keys()
        for key in input_keys:
            if key in default_keys:
                if key == "reciprocal":
                    for subkey in input_subkeys:
                        dictionary[key][subkey] = input_dict[key][subkey]
                else:
                    dictionary[key] = input_dict[key]

        _valid_types = ["monotonic", "linear", "labeled"]

        if dictionary["type"] not in _valid_types:
            raise ValueError(
                (
                    "'{0}' is an invalid value for the dimension type. The "
                    "allowed values are 'monotonic', 'linear' "
                    "and 'labeled'.".format(dictionary["type"])
                )
            )

        if dictionary["type"] == "labeled":
            if dictionary["values"] is None:
                raise KeyError(
                    "'values' key is missing for the labeled dimension."
                )

            _dimension_object = LabeledDimension(
                _values=dictionary["values"],
                _label=dictionary["label"],
                _description=dictionary["description"],
                _application={},
            )

        if dictionary["type"] == "monotonic":
            if dictionary["values"] is None:
                raise KeyError(
                    "'values' key is missing for the monotonic dimension."
                )

            _dimension_object = MonotonicDimension(
                _values=dictionary["values"],
                _index_zero_value=dictionary["index_zero_value"],
                _origin_offset=dictionary["origin_offset"],
                _quantity=dictionary["quantity"],
                _period=dictionary["period"],
                _label=dictionary["label"],
                _description=dictionary["description"],
                _application={},
                _reciprocal_index_zero_value=dictionary["reciprocal"][
                    "index_zero_value"
                ],
                _reciprocal_origin_offset=dictionary["reciprocal"][
                    "origin_offset"
                ],
                _reciprocal_quantity=dictionary["reciprocal"]["quantity"],
                _reciprocal_period=dictionary["reciprocal"]["period"],
                _reciprocal_label=dictionary["reciprocal"]["label"],
                _reciprocal_description=dictionary["reciprocal"][
                    "description"
                ],
                _reciprocal_application={},
            )

        if dictionary["type"] == "linear":
            if dictionary["increment"] is None:
                raise KeyError(
                    ("'increment' key is missing for the linear dimension.")
                )
            if dictionary["number_of_points"] is None:
                raise KeyError(
                    (
                        "'number_of_points' key is missing for the "
                        "linear dimension."
                    )
                )
            if not isinstance(dictionary["number_of_points"], int):
                raise ValueError(
                    (
                        "An integer value is required for the "
                        "'number_of_points' key, {0} is provided."
                    ).format(type(dictionary["number_of_points"]))
                )

            _dimension_object = LinearDimension(
                _number_of_points=dictionary["number_of_points"],
                _increment=dictionary["increment"],
                _index_zero_value=dictionary["index_zero_value"],
                _origin_offset=dictionary["origin_offset"],
                _quantity=dictionary["quantity"],
                _period=dictionary["period"],
                _label=dictionary["label"],
                _fft_output_order=dictionary["fft_output_order"],
                _description=dictionary["description"],
                _application={},
                _reciprocal_index_zero_value=dictionary["reciprocal"][
                    "index_zero_value"
                ],
                _reciprocal_origin_offset=dictionary["reciprocal"][
                    "origin_offset"
                ],
                _reciprocal_quantity=dictionary["reciprocal"]["quantity"],
                _reciprocal_period=dictionary["reciprocal"]["period"],
                _reciprocal_label=dictionary["reciprocal"]["label"],
                _reciprocal_description=dictionary["reciprocal"][
                    "description"
                ],
                _reciprocal_application={},
            )

        self.subtype = _dimension_object

    # ======================================================================= #
    #                          Dimension Attributes                           #
    # ======================================================================= #

    # absolute_coordinates--------------------------------------------------- #
    @property
    def absolute_coordinates(self):
        r"""
        Return an array of absolute coordinates along the dimension.

        The order of the absolute coordinates depends on the value of the
        :attr:`~csdfpy.Dimension.reverse` and the
        :attr:`~csdfpy.Dimension.fft_output_order`
        (only applicable for `linear` subtype)
        attributes of the Dimension instance. This attribute cannot
        be modified. This attribute is `invalid` for the labeled dimensions.

.. doctest::

    >>> print(x.origin_offset)
    10.0 T
    >>> print(x.absolute_coordinates)
    [100100. 100105. 100110. 100115. 100120. 100125. 100130. 100135. 100140.
        100145.] G

        :returns: A ``Quantity array`` for quantitative independent variables.
        :raises AttributeError: For labeled dimension.
        :raises AttributeError: When the attribute is modified.
        """
        if self.subtype != "labeled":
            return (self.coordinates + self.origin_offset).to(
                self.subtype._unit
            )
        else:
            raise AttributeError(
                (
                    "{0} has no attribute '{1}'.".format(
                        self.subtype.__class__.__name__, "absolute_coordinates"
                    )
                )
            )

    # application------------------------------------------------------------ #
    @property
    def application(self):
        """
        Return the application metadata to the CSDM object.

        .. doctest::

            >>> print(x.application)
            {}

        Use python dict object to assign an application metadata to the CSDM
        object,

        .. doctest::

            >>> x.application = {
            ...     "com.reverse.domain" : {
            ...         "my_key": "my_metadata"
            ...      }
            ... }
            >>> print(x.application)
            {'com.reverse.domain': {'my_key': 'my_metadata'}}
        """
        return self.subtype._application

    @application.setter
    def application(self, value):
        self.subtype.application = value

    # axis label------------------------------------------------------------- #
    @property
    def axis_label(self):
        r"""
        Return a formatted string for displaying the label along the dimension.

        This supplementary attribute is convenient for labeling axes.
        For quantitative independent variables, this attributes returns a
        string, `label / unit`,  if the `label` is not an empty string. If the
        `label` is an empty string, `quantity / unit` is returned instead. Here
        :attr:`~csdfpy.Dimension.quantity` and
        :attr:`~csdfpy.Dimension.label` are the attributes of the
        :ref:`iv_api` instances, and `unit` is the unit associated with the
        coordinates along the dimension.

        .. doctest::

            >>> x.label
            'field strength'
            >>> x.axis_label
            'field strength / (G)'

        For labled dimensions, this attribute returns 'label'.

        :returns: A ``String``.
        :raises AttributeError: When assigned a value.
        """
        if hasattr(self.subtype, "quantity"):
            if self.label.strip() == "":
                label = self.quantity
            else:
                label = self.label
            return _axis_label(label, self.subtype._unit)
        else:
            return self.label

    # coordinates------------------------------------------------------------ #
    @property
    def coordinates(self):
        r"""
        Return an array of reference coordinates along the dimension.

        The order of the reference coordinates
        depends on the value of the :attr:`~csdfpy.Dimension.reverse`
        and the :attr:`~csdfpy.Dimension.fft_output_order`
        (only applicable for `linear` subtype)
        attributes of the class instance. This attribute cannot be modified.

        .. doctest::

            >>> print(x.coordinates)
            [100. 105. 110. 115. 120. 125. 130. 135. 140. 145.] G

        :returns: A ``Quantity array`` for quantitative independent variables.
        :returns: A ``Numpy array`` for labeled dimensions.
        :raises AttributeError: When the attribute is modified.
        """
        _n = self.subtype._number_of_points
        coordinates = self.subtype._coordinates[:_n]
        if self.type != "linear":
            return coordinates
        else:
            return (coordinates + self.index_zero_value).to(self.subtype._unit)

    # data_structure--------------------------------------------------------- #
    @property
    def data_structure(self):
        r"""
        Return an :ref:`iv_api` instance as a JSON object.

        This supplementary attribute is useful for a quick preview of the data
        structure. The attribute cannot be modified.

        .. doctest::

            >>> print(x.data_structure)
            {
              "type": "linear",
              "description": "This is a test",
              "number_of_points": 10,
              "increment": "5.0 G",
              "index_zero_value": "10.0 mT",
              "origin_offset": "10.0 T",
              "quantity": "magnetic flux density",
              "label": "field strength"
            }

        :raises AttributeError: When modified.
        """
        dictionary = self._get_python_dictionary()
        return json.dumps(
            dictionary, ensure_ascii=False, sort_keys=False, indent=2
        )

    # description------------------------------------------------------------ #
    @property
    def description(self):
        """
        Brief description of the dimension object.

        The default value is an empty string, ''. The attribute can be
        modified, for example

        .. doctest::

            >>> print(x.description)
            This is a test

            >>> x.description = 'This is a test dimension.'

        :returns: A ``string`` with UTF-8 allows characters.
        :raises ValueError: When the non-string value is assigned.
        """
        return self.subtype._description

    @description.setter
    def description(self, value):
        self.subtype._description = value

    # fft_ouput_order-------------------------------------------------------- #
    @property
    def fft_output_order(self):
        r"""
        Return the coordinates along the dimension according to the fft order.

        This attribute is only `valid` for the Dimension instances
        with subtype `linear`.
        The value of the attribute is a boolean specifying if the coordinates
        along the dimension are ordered according to the output of a
        fast Fourier transform (FFT) routine. The
        universal behavior of all FFT routine is to order the :math:`N_k`
        output amplitudes by placing the zero `frequency` at the start
        of the output array, with positive `frequencies` increasing in
        magnitude placed at increasing array offset until reaching
        :math:`\frac{N_k}{2} -1` if :math:`N_k` is even, otherwise
        :math:`\frac{N_k-1}{2}`, followed by negative frequencies
        decreasing in magnitude until reaching :math:`N_k-1`.
        This is also the ordering needed for the input of the inverse FFT.
        For example, consider the coordinates along the dimension as

        .. math ::

            \mathbf{X}_k^\mathrm{ref} = [0, 1, 2, 3, 4, 5] \mathrm{~m/s}

        when the value of the fft_output_order attribute is `false`, then when
        the value is `true`, the order follows

        .. math ::

            \mathbf{X}_k^\mathrm{ref} = [0 ,1, 2, -3, -2, -1] \mathrm{~m/s}

        The following is a test example.

        .. doctest::

            >>> test = Dimension(
            ...            type='linear',
            ...	           increment = '1',
            ...            number_of_points = 10
            ...        )

            >>> print(test.coordinates)
            [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]
            >>> test.fft_output_order
            False

            >>> test.fft_output_order = True
            >>> print(test.coordinates)
            [ 0.  1.  2.  3.  4. -5. -4. -3. -2. -1.]

        :returns: A ``Boolean``.
        :raises TypeError: When the assigned value is not a boolean.
        """
        return self.subtype.fft_output_order

    @fft_output_order.setter
    def fft_output_order(self, value):
        self.subtype.fft_output_order = value

    # increment------------------------------------------------------------ #
    @property
    def increment(self):
        r"""
        Return the increment along the dimension.

        The attribute is only `valid` for Dimension instances with
        the subtype `linear`. When assigning,
        the dimensionality of the value must be consistent with the
        dimensionality of other members specifying the dimension.
        Additionally, the sampling interval must be a positive real number.
        The value is assigned as a string containing the sampling interval,
        for example,

        .. doctest::

            >>> print(x.increment)
            5.0 G
            >>> x.increment = "0.1 G"
            >>> print(x.coordinates)
            [100.  100.1 100.2 100.3 100.4 100.5 100.6 100.7 100.8 100.9] G

        :returns: A ``Quantity`` instance with the sampling interval.
        :raises AttributeError: For dimension with subtypes other than
                                `linear`.
        :raises TypeError: When the assigned value is not a string.
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

    # index zero value------------------------------------------------------- #
    @property
    def index_zero_value(self):
        r"""
        Return the value at the zeroth index of the dimension.

        When assigning a value, the dimensionality of the value
        must be consistent with the dimensionality of the other members
        specifying the dimension. The value is assigned as a string
        containing the reference offset,
        for example,

        .. doctest::

            >>> print(x.index_zero_value)
            10.0 mT
            >>> x.index_zero_value = "0 T"
            >>> print(x.coordinates)
            [ 0.  5. 10. 15. 20. 25. 30. 35. 40. 45.] G

        The attribute is `invalid` for the labeled dimensions.

        :returns: A ``Quantity`` instance with the reference offset.
        :raises AttributeError: For the labeled dimensions.
        :raises TypeError: When the assigned value is not a string.
        """
        if self.type == "linear":
            return self.subtype.index_zero_value
        else:
            raise AttributeError(
                ("`{0}` has no attribute `index_zero_value`.").format(
                    self.subtype.__class__.__name__
                )
            )

    @index_zero_value.setter
    def index_zero_value(self, value):
        self.subtype.index_zero_value = value

    # label------------------------------------------------------------------ #
    @property
    def label(self):
        r"""
        Return the label associated with the dimension.

        The attribute is modified with a string containing the label, for
        example,

        .. doctest::

            >>> print(x.label)
            field strength
            >>> x.label = 'magnetic field strength'
            >>> print(x.axis_label)
            magnetic field strength / (G)

        :returns: A ``String`` containing the label.
        :raises TypeError: When the assigned value is not a string.
        """
        return self.subtype.label

    @label.setter
    def label(self, label=""):
        self.subtype.label = label

    # number_of_points------------------------------------------------------- #
    @property
    def number_of_points(self):
        r"""
        Return the number of points, :math:`N_k \ge 1`, along the dimension.

        The attribute is modified with an integer specifying the number of
        points along the dimension, for example,

        .. doctest::

            >>> print(x.number_of_points)
            10
            >>> x.number_of_points = 5

        :returns: An ``Integer`` with the number of points.
        :raises TypeError: When the assigned value is not an integer.
        """
        return self.subtype._number_of_points

    @number_of_points.setter
    def number_of_points(self, value):
        if not isinstance(value, int):
            raise TypeError(_type_message(int, type(value)))

        if value <= 0:
            raise ValueError(
                ("A positive integer value is required, given {0}.").format(
                    value
                )
            )

        if self.type not in _dimension_generators:
            if value > self.number_of_points:
                raise ValueError(
                    (
                        "Cannot set the number of points, {0}, more than the"
                        "number of coordinates, {1}, for monotonic and labeled"
                        " dimensions."
                    ).format(value, self.number_of_points)
                )

            if value < self.number_of_points:
                warnings.warn(
                    (
                        "The number of coordinates, {0}, are truncated to {1}."
                    ).format(self.number_of_points, value)
                )
                self.subtype._number_of_points = value

        else:
            self.subtype._number_of_points = value
            self.subtype._get_coordinates()

    # origin offset---------------------------------------------------------- #
    @property
    def origin_offset(self):
        r"""
        Return the origin offset, :math:`o_k`, along the dimension.

        When assigning a value, the dimensionality of the value
        must be consistent with the dimensionality of other members specifying
        the dimension. The value is assigned as a string containing the
        origin offset, for example,

        .. doctest::

            >>> print(x.origin_offset)
            10.0 T
            >>> x.origin_offset = "1e5 G"

        The origin offset only affect the absolute_coordinates along the
        dimension. This attribute is `invalid` for the labeled dimensions.

        :returns: A ``Quantity`` instance with the origin offset.
        :raises AttributeError: For the labeled dimensions.
        :raises TypeError: When the assigned value is not a string.
        """
        return self.subtype.origin_offset

    @origin_offset.setter
    def origin_offset(self, value):
        self.subtype.origin_offset = value

    # period----------------------------------------------------------------- #
    @property
    def period(self):
        r"""
        Return the period of a quantitative independent variable dimension.

        The default value of the period is infinity, i.e., the dimension is
        non-periodic. The attribute is modified with a
        string containing a quantity which represents the period of the
        dimension. For example,

        .. doctest::

            >>> print(x.period)
            inf G
            >>> x.period = '1 T'

        To assign a dimension as non-periodic, one of the following may be
        used,

        .. doctest::

            >>> x.period = '1/0 T'
            >>> x.period = 'infinity µT'
            >>> x.period = '∞ G'

        :return: A ``Quantity`` instance with the period of the independent
                 variables.
        :raises AttributeError: For the labeled dimensions.
        :raises TypeError: When the assigned value is not a string.
        """
        return self.subtype.period

    @period.setter
    def period(self, value=None):
        self.subtype.period = value

    # quantity--------------------------------------------------------------- #
    @property
    def quantity(self):
        r"""
        Return the `quantity name` associated with the dimension.

        The attribute is `invalid` for the labeled dimension.

        .. doctest::

            >>> print(x.quantity)
            magnetic flux density

        :returns: A string with the `quantity name`.
        :raises AttributeError: For labeled dimensions.
        :raises NotImplementedError: When assigning a value.
        """
        return self.subtype.quantity

    @quantity.setter
    def quantity(self, value):
        self.subtype.quantity = value

    # type------------------------------------------------------------------- #
    @property
    def type(self):
        r"""
        Return the dimension type of the independent variable.

        There are three types of dimensions: LinearDimension,
        MonotonicDimension, and LabeledDimension with `type` names as
        `linear`, `monotonic` and `labeled`, respectively.
        This attribute cannot be modified.

        .. doctest::

            >>> print(x.type)
            linear

        :returns: A ``String``.
        :raises AttributeError: When the attribute is modified.
        """
        return self.subtype.__class__._type

    # values----------------------------------------------------------------- #
    @property
    def values(self):
        r"""
        Ordered array of values along the dimension.

        For dimensions with monotonically spaced coordinates, this array is
        an ascending order of physical quantities.

        .. doctest::

            >>> x1 = Dimension(
            ...         type='monotonic',
            ...         values=['0cm', '4.1µm', '0.3mm', '5.8m', '32.4km']
            ...      )
            >>> print(x1.data_structure)
            {
              "type": "monotonic",
              "values": [
                "0cm",
                "4.1µm",
                "0.3mm",
                "5.8m",
                "32.4km"
              ],
              "quantity": "length",
              "reciprocal": {
                "quantity": "wavenumber"
              }
            }

        For labeled dimensions, this array is an ordered collection of UTF-8
        allowed strings.

        .. doctest::

            >>> x2 = Dimension(
            ...         type='labeled',
            ...         values=['Cu', 'Ag', 'Au']
            ...      )
            >>> print(x2.data_structure)
            {
              "type": "labeled",
              "values": [
                "Cu",
                "Ag",
                "Au"
              ]
            }

        In the above examples, ``x1`` and ``x2`` are the instances of the
        :ref:`iv_api` class associated with the monotonically sampled
        and the labeled dimensions respectively.

        :returns: A ``Quantity array`` for dimensions with subtype
                  `arbitarily_sampled`.
        :returns: A ``Numpy array`` for dimensions with subtype `labeled`.
        :raises AttributeError: For dimensions with subtype `linear`.

        """
        # .. todo:
        #     raise type error if the values are not strings or numpy array
        #     of stings.
        # """
        return self.subtype.values

    @values.setter
    def values(self, array):
        self.subtype.values = array
        self.subtype._get_coordinates(array)

    # ======================================================================= #
    #                            Additional Attributes                        #
    # ======================================================================= #

    # reciprocal

    @property
    def reciprocal(self):
        r"""
        Return an instance of the ReciprocalVariable class.

        The attributes of ReciprocalVariable class are:
            - index_zero_value
            - origin_offset
            - period
            - quantity
            - label
        where the definision of each attribute is the same as the corresponding
        attribure from the Dimension instance.
        """
        return self.subtype.reciprocal

    # ======================================================================= #
    #                                  Methods                                #
    # ======================================================================= #

    # _get_python_dictionary()
    def _get_python_dictionary(self):
        r"""Return the Dimension instance as a python dictionary."""
        return self.subtype._get_python_dictionary()

    # is_quantitative()
    def is_quantitative(self):
        r"""Return True if the independent variable is quantitative."""
        return self.subtype._is_quantitative()

    # to()
    def to(self, unit="", equivalencies=None):
        r"""
        Convert the unit of the independent variable coordinates to `unit`.

        This method is a wrapper of the `to` method from the
        `Quantity <http://docs.astropy.org/en/stable/api/\
        astropy.units.Quantity.html#astropy.units.Quantity.to>`_ class
        and is only `valid` for physical dimensions.

        For example,

        .. doctest::

            >>> print(x.coordinates)
            [100. 105. 110. 115. 120. 125. 130. 135. 140. 145.] G
            >>> x.to('mT')
            >>> print(x.coordinates)
            [10.  10.5 11.  11.5 12.  12.5 13.  13.5 14.  14.5] mT

        :params: `unit` : A string containing a unit with the same
            dimensionality as the coordinates along the dimension.
        :raise AttributeError: For the labeled dimensions.
        """
        self.subtype._to(unit, equivalencies)

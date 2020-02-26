# -*- coding: utf-8 -*-
"""THE CSDM object"""
from __future__ import division
from __future__ import print_function

import datetime
import json
from copy import deepcopy

import numpy as np
from astropy.units.quantity import Quantity

from csdmpy.abstract_list import __dimensions_list__  # lgtm [py/import-own-module]
from csdmpy.abstract_list import DependentVariableList  # lgtm [py/import-own-module]
from csdmpy.abstract_list import DimensionList  # lgtm [py/import-own-module]
from csdmpy.dependent_variables import (  # lgtm [py/import-own-module] # noqa: F401
    as_dependent_variable,
)  # lgtm [py/unused-import]
from csdmpy.dependent_variables import DependentVariable  # lgtm [py/import-own-module]
from csdmpy.dimensions import as_dimension  # lgtm [py/import-own-module]
from csdmpy.dimensions import Dimension  # lgtm [py/import-own-module] # noqa: F401
from csdmpy.dimensions import (  # lgtm [py/import-own-module] # noqa: F401
    LabeledDimension,
)  # lgtm [py/unused-import]
from csdmpy.dimensions import (  # lgtm [py/import-own-module] # noqa: F401
    LinearDimension,
)
from csdmpy.dimensions import (  # lgtm [py/import-own-module] # noqa: F401
    MonotonicDimension,
)  # lgtm [py/unused-import]
from csdmpy.units import string_to_quantity  # lgtm [py/import-own-module]
from csdmpy.utils import _get_broadcast_shape  # lgtm [py/import-own-module]
from csdmpy.utils import check_scalar_object  # lgtm [py/import-own-module]
from csdmpy.utils import validate  # lgtm [py/import-own-module]

__all__ = ["CSDM"]
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

__function_reduction_list__ = [np.max, np.min, np.sum, np.mean, np.var, np.std, np.prod]

__other_functions__ = [np.round, np.real, np.imag, np.clip, np.around, np.angle]

__shape_manipulation_functions__ = [np.transpose]


class CSDM:
    r"""
    Create an instance of a CSDM class.

    This class is based on the root CSDM object of the core scientific dataset
    (CSD) model. The class is a composition of the :ref:`dv_api` and
    :ref:`dim_api` instances, where an instance of the :ref:`dv_api` class
    describes a :math:`p`-component dependent variable, and an instance of the
    :ref:`dim_api` class describes a dimension of a :math:`d`-dimensional
    space. Additional attributes of this class are listed below.
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

    def __init__(self, filename="", version=None, description="", **kwargs):
        """Python module from reading and writing csdm files."""
        if version is None:
            version = self.__latest_CSDM_version__
        elif version in self._old_incompatible_versions:
            raise Exception(
                f"Files created with the version {version} of the CSD Model "
                "are no longer supported."
            )

        self._tags = []
        self._read_only = False
        self._version = version
        self._timestamp = ""
        self._geographic_coordinate = {}
        self._description = description
        self._application = {}
        self._filename = filename

        kwargs_keys = kwargs.keys()

        self._dimensions = DimensionList([])
        if "dimensions" in kwargs_keys:
            if not isinstance(kwargs["dimensions"], list):
                t_ = type(kwargs["dimensions"])
                raise ValueError(
                    f"A list of valid Dimension objects or equivalent dictionary "
                    f"objects is required, found {t_}"
                )

            for item in kwargs["dimensions"]:
                self.add_dimension(item)

        self._dependent_variables = DependentVariableList([])
        if "dependent_variables" in kwargs_keys:
            t_ = type(kwargs["dependent_variables"])
            if not isinstance(kwargs["dependent_variables"], list):
                raise ValueError(
                    f"A list of valid DependentVariable objects or equivalent "
                    f"dictionary objects is required, found {t_}"
                )
            for item in kwargs["dependent_variables"]:
                self.add_dependent_variable(item)

    def __repr__(self):
        keys = (
            "dimensions",
            "dependent_variables",
            "tags",
            "read_only",
            "version",
            "timestamp",
            "geographic_coordinate",
            "description",
            "application",
        )
        prop = ", ".join([f"{k}={getattr(self, k).__repr__()}" for k in keys])
        return f"CSDM({prop})"

    def __str__(self):
        prop_dv = ",\n".join([item.__str__() for item in self.dependent_variables])
        prop_dim = ",\n".join([item.__str__() for item in self.dimensions])
        if prop_dv == "":
            return f"CSDM(\n{prop_dim}\n)"
        if prop_dim == "":
            return f"CSDM(\n{prop_dv}\n)"
        return f"CSDM(\n{prop_dv},\n{prop_dim}\n)"

    def __check_csdm_object(self, other, operator=""):
        """Check if the two objects are csdm objects"""
        if not isinstance(other, CSDM):
            raise TypeError(
                f"unsupported operand type(s) {operator}: 'CSDM' and "
                f"'{other.__class__.__name__}'."
            )

    def __check_dimension_equality(self, other):
        """Check if the dimensions of the two csdm objects are identical."""
        if self.dimensions != other.dimensions:
            raise Exception(
                f"Cannot operate on CSDM objects with different dimensions."
            )

    def __check_dependent_variable_len_equality(self, other):
        """
        Check if the length of dependent variables from the two csdm objects is equal.
        """
        if len(self.dependent_variables) != len(other.dependent_variables):
            raise Exception(
                "Cannot operate on CSDM objects with differnet lengths of "
                "dependent variables."
            )

    def __check_dependent_variable_dimensionality(self, other):
        """
        Check if the dependent variables from the two csdm objects have the same
        dimensionality.
        """
        for v1, v2 in zip(self.dependent_variables, other.dependent_variables):
            if v1.unit.physical_type != v2.unit.physical_type:
                raise Exception(
                    "Cannot operate on dependent variables with physical types: "
                    f"{v1.unit.physical_type} and {v2.unit.physical_type}."
                )

    def __check_csdm_object_additive_compatibility(self, other):
        """
            Check if the two objects are compatible for additive operations
                1) csdm objects,
                2) with identical dimension objects,
                3) same number of dependent-variables, and
                4) each dependent variables with identical dimensionality.
        """
        # self.__check_csdm_object(other)
        self.__check_dimension_equality(other)
        self.__check_dependent_variable_len_equality(other)
        self.__check_dependent_variable_dimensionality(other)

    def __eq__(self, other):
        """Check the other object is a CSDM object with identical attribute values.
        This does not check for the timestamp attribute."""
        if not isinstance(other, CSDM):
            return False
        check = [
            self.dimensions == other.dimensions,
            self.dependent_variables == other.dependent_variables,
            self.tags == other.tags,
            self.read_only == other.read_only,
            self.version == other.version,
            # self.timestamp == other.timestamp,
            self.geographic_coordinate == other.geographic_coordinate,
            self.description == other.description,
            self.application == other.application,
        ]
        if np.all(check):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __neg__(self):
        """Return negative of self."""
        return np.negative(self)

    def __pos__(self):
        """Return positive of self."""
        return self

    def __abs__(self):
        """Return absolute of self."""
        return np.absolute(self)

    # def __complex__(self):
    #     """Return self as complex."""
    #     return self.astype(complex)

    # def __int__(self):
    #     """Return self as int."""
    #     return self.astype(int)

    # def __float__(self):
    #     """Return self as float."""
    #     return self.astype(float)

    # def __invert__(self):
    #     raise NotImplementedError("")

    # def __lshift__(self, other):
    #     raise NotImplementedError()

    # def __ilshift__(self, other):
    #     raise NotImplementedError()

    # def __rshift__(self, other):
    #     raise NotImplementedError()

    # def __irshift__(self, other):
    #     raise NotImplementedError()

    def __ifunction__(self, function, symbol, other):

        if isinstance(other, CSDM):
            self.__check_csdm_object_additive_compatibility(other)

            for i, item in enumerate(self.dependent_variables):
                factor = other.dependent_variables[i].unit.to(item.unit)
                fn = getattr(item.components, function)
                fn(factor * other.dependent_variables[i].components)
            return self

        other = check_scalar_object(other, symbol)

        for i, item in enumerate(self.dependent_variables):
            fn = getattr(item.components, function)
            if not isinstance(other, Quantity):
                fn(other)
            else:
                factor = other.unit.to(item.unit)
                fn(factor * other.value)
        return self

    def __add__(self, other):
        """
        Add two objects (z=x+y), if the other object is a
            1) csdm or scalar object,
            2) with identical dimension objects,
            3) same number of dependent-variables, and
            4) each dependent variables with identical dimensionality.
        """
        if isinstance(other, CSDM):
            self.__check_csdm_object_additive_compatibility(other)

            d1 = self.copy()
            for i, item in enumerate(d1.dependent_variables):
                factor = other.dependent_variables[i].unit.to(item.unit)
                item.components = (
                    item.components + factor * other.dependent_variables[i].components
                )
            return d1

        other = check_scalar_object(other, "+")
        d1 = self.copy()
        for i, item in enumerate(d1.dependent_variables):
            if not isinstance(other, Quantity):
                item.components = item.components + other
            else:
                factor = other.unit.to(item.unit)
                item.components = item.components + factor * other.value
        return d1

    def __radd__(self, other):
        """Right add two objects. See __add__ for details."""
        return self.__add__(other)

    def __iadd__(self, other):
        """Add two objects in-place (y+=x).  See __add__ for details."""
        return self.__ifunction__("__iadd__", "+", other)

    def __sub__(self, other):
        """
        Subtract two objects (z=x-y), if the other is
            1) csdm or scalar object,
            2) with identical dimension objects,
            3) same number of dependent-variables, and
            4) each dependent variables with identical dimensionality.
        """
        if isinstance(other, CSDM):
            self.__check_csdm_object_additive_compatibility(other)

            d1 = self.copy()
            for i, item in enumerate(d1.dependent_variables):
                factor = other.dependent_variables[i].unit.to(item.unit)
                item.components = (
                    item.components - factor * other.dependent_variables[i].components
                )
            return d1

        other = check_scalar_object(other, "-")
        d1 = self.copy()
        for i, item in enumerate(d1.dependent_variables):
            if not isinstance(other, Quantity):
                item.components = item.components - other
            else:
                factor = other.unit.to(item.unit)
                item.components = item.components - factor * other.value
        return d1

    def __rsub__(self, other):
        """Right subtract two objects. See __sub__ for details."""
        return -self.__sub__(other)

    def __isub__(self, other):
        """Subtract two objects in-lace (y-=x). See __sub__ for details. """
        return self.__ifunction__("__isub__", "-", other)

    def __mul__(self, other):
        """Multiply the components of the CSDM object by a scalar."""
        other = check_scalar_object(other, "*")

        d1 = self.copy()
        for item in d1.dependent_variables:
            if not isinstance(other, Quantity):
                item.components = item.components * other
            else:
                value = 1 * item.subtype._unit * other
                item.subtype._unit = value.unit
                item.components = item.components * value.value
        return d1

    def __rmul__(self, other):
        """Right multiply the components of the CSDM object by a scalar."""
        return self.__mul__(other)

    def __imul__(self, other):
        """In place multiplication of the components of the CSDM object by a scalar."""

        other = check_scalar_object(other, "*")

        for item in self.dependent_variables:
            if not isinstance(other, Quantity):
                item.components *= other
            else:
                value = 1 * item.subtype._unit * other
                item.subtype._unit = value.unit
                item.components.__imul__(value.value)
        return self

    def __truediv__(self, other):
        """Divide the components of the CSDM object by a scalar."""
        other = check_scalar_object(other, "/")

        d1 = self.copy()
        for item in d1.dependent_variables:
            if not isinstance(other, Quantity):
                item.components = item.components / other
            else:
                value = (1 * item.subtype._unit) / other
                item.subtype._unit = value.unit
                item.components = item.components * value.value
        return d1

    def __rtruediv__(self, other):
        """Right divide the components of the CSDM object by a scalar."""
        return np.reciprocal(self) * other

    def __itruediv__(self, other):
        """In place division of the components of the CSDM object by a scalar."""
        other = check_scalar_object(other, "/")

        for item in self.dependent_variables:
            if not isinstance(other, Quantity):
                item.components *= 1 / other
            else:
                value = (1 * item.subtype._unit) / other
                item.subtype._unit = value.unit
                item.components *= value.value
        return self

    def __pow__(self, other):
        """Raise the components of the CSDM object to a scalar value."""
        other = check_scalar_object(other, "**")
        return np.power(self, other)

    def __ipow__(self, other):
        """Raise the components of the CSDM object to a scalar value."""
        other = check_scalar_object(other, "**")
        for item in self.dependent_variables:
            item.components.__ipow__(other)
            item.subtype._unit = item.subtype._unit ** other
        return self

    def _get_indices(self, indices):
        if isinstance(indices, tuple):
            l_ = len(indices)
            indices = indices + tuple(
                [slice(0, _.count, 1) for _ in self.dimensions[l_:]]
            )
        if isinstance(indices, (int, slice)):
            indices = (indices,) + tuple(
                [slice(0, _.count, 1) for _ in self.dimensions[1:]]
            )
        for item in indices:
            if isinstance(item, (tuple, list)):
                raise NotImplementedError(
                    "CSDMpy supports the grid base scientific dataset described in the"
                    " Core Scientific dataset model. Fancy indexing using tuples or "
                    "lists may result in a scatter dataset, and is not implemented in "
                    "the current version."
                )
        return indices

    def __setitem__(self, indices, values):
        indices = self._get_indices(indices)
        for variable in self.dependent_variables:
            section = (slice(0, len(variable.components), 1),) + indices[::-1]
            variable.components[section] = values

    def __getitem__(self, indices):
        """Return a csdm object corresponding to given indices."""
        indices = self._get_indices(indices)
        csdm = CSDM()
        for i, dim in enumerate(self.dimensions):
            s_ = indices[i]

            dim_ = dim
            if hasattr(dim, "subtype"):
                dim_ = dim.subtype

            length_ = dim.coordinates[s_].size
            if length_ > 1:
                if hasattr(dim_, "_equivalencies"):
                    equivalencies_ = dim_._equivalencies
                    dim_._equivalencies = None
                    x = dim.coordinates[s_]
                    new_dim = as_dimension(x.value, unit=str(x.unit))
                    dim_._equivalencies = equivalencies_
                    new_dim._equivalencies = equivalencies_

                else:
                    x = dim.coordinates[s_]
                    new_dim = as_dimension(x)

                new_dim._copy_metadata(dim_)
                if hasattr(new_dim, "complex_fft"):
                    new_dim.complex_fft = False

                if hasattr(dim_, "_equivalencies"):
                    dim_._equivalencies = equivalencies_
                    new_dim._equivalencies = equivalencies_

                csdm._dimensions += [new_dim]

        for variable in self.dependent_variables:
            section = (slice(0, len(variable.components), 1),) + indices[::-1]
            y = variable.components[section]
            dv = empty_dependent_variable(variable.numeric_type)
            dv.subtype._components = y
            dv._copy_metadata(variable)
            csdm._dependent_variables += [dv]

        csdm._copy_metadata(self)
        return csdm

    def _copy_metadata(self, other):
        self._version = other._version
        self._description = other._description
        self._read_only = other._read_only
        self._tags = other._tags
        self._timestamp = other._timestamp
        self._geographic_coordinate = other._geographic_coordinate
        self._application = other._application
        self._filename = other._filename

    # ----------------------------------------------------------------------- #
    #                                Attributes                               #
    # ----------------------------------------------------------------------- #
    @property
    def version(self):
        """Version number of the CSD model on file."""
        return self._version

    @property
    def description(self):
        """Description of the dataset. The default value is an empty string.

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
    def read_only(self):
        """
        If True, the data-file is serialized as read only, otherwise, False.

        By default, the :ref:`csdm_api` object loads a copy of the .csdf(e) file,
        irrespective of the value of the `read_only` attribute. The value of this
        attribute may be toggled at any time after the file import.
        When serializing the `.csdf(e)` file, if the value of the `read_only`
        attribute is found True, the file will be serialized as read only.
        """
        return self._read_only

    @read_only.setter
    def read_only(self, value):
        self._read_only = validate(value, "read_only", bool)

    @property
    def tags(self):
        """List of tags attached to the dataset."""
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = validate(value, "tags", list)

    @property
    def timestamp(self):
        """
        Timestamp from when the file was last serialized. This attribute is real only.

        The timestamp stamp is a string representation of the Coordinated Universal
        Time (UTC) formatted according to the iso-8601 standard.

        Raises:
            AttributeError: When the attribute is modified.
        """
        return self._timestamp

    @property
    def geographic_coordinate(self):
        """
        Geographic coordinate, if present, from where the file was last serialized.
        This attribute is read-only.

        The geographic coordinates correspond to the location where the file was last
        serialized. If present, the geographic coordinates are described with three
        attributes, the required latitude and longitude, and an optional altitude.

        Raises:
            AttributeError: When the attribute is modified.
        """
        return self._geographic_coordinate

    @property
    def dimensions(self):
        """Tuple of the :ref:`dim_api` instances."""
        return self._dimensions

    @property
    def dependent_variables(self):
        """Tuple of the :ref:`dv_api` instances."""
        return self._dependent_variables

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
        return self._application

    @application.setter
    def application(self, value):
        self._application = validate(value, "application", dict)

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
        dictionary = self._to_dict(filename=self.filename, for_display=True)

        return json.dumps(dictionary, ensure_ascii=False, sort_keys=False, indent=2)

    @property
    def filename(self):
        """Local file address of the current file. """
        return self._filename

    # Numpy - like property

    @property
    def real(self):
        """Return a csdm object with only the real part of the dependent variable
        components."""
        return np.real(self)

    @property
    def imag(self):
        """Return a csdm object with only the imaginary part of the dependent variable
        components."""
        return np.imag(self)

    @property
    def T(self):
        """Return a csdm object with a transpose of the dataset."""
        new = CSDM()
        new._copy_metadata(self)
        # new = self.copy()
        new._dimensions += self._dimensions[::-1]

        for item in self.dependent_variables:
            dv = empty_dependent_variable(item.numeric_type)
            dv._copy_metadata(item)
            dv.subtype._components = np.moveaxis(item.subtype._components.T, -1, 0)
            new._dependent_variables += [dv]

        return new

    @property
    def shape(self):
        """Return the count along each dimension of the csdm objects as a
        tuple."""
        return tuple([item.count for item in self.dimensions])

    @property
    def ndim(self):
        """Return the total number of dimensions."""
        return len(self.dimensions)

    # ----------------------------------------------------------------------- #
    #                                  Methods                                #
    # ----------------------------------------------------------------------- #

    def add_dimension(self, *args, **kwargs):
        """
        Add a new :ref:`dim_api` instance to the :ref:`csdm_api` object.

        There are several ways to add a new independent variable.

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

        *Using keyword as the arguments.*

        .. doctest::

            >>> datamodel.add_dimension(
            ...     type = 'linear',
            ...     increment = '5 G',
            ...     count = 50,
            ...     coordinates_offset = '-10 mT'
            ... )

        *Using a* :ref:`dim_api` *class.*

        .. doctest::

            >>> var1 = Dimension(type = 'linear',
            ...                  increment = '5 G',
            ...                  count = 50,
            ...                  coordinates_offset = '-10 mT')
            >>> datamodel.add_dimension(var1)

        *Using a subtype class.*

        .. doctest::

            >>> var2 = cp.LinearDimension(count = 50,
            ...                  increment = '5 G',
            ...                  coordinates_offset = '-10 mT')
            >>> datamodel.add_dimension(var2)

        *From a numpy array.*

        .. doctest::

            >>> array = np.arange(50)
            >>> dim = cp.as_dimension(array)
            >>> datamodel.add_dimension(dim)

        In the third and fourth example, the instances, ``var1`` and ``var2`` are added
        to the ``datamodel`` as a reference, `i.e.`, if the instance ``var1`` or
        ``var2`` is destroyed, the ``datamodel`` instance will become corrupt. As a
        recommendation, always pass a copy of the :ref:`dim_api` instance to the
        :meth:`~csdmpy.CSDM.add_dimension` method.
        """
        if args != () and isinstance(args[0], __dimensions_list__):
            self._dimensions += [args[0]]
            return

        self._dimensions += [Dimension(*args, **kwargs)]

    def add_dependent_variable(self, *args, **kwargs):
        """
        Add a new :ref:`dv_api` instance to the :ref:`csdm_api` instance.

        There are again several ways to add a new dependent variable instance.

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
        :meth:`~csdmpy.add_dependent_variable` method.
        """
        if args != () and isinstance(args[0], DependentVariable):
            dv = args[0]
        else:
            dv = DependentVariable(filename=self.filename, *args, **kwargs)
            dv.encoding = "base64"
            dv.type = "internal"

        shape = self.shape
        if shape != ():
            dv._reshape(shape[::-1])

        self._dependent_variables += [dv]
        return

    def to_dict(
        self, update_timestamp=False, read_only=False, version=__latest_CSDM_version__
    ):
        """
        Serialize the :ref:`CSDM_api` instance as a python dictionary.

        Args:
            update_timestamp(bool): If True, timestamp is updated to current time.
            read_only (bool): If true, the read_only flag is set true.
            version (str): Serialize the dict with the given csdm version.

        Example:
            >>> data.to_dict() # doctest: +SKIP
            {'csdm': {'version': '1.0', 'timestamp': '1994-11-05T13:15:30Z',
            'geographic_coordinate': {'latitude': '10 deg', 'longitude': '93.2 deg',
            'altitude': '10 m'}, 'description': 'A simulated sine curve.',
            'dimensions': [{'type': 'linear', 'description': 'A temporal dimension.',
            'count': 10, 'increment': '0.1 s', 'quantity_name': 'time','label': 'time',
            'reciprocal': {'quantity_name': 'frequency'}}], 'dependent_variables':
            [{'type': 'internal', 'description': 'A response dependent variable.',
            'name': 'sine curve', 'encoding': 'base64', 'numeric_type': 'float32',
            'quantity_type': 'scalar', 'component_labels': ['response'],'components':
            ['AAAAABh5Fj9xeHM/cXhzPxh5Fj8yMQ0lGHkWv3F4c79xeHO/GHkWvw==']}]}}
        """
        return self._to_dict()

    def _to_dict(
        self,
        filename=None,
        update_timestamp=False,
        read_only=False,
        version=__latest_CSDM_version__,
        for_display=False,
    ):
        dictionary = {}

        dictionary["version"] = self.version

        if self.read_only:
            dictionary["read_only"] = self.read_only

        if update_timestamp:
            timestamp = datetime.datetime.utcnow().isoformat()[:-7] + "Z"
            dictionary["timestamp"] = timestamp
        else:
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
            dictionary["dimensions"].append(self.dimensions[i].to_dict())

        _length_of_dependent_variables = len(self.dependent_variables)
        for i in range(_length_of_dependent_variables):
            dictionary["dependent_variables"].append(
                self.dependent_variables[i]._to_dict(
                    filename=filename,
                    dataset_index=i,
                    for_display=for_display,
                    version=self.__latest_CSDM_version__,
                )
            )

        csdm = {}
        csdm["csdm"] = dictionary
        return csdm

    def dumps(
        self, update_timestamp=False, read_only=False, version=__latest_CSDM_version__
    ):
        """
        Serialize the :ref:`CSDM_api` instance as a JSON data-exchange string.

        Args:
            update_timestamp(bool): If True, timestamp is updated to current time.
            read_only (bool): If true, the file is serialized as read_only.
            version (str): The file is serialized with the given CSD model version.

        Example:
            >>> data.dumps()  # doctest: +SKIP
        """
        return json.dumps(
            self._to_dict(update_timestamp, read_only, version),
            ensure_ascii=False,
            sort_keys=False,
            indent=2,
            allow_nan=False,
        )

    def save(
        self,
        filename="",
        read_only=False,
        version=__latest_CSDM_version__,
        output_device=None,
    ):
        """
        Serialize the :ref:`CSDM_api` instance as a JSON data-exchange file.

        There are two types of file serialization extensions, `.csdf` and
        `.csdfe`. In the CSD model, when every instance of the DependentVariable
        objects from a CSDM class has an `internal` subtype, the corresponding
        CSDM instance is serialized with a `.csdf` file extension.
        If any single DependentVariable instance has an `external` subtype, the
        CSDM instance is serialized with a `.csdfe` file extension.
        The two different file extensions are used to alert the end-user of the
        possible deserialization error associated with the `.csdfe` file
        extensions had the external data file becomes inaccessible.

        In `csdmpy`, however, irrespective of the dependent variable subtypes
        from the serialized JSON file, by default, all instances of
        DependentVariable class are treated an `internal` after import.
        Therefore, when serialized, the CSDM object should be stored as a `.csdf`
        file.

        To store a file as a `.csdfe` file, the user much set the value of
        the :attr:`~csdmpy.DependentVariable.encoding`
        attribute from the dependent variables to ``raw``.
        In which case, a binary file named `filename_i.dat` will be generated
        where :math:`i` is the :math:`i^\\text{th}` dependent variable.
        The parameter `filename` is an argument of this method.

        .. note:: Only dependent variables with ``encoding="raw"`` will be
            serialized to a binary file.

        Args:
            filename (str): The filename of the serialized file.
            read_only (bool): If true, the file is serialized as read_only.
            version (str): The file is serialized with the given CSD model version.
            output_device(object): Object where the data is written. If provided,
                the argument `filename` become irrelevant.

        Example:
            >>> data.save('my_file.csdf')

        .. testcleanup::
            import os
            os.remove('my_file.csdf')
        """
        dictionary = self._to_dict(filename=filename, version=version)

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

    def to_list(self):
        """Return the dimension coordinates and dependent variable components as
        a list of numpy arrays."""
        dim = [item.coordinates for item in self.dimensions]
        dep = [i for item in self.dependent_variables for i in item.components]
        return [*dim, *dep]

    def astype(self, numeric_type):
        """Return a copy of the CSDM object by converting the numeric type of each
        dependent variables components to the given value.

        Args:
            numeric_type: A numpy dtype or a string with a valid numeric type

        Example:
            >>> data_32 = data_64.astype('float32')  # doctest: +SKIP
        """
        copy_ = self.copy()
        for var in copy_.dependent_variables:
            var.numeric_type = numeric_type
        return copy_

    def copy(self):
        """
        Create a copy of the current CSDM instance.

        Returns:
            A CSDM instance.

        Example:
            >>> data.copy()  # doctest: +SKIP
        """
        return deepcopy(self)

    def split(self):
        """Split the dependent-variables into view of individual csdm objects.

        Return:
            A list of CSDM objects, each with one dependent variable. The
            objects are returned as a view.

        Example:
            >>> # data contains two dependent variables
            >>> d1, d2 = data.split()  #doctest: +SKIP
        """

        def new_object():
            a = CSDM()
            a._dimensions = self._dimensions
            a._dependent_variables = DependentVariableList([])
            a._tags = self._tags
            a._read_only = self._read_only
            a._version = self._version
            a._timestamp = self._timestamp
            a._geographic_coordinate = self._geographic_coordinate
            a._description = self._description
            a._application = self._application
            a._filename = self._filename
            return a

        dv = []
        for variable in self.dependent_variables:
            a = new_object()
            a._dependent_variables += [variable]
            dv.append(a)
        return dv

    # ----------------------------------------------------------------------- #
    #                            NumPy-like functions                         #
    # ----------------------------------------------------------------------- #
    def max(self, axis=None):
        """
        Return a csdm object with the maximum dependent variable component along a
        given axis.

        Args:
            axis: An integer or None or a tuple of `m` integers cooresponding to
                    the index/indices of dimensions along which the sum of the
                    dependent variable components is performed. If None, the output is
                    the sum over all dimensions per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a numpy array when dimension
            is None.

        Example:
            >>> data2 = data.max()  #doctest: +SKIP
        """
        return np.max(self, axis=axis)

    def argmax(self, axis=None):
        raise NotImplementedError("")

    def min(self, axis=None):
        """
        Return a csdm object with the minimum dependent variable component along a
        given axis.

        Args:
            axis: An integer or None or a tuple of `m` integers cooresponding to
                    the index/indices of dimensions along which the sum of the
                    dependent variable components is performed. If None, the output is
                    over all dimensions per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a list when `axis` is None.
        """
        return np.min(self, axis=axis)

    def argmin(self, axis=None):
        raise NotImplementedError("")

    def ptp(self, axis=None):
        raise NotImplementedError("")

    def clip(self, min=None, max=None):
        """
        Clip the dependent variable components between the `min` and `max` values.

        Args:
            min: The minimum clip value.
            max: The maximum clip value.

        Return:
            A CSDM object with values clipped between min and max.
        """
        if len(self.dependent_variables) > 1:
            raise NotImplementedError(
                "CSDM objects with more that one dependent variable does not support "
                "the clip method. Used `.split()` method to split the dependent "
                "variables into individual csdm objects and try again."
            )
        a_max = max
        if max is None:
            a_max = self.dependent_variables[0].components.max()
        a_min = min
        if min is None:
            a_min = self.dependent_variables[0].components.min()
        return np.clip(self, a_min, a_max)

    def conj(self):
        """Return a csdm object with the complex conjugate of all dependent variable
        components."""
        return np.conj(self)

    def round(self, decimals=0):
        """Return a csdm object by rounding the dependent variable components to the
        given `decimals`."""
        return np.round(self, decimals)

    def trace(self, offset=0, axis1=0, axis2=-1):
        raise NotImplementedError("")

    def sum(self, axis=None):
        """Return a csdm object with the sum of the dependent variable components over
        a given `dimension=axis`.

        Args:
            axis: An integer or None or a tuple of `m` integers cooresponding to
                    the index/indices of dimensions along which the sum of the
                    dependent variable components is performed. If None, the output is
                    over all dimensions per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a list when `axis` is None.
        """
        return np.sum(self, axis=axis)

    def cumsum(self, axis=None):
        raise NotImplementedError("")

    def mean(self, axis=None):
        """Return a csdm object with the mean of the dependent variable components over
        a given `dimension=axis`.

        Args:
            axis: An integer or None or a tuple of `m` integers cooresponding to
                    the index/indices of dimensions along which the sum of the
                    dependent variable components is performed. If None, the output is
                    over all dimensions per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a list when `axis` is None.
        """
        return np.mean(self, axis=axis)

    def var(self, axis=None):
        """Return a csdm object with the variance of the dependent variable components
        over a given `dimension=axis`.

        Args:
            axis: An integer or None or a tuple of `m` integers cooresponding to
                    the index/indices of dimensions along which the sum of the
                    dependent variable components is performed. If None, the output is
                    over all dimensions per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a list when `axis` is None.
        """
        return np.var(self, axis=axis)

    def std(self, axis=None):
        """Return a csdm object with the standard deviation of the dependent variable
        components over a given `dimension=axis`.

        Args:
            axis: An integer or None or a tuple of `m` integers cooresponding to
                    the index/indices of dimensions along which the sum of the
                    dependent variable components is performed. If None, the output is
                    over all dimensions per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a list when `axis` is None.
        """
        return np.std(self, axis=axis)

    def prod(self, axis=None):
        """Return a csdm object with the product of the dependent variable components
        over a given `dimension=axis`.

        Args:
            axis: An integer or None or a tuple of `m` integers cooresponding to
                    the index/indices of dimensions along which the product of the
                    dependent variable components is performed. If None, the output is
                    over all dimensions per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a list when `axis` is None.
        """
        return np.prod(self, axis=axis)

    def cumprod(self, axis=None):
        raise NotImplementedError("")

    # csdm dimension order manipulation
    def transpose(self):
        return self.T

    def __array_ufunc__(self, function, method, *inputs, **kwargs):
        # print("__array_ufunc__")
        # print(inputs)
        # print(kwargs)

        csdm = inputs[0]
        input_ = []
        if len(inputs) > 1:
            input_ = inputs[1:]

        if function in __ufunc_list_dimensionless_unit__:
            factor = np.ones(len(csdm.dependent_variables))
            for i, variable in enumerate(csdm.dependent_variables):
                if variable.unit.physical_type != "dimensionless":
                    raise ValueError(
                        f"Cannot apply `{function.__name__}` to quantity with physical "
                        f"type `{variable.unit.physical_type}`."
                    )
                factor[i] = variable.unit.to("")
            return _get_new_csdm_object_after_applying_ufunc(
                inputs[0], function, method, factor, *input_, **kwargs
            )

        if function in __ufunc_list_unit_independent__:
            return _get_new_csdm_object_after_applying_ufunc(
                inputs[0], function, method, None, *input_, **kwargs
            )

        if function in __ufunc_list_applies_to_unit__:
            obj = _get_new_csdm_object_after_applying_ufunc(
                inputs[0], function, method, None, *input_, **kwargs
            )
            for i, variable in enumerate(obj.dependent_variables):
                scalar = function(1 * variable.unit, *input_)
                variable.components *= scalar.value
                variable.subtype._unit = scalar.unit
            return obj

        raise NotImplementedError(f"Function {function} is not implemented.")

    def __array_function__(self, function, types, *args, **kwargs):
        # print("__array_function__")
        # print(types)
        # print(kwargs)
        # print(function)
        # print(args)
        if function in __function_reduction_list__:
            return _get_new_csdm_object_after_dimension_reduction_func(
                function, *args[0], **args[1], **kwargs
            )
        if function in __other_functions__:
            return _get_new_csdm_object_after_applying_function(
                function, *args[0], **args[1], **kwargs
            )
        if function in __shape_manipulation_functions__:
            if "axes" in args[1].keys():
                args[1]["axes"] = (0,) + tuple(np.asarray(args[1]["axes"]) + 1)
            else:
                dim_len = len(args[0][0].dimensions)
                args[1]["axes"] = (0,) + tuple([-i - 1 for i in range(dim_len)])

            csdm = _get_new_csdm_object_after_applying_function(
                function, *args[0], **args[1], **kwargs
            )
            csdm._dimensions = tuple(
                [
                    csdm.dimensions[args[1]["axes"][1:][i]]
                    for i in range(len(csdm.dimensions))
                ]
            )

        raise NotImplementedError(f"Function {function.__name__} is not implemented.")

    # def __array_interface__(self, *args, **kwargs):
    #     print("__array_interface__")
    #     pass

    # def atleast_1d(self, *args, **kwargs):
    #     print(args)
    #     print(kwargs)


def _check_dimension_indices(d, index=-1):
    """
        Check the list of indexes to ensure that each index is an integer
        and within the counts of dimensions.
    """

    index = deepcopy(index)

    def _correct_index(i, d):
        if not isinstance(i, int):
            raise TypeError(f"{message}, found {type(i)}")
        if i < 0:
            i += d
        if i > d:
            raise IndexError(
                f"The `index` {index} cannot be greater than the total number of "
                f"dimensions - 1, {d}."
            )
        return -1 - i

    message = "Index/Indices are expected as integer(s)"

    if isinstance(index, tuple):
        index = list(index)

    if isinstance(index, (list, np.ndarray)):
        for i, item in enumerate(index):
            index[i] = _correct_index(item, d)
        return tuple(index)

    elif isinstance(index, int):
        return tuple([_correct_index(index, d)])

    else:
        raise TypeError(f"{message}, found {type(index)}")


def _check_for_out(csdm, **kwargs):
    out = kwargs.get("out", None)
    if out is not None:
        if len(csdm.dependent_variables) > 1:
            raise NotImplementedError(
                "Keyword `out` is not implemented for csdm objects with more that "
                "one dependent variables."
            )


def _get_new_csdm_object_after_applying_ufunc(
    csdm, func, method=None, factor=None, *inputs, **kwargs
):
    """
    Perform the operation, func, on the components of the dependent variables, and
    return the corresponding CSDM object.
    """
    if factor is None:
        factor = np.ones(len(csdm.dependent_variables))
    axis = kwargs.get("axis", None)
    if axis is not None:
        kwargs["axis"] = _check_dimension_indices(len(csdm.dimensions), axis)

    _check_for_out(csdm, **kwargs)

    new = CSDM()

    # dimension should be added first so that the dependent variables can be
    # shaped appropriately.
    new._dimensions = deepcopy(csdm.dimensions)

    for i, variable in enumerate(csdm.dependent_variables):
        y = func(variable.components * factor[i], *inputs, **kwargs)

        obj = empty_dependent_variable(
            numeric_type=y.dtype, quantity_type=variable.quantity_type
        )
        obj._copy_metadata(variable)
        obj.subtype._components = y
        new._dependent_variables += [obj]
        # obj = as_dependent_variable(y, quantity_type=variable.quantity_type)
        # obj._copy_metadata(variable)
        # new.add_dependent_variable(obj)

    new._copy_metadata(csdm)
    return new


def _get_new_csdm_object_after_applying_function(func, *args, **kwargs):
    """
    Perform the operation, func, on the components of the dependent variables, and
    return the corresponding CSDM object.
    """
    args_ = []
    csdm = args[0]
    if len(args) > 1:
        args_ = args[1:]

    _check_for_out(csdm, **kwargs)

    new = CSDM()

    # dimension should be added first so that the dependent variables can be
    # shaped appropriately.
    new._dimensions = deepcopy(csdm.dimensions)

    for variable in csdm.dependent_variables:
        y = func(variable.components, *args_, **kwargs)
        obj = empty_dependent_variable(
            numeric_type=y.dtype, quantity_type=variable.quantity_type
        )
        obj._copy_metadata(variable)
        obj.subtype._components = y
        new._dependent_variables += [obj]

    new._copy_metadata(csdm)
    return new


def _get_new_csdm_object_after_apodization(csdm, func, arg, index=-1):
    """
    Perform the operation, func, on the components of the dependent variables, and
    return the corresponding CSDM object.
    """
    index = _check_dimension_indices(len(csdm.dimensions), index)

    quantity = string_to_quantity(arg)

    apodization_vector_nd = 1
    for i in index:
        dimension_coordinates = csdm.dimensions[-i - 1].coordinates
        function_arguments = quantity * dimension_coordinates

        if function_arguments.unit.physical_type != "dimensionless":
            raise ValueError(
                f"The value of the argument, `arg`, must have the dimensionality "
                f"`1/{dimension_coordinates.unit.physical_type}`, instead found "
                f"`{quantity.unit.physical_type}`."
            )
        apodization_vector = func(function_arguments.to("").value)

        apodization_vector_1d = _get_broadcast_shape(
            apodization_vector, len(csdm.dimensions), i
        )
        apodization_vector_nd = apodization_vector_nd * apodization_vector_1d

    new = CSDM()

    # dimension should be added first so that the dependent variables can be
    # shaped appropriately.
    new._dimensions = deepcopy(csdm.dimensions)

    for variable in csdm.dependent_variables:
        y = variable.components * apodization_vector_nd

        obj = empty_dependent_variable(
            numeric_type=y.dtype, quantity_type=variable.quantity_type
        )
        obj._copy_metadata(variable)
        obj.subtype._components = y
        new._dependent_variables += [obj]

        # obj = as_dependent_variable(y, quantity_type=variable.quantity_type)
        # obj._copy_metadata(variable)
        # new.add_dependent_variable(obj)

    new._copy_metadata(csdm)
    return new


def _get_new_csdm_object_after_dimension_reduction_func(func, *args, **kwargs):
    """
    Perform the operation, func, on the components of the dependent variables, and
    return the corresponding CSDM object.
    """
    axis = None
    args_ = []
    if args is not ():
        csdm = args[0]
        args_ = list(args[1:])
        if len(args) > 1:
            args_[0] = _check_dimension_indices(len(csdm.dimensions), args[1])
            axis = args_[0]
    if "a" in kwargs.keys():
        csdm = kwargs["a"]
        kwargs.pop("a")
    if "axis" in kwargs.keys():
        if kwargs["axis"] is not None:
            axis = _check_dimension_indices(len(csdm.dimensions), kwargs["axis"])
            kwargs["axis"] = axis

    _check_for_out(csdm, **kwargs)

    new = CSDM()
    lst = []

    # dimension should be added first so that the dependent variables can be
    # shaped appropriately.
    if axis is not None:
        for i, variable in enumerate(csdm.dimensions):
            if -1 - i not in axis:
                new.add_dimension(variable.copy())

    for variable in csdm.dependent_variables:
        y = func(variable.components, *args_, **kwargs)

        if axis is not None:
            obj = empty_dependent_variable(
                numeric_type=y.dtype, quantity_type=variable.quantity_type
            )
            obj._copy_metadata(variable)
            obj.subtype._components = y
            new._dependent_variables += [obj]

            # obj = as_dependent_variable(y, quantity_type=variable.quantity_type)
            # obj._copy_metadata(variable)
            # new.add_dependent_variable(obj)
        else:
            lst.append(y * variable.unit)

    if axis is None:
        del new
        if len(lst) > 1:
            return lst
        return lst[0]

    new._copy_metadata(csdm)
    return new


def empty_dependent_variable(numeric_type, quantity_type="scalar"):
    return DependentVariable(
        type="internal",
        components=np.empty(0),
        quantity_type=quantity_type,
        numeric_type=numeric_type,
    )

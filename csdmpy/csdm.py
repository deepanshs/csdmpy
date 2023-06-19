"""THE CSDM object"""
import datetime
import json
import warnings
from copy import deepcopy

import numpy as np
from astropy.units.quantity import Quantity

from .abstract_list import __dimensions_list__
from .abstract_list import DependentVariableList
from .abstract_list import DimensionList
from .dependent_variable import as_dependent_variable  # noqa: F401
from .dependent_variable import DependentVariable
from .dimension import as_dimension
from .dimension import Dimension  # noqa: F401
from .dimension import LabeledDimension  # noqa: F401
from .dimension import LinearDimension  # noqa: F401
from .dimension import MonotonicDimension  # noqa: F401
from .helper_functions import _preview
from .numpy_wrapper import __array_manipulation__
from .numpy_wrapper import __function_reduction_list__
from .numpy_wrapper import __other_functions__
from .numpy_wrapper import __shape_manipulation_functions__
from .numpy_wrapper import __ufunc_list_applies_to_unit__
from .numpy_wrapper import __ufunc_list_dimensionless_unit__
from .numpy_wrapper import __ufunc_list_unit_independent__
from .numpy_wrapper import fft
from .units import string_to_quantity
from .utils import _check_dimension_indices
from .utils import _get_broadcast_shape
from .utils import check_scalar_object
from .utils import get_CSDM_object__args__axes
from .utils import np_check_for_out
from .utils import np_check_pads
from .utils import validate

__all__ = ["CSDM"]


class CSDM:
    """Create an instance of a CSDM class.

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
        self._geographic_coordinate = None
        self._description = description
        self._application = None
        self._filename = filename

        kwargs_keys = kwargs.keys()

        _ = [
            setattr(self, f"_{k}", v)
            for k, v in kwargs.items()
            if f"_{k}" in CSDM.__slots__
        ]

        self._dimensions = DimensionList([])
        if "dimensions" in kwargs_keys:
            if not isinstance(kwargs["dimensions"], (list, DimensionList)):
                dim_type = type(kwargs["dimensions"])
                raise ValueError(
                    "A list of valid Dimension or equivalent dictionary objects is "
                    f"required, found {dim_type}."
                )
            _ = [self.dimensions.append(item) for item in kwargs["dimensions"]]

        self._dependent_variables = DependentVariableList([])
        if "dependent_variables" in kwargs_keys:
            dv_type = type(kwargs["dependent_variables"])
            if not isinstance(
                kwargs["dependent_variables"], (list, DependentVariableList)
            ):
                raise ValueError(
                    "A list of valid DependentVariable or equivalent dictionary "
                    f"objects is required, found {dv_type}."
                )
            for item in kwargs["dependent_variables"]:
                if isinstance(item, dict):
                    item.update({"filename": self.filename})
                self.dependent_variables.append(item)
                if self.shape != ():
                    shape = self.shape[::-1]
                    self.dependent_variables[-1]._reshape(shape)

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

    # def __check_csdm_object(self, other, operator=""):
    #     """Check if the two objects are csdm objects"""
    #     if isinstance(other, CSDM):
    #         return

    #     name = other.__class__.__name__
    #     raise TypeError(
    #           f"unsupported operand type(s) {operator}: 'CSDM' and '{name}'."
    #     )

    def __check_dimension_equality(self, other):
        """Check if the dimensions of the two csdm objects are identical."""
        if self.dimensions != other.dimensions:
            raise Exception("Cannot operate on CSDM objects with different dimensions.")

    def __check_dependent_variable_len_equality(self, other):
        """Check if the length of dependent variables from the two csdm objects are
        equal.
        """
        if len(self.dependent_variables) != len(other.dependent_variables):
            raise Exception(
                "Cannot operate on CSDM objects with different lengths of "
                "dependent variables."
            )

    def __check_dependent_variable_dimensionality(self, other):
        """Check if the dependent variables from the two csdm objects have the same
        dimensionality.
        """
        for v_1, v_2 in zip(self.dependent_variables, other.dependent_variables):
            if v_1.unit.physical_type != v_2.unit.physical_type:
                raise Exception(
                    "Cannot operate on dependent variables with physical types: "
                    f"{v_1.unit.physical_type} and {v_2.unit.physical_type}."
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
        return np.all(check)

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
                f_n = getattr(item.components, function)
                f_n(factor * other.dependent_variables[i].components)
            return self

        other = check_scalar_object(other, symbol)

        for i, item in enumerate(self.dependent_variables):
            f_n = getattr(item.components, function)
            if not isinstance(other, Quantity):
                f_n(other)
            else:
                factor = other.unit.to(item.unit)
                f_n(factor * other.value)
        return self

    def _default_addition_(self, other, f_n, operation):
        """Operate on two objects (z=x+/-y), if the other object is a
            1) csdm or scalar object,
            2) with identical dimension objects,
            3) same number of dependent-variables, and
            4) each dependent variables with identical dimensionality.

        Args:
            other: the object to add/subtract
            f_n: addition/subtraction function
            operation: "+" or "-"
        """
        if isinstance(other, CSDM):
            self.__check_csdm_object_additive_compatibility(other)

            obj = self.copy()
            for i, item in enumerate(obj.dependent_variables):
                factor = other.dependent_variables[i].unit.to(item.unit)
                item.components = item.components + f_n(
                    factor, other.dependent_variables[i].components
                )
            return obj

        other = check_scalar_object(other, operation)
        obj = self.copy()
        for i, item in enumerate(obj.dependent_variables):
            item.components = (
                item.components + f_n(1, other)
                if not isinstance(other, Quantity)
                else item.components + f_n(1, other.unit.to(item.unit) * other.value)
            )
        return obj

    def __add__(self, other):
        """Add two objects (z=x+y)"""

        def function(val_1, val_2):
            return val_1 * val_2

        return self._default_addition_(other, function, "+")

    def __radd__(self, other):
        """Right add two objects. See __add__ for details."""
        return self.__add__(other)

    def __iadd__(self, other):
        """Add two objects in-place (y+=x).  See __add__ for details."""
        return self.__ifunction__("__iadd__", "+", other)

    def __sub__(self, other):
        """Subtract two objects (z=x+y)"""

        def function(val_1, val_2):
            return -val_1 * val_2

        return self._default_addition_(other, function, "-")

    def __rsub__(self, other):
        """Right subtract two objects. See __sub__ for details."""
        return -self.__sub__(other)

    def __isub__(self, other):
        """Subtract two objects in-lace (y-=x). See __sub__ for details."""
        return self.__ifunction__("__isub__", "-", other)

    def __mul__(self, other):
        """Multiply the components of the CSDM object by a scalar."""
        other = check_scalar_object(other, "*")

        obj = self.copy()
        for item in obj.dependent_variables:
            if not isinstance(other, Quantity):
                item.components = item.components * other
            else:
                value = 1 * item.subtype._unit * other
                item.subtype._unit = value.unit
                item.components = item.components * value.value
        return obj

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

        obj = self.copy()
        for item in obj.dependent_variables:
            if not isinstance(other, Quantity):
                item.components = item.components / other
            else:
                value = (1 * item.subtype._unit) / other
                item.subtype._unit = value.unit
                item.components = item.components * value.value
        return obj

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
            item.subtype._unit = item.subtype._unit**other
        return self

    def _get_indices(self, indices):
        if isinstance(indices, tuple):
            size = len(indices)
            indices = indices + tuple(
                slice(0, _.count, 1) for _ in self.dimensions[size:]
            )
        if isinstance(indices, (int, slice)):
            indices = (indices,) + tuple(
                slice(0, _.count, 1) for _ in self.dimensions[1:]
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
            dim_ = Dimension(**dim.dict()) if not hasattr(self, "subtype") else dim
            dim_.copy_metadata(dim)
            new_dim = dim_[indices[i]]
            if new_dim.size > 1:
                csdm._dimensions += [new_dim]

        for variable in self.dependent_variables:
            section = (slice(0, len(variable.components), 1),) + indices[::-1]
            components = variable.components[section]
            dv_obj = empty_dependent_variable(
                variable.numeric_type, variable.quantity_type
            )
            dv_obj.subtype._components = components
            dv_obj.copy_metadata(variable)
            csdm._dependent_variables += [dv_obj]

        csdm.copy_metadata(self)
        if len(csdm.dimensions) == 0 and len(csdm.dependent_variables) == 1:
            value = np.squeeze(csdm.dependent_variables[0].components)
            unit = csdm.dependent_variables[0].unit
            return value * unit
        return csdm

    def copy_metadata(self, other):
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
        """If True, the data-file is serialized as read only, otherwise, False.

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
        """Timestamp from when the file was last serialized. Attribute is real only.

        The timestamp stamp is a string representation of the Coordinated Universal
        Time (UTC) formatted according to the iso-8601 standard.

        Raises:
            AttributeError: When the attribute is modified.
        """
        return self._timestamp

    @property
    def geographic_coordinate(self):
        """Geographic coordinate, if present, from where the file was last serialized.
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

    @dimensions.setter
    def dimensions(self, other):
        pass

    @property
    def x(self):
        """Alias for the dimensions attribute."""
        return self._dimensions

    @property
    def dependent_variables(self):
        """Tuple of the :ref:`dv_api` instances."""
        return self._dependent_variables

    @dependent_variables.setter
    def dependent_variables(self, other):
        pass

    @property
    def y(self):
        """Alias for the dependent_variables attribute."""
        return self._dependent_variables

    @property
    def application(self):
        """Application metadata dictionary of the CSDM object.

        .. doctest::

            >>> print(data.application)
            None

        By default, the application attribute is an empty object, that is,
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
        self._application = validate(value, "application", (dict, type(None)))

    @property
    def data_structure(self):
        """Json serialized string describing the CSDM class instance.

        The data_structure attribute is only intended for a quick preview of
        the dataset. This JSON serialized string from this attribute avoids
        displaying large datasets. Do not use the value of this attribute to
        save the data to a file, instead use the :meth:`~csdmpy.CSDM.save`
        methods of the instance.

        Raises:
            AttributeError: When modified.
        """
        dictionary = self._dict(filename=self.filename, for_display=True)

        return json.dumps(dictionary, ensure_ascii=False, sort_keys=False, indent=2)

    @property
    def filename(self):
        """Local file address of the current file."""
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
        new.copy_metadata(self)
        new._dimensions += self._dimensions[::-1]

        for item in self.dependent_variables:
            dv_obj = empty_dependent_variable(item.numeric_type, item.quantity_type)
            dv_obj.copy_metadata(item)
            dv_obj.subtype._components = np.moveaxis(item.subtype._components.T, -1, 0)
            new._dependent_variables += [dv_obj]

        return new

    @property
    def shape(self):
        """Return the count along each dimension of the csdm object."""
        return tuple(item.count for item in self._dimensions)

    @property
    def size(self):
        """Return the size of the dependent_variable components."""
        return np.prod([item.count for item in self.dimensions])

    @property
    def ndim(self):
        """Return the total number of dimensions."""
        return len(self.dimensions)

    def reshape(self, shape):
        """Reshape the csdm object to shape.

        Args:
            shape: A list of dimension objects or integers.
        """
        size = self.y[0].components[0].size

        shape_int = [item if isinstance(item, int) else item.size for item in shape]
        new_dim = []
        for index in shape:
            sh = int(-size / np.prod(shape_int)) if index == -1 else index
            dim = (
                Dimension(type="linear", count=sh, increment="1")
                if isinstance(sh, int)
                else sh
            )
            new_dim.append(dim)

        for d_v in self.y:
            new_shape = (d_v.components.shape[0],) + tuple(shape_int[::-1])
            new_dv = as_dependent_variable(array=d_v.components.reshape(new_shape))
            new_dv.copy_metadata(d_v)

        new_csdm = CSDM(dimensions=new_dim, dependent_variables=[new_dv])
        new_csdm.copy_metadata(self)
        return new_csdm

    # ----------------------------------------------------------------------- #
    #                                  Methods                                #
    # ----------------------------------------------------------------------- #
    # deprecated
    def add_dimension(self, *args, **kwargs):
        """Add a new :ref:`dim_api` instance to the :ref:`csdm_api` object.

        There are several ways to add a new independent variable.
        *From a python dictionary containing valid keywords.*

        .. doctest::

            >>> import csdmpy as cp
            >>> data_model = cp.new()
            >>> py_dictionary = {
            ...     "type": "linear",
            ...     "increment": "5 G",
            ...     "count": 50,
            ...     "coordinates_offset": "-10 mT",
            ... }
            >>> data_model.add_dimension(py_dictionary)

        *Using keyword as the arguments.*

        .. doctest::

            >>> data_model.add_dimension(type="linear", increment="5 G", count=50)

        *Using a* :ref:`dim_api` *class.*

        .. doctest::

            >>> var1 = Dimension(type="linear", increment="5 G", count=50)
            >>> data_model.add_dimension(var1)

        *Using a subtype class.*

        .. doctest::

            >>> var2 = cp.LinearDimension(count=50, increment="5 G")
            >>> data_model.add_dimension(var2)

        *From a numpy array.*

        .. doctest::

            >>> array = np.arange(50)
            >>> dim = cp.as_dimension(array)
            >>> data_model.add_dimension(dim)

        In the third and fourth example, the instances, ``var1`` and ``var2`` are added
        to the ``data_model`` as a reference, `i.e.`, if the instance ``var1`` or
        ``var2`` is destroyed, the ``data_model`` instance will become corrupt. As a
        recommendation, always pass a copy of the :ref:`dim_api` instance to the
        :meth:`~csdmpy.CSDM.add_dimension` method.

        .. deprecated:: 0.4
            Use cp.CSDM(dimensions=[..]) instead.
        """
        warnings.warn(
            (
                "The `add_dimension` methods is deprecated since v0.4. "
                "Use cp.CSDM(dimensions=[..]) instead."
            ),
            DeprecationWarning,
        )
        if args != () and isinstance(args[0], __dimensions_list__):
            self._dimensions += [args[0]]
            return

        self._dimensions += [Dimension(*args, **kwargs)]

    def add_dependent_variable(self, *args, **kwargs):
        """Add a new :ref:`dv_api` instance to the :ref:`csdm_api` instance.

        There are again several ways to add a new dependent variable instance.
        *From a python dictionary containing valid keywords.*

        .. doctest::

            >>> import numpy as np

            >>> data_model = cp.new()

            >>> numpy_array = (100 * np.random.rand(3, 50)).astype(np.uint8)
            >>> py_dictionary = {
            ...     "type": "internal",
            ...     "components": numpy_array,
            ...     "name": "star",
            ...     "unit": "W s",
            ...     "quantity_name": "energy",
            ...     "quantity_type": "pixel_3",
            ... }
            >>> data_model.add_dependent_variable(py_dictionary)

        *From a list of valid keyword arguments.*

        .. doctest::

            >>> data_model.add_dependent_variable(
            ...     type="internal",
            ...     name="star",
            ...     unit="W s",
            ...     quantity_type="pixel_3",
            ...     components=numpy_array,
            ... )

        *From a* :ref:`dv_api` *instance.*

        .. doctest::

            >>> from csdmpy import DependentVariable
            >>> var1 = DependentVariable(
            ...     type="internal",
            ...     name="star",
            ...     unit="W s",
            ...     quantity_type="pixel_3",
            ...     components=numpy_array,
            ... )
            >>> data_model.add_dependent_variable(var1)

        If passing a :ref:`dv_api` instance, as a general recommendation,
        always pass a copy of the DependentVariable instance to the
        :meth:`~csdmpy.add_dependent_variable` method.

        .. deprecated:: 0.4
            Use cp.CSDM(dependent_variables=[..]) instead.
        """
        warnings.warn(
            (
                "The `add_dependent_variable` methods is deprecated since v0.4. "
                "Use cp.CSDM(dependent_variables=[..]) instead."
            ),
            DeprecationWarning,
        )
        if args != () and isinstance(args[0], DependentVariable):
            d_v = args[0]
        else:
            d_v = DependentVariable(filename=self.filename, *args, **kwargs)
            d_v.encoding = "base64"
            d_v.type = "internal"

        if self.shape != ():
            d_v._reshape(self.shape[::-1])

        self._dependent_variables += [d_v]

    def to_dict(self, update_timestamp=False, read_only=False):
        """Alias to the `dict()` method of the class."""
        return self.dict(update_timestamp, read_only)

    def dict(self, update_timestamp=False, read_only=False):
        """Serialize the :ref:`CSDM_api` instance as a python dictionary.

        Args:
            update_timestamp(bool): If True, timestamp is updated to current time.
            read_only (bool): If true, the read_only flag is set true.

        Example:
            >>> data.dict()['csdm']['version']
            '1.0'
        """
        return self._dict(update_timestamp=update_timestamp, read_only=read_only)

    def _dict(
        self,
        filename=None,
        update_timestamp=False,
        read_only=None,
        version=None,
        for_display=False,
    ):
        obj = {}
        obj["version"] = self.version if version is None else version
        obj["read_only"] = self.read_only if read_only is None else read_only
        obj["timestamp"] = (
            datetime.datetime.utcnow().isoformat()[:-7] + "Z"
            if update_timestamp
            else self.timestamp
        )
        obj["geographic_coordinate"] = self.geographic_coordinate
        obj["tags"] = self.tags
        obj["description"] = self.description.strip()
        obj["application"] = self.application
        obj["dimensions"] = [dim.dict() for dim in self.dimensions]
        obj["dependent_variables"] = [
            dv._dict(filename=filename, dataset_index=i, for_display=for_display)
            for i, dv in enumerate(self.dependent_variables)
        ]

        empty_values = [[], "", {}, False, None]
        _ = [obj.pop(_) for _ in [k for k, v in obj.items() if v in empty_values]]

        return {"csdm": obj}

    def dumps(self, update_timestamp=False, read_only=False, **kwargs):
        """Serialize the :ref:`CSDM_api` instance as a JSON data-exchange string.

        Args:
            update_timestamp(bool): If True, timestamp is updated to current time.
            read_only (bool): If true, the file is serialized as read_only.

        Example:
            >>> data.dumps()[:63] # first 63 characters
            '{"csdm": {"version": "1.0", "timestamp": "1994-11-05T13:15:30Z"'
        """
        dict_ = self._dict(
            update_timestamp=update_timestamp, read_only=read_only, version=self.version
        )
        return json.dumps(
            dict_, ensure_ascii=False, sort_keys=False, allow_nan=False, **kwargs
        )

    def save(self, filename="", read_only=False, output_device=None, indent=0):
        """Serialize the :ref:`CSDM_api` instance as a JSON data-exchange file.

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
            output_device(object): Object where the data is written. If provided,
                the argument `filename` become irrelevant.

        Example:
            >>> data.save('my_file.csdf')

        .. testcleanup::

            import os

            os.remove("my_file.csdf")
        """
        dictionary = self._dict(filename=filename, version=self.version)

        timestamp = datetime.datetime.utcnow().isoformat()[:-7] + "Z"
        dictionary["csdm"]["timestamp"] = timestamp

        if read_only:
            dictionary["csdm"]["read_only"] = read_only

        kwargs = dict(
            ensure_ascii=False, sort_keys=False, indent=indent, allow_nan=False
        )
        if output_device is not None:
            json.dump(dictionary, output_device, **kwargs)

        with open(filename, "w", encoding="utf8") as outfile:
            json.dump(dictionary, outfile, **kwargs)

    def to_list(self):
        r"""Return the dimension coordinates and dependent variable components as
        a list of numpy arrays. For multiple dependent variables, the components
        of each dependent variable is appended in the order of the dependent
        variables.

        For example,
         - A 2D{1} will be packed as :math:`[x_{0}, x_{1}, y_{0,0}]`
         - A 2D{3} will be packed as :math:`[x_{0}, x_{1}, y_{0,0}, y_{0,1}, y_{0,2}]`
         - A 1D{1,2} will be packed as :math:`[x_{0}, y_{0,0}, y_{1,0}, y_{1,1}]`

        where :math:`x_i` represents the :math:`i^\text{th}` dimension and
        :math:`y_{i,j}` represents the :math:`j^\text{th}` component of the
        :math:`i^\text{th}` dependent variable.
        """
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
        """Create a copy of the current CSDM instance.

        Returns:
            A CSDM instance.

        Example:
            >>> data2 = data.copy()
        """
        return deepcopy(self)

    def split(self):
        """View of the dependent-variables as individual csdm objects.

        Return:
            A list of CSDM objects, each with one dependent variable. The
            objects are returned as a view.

        Example:
            >>> # data contains two dependent variables
            >>> d1, d2 = data.split()  #doctest: +SKIP
        """

        def new_object(var):
            new = CSDM()
            new._dimensions = self._dimensions
            new._dependent_variables = DependentVariableList([var])
            new._tags = self._tags
            new._read_only = self._read_only
            new._version = self._version
            new._timestamp = self._timestamp
            new._geographic_coordinate = self._geographic_coordinate
            new._description = self._description
            new._application = self._application
            new._filename = self._filename
            return new

        return [new_object(variable) for variable in self.dependent_variables]

    # csdm dimension order manipulation
    def transpose(self):
        """Return a transpose of the CSDM object."""
        return self.T

    def fft(self, axis=0):
        """Perform a FFT along the given `dimension=axis`, for linear dimension,
        assuming Nyquist-Shannon relation.

        Args:
            axis: dimension index along which the FFT is performed.

        The FFT method uses the :attr:`~csdmpy.Dimension.complex_fft` attribute of the
        Dimension object to decide whether a forward or inverse Fourier transform is
        performed. If the value of the `complex_fft` is True, an inverse FFT is
        performed, otherwise a forward FFT.

        For FFT process, this function is equivalent to performing

        .. code:: python

            phase = np.exp(-2j * np.pi * coordinates_offset * reciprocal_coordinates)
            x_fft = np.fft.fftshift(np.fft.fft(x)) * phase

        over all components for every dependent variable.

        Similarly, for inverse FFT process, this function is equivalent to performing

        .. code:: python

            phase = np.exp(2j * np.pi * reciprocal_coordinates_offset * coordinates)
            x = np.fft.ifft(np.fft.ifftshift(x_fft * phase))

        over all components for every dependent variable.

        Return:
            A CSDM object with the Fourier Transform data.
        """
        return fft(self, axis)

    # ----------------------------------------------------------------------- #
    #                            NumPy-like functions                         #
    # ----------------------------------------------------------------------- #
    def max(self, axis=None):
        """Return a csdm object of maximum dependent variable along a given axis.s

        Args:
            axis: An integer or None or a tuple of `m` integers corresponding to the
                dimension index/indices along which the operation is performed. If None,
                the output is over all dimensions per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a numpy array when dimension
            is None.

        Example:
            >>> data.max()
            <Quantity 0.95105654>
        """
        return np.max(self, axis=axis)

    def argmax(self, axis=None):
        """Return a csdm object of argmax dependent variable along a given axis.s

        Args:
            axis: An integer or None or a tuple of `m` integers corresponding to the
                dimension index/indices along which the operation is performed. If None,
                the output is over all dimensions per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a numpy array when dimension
            is None.

        Example:
            >>> data.max()
            <Quantity 0.95105654>
        """
        return np.argmax(self, axis=axis)

    def min(self, axis=None):
        """Return a csdm object of minimum dependent variable component along a
        given axis.

        Args:
            axis: An integer or None or a tuple of `m` integers corresponding to the
                dimension index/indices along which the operation is performed. If
                None, the output is over all dimensions per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a list when `axis` is None.
        """
        return np.min(self, axis=axis)

    def argmin(self, axis=None):
        """Return a csdm object of argmin dependent variable component along a
        given axis.

        Args:
            axis: An integer or None or a tuple of `m` integers corresponding to the
                dimension index/indices along which the operation is performed. If
                None, the output is over all dimensions per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a list when `axis` is None.
        """
        return np.argmin(self, axis=axis)

    def ptp(self, axis=None):
        raise NotImplementedError("")

    def clip(self, min=None, max=None):
        """Clip the dependent variable components between the `min` and `max` values.

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
        """Return a complex conjugate of the csdm object."""
        return np.conj(self)

    def round(self, decimals=0):
        """Rounds a csdm object to the given `decimals`."""
        return np.round(self, decimals)

    def trace(self, offset=0, axis1=0, axis2=-1):
        raise NotImplementedError("")

    def sum(self, axis=None):
        """Return a csdm object sum over a given axis.

        Args:
            axis: An integer or None or a tuple of `m` integers corresponding to the
                dimension index/indices along which the operation is performed. If None,
                the output is over all dimensions per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a list when `axis` is None.
        """
        return np.sum(self, axis=axis)

    def cumsum(self, axis=None):
        """Return a csdm object cumulative sum over a given axis.

        Args:
            axis: An integer or None corresponding to the dimension index along which
                the operation is performed. If None, the output is over all dimensions
                per dependent variable.
        Return:
            A CSDM object with `1` dimension removed, or a list when `axis` is None.
        """
        return np.cumsum(self, axis=axis)

    def mean(self, axis=None):
        """Return a csdm object mean over a given axis.

        Args:
            axis: An integer or None or a tuple of `m` integers corresponding to the
                dimension index/indices along which the operation is performed. If None,
                the output is over all dimensions per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a list when `axis` is None.
        """
        return np.mean(self, axis=axis)

    def var(self, axis=None):
        """Return a csdm object variance over a given axis.

        Args:
            axis: An integer or None or a tuple of `m` integers corresponding to the
                dimension index/indices along which the operation is performed. If None,
                the output is over all dimensions per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a list when `axis` is None.
        """
        return np.var(self, axis=axis)

    def std(self, axis=None):
        """Return a csdm object standard deviation over a given axis.

        Args:
            axis: An integer or None or a tuple of `m` integers corresponding to the
                dimensions index/indices along which the operation is performed.
                If None, the output is over all dimensions per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a list when `axis` is None.
        """
        return np.std(self, axis=axis)

    def prod(self, axis=None):
        """Return a csdm object product over a given axis.

        Args:
            axis: An integer or None or a tuple of `m` integers corresponding to the
                dimension index/indices along which the operation is performed.
                If None, the output is over all dimensions per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a list when `axis` is None.
        """
        return np.prod(self, axis=axis)

    def cumprod(self, axis=None):
        """Return a csdm object cumulative product over a given axis.

        Args:
            axis: An integer or None corresponding to the dimension index along which
                the operation is performed. If None, the output is over all dimensions
                per dependent variable.
        Return:
            A CSDM object with `m` dimensions removed, or a list when `axis` is None.
        """
        return np.cumprod(self, axis=axis)

    def __array_ufunc__(self, function, method, *inputs, **kwargs):
        if function == np.multiply:
            return inputs[1] * inputs[0]
        if function == np.divide:
            return (1.0 / inputs[1]) * inputs[0]

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
            return get_new_csdm_object_after_applying_ufunc(
                csdm, function, method, factor, *input_, **kwargs
            )

        if function in __ufunc_list_unit_independent__:
            return get_new_csdm_object_after_applying_ufunc(
                csdm, function, method, None, *input_, **kwargs
            )

        if function in __ufunc_list_applies_to_unit__:
            obj = get_new_csdm_object_after_applying_ufunc(
                csdm, function, method, None, *input_, **kwargs
            )
            for i, variable in enumerate(obj.dependent_variables):
                scalar = function(1 * variable.unit, *input_)
                variable.components *= scalar.value
                variable.subtype._unit = scalar.unit
            return obj

        raise NotImplementedError(f"Function {function} is not implemented.")

    def __array_function__(self, function, _, *args, **kwargs):
        if function in __function_reduction_list__:
            return get_new_csdm_object_after_dimension_reduction_func(
                function, *args[0], **args[1], **kwargs
            )
        if function in __other_functions__:
            return get_new_csdm_object_after_applying_function(
                function, *args[0], **args[1], **kwargs
            )
        if function in __array_manipulation__:
            csdm = args[0][0]
            args_ = ()
            if len(args[0]) > 1:
                args_ = args[0][1:]
            args_kw = args[1]
            return get_new_csdm_object_after_applying_ufunc(
                csdm, function, None, None, *args_, **args_kw
            )
        if function in [np.pad]:
            return apply_np_padding(function, *args, **kwargs)

        if function in __shape_manipulation_functions__:
            dim_len = len(args[0][0].dimensions)
            if "axes" in args[1].keys():
                axes = (0,) + tuple(-np.asarray(args[1]["axes"]) - 1)
                axes_dim = args[1]["axes"]
                args[1]["axes"] = axes

            elif len(args[0]) == 2:
                args = list(args)
                args[0] = list(args[0])
                axes = (0,) + tuple(-np.asarray(args[0][1]) - 1)
                axes_dim = args[0][1]
                args[0][1] = axes
            else:
                axes = (0,) + tuple(-i - 1 for i in range(dim_len))
                axes_dim = np.arange(dim_len)[::-1]
                args[1]["axes"] = axes

            csdm = get_new_csdm_object_after_applying_function(
                function, *args[0], **args[1], **kwargs
            )

            csdm._dimensions = tuple(
                csdm.dimensions[axes_dim[i]] for i in range(len(csdm.dimensions))
            )
            return csdm

        # if function in __return_np__:
        #     if len(self.y) > 1:
        #         raise NotImplementedError(
        #             f"Function {function.__name__} is not implemented for multi "
        #              "dependent variable csdm object."
        #         )
        #     csdm, args_, axis, kwargs = get_CSDM_object__args__axes(
        #         *args[0], **args[1], **kwargs
        #     )
        #     nd_array = csdm.y[0].components
        #     return function(nd_array, *args_, **kwargs)

        raise NotImplementedError(f"Function {function.__name__} is not implemented.")

    # def __array_interface__(self, *args, **kwargs):
    #     print("__array_interface__")
    #     pass

    # def atleast_1d(self, *args, **kwargs):
    #     print(args)
    #     print(kwargs)

    def plot(self, reverse_axis=None, range=None, **kwargs):
        """A supplementary function for plotting basic 1D and 2D datasets only.

        Args:
            csdm_object: The CSDM object.
            reverse_axis: An ordered array of boolean specifying which dimensions will
                be displayed on a reverse axis.
            range: A list of minimum and maximum coordinates along the dimensions. The
                range along each dimension is given as [min, max]
            kwargs: Additional keyword arguments are used in matplotlib plotting
                functions. We implement the following matplotlib methods for the one
                and two-dimensional datasets.

                - The 1D{1} scalar dataset use the plt.plot() method.
                - The 1D{2} vector dataset use the plt.quiver() method.
                - The 2D{1} scalar dataset use the plt.imshow() method if the two
                  dimensions have a `linear` subtype. If any one of the dimension is
                  `monotonic`, plt.NonUniformImage() method is used instead.
                - The 2D{2} vector dataset use the plt.quiver() method.
                - The 2D{3} pixel dataset use the plt.imshow(), assuming the pixel
                  dataset as an RGB image.

        Returns:
            A matplotlib figure instance.

        Example:
            >>> cp.plot(data_object) # doctest: +SKIP
        """
        return _preview(self, reverse_axis, range, **kwargs)

    def to_positive_inc(self):
        """Convert the csdm object with negative increment dimensions to positive
        increments.

        Args:
            csdm_obj: CSDM object
        """
        reverse_index = []
        new_dimensions = []
        for i, dim in enumerate(self.dimensions):
            if dim.type in ["linear", "monotonic"]:
                diff = dim.coordinates[1] - dim.coordinates[0]
                if diff.value < 0:
                    reverse_index.append(-i - 1)
                    coords = dim.coordinates
                    array, unit = coords.value[::-1], coords.unit
                    new_axis = as_dimension(array=array, unit=str(unit))
                    new_axis.copy_metadata(dim)
                    new_dimensions.append(new_axis)
                else:
                    new_dimensions.append(dim)
            else:
                new_dimensions.append(dim)

        new_dvs = []
        for d_v in self.dependent_variables:
            datum = d_v.components
            datum = (
                datum
                if reverse_index == []
                else np.flip(datum, axis=tuple(reverse_index))
            )
            new_dv = as_dependent_variable(array=datum)
            new_dv.copy_metadata(d_v)
            new_dvs.append(new_dv)

        new_csdm = CSDM(dimensions=new_dimensions, dependent_variables=new_dvs)
        new_csdm.copy_metadata(self)

        return new_csdm


def get_new_csdm_object_after_applying_ufunc(
    csdm, func, method=None, factor=None, *inputs, **kwargs
):
    """Perform the operation, func, on the components of the dependent variables, and
    return the corresponding CSDM object.
    """
    if factor is None:
        factor = np.ones(len(csdm.dependent_variables))
    axis = kwargs.get("axis", None)
    if axis is not None:
        kwargs["axis"] = _check_dimension_indices(len(csdm.dimensions), axis)

    np_check_for_out(csdm, **kwargs)

    new = CSDM()

    # dimension should be added first so that the dependent variables can be
    # shaped appropriately.
    new._dimensions = deepcopy(csdm.dimensions)

    for i, variable in enumerate(csdm.dependent_variables):
        res = func(variable.components * factor[i], *inputs, **kwargs)

        obj = empty_dependent_variable(
            numeric_type=res.dtype, quantity_type=variable.quantity_type
        )
        obj.copy_metadata(variable)
        obj.subtype._components = res
        new._dependent_variables += [obj]
        # obj = as_dependent_variable(y, quantity_type=variable.quantity_type)
        # obj.copy_metadata(variable)
        # new.add_dependent_variable(obj)

    new.copy_metadata(csdm)
    return new


def get_new_csdm_object_after_applying_function(func, *args, **kwargs):
    """Perform the operation, func, on the components of the dependent variables, and
    return the corresponding CSDM object.
    """
    args_ = []
    csdm = args[0]
    if len(args) > 1:
        args_ = args[1:]

    np_check_for_out(csdm, **kwargs)

    new = CSDM()

    # dimension should be added first so that the dependent variables can be
    # shaped appropriately.
    new._dimensions = deepcopy(csdm.dimensions)

    for variable in csdm.dependent_variables:
        components = func(variable.components, *args_, **kwargs)
        obj = empty_dependent_variable(
            numeric_type=components.dtype, quantity_type=variable.quantity_type
        )
        obj.copy_metadata(variable)
        obj.subtype._components = components
        new._dependent_variables += [obj]

    new.copy_metadata(csdm)
    return new


def get_new_csdm_object_after_apodization(csdm, func, arg, index=-1):
    """Perform the operation, func, on the components of the dependent variables, and
    return the corresponding CSDM object.
    """
    index = _check_dimension_indices(len(csdm.dimensions), index)
    index = [index] if isinstance(index, int) else index

    quantity = string_to_quantity(arg)

    apodization_vector_nd = 1
    for i in index:
        dimension_coordinates = csdm.dimensions[-i - 1].coordinates
        function_arguments = quantity * dimension_coordinates

        if function_arguments.unit.physical_type != "dimensionless":
            raise ValueError(
                "The value of the argument, `arg`, must have the dimensionality "
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
        components = variable.components * apodization_vector_nd

        obj = empty_dependent_variable(
            numeric_type=components.dtype, quantity_type=variable.quantity_type
        )
        obj.copy_metadata(variable)
        obj.subtype._components = components
        new._dependent_variables += [obj]

        # obj = as_dependent_variable(y, quantity_type=variable.quantity_type)
        # obj.copy_metadata(variable)
        # new.add_dependent_variable(obj)

    new.copy_metadata(csdm)
    return new


def get_new_csdm_object_after_dimension_reduction_func(func, *args, **kwargs):
    """Perform the operation, func, on the components of the dependent variables, and
    return the corresponding CSDM object.
    """
    csdm, args_, axis, kwargs = get_CSDM_object__args__axes(*args, **kwargs)

    new = CSDM()
    lst = []

    axis = [axis] if isinstance(axis, int) else axis
    # dimension should be added first so that the dependent variables can be
    # shaped appropriately.
    if axis is not None:
        for i, variable in enumerate(csdm.dimensions):
            if -1 - i not in axis:
                new.dimensions.append(variable.copy())

    for variable in csdm.dependent_variables:
        components = func(variable.components, *args_, **kwargs)

        if axis is not None:
            obj = empty_dependent_variable(
                numeric_type=components.dtype, quantity_type=variable.quantity_type
            )
            obj.copy_metadata(variable)
            obj.subtype._components = components
            new._dependent_variables += [obj]

            # obj = as_dependent_variable(y, quantity_type=variable.quantity_type)
            # obj.copy_metadata(variable)
            # new.add_dependent_variable(obj)
        else:
            lst.append(components * variable.unit)

    if axis is None:
        del new
        return lst if len(lst) > 1 else lst[0]

    new.copy_metadata(csdm)
    return new


def empty_dependent_variable(numeric_type, quantity_type="scalar"):
    """Create an empty dependent variable object"""
    return DependentVariable(
        type="internal",
        components=np.empty(0),
        quantity_type=quantity_type,
        numeric_type=numeric_type,
    )


def apply_np_padding(function, *args, **kwargs):
    """Apply numpy padding"""
    args0 = list(args[0])
    n_dims = len(args0[0].x)
    if "pad_width" in args[1].keys():
        pads = np_check_pads(args[1]["pad_width"], n_dims)
        pads = ((0, 0),) + tuple(pads)[::-1]
        args[1]["pad_width"] = pads
    else:
        pads = np_check_pads(args0[1], n_dims)
        pads = ((0, 0),) + tuple(pads)[::-1]
        args0[1] = pads

    for key, val in args[1].items():
        if key in ["stat_length", "constant_values", "end_values"]:
            args[1][key] = ((0, 0),) + tuple(np_check_pads(val, n_dims))[::-1]

    csdm = get_new_csdm_object_after_applying_function(
        function, *args0, **args[1], **kwargs
    )
    for dim, pads in zip(csdm.dimensions, pads[::-1][:-1]):
        if dim.type == "linear":
            dim.count += int(np.sum(pads))
            offset = int(pads[0] / 2 - 1) if dim.complex_fft else pads[0]
            dim.coordinates_offset -= dim.increment * offset
        if dim.type == "monotonic":
            inc = dim.coordinates[1] - dim.coordinates[0]
            left = inc * (np.arange(pads[0]) - pads[0]) + dim.coordinates[0]
            right = inc * np.arange(pads[1]) + dim.coordinates[0]
            coords = np.concatenate((left, dim.coordinates, right))
            dim.coordinates = coords
        if dim.type == "labeled":
            left = ["0"] * pads[0]
            right = ["0"] * pads[1]
            coords = left + list(dim.labels) + right
            dim.labels = coords
    return csdm

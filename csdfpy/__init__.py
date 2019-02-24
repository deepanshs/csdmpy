
"""CSDModel."""

from __future__ import print_function, division
from .cv import ControlledVariable
from .uv import UncontrolledVariable
import numpy as np
import json
from scipy.fftpack import fft, fftshift
import os
from copy import deepcopy
from .__version__ import __version__ as version

script_path = os.path.dirname(os.path.abspath(__file__))
# print (script_path)

test_file = {
    "test01": script_path+'/testFiles/test01.csdf',
    "test02": script_path+'/testFiles/test02.csdf'
    }


def _import_json(filename):
    with open(filename, "rb") as f:
        content = f.read()
        return (json.loads(str(content, encoding="UTF-8")))


def load(filename=None):
    r"""
    Open a `.csdf or `.csdfx` file and return a :ref:`csdm_api` object.

    The file must be a json serialization of the CSD Model. ::

        >>> import csdfpy
        >>> data1 = csdfpy.load('local/address/to/the/file.csdf')

    In the above example, ``data1`` is an instance of CSDModel class.

    :params: filename: A local address to the `.csdf or `.csdfx` file.
    :returns: CSDModel object.
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

    for dim in dictionary['CSDM']['controlled_variables']:
        csdm.add_controlled_variable(dim)

    for dat in dictionary['CSDM']['uncontrolled_variables']:
        csdm.add_uncontrolled_variable(dat)    # filename)

    _type = [(item.sampling_type == 'grid')
             for item in csdm.controlled_variables]

    if np.all(_type):
        npts = [item.number_of_points for item in csdm.controlled_variables]
        [item.reshape(npts[::-1]) for item in csdm.uncontrolled_variables]
    else:
        _type = [(item.sampling_type == 'scatter')
                 for item in csdm.controlled_variables]

        if not np.all(_type):
            raise Exception(
                (
                    "controlled_variables can be either be all grid "
                    "or all scatter type. Type mixing is not supported."
                )
            )

# Create the augmentation layer model #

    return csdm


def new():
    r"""
    Return an empty CSDModel object. ::

        >>> import csdfpy
        >>> emptydata = csdfpy.new()
        >>> print(emptydata.data_structure)
        {
          "CSDM": {
            "uncontrolled_variables": [],
            "controlled_variables": [],
            "version": "0.0.9"
          }
        }

    :returns: A CSDModel object
    """
    return CSDModel()


class CSDModel:
    r"""
    A python module for handling the CSD format files, `.csdf` and `.csdfx`.

    The module is bulit on the concept of the core scientific dataset (CSD)
    model which follows,

    .. math::

        y_\alpha = f_\alpha(x_0, x_1, ... x_k, ... x_{d-1})
        \forall \alpha \in \mathbb{Z}

    where :math:`y_\alpha` is the uncontrolled variable and the :math:`x_k`,
    :math:`k \in \{0, 1, ... ,d-1\}`, are the controlled variables. The model
    supports any arbitrary :math:`d`-dimensional controlled variable space
    where :math:`x_k` is its :math:`k^\mathrm{th}` dimension, and any arbitrary
    :math:`p_\alpha`-dimensional uncontrolled variable space.

    The CSDModel class also support multiple uncontrolled variables. This
    is represented with the subscript :math:`\alpha`,
    :math:`\alpha \in \mathbb{Z}`, where each uncontrolled variable lives in a
    unique :math:`p_\alpha`-dimensional space, with the limitation that all
    :math:`y_\alpha` must share the same set of controlled variable
    coordinates.

    In ``csdfpy`` package, every control variable, :math:`x_k`, is represented
    as a :ref:`cv_api` object and every uncontrol variable, :math:`y_\alpha`,
    by :ref:`uv_api` object. The ``CSDModel`` class holdes and manages the
    tuples of both these variable objects.

    :returns: A CSDM object.
    """

    __version__ = version
    _old_compatible_versions = ('0.0.9')
    _old_incompatible_versions = ()

    __slots__ = [
            '_controlled_variables',
            '_uncontrolled_variables',
            '_version',
            '_filename',
        ]

    def __init__(self, filename='', version=None):
        """Python module from reading and writing CSDF files."""
        if version is None:
            version = self.__version__
        elif version in self._old_incompatible_versions:
            raise Exception(
                (
                    "Files created with the version {0} of the CSDModel "
                    "are no longer supported."
                ).format(version)
            )

        super(CSDModel, self).__setattr__('_controlled_variables', ())
        super(CSDModel, self).__setattr__('_uncontrolled_variables', ())
        super(CSDModel, self).__setattr__('_version', version)
        super(CSDModel, self).__setattr__('_filename', filename)

    @classmethod
    def __delattr__(cls, name):
        """Delete attribute."""
        if name in cls.__slots__:
            raise AttributeError(
                "Attribute '{0}' cannot be deleted.".format(name)
            )

    @classmethod
    def __setattr__(cls, name, value):
        """Set attribute."""
        if name in cls.__slots__:
            raise AttributeError(
                "Attribute '{0}' cannot be modified.".format(name)
            )
        else:
            raise AttributeError(
                "The '{0}' object has no attribute '{1}'.".format(
                    cls.__name__, name)
            )

# ---- Attribute ----#
# controlled variables
    @property
    def controlled_variables(self):
        """Return a tuple of :ref:`cv_api` objects."""
        return self._controlled_variables

# uncontrolled variables
    @property
    def uncontrolled_variables(self):
        """Return a tuple of :ref:`uv_api` objects."""
        return self._uncontrolled_variables

# CSD model version on file
    @property
    def version(self):
        """Return a the version number of the :ref:`csdm_api` on file."""
        return self._version

# CSD model version on file
    @property
    def filename(self):
        """
        Return the local file address to the current file.

        The file extensions include the `.csdf` and the `.csdfx`.
        """
        return self._filename

    @property
    def data_structure(self):
        r"""
        Return the :ref:`csdm_api` object as a json object.

        The attribute cannot be modified.

        :raises AttributeError: When modified.
        """
        dictionary = self.get_python_dictionary(
            self.filename, print_function=True
        )

        return (json.dumps(dictionary, ensure_ascii=False,
                           sort_keys=False, indent=2))

# ----------- Public Methods -------------- #

    def add_controlled_variable(self, *arg, **kwargs):
        """
        Add a new :ref:`cv_api` to the :ref:`csdm_api` object.

        There are a number of different ways to add a control variable.

        Add a control variable with a python dictionary containing valid
        keywords. ::

            >>> datamodel = CSDModel()
            ...
            >>> py_dictionary = {
                    'sampling_interval': '5 G'
                    'number_of_points: 50,
                    'reference_offset': '-10 mT'
                }
            >>> datamodel.add_controlled_variable(py_dictionary)

        Add a control variable with valid keyword arguaments. ::

            >>> datamodel.add_controlled_variable(sampling_interval = '5 G',
                                                  number_of_points = 50,
                                                  reference_offset = '-10 mT')

        Add a control variable with a :ref:`cv_api` instance. ::

            >>> from csdfpy import ControlledVariable
            >>> var1 = ControlledVariable(sampling_interval = '5 G',
                                          number_of_points = 50,
                                          reference_offset = '-10 mT')
            >>> datamodel.add_controlled_variable(var1)
        """
        if arg != () and isinstance(arg[0], ControlledVariable):
            super(CSDModel, self).__setattr__(
                '_controlled_variables', self.controlled_variables + (
                    arg[0],
                    )
                )
        else:
            super(CSDModel, self).__setattr__(
                '_controlled_variables', self.controlled_variables + (
                    ControlledVariable(*arg, **kwargs),
                    )
                )

    def add_uncontrolled_variable(self, *arg, **kwargs):
        """
        Add a new :ref:`uv_api` to the :ref:`csdm_api` object.

        There are again a number of different ways to add an uncontrol
        variable.

        Add an uncontrol variable with a python dictionary containing valid
        keywords. ::

            >>> datamodel = CSDModel()
            ...
            >>> numpy_array = (100*np.random.rand(3,50)).astype(np.uint8))
            >>> py_dictionary = {
            ...     'components': numpy_array,
            ...     'name': 'star',
            ...     'unit': 'W s',
            ...     'quantity': 'energy',
            ...     'dataset_type': 'RGB'
            ... }
            >>> datamodel.add_uncontrolled_variable(py_dictionary)


        Add an uncontrol variable with valid keyword arguaments. ::

            >>> datamodel.add_uncontrolled_variable(name='star',
            ...                                     unit='W s',
            ...                                     dataset_type='RGB',
            ...                                     components=numpy_array)

        Add an uncontrol variable with a :ref:`uv_api` instance. ::

            >>> from csdfpy import UncontrolledVariable
            >>> var1 = UncontrolledVariable(name='star',
            ...                             unit='W s',
            ...                             dataset_type='RGB',
            ...                             components=numpy_array)
            >>> datamodel.add_uncontrolled_variable(var1)
        """
        if arg != () and isinstance(arg[0], UncontrolledVariable):
            super(CSDModel, self).__setattr__(
                '_uncontrolled_variables', self.uncontrolled_variables + (
                    arg[0],
                    )
                )
        else:
            super(CSDModel, self).__setattr__(
                '_uncontrolled_variables', self.uncontrolled_variables + (
                    UncontrolledVariable(
                        filename=self.filename, *arg, **kwargs
                        ),
                    )
                )

    def _info(self):
        x = [
            'sampling_type',
            'non_quantitative',
            'number_of_points',
            'sampling_interval',
            'reference_offset',
            'origin_offset',
            'made_dimensionless',
            'reverse',
            'quantity',
            'label',
            'ftFlag',
            'period'
        ]

        y = []
        for i in range(len(self.controlled_variables)):
            y.append(self.controlled_variables[i]._info())
        pack = np.asarray(y).T, x, ['dimension '+str(i)
                                    for i in range(
                                        len(self.controlled_variables)
                                        )
                                    ]

        return pack

    def get_python_dictionary(self, filename, print_function=False,
                              version=__version__):
        """Return the CSDModel object as a python dictionary."""
        dictionary = {}
        dictionary["uncontrolled_variables"] = []
        dictionary["controlled_variables"] = []
        dictionary["version"] = version
        for i in range(len(self.controlled_variables)):
            dictionary["controlled_variables"].append(
                self.controlled_variables[i].get_python_dictionary()
            )

        _length_of_uncontrolled_variables = len(self.uncontrolled_variables)

        for i in range(_length_of_uncontrolled_variables):
            dictionary["uncontrolled_variables"].append(
                self.uncontrolled_variables[i].get_python_dictionary(
                    filename=filename,
                    dataset_index=i,
                    for_display=print_function,
                    version=self.__version__)
                )

        csdm = {}
        csdm['CSDM'] = dictionary
        return csdm

    def save(self, filename, version=__version__):
        """
        Save the CSD model to a file.

        This method allows data storage with two types file extensions.
        When the data values are stored within the file, a ``.csdf`` file
        extension is added. When the data values are store in an external
        file either at a local or a remote server, a ``.csdfx`` file
        extension is used. ::

            >>> datamodel.save('myfile')

        where ``datamodel`` is an instance of the CSDModel class.
        """
        dictionary = self.get_python_dictionary(filename, version=version)
        with open(filename, 'w', encoding='utf8') as outfile:
            json.dump(dictionary, outfile, ensure_ascii=False,
                      sort_keys=False, indent=2)

    def copy(self):
        """Return a copy of the current CSDModel object."""
        return deepcopy(self)

    def replace(self,
                controlled_variable=None,
                cv_index=-1,
                uncontrolled_variable=None,
                uv_index=-1):
        """
        Repalce the controlled or the uncontrolled variable at the index.

        :params: controlled_variable: A new ControlledVariable object or a
            python dictionary corresponding to a new ControlledVariable object.
        :params: cv_index: An integer corresponding to the
            UncontrolledVariable object to the updated.
        :params: uncontrolled_variable: A new UncontrolledVariable object or a
            python dictionary corresponding to a new UncontrolledVariable
            object.
        :params: uv_index: An integer corresponding to the
            UncontrolledVariable object to the updated.

        .. todo::
            Well, write the method.
        """
        pass

    def sum(self, cv=-1):
        """
        Project the data values onto the control variable at index, `cv`.

        :params: cv: An integer cooresponding to the control variable onto
            which the data values are projected.
        :returns: A ``CSDModel`` object.
        """
        new = CSDModel()
        d = len(self.controlled_variables)
        if cv > d:
            raise ValueError(
                (
                    "`cv` {0} cannot be greater than number of control"
                    "variables, {1}."
                ).format(cv, d)
            )
        for variable in self.uncontrolled_variables:
            y = variable.components.sum(axis=-1-cv)
            new.add_uncontrolled_variable(
                components=y,
                name=variable.name,
                quantity=variable.quantity,
                encoding=variable.encoding,
                numeric_type=variable.numeric_type,
                dataset_type=variable.dataset_type,
                component_labels=variable.component_labels,
                components_uri=variable.components_uri,
            )
        for i, variable in enumerate(self.controlled_variables):
            if i != cv:
                new.add_controlled_variable(variable)

        return new

    def fft(self, cv=0):
        """
        Perform a FFT along the specified control variable (cv).

        Needs debugging.
        """
        if not self.controlled_variables[cv].is_quantitative():
            raise ValueError(
                'Non-quantitative dimensions cannot be Fourier transformed.'
            )

        s = "Arbitrarily sampled grid controlled variable"
        if self.controlled_variables[cv].variable_type == s:
            raise NotImplementedError(
                (
                    "Fourier tranform of an arbitrarily sampled "
                    "grid dimension is not implemanted."
                )
            )

        if self.controlled_variables[cv].sampling_type == 'scatter':
            raise NotImplementedError(
                (
                    "Fourier transform of a scattered "
                    "dimensions is not implemented."
                )
            )

        cs = self.controlled_variables[cv].reciprocal_coordinates

        # + \
        # self.controlled_variables[cv].reciprocal_reference_offset

        phase = np.exp(
            1j * 2*np.pi *
            self.controlled_variables[cv].reference_offset * cs
        )

        ndim = len(self.controlled_variables)

        for i in range(len(self.uncontrolled_variables)):
            signal_ft = fftshift(
                fft(self.uncontrolled_variables[i].components,
                    axis=-cv-1), axes=-cv-1
                ) * get_broadcase_shape(phase, ndim, axis=-cv-1)

            self.uncontrolled_variables[i].uv.set_attribute(
                '_components', signal_ft
            )

        self.controlled_variables[cv].gcv._reciprocal()
        self._toggle_fft_output_order(self.controlled_variables[cv])

    def _toggle_fft_output_order(self, control_variable):
        if control_variable.fft_output_order:
            control_variable.fft_output_order = False
        else:
            control_variable.fft_output_order = True

    def __add__(self, other):
        """
        Add two CSDModel instances.

        We follow a safe rule---the addition of two CSDModel instances
        will only be successfull when the attributes of the corresponding
        ControlledVariable instances are identical.
        """
        if not _compare_cv_objects(self, other):
            raise Exception("Cannot add")

        dim1 = len(self.uncontrolled_variables)
        dim2 = len(other.uncontrolled_variables)

        if dim1 != dim2:
            raise Exception(
                (
                    "Cannot add {0} and {1}. They have differnet "
                    "number of uncontrolled variables."
                ).format(self.__class__.__name__, other.__class__.__name__)
            )

        d1 = deepcopy(self)
        for i in range(dim1):
            if _compare_uv(
                self.uncontrolled_variables[i],
                other.uncontrolled_variables[i]
            ):
                d1.uncontrolled_variables[i].components += \
                    other.uncontrolled_variables[i].components

        return d1

    def __sub__(self, other):
        """
        Subtract two CSDModel instances.

        We follow a safe rule---the subtraction of two CSDModel instances
        will only be successfull when the attributes of the corresponding
        ControlledVariable instances are identical.
        """
        pass

    def __mul__(self, other):
        """
        Multiply two CSDModel instances.

        We follow a safe rule---the multiplication of two CSDModel instances
        will only be successfull when the attributes of the corresponding
        ControlledVariable instances are identical.
        """
        pass

    def __div__(self, other):
        """
        Divide two CSDModel instances.

        We follow a safe rule---the division of two CSDModel instances
        will only be successfull when the attributes of the corresponding
        ControlledVariable instances are identical.
        """
        pass


def get_broadcase_shape(array, ndim, axis):
    """Return the broadcast array for numpy ndarray operations."""
    s = [None for i in range(ndim)]
    s[axis] = slice(None, None, None)
    return array[tuple(s)]


def _compare_cv_object(cv1, cv2):
    if cv1.gcv._getparams == cv2.gcv._getparams:
        return True
    return False


def _compare_cv_objects(object1, object2):
    dim1 = len(object1.controlled_variables)
    dim2 = len(object2.controlled_variables)

    message = (
        "{0} and {1} do not have the same set of "
        "controlled variables."
    ).format(object1.__name__, object2.__name__)

    if dim1 != dim2:
        raise Exception(message)

    for i in range(dim1):
        if not _compare_cv_object(
            object1.controlled_variables[i],
            object2.controlled_variables[i]
        ):
            raise Exception(message)

    return True


def _compare_uv(uv1, uv2):
    # a = {
    #     'unit': True,
    #     'quantity': True,
    #     'dataset_type': True
    # }
    a = True
    if uv1.unit.physical_type != uv2.unit.physical_type:
        a = False
    if uv1.quantity != uv2.quantity:
        raise Exception(
            (
                "Binary operates are not supported for "
                "objects with different quantity."
            )
        )
    if uv1.dataset_type != uv2.dataset_type:
        raise Exception(
            (
                "Binary operates are not supported for "
                "objects with different dataset_type."
            )
        )
    return a


# def _compare_uv_objects(object1, object2):
#     dim1 = len(object1.uncontrolled_variables)
#     dim2 = len(object2.uncontrolled_variables)

#     for j in range(dim1):
#         for i in range(dim2):
#             a = _compare_uv(
#                 object1.uncontrolled_variables[i],
#                 object2.uncontrolled_variables[j]
#             )

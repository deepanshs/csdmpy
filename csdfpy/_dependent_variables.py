"""The DependentVariable SubType classes."""

from __future__ import print_function, division
import numpy as np
import base64
from os import path

from urllib.request import urlopen
from urllib.parse import urlparse

import warnings
from copy import deepcopy

from ._utils import (
    numpy_dtype_to_numeric_type,
    _check_encoding,
    _type_message,
    NumericType,
    QuantityType
)


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


# Decode data functions #

def _decode_base64(_components, _dtype):
    _components = np.asarray([np.frombuffer(base64.b64decode(item),
                             dtype=_dtype)
                             for item in _components])

    # _components.setflags(write=1)
    return _components


def _decode_none(_components, _dtype):
    if _dtype in ['<c8', '<c16']:
        _components = np.asarray(
            [np.asarray(item[0::2]) + 1j*np.asarray(item[1::2])
                for item in _components], dtype=_dtype
        )
    else:
        _components = np.asarray(
            [np.asarray(item) for item in _components],
            dtype=_dtype
        )

    # _components.setflags(write=1)
    return _components


def _decode_raw(_components, _dtype, _component_num):
    _components = np.fromstring(_components, dtype=_dtype)
    # print(_components.flags)
    # _components = np.array(_components, copy=True)
    # _components.setflags(write=1)
    _components.shape = _component_num, int(_components.size/_component_num)
    return _components
# --------------------------------------------------------------


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


# def _get_relative_data_address(data_absolute_uri, file):
#     res = urlparse(data_absolute_uri)
#     _data_abs_path = path.abspath(res.path)
#     _file_abs_path = path.split(path.abspath(file))[0]
#     _data_rel_path = path.relpath(_data_abs_path, start=_file_abs_path)
#     return 'file:./'+_data_rel_path


def _get_absolute_uri_path(uri, file):
    res = urlparse(uri)
    path = uri
    # print(res)
    if res.scheme in ['file', '']:
        if res.netloc == '':
            path = _get_absolute_data_address(res.path, file)
    return path


def _get_relative_uri_path(dataset_index, filename):
    index = str(dataset_index)
    file_save_path_abs = _get_absolute_uri_path('', filename)

    _name = path.splitext(path.split(filename)[1])[0] + '_' + index + '.dat'

    _URI_data_path_relative = path.join('file:.', _name)

    data_path_absolute = path.abspath(
        urlparse(path.join(
            file_save_path_abs, urlparse(_URI_data_path_relative).path
        )).path
    )
    return _URI_data_path_relative, data_path_absolute

# =========================================================================== #
#               	       BaseDependentVariable Class      			      #
# =========================================================================== #


class BaseDependentVariable:
    r"""Declare a BaseDependentVariable class."""

    __slots__ = (
        '_encoding',
        '_numeric_type',
        '_quantity_type',
        '_component_labels',
        '_total_components',
    )

    def __init__(
            self,
            _encoding='none',
            _numeric_type='float32',
            _quantity_type='scalar',
            _component_labels=None):

        r"""Instantiate a BaseDependentVariable class."""

        self._set_parameters(
            _encoding,
            _numeric_type,
            _quantity_type,
            _component_labels)

    def _set_parameters(
            self,
            _encoding='none',
            _numeric_type='float32',
            _quantity_type='scalar',
            _component_labels=None):

        # encoding
        self.encoding = _encoding

        # numeric type
        self._numeric_type = NumericType(_numeric_type)

        # dataset_tpye
        self._quantity_type = QuantityType(_quantity_type)

        # components label
        self.set_components_label(_component_labels)

    def set_components_label(self, component_labels):
        """
        Assign an array of strings, based on the number of components.

        If no label is provided, a default values,
        :math:`['', '', N_k]`, is assigned. If the number of component labels
        does not match the total number of components, a warning is raised and
        the inconsistency is resolved by appropriate truncating or additing the
        required number of strings.
        """
        _n = self._quantity_type._p
        if component_labels is None:
            _labels = ['' for i in range(_n)]
            self._component_labels = _labels
            return

        if not isinstance(component_labels, list):
            raise ValueError((
                    "A list of string labels is required, "
                    "{0} provided."
                ).format(type(component_labels))
            )

        _component_length = len(component_labels)
        if _component_length != _n:
            warnings.warn((
                    "The number of component labels, {0}, is not equal to the "
                    "number of components, {1}. The inconsistency is resolved "
                    "by appropriate truncation or addition of the strings."
                ).format(len(component_labels), _n)
            )

            if _component_length > _n:
                self._component_labels = component_labels[:_n]
            else:
                _lables = ['' for i in range(_n)]
                for i, item in enumerate(component_labels):
                    _lables[i] = item
                self._component_labels = _lables
            return

        self._component_labels = component_labels

# --------------------------------------------------------------------------- #
#                     BaseIndependentVariable Attributes                      #
# --------------------------------------------------------------------------- #

# encoding
    @property
    def encoding(self):
        r"""Return the data encoding method."""
        return deepcopy(self._encoding)

    @encoding.setter
    def encoding(self, value):
        if not isinstance(value, str):
            raise TypeError(_type_message(str, type(value)))
        value = _check_encoding(value)
        self._encoding = value

# numeric type
    @property
    def numeric_type(self):
        r"""Return the numeric type of data values."""
        return deepcopy(self._numeric_type)

    @numeric_type.setter
    def numeric_type(self, value):
        self._numeric_type._update(value)

# quantity type
    @property
    def quantity_type(self):
        r"""Returns the quantity type of the dataset."""
        return deepcopy(self._quantity_type)

    @quantity_type.setter
    def quantity_type(self, value):
        self._quantity_type._update(value)

# component labels
    @property
    def component_labels(self):
        r"""Returns an ordered array of labels."""
        return deepcopy(self._component_labels)

    @component_labels.setter
    def component_labels(self, value):
        self.set_components_label(value)

# --------------------------------------------------------------------------- #
#                      BaseIndependentVariable Methods                        #
# --------------------------------------------------------------------------- #

    def _get_dictionary(self):
        r"""Return a dictionary object of the base class."""

        dictionary = {}

        dictionary['encoding'] = str(self._encoding)
        dictionary['numeric_type'] = str(self._numeric_type)

        if str(self._quantity_type) != 'scalar':
            dictionary['quantity_type'] = str(self._quantity_type)

        print_label = False
        for label in self._component_labels:
            if label.strip() != '':
                print_label = True
                break

        if print_label:
            dictionary['component_labels'] = self._component_labels

        return dictionary


# =========================================================================== #
#                             InternalDataset Class                           #
# =========================================================================== #


class InternalDataset(BaseDependentVariable):

    __slots__ = (
        '_components',
    )

    def __init__(
            self,
            _name='',
            _unit='',
            # _type='internal',
            _quantity=None,
            _encoding='none',
            _numeric_type=None,
            _quantity_type='scalar',
            _component_labels=None,
            _components=None):

        # self._type = internal

        # if components is a python list
        if isinstance(_components, list) and _components != []:
            if isinstance(_components[0], np.ndarray):
                _components = np.asarray(_components)
            # if isinstance(_components[0], list):
            #     if _numeric_type not in ['complex64', 'complex128']:
            #         _components = np.asarray(_components)

        # if components is numpy array
        if isinstance(_components, np.ndarray):
            # if _numeric_type not in ['complex64', 'complex128']:
            _numeric_type = numpy_dtype_to_numeric_type(
                str(_components.dtype)
            )

            self._components = _components

        self._set_parameters(
            _encoding,
            _numeric_type,
            _quantity_type,
            _component_labels)

        if not isinstance(_components, np.ndarray):
            _components = self._decode_components(_components)
            self._components = _components

        # sampling schedule
        """
        .. todo::
            Support for under sampled orthogonal grid based datasets
        """
        # self.set_attribute('_sampling_schedule', _sampling_schedule)

# --------------------------------------------------------------------------- #
#                          InternalDataset Methods                            #
# --------------------------------------------------------------------------- #

    def _check_number_of_components_and_encoding_key(self, length):
        """Verify the consistency of encoding wrt the number of components."""
        if length != self._quantity_type._p:
            raise Exception((
                "quantity_type '{0}' requires exactly {1} component(s), "
                "found {2}."
                ).format(
                    self._quantity_type._value,
                    self._quantity_type._p,
                    length
                )
            )

    def _set_components(self, _components, _numeric_type=None):
        # numeric type
        if _numeric_type is None:
            _numeric_type = numpy_dtype_to_numeric_type(
                str(_components.dtype)
            )
        self._numeric_type._update(_numeric_type)

        # components
        self._components = np.asarray(_components, self._numeric_type._nptype)

    def _decode_components(self, _components):
        """
        Decode the components based on the encoding key value.

        The valid encodings are 'base64', 'none' (text), and 'raw' (binary).
        """
        _val_len = len(_components)

        if self.encoding == 'base64':
            self._check_number_of_components_and_encoding_key(_val_len)
            return _decode_base64(_components, self._numeric_type._nptype)

        if self._encoding == 'none':
            self._check_number_of_components_and_encoding_key(_val_len)
            return _decode_none(_components, self._numeric_type._nptype)

        if self._encoding == 'raw':
            _dtype = self._numeric_type._nptype
            _component_num = self._quantity_type._p
            return _decode_raw(_components, _dtype, _component_num)

        raise Exception(
            "'{0}' is an invalid data 'encoding'.".format(self._encoding)
        )

    def _ravel_data(self):
        """Encode data based on the encoding key value."""
        _n = self._quantity_type._p
        size = self._components[0].size
        if self._numeric_type._value in ['complex64', 'complex128']:

            if self._numeric_type._value == 'complex64':
                c = np.empty((_n, size*2), dtype=np.float32)

            if self._numeric_type._value == 'complex128':
                c = np.empty((_n, size*2), dtype=np.float64)

            for i in range(_n):
                c[i, 0::2] = self._components.real[i].ravel()
                c[i, 1::2] = self._components.imag[i].ravel()

        else:
            c = np.empty((_n, size), dtype=self._numeric_type._nptype)
            for i in range(_n):
                c[i] = self._components[i].ravel()

        return c

    def _reduced_display(self):
        """
            Reduced display for quick view of the data structure. The method
            shows the first and the last two data values.
        """
        _str = ''
        for i in range(len(self._components)):
            temp = self._components[i].ravel()
            lst = [str(temp[0]), str(temp[0]),
                   str(temp[-2]), str(temp[-2])]
            _string = (
                "[{0}, {1}, ...... {2}, {3}], "
            ).format(*lst)
            _str = _str + _string
        temp = None
        return _str

    def _get_python_dictionary(self, filename=None, dataset_index=None,
                               for_display=True, version=None):
        """Return the InternalData object as a python dictionary."""
        dictionary = {}

        if for_display:
            dictionary.update(self._get_dictionary())
            dictionary['components'] = self._reduced_display()[:-2]
            del dictionary['encoding']
            return dictionary

        c = self._ravel_data()

        if self.encoding == 'none':
            dictionary['type'] = 'internal'
            dictionary.update(self._get_dictionary())
            dictionary['components'] = c.tolist()
        if self.encoding == 'base64':
            dictionary['type'] = 'internal'
            dictionary.update(self._get_dictionary())
            dictionary['components'] = [base64.b64encode(item).decode(
                "utf-8") for item in c]

        if self.encoding == 'raw':
            _URI_data_path_relative, data_path_absolute = \
                _get_relative_uri_path(dataset_index, filename)

            c.ravel().tofile(data_path_absolute)

            dictionary['type'] = 'external'
            dictionary.update(self._get_dictionary())
            dictionary['components_URI'] = _URI_data_path_relative

        del c
        return dictionary

# --------------------------------------------------------------------------- #
#                        InternalDataset Attributes                           #
# --------------------------------------------------------------------------- #

    @property
    def components(self):
        dtype = self._numeric_type._nptype
        if self._components.dtype != dtype:
            self._components = np.asarray(self._components, dtype)
        return self._components

    @components.setter
    def components(self, value):
        value = np.asarray(value)
        if value.shape == self.components.shape:
            self._set_components(value)
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

# =========================================================================== #
#                            ExternalDataset Class                            #
# =========================================================================== #


class ExternalDataset(InternalDataset):

    __slots__ = (
        '_components_uri'
    )

    def __init__(
            self,
            _name='',
            _unit='',
            _quantity=None,
            _encoding='none',
            _numeric_type=None,
            _quantity_type='scalar',
            _component_labels=None,
            _components_uri=None,
            _filename=''):

        self._set_parameters(
            _encoding,
            _numeric_type,
            _quantity_type,
            _component_labels)

        # self._type = 'external'

        _absolute_URI = _get_absolute_uri_path(
            _components_uri, _filename
        )
        self._components_uri = _components_uri

        _components = urlopen(_absolute_URI).read()
        self._components = self._decode_components(_components)

    @property
    def components_uri(self):
        return self._components_uri

    def _download_file_contents_from_url(self, filename):
        pass

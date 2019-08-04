# -*- coding: utf-8 -*-
"""The Internal DependentVariable SubType classes."""
from __future__ import division
from __future__ import print_function

import numpy as np

from csdmpy.dependent_variables.base_class import BaseDependentVariable
from csdmpy.dependent_variables.decoder import Decoder
from csdmpy.dependent_variables.sparse import SparseSampling
from csdmpy.utils import numpy_dtype_to_numeric_type


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["InternalDataset"]


class InternalDataset(BaseDependentVariable):
    """InternalDataset class."""

    __slots__ = ("_components", "_sparse_sampling")

    def __init__(self, **kwargs):
        """Initialize."""
        self._sparse_sampling = {}

        components = kwargs["components"]
        if isinstance(components, list) and components != []:
            if isinstance(components[0], np.ndarray):
                components = np.asarray(components)

        if isinstance(components, np.ndarray):
            if kwargs["numeric_type"] is None:
                kwargs["numeric_type"] = numpy_dtype_to_numeric_type(
                    str(components.dtype)
                )
                kwargs["components"] = components
            else:
                kwargs["components"] = components.astype(kwargs["numeric_type"])

        if kwargs["numeric_type"] is None:
            raise ValueError(
                "Missing a required `numeric_type` key from the dependent variable."
            )

        # super base class must be initialized before retrieving
        # the components array.
        super(InternalDataset, self).__init__(**kwargs)

        if not isinstance(components, np.ndarray):
            components = Decoder(
                self._encoding,
                self._quantity_type,
                components,
                self._numeric_type.dtype,
            )
            self._components = components

        if kwargs["sparse_sampling"] != {}:
            self._sparse_sampling = SparseSampling(**kwargs["sparse_sampling"])

    def _get_python_dictionary(
        self, filename=None, dataset_index=None, for_display=True, version=None
    ):
        """Serialize the InternalData object as a python dictionary."""
        dictionary = {}

        dictionary["type"] = "internal"
        dictionary.update(
            self._get_dictionary(filename, dataset_index, for_display, version)
        )
        return dictionary

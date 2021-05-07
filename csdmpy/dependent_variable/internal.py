# -*- coding: utf-8 -*-
"""The Internal DependentVariable SubType class."""
from __future__ import division
from __future__ import print_function

import numpy as np

from .base_class import BaseDependentVariable
from .decoder import Decoder
from csdmpy.utils import numpy_dtype_to_numeric_type


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["InternalDataset"]


class InternalDataset(BaseDependentVariable):
    """InternalDataset class."""

    def __init__(self, **kwargs):
        """Initialize."""
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
            raise KeyError(
                "Missing a required `numeric_type` key from the DependentVariable "
                "object."
            )

        # super base class must be initialized before retrieving
        # the components array.
        super().__init__(**kwargs)

        if not isinstance(components, np.ndarray):
            self._components = Decoder(
                self._encoding,
                self._quantity_type,
                components,
                self._numeric_type.dtype,
            )

        size = self._components.size
        p = self.quantity_type.p
        self._components.shape = (p, int(size / p))

    def dict(self, filename=None, dataset_index=None, for_display=False):
        """Return InternalDataset object as a python dictionary."""
        dictionary = {}
        dictionary["type"] = "internal"
        dictionary.update(super().dict(filename, dataset_index, for_display))
        return dictionary

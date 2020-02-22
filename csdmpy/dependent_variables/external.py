# -*- coding: utf-8 -*-
"""The External DependentVariable SubType class."""
from __future__ import division
from __future__ import print_function

from urllib.request import urlopen

import numpy as np

from csdmpy.dependent_variables.base_class import BaseDependentVariable
from csdmpy.dependent_variables.decoder import Decoder
from csdmpy.dependent_variables.download import get_absolute_url_path
from csdmpy.dependent_variables.sparse import SparseSampling

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["ExternalDataset"]


class ExternalDataset(BaseDependentVariable):
    """ExternalDataset class."""

    __slots__ = ("_components_url", "_sparse_sampling")

    def __init__(self, **kwargs):
        """Initialize."""
        self._sparse_sampling = {}
        kwargs["encoding"] = "raw"

        if kwargs["numeric_type"] is None:
            raise KeyError(
                "Missing a required `numeric_type` key from the DependentVariable "
                "object."
            )

        super().__init__(**kwargs)

        components_url = kwargs["components_url"]
        filename = kwargs["filename"]
        absolute_url = get_absolute_url_path(components_url, filename)
        self._components_url = components_url

        components = urlopen(absolute_url).read()
        self._components = Decoder(
            self._encoding, self._quantity_type, components, self._numeric_type.dtype
        )

        if self._components.ndim == 1:
            self._components = self._components[np.newaxis, :]

        if kwargs["sparse_sampling"] != {}:
            self._sparse_sampling = SparseSampling(**kwargs["sparse_sampling"])

    @property
    def components_url(self):
        """Return the components_url of the CSDM serialized file."""
        return self._components_url

    def to_dict(
        self, filename=None, dataset_index=None, for_display=False, version=None
    ):
        """Return ExternalDataset object as a python dictionary."""
        dictionary = {}

        dictionary["type"] = "internal"
        dictionary.update(
            self._get_dictionary(filename, dataset_index, for_display, version)
        )
        return dictionary

    def __eq__(self, other):
        """Overrides the default implementation"""
        check = [
            self._name == other._name,
            self._unit == other._unit,
            self._quantity_name == other._quantity_name,
            self._encoding == other._encoding,
            self._numeric_type == other._numeric_type,
            self._quantity_type == other._quantity_type,
            self._component_labels == other._component_labels,
            self._description == other._description,
            self._application == other._application,
            np.allclose(self._components, other._components),
            self._sparse_sampling == other._sparse_sampling,
            self._components_url == other._components_url,
        ]
        if False in check:
            return False
        return True

# -*- coding: utf-8 -*-
"""The External DependentVariable SubType classes."""
from __future__ import division
from __future__ import print_function

from urllib.request import urlopen

from csdfpy.dependent_variables.base_class import BaseDependentVariable
from csdfpy.dependent_variables.decoder import Decoder
from csdfpy.dependent_variables.download import _get_absolute_uri_path
from csdfpy.dependent_variables.sparse import SparseSampling


class ExternalDataset(BaseDependentVariable):
    """ExternalDataset class."""

    __slots__ = ("_components", "_components_url", "_sparse_sampling")

    def __init__(self, **kwargs):
        """Initialize."""
        self._sparse_sampling = {}
        kwargs["encoding"] = "raw"
        super(ExternalDataset, self).__init__(**kwargs)

        components_url = kwargs["components_url"]
        filename = kwargs["filename"]
        _absolute_URI = _get_absolute_uri_path(components_url, filename)
        self._components_url = components_url

        components = urlopen(_absolute_URI).read()
        self._components = Decoder(
            self._encoding,
            self._quantity_type,
            components,
            self._numeric_type._nptype,
        )

        if kwargs["sparse_sampling"] != {}:
            self._sparse_sampling = SparseSampling(**kwargs["sparse_sampling"])

    @property
    def components_url(self):
        """Return components_url of the CSDM serialized file."""
        return self._components_url

    def _get_python_dictionary(
        self, filename=None, dataset_index=None, for_display=True, version=None
    ):
        """Return the InternalData object as a python dictionary."""
        dictionary = {}

        dictionary["type"] = "internal"
        dictionary.update(
            self._get_dictionary(filename, dataset_index, for_display, version)
        )
        return dictionary

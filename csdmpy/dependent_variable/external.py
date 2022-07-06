"""The External DependentVariable SubType class."""
from urllib.request import urlopen

import numpy as np

from csdmpy.dependent_variable.base_class import BaseDependentVariable
from csdmpy.dependent_variable.decoder import Decoder
from csdmpy.dependent_variable.download import get_absolute_url_path

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["ExternalDataset"]


class ExternalDataset(BaseDependentVariable):
    """ExternalDataset class."""

    __slots__ = ["_components_url"]

    def __init__(self, **kwargs):
        """Initialize."""
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

    @property
    def components_url(self):
        """Return the components_url of the CSDM serialized file."""
        return self._components_url

    def dict(self, filename=None, dataset_index=None, for_display=False):
        """Return ExternalDataset object as a python dictionary."""
        dictionary = {}
        dictionary["type"] = "internal"
        dictionary.update(super().dict(filename, dataset_index, for_display))
        return dictionary

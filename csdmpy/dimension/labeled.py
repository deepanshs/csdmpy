"""The Labeled Dimension sub type class."""
import numpy as np

from .base import _copy_core_metadata
from .base import BaseDimension
from .base import check_count


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["LabeledDimension"]


class LabeledDimension(BaseDimension):
    """A labeled dimension.

    Generates an object representing a non-physical dimension whose coordinates are
    labels. See :ref:`labeledDimension_uml` for details.
    """

    __slots__ = ("_count", "_labels")

    _type = "labeled"

    def __init__(self, labels, label="", description="", application=None, **kwargs):
        """Instantiate a LabeledDimension class."""
        super().__init__(label, application, description)
        self.labels = labels

    def __repr__(self):
        content = [f"{k}={v}" for k, v in self.dict().items() if k != "type"]
        properties = ", ".join(content)
        return f"LabeledDimension({properties})"

    def __str__(self):
        return f"LabeledDimension({self.coordinates.__str__()})"

    def __eq__(self, other):
        other = other.subtype if hasattr(other, "subtype") else other
        if not isinstance(other, LabeledDimension):
            return False
        check = [
            self._count == other._count,
            np.all(self._labels == other._labels),
            super().__eq__(other),
        ]
        return np.all(check)

    def is_quantitative(self):
        """Return `True`, if the dimension is quantitative, otherwise `False`.
        :returns: A Boolean.
        """
        return False

    # ----------------------------------------------------------------------- #
    #                                 Attributes                              #
    # ----------------------------------------------------------------------- #

    @property
    def type(self):
        """Return the type of the dimension."""
        return self.__class__._type

    @property
    def count(self):
        """Total number of labels along the dimension."""
        return self._count

    @count.setter
    def count(self, value):
        self._count = check_count(value, self._count, "labeled")

    @property
    def labels(self):
        """Return a list of labels along the dimension."""
        return self._labels

    @labels.setter
    def labels(self, labels):
        if not isinstance(labels, list):
            raise ValueError(f"A list of labels is required, found {type(labels)}.")

        items = np.asarray([isinstance(item, str) for item in labels])
        if np.all(items):
            self._labels = np.asarray(labels)
            self._count = self._labels.size
            return

        i = np.where(items == 0)[0][0]
        name = labels[i].__class__.__name__
        raise ValueError(
            f"A list of string labels are required, found {name} at index {i}."
        )

    @property
    def coordinates(self):
        """Return the coordinates along the dimensions. This is an alias for labels."""
        return self.labels[: self._count]

    @coordinates.setter
    def coordinates(self, value):
        self.labels = value

    # ----------------------------------------------------------------------- #
    #                                 Methods                                 #
    # ----------------------------------------------------------------------- #

    def _copy_metadata(self, obj):
        """Copy LabeledDimension metadata."""
        obj = obj.subtype if hasattr(obj, "subtype") else obj
        if isinstance(obj, LabeledDimension):
            _copy_core_metadata(self, obj, "labeled")

    def dict(self):
        """Return the LabeledDimension as a python dictionary."""
        dictionary = {}
        dictionary["type"] = self.__class__._type
        dictionary["labels"] = self._labels.tolist()
        dictionary.update(super().dict())
        return dictionary

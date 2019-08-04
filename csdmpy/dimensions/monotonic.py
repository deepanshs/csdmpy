# -*- coding: utf-8 -*-
"""The MonotonicDimension SubTypes class."""
from __future__ import division
from __future__ import print_function

from copy import deepcopy

import numpy as np

from csdmpy.dimensions.quantitative import BaseQuantitativeDimension
from csdmpy.dimensions.quantitative import ReciprocalVariable
from csdmpy.units import ScalarQuantity


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["MonotonicDimension"]

# =========================================================================== #
#                     ArbitrarilySampledDimension Class                       #
# =========================================================================== #


class MonotonicDimension(BaseQuantitativeDimension):
    r"""
    A monotonic grid dimension.

    .. warning ::
        This class should not be used directly. Instead,
        use the ``CSDM`` object to access the attributes
        and methods of this class. See example, :ref:`asgd`.

    This class returns an object which represents a physical
    dimension, sampled monotonically along a grid dimension.
    Let :math:`\mathbf{A}_k` be an ordered array of physical
    quantities, :math:`c_k` be the reference offset, and
    :math:`o_k` be the origin offset along the :math:`k^{th}`
    grid dimension, then the coordinates along this dimension
    are given as

    .. math ::
        \mathbf{X}_k^\mathrm{ref} = \mathbf{A}_k - c_k \mathbf{1},
    .. math ::
        \mathbf{X}_k^\mathrm{abs} = \mathbf{X}_k^\mathrm{ref} + o_k \mathbf{1},

    where :math:`\mathbf{X}_k^\mathrm{ref}` is an ordered array of the
    reference controlled variable coordinates,
    :math:`\mathbf{X}_k^\mathrm{abs}` is an ordered array of the absolute
    controlled variable coordinates, and
    :math:`\mathbf{1}` is an array of ones.
    """

    __slots__ = ("_unit", "reciprocal", "_count", "_values", "_coordinates")

    _type = "monotonic"

    def __init__(self, values, **kwargs):
        """Instantiate a MonotonicDimension class."""
        self._unit = ScalarQuantity(values[0]).quantity.unit
        super(MonotonicDimension, self).__init__(unit=self._unit, **kwargs)

        _reciprocal_unit = self._unit ** -1
        self.reciprocal = ReciprocalVariable(
            unit=_reciprocal_unit, **kwargs["reciprocal"]
        )

        self._get_coordinates(values)

    # ----------------------------------------------------------------------- #
    #                                 Methods                                 #
    # ----------------------------------------------------------------------- #

    def _get_coordinates(self, values):
        _unit = self._unit
        _value = [
            ScalarQuantity(item, _unit).quantity.to(_unit).value for item in values
        ]
        _value = np.asarray(_value, dtype=np.float64) * _unit
        self._count = _value.size
        self._values = values
        self._coordinates = _value

    def _get_python_dictionary(self):
        dictionary = {}

        dictionary["type"] = self.__class__._type

        if self._description.strip() != "":
            dictionary["description"] = self._description.strip()

        dictionary["coordinates"] = self._values
        dictionary.update(self._get_quantitative_dictionary())

        reciprocal_dictionary = {}
        if self.reciprocal._description.strip() != "":
            reciprocal_dictionary["description"] = self.reciprocal._description.strip()
        reciprocal_dictionary.update(self.reciprocal._get_quantitative_dictionary())
        if reciprocal_dictionary == {}:
            del reciprocal_dictionary
        else:
            dictionary["reciprocal"] = reciprocal_dictionary

        return dictionary

    # ----------------------------------------------------------------------- #
    #                                 Attributes                              #
    # ----------------------------------------------------------------------- #
    @property
    def values(self):
        r"""Return a list of values along the dimension."""
        return deepcopy(self._values)

    @values.setter
    def values(self, array):
        self._get_coordinates(array)

# -*- coding: utf-8 -*-
"""The LinearDimension SubTypes class."""
from __future__ import division
from __future__ import print_function

from copy import deepcopy

import numpy as np
from astropy.units import Quantity

from csdfpy.dimensions.quantitative import BaseQuantitativeDimension
from csdfpy.dimensions.quantitative import ReciprocalVariable
from csdfpy.units import ScalarQuantity
from csdfpy.utils import check_and_assign_bool
from csdfpy.utils import validate

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__all__ = ["LinearDimension"]

# =========================================================================== #
#                          LinearDimension Class                              #
# =========================================================================== #


class LinearDimension(BaseQuantitativeDimension):
    r"""
    LinearDimension class.

    .. warning ::
        This class should not be used directly. Instead,
        use the ``CSDModel`` object to access the attributes
        and methods of this class. See example, :ref:`lsgd`.

    The class returns an object which represents a physical
    dimension, sampled uniformly along a grid dimension.
    Let :math:`m_k` be the increment, :math:`N_k \ge 1` be the
    number of points, :math:`c_k` be the reference offset, and
    :math:`o_k` be the origin offset along the :math:`k^{th}`
    grid dimension, then the coordinates along the
    grid dimension are given as

    .. math ::
        \mathbf{X}_k^\mathrm{ref} = [m_k j ]_{j=0}^{N_k-1} - c_k \mathbf{1},
    .. math ::
        \mathbf{X}_k^\mathrm{abs} = \mathbf{X}_k^\mathrm{ref} + o_k \mathbf{1},

    where :math:`\mathbf{X}_k^\mathrm{ref}` is an ordered array of the
    reference controlled variable coordinates,
    :math:`\mathbf{X}_k^\mathrm{abs}` is an ordered array of the absolute
    controlled variable coordinates, and :math:`\mathbf{1}`
    is an array of ones.
    """

    __slots__ = (
        "_count",
        "_increment",
        "_fft_output_order",
        "reciprocal",
        "_reciprocal_count",
        "_reciprocal_increment",
        "_coordinates",
    )

    _type = "linear"

    def __init__(self, count, increment, fft_output_order=False, **kwargs):
        r"""Instantiate a DimensionWithLinearSpacing class instance."""
        self._count = count
        self._increment = ScalarQuantity(increment).quantity
        self._fft_output_order = check_and_assign_bool(fft_output_order)
        self._unit = self._increment.unit

        super(LinearDimension, self).__init__(unit=self._unit, **kwargs)

        # create a reciprocal dimension
        _reciprocal_unit = self._unit ** -1
        self.reciprocal = ReciprocalVariable(
            unit=_reciprocal_unit, **kwargs["reciprocal"]
        )
        self._get_coordinates()

    # ----------------------------------------------------------------------- #
    #                                  Methods                                #
    # ----------------------------------------------------------------------- #
    def _swap(self):
        self._description, self.reciprocal._description = (
            self.reciprocal._description,
            self._description,
        )

        self._application, self.reciprocal._application = (
            self.reciprocal._application,
            self._application,
        )

        self._coordinates_offset, self.reciprocal._coordinates_offset = (
            self.reciprocal._coordinates_offset,
            self._coordinates_offset,
        )

        self._origin_offset, self.reciprocal._origin_offset = (
            self.reciprocal._origin_offset,
            self._origin_offset,
        )

        self._period, self.reciprocal._period = (self.reciprocal._period, self._period)

        self._quantity_name, self.reciprocal._quantity_name = (
            self.reciprocal._quantity_name,
            self._quantity_name,
        )

        self._label, self.reciprocal._label = (self.reciprocal._label, self._label)

        self._unit, self.reciprocal._unit = self.reciprocal._unit, self._unit

    def _get_coordinates(self):
        _unit = self._unit
        _count = self._count
        _increment = self._increment.to(_unit)

        _index = np.arange(_count, dtype=np.float64)

        if self._fft_output_order:
            _index = np.empty(_count, dtype=np.int)
            n = (_count - 1) // 2 + 1
            p1 = np.arange(0, n, dtype=np.int)
            _index[:n] = p1
            p2 = np.arange(-(_count // 2), 0, dtype=np.int)
            _index[n:] = p2

        _value = _index * _increment
        self._coordinates = _value

    def _get_python_dictionary(self):
        obj = {}
        obj["type"] = self.__class__._type

        if self._description.strip() != "":
            obj["description"] = self._description.strip()

        obj["count"] = self._count
        obj["increment"] = ScalarQuantity(self.increment).format()
        obj.update(self._get_quantitative_dictionary())

        if self.fft_output_order:
            obj["fft_output_order"] = True

        # reciprocal dictionary
        reciprocal_obj = {}
        if self.reciprocal._description.strip() != "":
            reciprocal_obj["description"] = self.reciprocal._description
        reciprocal_obj.update(self.reciprocal._get_quantitative_dictionary())
        if reciprocal_obj == {}:
            del reciprocal_obj
        else:
            obj["reciprocal"] = reciprocal_obj

        return obj

    # ----------------------------------------------------------------------- #
    #                                  Attributes                             #
    # ----------------------------------------------------------------------- #
    # @property
    # def count(self):
    #     r"""Total number of points along the linear dimension."""
    #     return deepcopy(self._count)

    @property
    def increment(self):
        r"""Increment of the grid points along the linear dimension."""
        return deepcopy(self._increment)

    @increment.setter
    def increment(self, value):
        allowed_types = (Quantity, str, ScalarQuantity)
        value = validate(value, "increment", allowed_types)
        self._increment = ScalarQuantity(value, self._unit).quantity
        self._get_coordinates()

    @property
    def fft_output_order(self):
        """If True, orders the coordinates according to FFT output order."""
        return deepcopy(self._fft_output_order)

    @fft_output_order.setter
    def fft_output_order(self, value):
        self._fft_output_order = validate(value, "fft_output_order", bool)
        self._get_coordinates()

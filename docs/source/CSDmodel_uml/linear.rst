

.. _linearDimension_uml:

===============
LinearDimension
===============

--------------------
Generalized Elements
--------------------

.. cssclass:: btn btn-outline-secondary
    :button: button

    :ref:`dimension_uml`


Description
***********

A LinearDimension is where the coordinates along this dimension follow a linear
relationship with the indices along the dimension. Let :math:`\Delta x_k` be
the `increment`, :math:`N_k \ge 1`, the number of points (`counts`),
:math:`b_k`, the `coordinates offset`, and :math:`o_k`, the `origin offset`
along the :math:`k^{th}` dimension, then the corresponding coordinates along
the dimension, :math:`\mathbf{X}_k`, are given as

.. math ::
    \mathbf{X}_k = \Delta x_k \mathbf{J}_k - b_k \mathbf{1},

and the absolute coordinates as,

.. math::
    \mathbf{X}_k^\mathrm{abs} = \mathbf{X}_k + o_k \mathbf{1}.

Here, :math:`\mathbf{1}` is an array of ones. The parameter,
:math:`\mathbf{J}_k`, is an array of indexes along the :math:`k^\mathrm{th}`
dimension and is given by

.. math::
    \mathbf{J}_k = [0, 1, 2, 3, ..., N_k-1]

when the value of the `fft_output_order` attribute is false, otherwise,

.. math::
    \mathbf{J}_k = \left[0, 1, ... \frac{N_k}{2}-1, \pm\frac{N_k}{2},
                            -\frac{N_k}{2}+1, ..., -1 \right]

when :math:`N_k` is even, and

.. math::
    \mathbf{J}_k = \left[0, 1, ... \frac{N_k-1}{2}, -\frac{N_k-1}{2}, ..., -1 \right]

when :math:`N_k` is odd.


Attributes
**********

.. cssclass:: table-bordered table-hover

=====================   ===================  ==================================
Name                    Type                 Description
=====================   ===================  ==================================
count                   Integer              The number of grid points,
                                             :math:`N_k` along the dimension.
increment               ScalarQuantity       The increment, :math:`\Delta x_k`,
                                             along for the dimension.
coordinates_offset      ScalarQuantity       The value corresponding to index
                                             zero, :math:`b_k`.
origin_offset           ScalarQuantity       The origin offset, :math:`o_k` of
                                             the dimension.
quantity_name           String               The quantity name associated with
                                             the physical quantities along the
                                             dimension.
period                  ScalarQuantity       The period of the dimension.
fft_output_order        Boolean              If true, the coordinates along the
                                             dimension is ordered according to
                                             the output of a fast-Fourier
                                             transform. See above description.
reciprocal              ReciprocalDimension  The ReciprocalDimension object.
=====================   ===================  ==================================

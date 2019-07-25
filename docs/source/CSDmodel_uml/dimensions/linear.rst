

.. _linearDimension_uml:

===============
LinearDimension
===============

-----------------
Generalized Class
-----------------

.. cssclass:: btn btn-outline-secondary
    :button: button

    :ref:`dimension_uml`


Description
***********

A LinearDimension is where the coordinates along the  dimension follow a linear
relationship with the indexes, :math:`\mathbf{J}_k`, along the dimension. Let
:math:`\Delta x_k` be the `increment`, :math:`N_k \ge 1`, the number of points
(`counts`), :math:`b_k`, the `coordinates offset`, and :math:`o_k`, the
`origin offset` along the :math:`k^{th}` dimension, then the corresponding
coordinates along the dimension, :math:`\mathbf{X}_k`, are given as

.. math ::
    \mathbf{X}_k = \Delta x_k \mathbf{J}_k + b_k \mathbf{1},

and the absolute coordinates as,

.. math::
    \mathbf{X}_k^\mathrm{abs} = \mathbf{X}_k + o_k \mathbf{1}.

Here, :math:`\mathbf{1}` is an array of ones. The indexes array,
:math:`\mathbf{J}_k`, along the :math:`k^\mathrm{th}` dimension is given as

.. math::
    \mathbf{J}_k = [0, 1, 2, 3, ..., N_k-1]

when the `fft_output_order` is false, otherwise,

.. math::
    \mathbf{J}_k = \left[-\frac{T_k}{2}, ... -1, 0, 1, ..., \frac{T_k}{2} \right]

where :math:`T_k=N_k` and :math:`T_k=N_k-1` for even and odd :math:`N_k`,
respectively.

.. note::
    When `fft_outout_order` is true and :math:`N_k` is even, the dependent variable
    value corresponding to the index :math:`\pm N_k/2` is alias.


Attributes
**********

.. cssclass:: table-bordered table-hover table-striped

=====================   ===================  ==================================
Name                    Type                 Description
=====================   ===================  ==================================
count                   Integer              The number of points, :math:`N_k`,
                                             along the dimension.
increment               :ref:`sQ_uml`        The increment, :math:`\Delta x_k`,
                                             along the dimension.
coordinates_offset      :ref:`sQ_uml`        The coordinate, :math:`b_k`,
                                             corresponding to the zero of the
                                             indexes array, :math:`\bf{J}_k`.
origin_offset           :ref:`sQ_uml`        The origin offset, :math:`o_k`,
                                             along the dimension.
quantity_name           String               The quantity name associated with
                                             the physical quantities describing
                                             the dimension.
period                  :ref:`sQ_uml`        The period of the dimension.
fft_output_order        Boolean              If true, the coordinates along the
                                             dimension are evaluated as the
                                             output of a complex fast Fourier
                                             transform (FFT) routine. See the
                                             above description.
reciprocal              ReciprocalDimension  Object with attributes required to
                                             describe the reciprocal dimension.
=====================   ===================  ==================================

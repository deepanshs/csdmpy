

.. _monotonicDimension_uml:

==================
MonotonicDimension
==================

-----------------
Generalized Class
-----------------

.. cssclass:: btn btn-outline-secondary
    :button: button

    :ref:`dimension_uml`


Description
***********

A monotonic dimension is a quantitative dimension where the coordinates along
the dimension are explicitly defined and, unlike a LinearDimension, may not
be derivable from the ordered array of indexes along the dimension.
Let :math:`\mathbf{A}_k` be an ordered set of strictly ascending or descending
physical quantities and :math:`o_k`, the origin offset along the :math:`k^{th}`
dimension, then the coordinates, :math:`\mathbf{X}_k`, and the absolute
coordinates, :math:`\mathbf{X}_k^\mathrm{abs}`, along a monotonic dimension
follow

.. math ::
    \begin{align}
    \mathbf{X}_k &= \mathbf{A}_k\\
    \mathbf{X}_k^\mathrm{abs} &= \mathbf{X}_k + o_k \mathbf{1},
    \end{align}

where :math:`\mathbf{1}` is an array of ones.

Attributes
**********

.. cssclass:: table-bordered table-hover table-striped

===============  ====================================== =====================
Name             Type                                   Description
===============  ====================================== =====================
coordinates      [:ref:`sQ_uml`, :ref:`sQ_uml`, ... ]   An array of strictly
                                                        ascending or descending
                                                        ScalarQuantity.
origin_offset    ScalarQuantity                         The origin offset, :math:`o_k`,
                                                        of the dimension.
quantity_name    String                                 The quantity name
                                                        associated with the
                                                        physical quantities
                                                        describing the
                                                        dimension.
period           ScalarQuantity                         The period of the
                                                        dimension.
reciprocal       ReciprocalDimension                    The ReciprocalDimension
                                                        object.
===============  ====================================== =====================



.. _monotonicDimension_uml:

==================
MonotonicDimension
==================

--------------------
Generalized Elements
--------------------

.. cssclass:: btn btn-outline-secondary
    :button: button

    :ref:`dimension_uml`


Description
***********

A monotonic dimension a quantitative dimension is where the coordinates along
the dimension are explicitly defined and, unlike the linear dimension, may not
be derivable from the ordered set of dimension indices.
Let :math:`\mathbf{A}_k` be an ordered set of strictly ascending or descending
quantities and :math:`o_k`, the origin offset along the :math:`k^{th}`
dimension, then the coordinates, :math:`\mathbf{X}_k`, and the absolute
coordinates, :math:`\mathbf{X}_k^\mathrm{abs}`, along a monotonic dimension are
given as,

.. math ::
    \begin{align}
    \mathbf{X}_k &= \mathbf{A}_k\\
    \mathbf{X}_k^\mathrm{abs} &= \mathbf{X}_k + o_k \mathbf{1},
    \end{align}


Attributes
**********

.. cssclass:: table-bordered table-hover

===============  ====================================== =====================
Name             Type                                   Description
===============  ====================================== =====================
coordinates      [ScalarQuantity, ScalarQuantity, . . ] An array of strictly
                                                        ascending or descending
                                                        ScalarQuantity.
origin_offset    ScalarQuantity                         The origin offset, :math:`o_k`
                                                        of the dimension.
quantity_name    String                                 The quantity name
                                                        associated with the
                                                        physical quantities
                                                        along the dimension.
period           ScalarQuantity                         The period of the
                                                        dimension.
reciprocal       ReciprocalDimension                    The ReciprocalDimension
                                                        object.
===============  ====================================== =====================

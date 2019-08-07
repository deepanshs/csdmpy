

.. _monotonicDimension_uml:

==================
MonotonicDimension
==================

-----------------
Generalized Class
-----------------

.. raw:: html

    <a class="btn btn-default" href=./dimension.html#dimension-uml>
    Dimension </a>


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
origin_offset    :ref:`sQ_uml`                          The origin offset, :math:`o_k`,
                                                        of the dimension.
quantity_name    String                                 The quantity name
                                                        associated with the
                                                        physical quantities
                                                        describing the
                                                        dimension.
period           :ref:`sQ_uml`                          The period of the
                                                        dimension.
reciprocal       ReciprocalDimension                    The ReciprocalDimension
                                                        object.
===============  ====================================== =====================

Example
*******

The following MonotonicDimension object,

.. code::

    {
        "type": "monotonic",
        "coordinates": ["1 µs", "10 µs", "100 µs", "1 ms", "10 ms", "100 ms", "1 s", "10 s"]
    }

will generate a dimension where coordinates :math:`\mathbf{X}_k` are

.. code::

    [1 µs, 10 µs, 100 µs, 1 ms, 10 ms, 100 ms, 1 s, 10 s]

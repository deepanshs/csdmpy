

.. _monotonicDimension_uml:

MonotonicDimension
^^^^^^^^^^^^^^^^^^

.. only:: html

  Generalized Class
  """""""""""""""""

  .. raw:: html

      <a class="btn btn-default" href=./dimension.html#dimension-uml>
      Dimension </a>


Description
"""""""""""

A monotonic dimension is a quantitative dimension where the coordinates along
the dimension are explicitly defined and, unlike a LinearDimension, may not
be derivable from the ordered array of indexes along the dimension.
Let :math:`\mathbf{A}_k` be an ordered set of strictly ascending or descending
physical quantities and, :math:`o_k`, the origin offset along the
:math:`k^{th}` dimension, then the coordinates, :math:`\mathbf{X}_k`, and the
absolute coordinates, :math:`\mathbf{X}_k^\mathrm{abs}`, along a monotonic
dimension follow

.. math::
    \begin{aligned}
    \mathbf{X}_k &= \mathbf{A}_k \text{ and}\\
    \mathbf{X}_k^\mathrm{abs} &= \mathbf{X}_k + o_k \mathbf{1},
    \end{aligned}

respectively, where :math:`\mathbf{1}` is an array of ones.

Attributes
""""""""""

.. cssclass:: table-bordered table-hover centered table-striped

.. list-table::
  :widths: 25 25 50
  :header-rows: 1

  * - Name
    - Type
    - Description

  * - coordinates
    - [:ref:`sQ_uml`, :ref:`sQ_uml`, ... ]
    - A `required` array of strictly ascending or descending ScalarQuantity.

  * - origin_offset
    - :ref:`sQ_uml`
    - An `optional` origin offset, :math:`o_k`, along the dimension. The
      default value is a physical quantity with zero numerical value.

  * - quantity_name
    - String
    - An `optional` quantity name associated with the physical quantities
      describing the dimension.

  * - period
    - :ref:`sQ_uml`
    - An `optional` period of the dimension. By default, the dimension is
      considered non-periodic.

  * - reciprocal
    - ReciprocalDimension
    - An `optional` object with attributes required to describe the reciprocal
      dimension.


Example
"""""""

The following MonotonicDimension object,

.. code::

    {
        "type": "monotonic",
        "coordinates": ["1 µs", "10 µs", "100 µs", "1 ms", "10 ms", "100 ms", "1 s", "10 s"]
    }

will generate a dimension, where the coordinates :math:`\mathbf{X}_k` are

.. code::

    ["1 µs", "10 µs", "100 µs", "1 ms", "10 ms", "100 ms", "1 s", "10 s"]

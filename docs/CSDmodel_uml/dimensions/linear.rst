

.. _linearDimension_uml:


LinearDimension
^^^^^^^^^^^^^^^

.. only:: html

  Generalized Class
  """""""""""""""""

  .. raw:: html

      <a class="btn btn-default" href=./dimension.html#dimension-uml>
      Dimension </a>


Description
"""""""""""

A LinearDimension is where the coordinates along the dimension follow a linear
relationship with the indexes, :math:`\mathbf{J}_k`, along the dimension. Let
:math:`\Delta x_k` be the `increment`, :math:`N_k \ge 1`, the number of points
(`counts`), :math:`b_k`, the `coordinates offset`, and :math:`o_k`, the
`origin offset` along the :math:`k^{th}` dimension, then the corresponding
coordinates along the dimension, :math:`\mathbf{X}_k`, are given as

.. math ::
    \mathbf{X}_k = \Delta x_k (\mathbf{J}_k - Z_k) + b_k \mathbf{1},

and the absolute coordinates as,

.. math::
    \mathbf{X}_k^\mathrm{abs} = \mathbf{X}_k + o_k \mathbf{1}.

Here, :math:`\mathbf{1}` is an array of ones, and :math:`\mathbf{J}_k` is the
array of indexes along the :math:`k^\mathrm{th}` dimension given as

.. math::
    \mathbf{J}_k = [0, 1, 2, 3, ..., N_k-1].

The term, :math:`Z_k`, is an integer with a value of :math:`Z_k=0` or
:math:`\frac{T_k}{2}` when the value of `complex_fft` attribute of the
corresponding dimension object is false or true, respectively.
Here, :math:`T_k=N_k` and :math:`N_k-1` for even and odd
value of :math:`N_k`, respectively.

.. note::
    When the value of the `complex_fft` attribute is true, and :math:`N_k`
    is even, the dependent variable value corresponding to the index
    :math:`\pm N_k/2` is an alias.


Attributes
""""""""""

.. cssclass:: table-bordered table-hover centered table-striped

.. list-table::
  :widths: 25 25 50
  :header-rows: 1

  * - Name
    - Type
    - Description

  * - count
    - Integer
    - A `required` number of points, :math:`N_k`, along the dimension.

  * - increment
    - :ref:`sQ_uml`
    - A `required` increment, :math:`\Delta x_k`, along the dimension.

  * - coordinates_offset
    - :ref:`sQ_uml`
    - An `optional` coordinate, :math:`b_k`, corresponding to the zero of the
      indexes array, :math:`\bf{J}_k`. The default value is a physical quantity
      with zero numerical value.

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

  * - complex_fft
    - Boolean
    - An `optional` boolean with default value as False.
      If true, the coordinates along the dimension are evaluated as the output
      of a complex fast Fourier transform (FFT) routine. See the description.

  * - reciprocal
    - ReciprocalDimension
    - An `optional` object with attributes required to describe the reciprocal
      dimension.


Example
"""""""

The following LinearDimension object,

.. code::

    {
        "type": "linear",
        "count": 10,
        "increment": "2 µA",
        "coordinates_offset": "0.1 µA"
    }

will generate a dimension, where the coordinates :math:`\mathbf{X}_k` are

.. code::

    [
        "0.1 µA",
        "2.1 µA",
        "4.1 µA",
        "6.1 µA",
        "8.1 µA",
        "10.1 µA",
        "12.1 µA",
        "14.1 µA",
        "16.1 µA",
        "18.1 µA"
    ]

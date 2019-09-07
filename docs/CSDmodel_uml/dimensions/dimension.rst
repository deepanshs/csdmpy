
.. _dimension_uml:

=========
Dimension
=========

A generalized object describing a dimension of a multi-dimensional
grid/space.

.. only:: html

  Specialized Class
  -----------------

  .. raw:: html

      <div class="btn-group">

          <a class="btn btn-default" href=./linear.html#lineardimension-uml>
          LinearDimension </a>

          <a class="btn btn-default" href=./monotonic.html#monotonicdimension-uml>
          MonotonicDimension </a>

          <a class="btn btn-default" href=./labeled.html#labeleddimension-uml>
          LabeledDimension </a>
      </div>

Attributes
----------

.. cssclass:: table-bordered table-hover centered table-striped

.. list-table::
  :widths: 25 25 50
  :header-rows: 1

  * - Name
    - Type
    - Description

  * - type
    - :ref:`dimObjectSubtype_uml`
    - A `required` enumeration literal with a valid dimension subtype.

  * - label
    - String
    - An `optional` label of the dimension.

  * - description
    - String
    - An `optional` description of the dimension.

  * - application
    - Generic
    - An `optional` generic dictionary object containing application specific
      metadata describing the dimension.

.. only:: latex

  Specialized Class
  -----------------

  .. include:: linear.rst

  .. include:: monotonic.rst

  .. include:: labeled.rst

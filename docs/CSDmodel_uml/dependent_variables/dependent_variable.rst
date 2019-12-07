
.. _dependent_var_uml:


DependentVariable
=================


Description
-----------

A generalized object describing a dependent variable of the dataset, which
holds an ordered list of `p` components, indexed as `q=0` to `p-1`, as

.. math::
    [\mathbf{U}_0, ... \mathbf{U}_q, ... \mathbf{U}_{p-1}].

.. only:: html

  Specialized Class
  -----------------

  .. raw:: html

      <div class="btn-group">

          <a class="btn btn-default" href=./internal.html#internal-uml>
          InternalDependentVariable </a>

          <a class="btn btn-default" href=./external.html#external-uml>
          ExternalDependentVariable </a>

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
    - :ref:`DVObjectSubtype_uml`
    - An enumeration literal with a valid dependent variable subtype.

  * - name
    - String
    - Name of the dependent variable.

  * - unit
    - String
    - The unit associated with the physical quantities describing the dependent
      variable.

  * - quantity_name
    - String
    - Quantity name associated with the physical quantities describing the
      dependent variable.

  * - numeric_type
    - :ref:`numericType_uml`
    - An enumeration literal with a valid numeric type.

  * - quantity_type
    - :ref:`quantityType_uml`
    - An enumeration literal with a valid quantity type.

  * - component_labels
    - [String, String, ... ]
    - Ordered array of labels associated with ordered array of components of
      the dependent variable.

  * - sparse_sampling
    - :ref:`sparseSampling_uml`
    - Object with attribute required to describe a sparsely sampled dependent
      variable components.

  * - description
    - String
    - Description of the dependent variable.

  * - application
    - Generic
    - Generic dictionary object containing application specific metadata
      describing the dependent variable.

.. only:: latex

  Specialized Class
  -----------------

  .. include:: internal.rst

  .. include:: external.rst

  .. include:: sparse_sampling.rst

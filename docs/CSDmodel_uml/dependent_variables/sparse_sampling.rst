
.. _sparseSampling_uml:

SparseSampling
^^^^^^^^^^^^^^


Description
"""""""""""

A SparseSampling object describes the dimensions indexes and grid vertexes
where the components of the dependent variable are sparsely sampled.


Attributes
""""""""""

.. cssclass:: table-bordered table-hover centered table-striped

.. list-table::
  :widths: 25 25 50
  :header-rows: 1

  * - Name
    - Type
    - Description

  * - dimension_indexes
    - [Integer, Integer, ...]
    - A `required` array of integers indicating along which dimensions the
      :ref:`dependent_var_uml` is sparsely sampled.

  * - sparse_grid_vertexes
    - [Integer, Integer, ...]
    - A required flattened array of integer indexes along the sparse dimensions
      where the components of the dependent variable are sampled. This is only
      `valid` when the encoding from the corresponding SparseSampling object is
      ``none``.

  * - sparse_grid_vertexes
    - String
    - A `required` base64 string of a flattened binary array of integer indexes
      along the sparse dimensions where the components of the dependent
      variable are sampled. This is only `valid` when the encoding from the
      corresponding SparseSampling object is ``base64``.

  * - encoding
    - String
    - A `required` enumeration with the following valid literals.
      ``none``, ``base64``

  * - unsigned_integer_type
    - String
    - A `required` enumeration with the following valid literals.
      ``uint8``, ``uint16``, ``uint32``, ``uint64``

  * - description
    - String
    - An `optional` description of the dependent variable.

  * - application
    - Generic
    - An `optional` generic dictionary object containing application specific
      metadata describing the SparseSampling object.

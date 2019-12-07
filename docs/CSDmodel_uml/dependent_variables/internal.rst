

.. _internal_uml:


InternalDependentVariable
^^^^^^^^^^^^^^^^^^^^^^^^^

.. only:: html

  Generalized Class
  """""""""""""""""

  .. raw:: html

      <a class="btn btn-default" href=./dependent_variable.html#_dependent-var-uml>
      DependentVariable </a>


Description
"""""""""""

An InternalDependentVariable is where the components of the dependent variable
are defined within the object as the value of the `components` key, along
with other metadata describing the dependent variable.


Attributes
""""""""""

.. cssclass:: table-bordered table-hover centered table-striped

.. list-table::
  :widths: 15 35 50
  :header-rows: 1

  * - Name
    - Type
    - Description

  * - components
    - [String, String, ... ]
    - A `required` attribute. The value is an array of base64 encoded strings
      where each string is a component of the dependent variable and decodes
      to a binary array of `M` data values. This value is only `valid`
      only when the corresponding value of the `encoding` attribute is `base64`.

  * - components
    - [[Float, Float, ...], [Float, Float, ...], ...]
    - A `required` attribute. The value is an array of arrays where each inner
      array is a component of the dependent variable with `M` data values. This
      value is `valid` only when the value of `encoding` is `none`.

  * - encoding
    - String
    - A required enumeration literal, where the valid literals are `none` or
      `base64`.

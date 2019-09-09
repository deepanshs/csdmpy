

.. _external_uml:

ExternalDependentVariable
^^^^^^^^^^^^^^^^^^^^^^^^^

.. only:: html

  Generalized Class
  """""""""""""""""

  .. raw:: html

      <a class="btn btn-default" href=./dependent_variable.html#_dependent-var-uml>
      DependentVariable </a>


Description
"""""""""""

An ExternalDependentVariable is where the components of the dependent variable
are defined in an external file whose location is defined as the value of the
``components_url`` key.


Attributes
""""""""""

.. cssclass:: table-bordered table-hover centered table-striped

.. list-table::
  :widths: 25 25 50
  :header-rows: 1

  * - Name
    - Type
    - Description

  * - components_url
    - String
    - A `required` URL location where the components of the dependent variable
      are serialized as a binary data.

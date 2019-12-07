
.. _csdm_uml:

CSDM
====


Description
-----------

The root level object of the CSD model.


Attributes
----------

.. cssclass:: table-bordered table-hover centered table-striped

.. list-table::
  :widths: 25 25 50
  :header-rows: 1

  * - Name
    - Type
    - Description

  * - version
    - String
    - A `required` version number of CSDM file-exchange format.

  * - dimensions
    - [:ref:`dimension_uml`, ...]
    - A `required` ordered and unique array of dimension objects. An empty
      array is a valid value.

  * - dependent_variables
    - [:ref:`dependent_var_uml`, ...]
    - A `required` array of dependent-variable objects. An empty array is a
      valid value.

  * - tags
    - [String, ...]
    - An `optional` list of keywords associated with the dataset.

  * - read_only
    - Boolean
    - An `optional` value with default as False. If true, the serialized file
      is archived.

  * - timestamp
    - String
    - An `optional` UTC ISO-8601 format timestamp from when the
      CSDM-compliant file was last serialized.

  * - geographic_coordinate
    - geographic_coordinate
    - An `optional` object with attributes required to describe the location
      from where the CSDM-compliant file was last serialized.

  * - description
    - String
    - An `optional` description of the datasets in the CSD model.

  * - application
    - Generic
    - An `optional` generic dictionary object containing application specific
      metadata describing the CSDM object.

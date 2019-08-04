
.. _csdm_uml:

====
CSDM
====


Description
***********

The root level object of the CSD model.


Attributes
**********

.. cssclass:: table-bordered table-hover

=====================   =============================== =======================
Name                    Type                            Description
=====================   =============================== =======================
dimensions              [:ref:`dimension_uml`, ...]     An ordered and unique
                                                        array of dimension
                                                        objects.
dependent_variables     [:ref:`dependent_var_uml`, ...] An ordered and unique
                                                        array of dependent
                                                        variable objects.
tags                    [String, ...]                   Set of keywords
                                                        associated with
                                                        the dataset.
read_only               Boolean                         If true, the serialized
                                                        file is archived.
version                 String                          The version number of
                                                        CSDM file-exchange
                                                        format.
timestamp               String                          UTC iso-8601 standard
                                                        formatted timestamp
                                                        from when the CSDM file
                                                        was last serialized.
geographic_coordinate   geographic_coordinate           Object with attributes
                                                        required to record the
                                                        location where the CSDM
                                                        file was last
                                                        serialized.
description             String                          Description of the
                                                        datasets in the CSD
                                                        model.
application             Generic                         Generic dictionary
                                                        object containing
                                                        application specific
                                                        metadata describing the
                                                        CSDM object.
=====================   =============================== =======================

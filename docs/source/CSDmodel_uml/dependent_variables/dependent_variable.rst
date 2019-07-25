
.. _dependent_var_uml:

=================
DependentVariable
=================


Description
***********

A generalized object describing a dependent variable of the dataset.

Specialized Class
*****************

.. cssclass:: btn btn-light

    :ref:`linearDimension_uml`

.. cssclass:: btn btn-light

    :ref:`monotonicDimension_uml`

.. cssclass:: btn btn-outline-dark

    :ref:`labeledDimension_uml`


Attributes
**********

.. cssclass:: table-bordered table-hover

================    ==========================  ===============================
Name                Type                        Description
================    ==========================  ===============================
type                :ref:`DVObjectSubtype_uml`  An enumeration literal with a
                                                valid dependent variable
                                                subtype.
name                String                      Name of the dependent variable.
unit                String                      Unit associated with the
                                                physical quantities describing
                                                the dependent variable.
quantity_name       String                      Quantity name associated with
                                                the physical quantities
                                                describing the dependent
                                                variable.
numeric_type        :ref:`numericType_uml`      An enumeration literal with a
                                                valid numeric type.
quantity_type       :ref:`quantityType_uml`     An enumeration literal with a
                                                valid quantity type.
component_labels    [String, String, ... ]      Ordered array of labels
                                                associated with each component
                                                of the dependent variable.
sparse_sampling     :ref:`SparseSampling`       Object with attribute required
                                                to describe a sparsely sampled
                                                dependent variable components.
description         String                      Description of the dependent
                                                variable.
application         Generic                     Generic dictionary object
                                                containing application specific
                                                metadata describing the
                                                dependent variable.
================    ==========================  ===============================


.. _dimension_uml:

=========
Dimension
=========


Description
***********

A generalized object describing a dimension of a multi-dimensional
grid/space.

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

==============  ===========================  ==================================
Name            Type                         Description
==============  ===========================  ==================================
type            :ref:`dimObjectSubtype_uml`  An enumeration literal with a
                                             valid dimension subtype.
label           String                       Label of the dimension.
description     String                       Description of the dimension.
application     Generic                      Generic dictionary object containing
                                             application specific metadata
                                             describing the dimension.
==============  ===========================  ==================================

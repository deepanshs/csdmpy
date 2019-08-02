
.. _dimension_uml:

=========
Dimension
=========


.. Description
.. ***********

A generalized object describing a dimension of a multi-dimensional
grid/space.

Specialized Class
*****************

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

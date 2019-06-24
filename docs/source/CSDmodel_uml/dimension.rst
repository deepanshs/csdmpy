
.. _dimension_uml:

=========
Dimension
=========

-----------
Description
-----------

The root level object of the CSD model.

--------------------
Specialized Elements
--------------------

.. cssclass:: btn-group
    :role: group
    :aria-label: Basic example

    .. cssclass:: btn btn-secondary
        :type: button

        LinearDimension

    .. cssclass:: btn btn-secondary
        :type: button

        MonotonicDimension

    .. cssclass:: btn btn-secondary
        :type: button

        LabeledDimension


----------
Attributes
----------
.. cssclass:: table-bordered table-hover

=============   ===============   ============
Name            Type              Description
=============   ===============   ============
type            DVObjectSubtype   A DVObjectSubtype enumeration literal.
label           String            The label along the dimension object.
description     String            The description of the dimension object.
application     Generic           A generic dictionary object with the
                                  application metadata.
=============   ===============   ============



.. _linearDimension_uml:

===============
LinearDimension
===============

-----------
Description
-----------


--------------------
Generalized Elements
--------------------

.. cssclass:: btn btn-outline-secondary
    :button: button
    :href: `dimension_uml`

    Dimension




----------
Attributes
----------

.. cssclass:: table-bordered table-hover

=====================   ===================  ==================================
Name                    Type                 Description
=====================   ===================  ==================================
count                   Integer              The number of grid points along
                                             the dimension.
increment               ScalarQuantity       The increment along for the
                                             dimension.
index_zero_coordinate   ScalarQuantity       The value of the zero index along
                                             the dimension.
origin_offset           ScalarQuantity       The origin offset along the
                                             dimension.
quantity_name           String               The quantity name associated with
                                             the physical quantities along the
                                             dimension.
period                  ScalarQuantity       The period of the dimension.
fft_output_order        Boolean              If true, the coordinates along the
                                             dimension is ordered according to
                                             the output of a fast-Fourier
                                             transform.
reciprocal              ReciprocalDimension  The value is a ReciprocalDimension
                                             object.
=====================   ===================  ==================================

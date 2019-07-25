

.. _internal_uml:

=========================
InternalDependentVariable
=========================

-----------------
Generalized Class
-----------------

.. cssclass:: btn btn-outline-secondary
    :button: button

    :ref:`dimension_uml`


Description
***********

A labeled dimension is a qualitative dimension where the coordinates along
the dimension are explicitly defined as labels. Let :math:`\mathbf{A}_k` be an
ordered set of unique labels along the :math:`k^{th}` dimension, then the
coordinates, :math:`\mathbf{X}_k`, along a labeled dimension are

.. math ::
    \mathbf{X}_k = \mathbf{A}_k


Attributes
**********

.. cssclass:: table-bordered table-hover table-striped

===============  =======================    =====================
Name             Type                       Description
===============  =======================    =====================
labels           [String, String, ... ]     An ordered array of labels along
                                            the dimension.
===============  =======================    =====================

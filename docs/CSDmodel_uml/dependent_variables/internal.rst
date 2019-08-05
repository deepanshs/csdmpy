

.. _internal_uml:

=========================
InternalDependentVariable
=========================

-----------------
Generalized Class
-----------------

.. raw:: html

    <a class="btn btn-default" href=./dependent_variable.html#_dependent-var-uml>
    DependentVariable </a>


Description
***********

An InternalDependentVariable is where the components of the dependent variable
are defined within object as the value of the ``components`` key, along with
other metadata describing the dependent variable.


Attributes
**********

.. cssclass:: table-bordered table-hover table-striped

===============  =======================    =====================
Name             Type                       Description
===============  =======================    =====================
components       [String, String, ... ]     A base64 encoded array of strings
                                            where each string is a component of
                                            the dependent variable and decodes
                                            to a binary array of `M` data
                                            values. `Valid` only when the
                                            ``encoding`` is `base64`.

components       [[Float, Float, ...],      An array of arrays where each inner
                 [Float, Float, ...],       array is a component of the
                 ...]                       dependent variable with `M` data
                                            values. `Valid` only when the
                                            ``encoding`` is `none`.
encoding         String                     Enumeration with the following valid
                                            literals.

                                            - ``none``
                                            - ``base64``
===============  =======================    =====================

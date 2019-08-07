
.. _sparseSampling_uml:

==============
SparseSampling
==============


Description
***********

A SparseSampling object describes the dimensions indexes and grid vertexes
where the components of the dependent variable are sparsely sampled.


Attributes
**********

.. cssclass:: table-bordered table-hover table-striped

====================  ========================   =====================
Name                  Type                       Description
====================  ========================   =====================
dimension_indexes     [Integer, Integer, ...]    An array integers indicating
                                                 along which dimensions the
                                                 :ref:`dependent_var_uml` is
                                                 sparsely sampled.
sparse_grid_vertexes  [Integer, Integer, ...]    An flattened array of integer
                                                 indexes along the sparse
                                                 dimensions where the dependent
                                                 variable is sampled. This is
                                                 only `valid` when encoding is
                                                 ``none``.
sparse_grid_vertexes  String                     A `base64` string of a binary
                                                 integer array of ``int32``
                                                 numeric type representing
                                                 the grid vertexes where the
                                                 dependent variable is sampled
                                                 This is only `valid` when
                                                 encoding is ``base64``.
encoding              String                     Enumeration with the following
                                                 valid literals.

                                                 - ``none``
                                                 - ``base64``
description           String                     Description of the dependent
                                                 variable.
application           Generic                    Generic dictionary object
                                                 containing application
                                                 specific metadata describing
                                                 the dependent variable.
====================  ========================   =====================

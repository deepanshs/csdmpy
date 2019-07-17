

===========
Enumeration
===========


.. _dimObjectSubtype_uml:

----------------
DimObjectSubtype
----------------

Description
***********

The `DimObjectSubtype` contains the enumeration literals of the dimension
objects.

.. cssclass:: table-bordered table-hover

========= ===========
Enum      Description
========= ===========
linear    The coordinates along the dimension is expressed as a linear
          function of the indexes along the dimension.
monotonic The coordinates along the dimension are explicitly defined and may
          not be expressed as a function of indexes along the dimension.
labeled   The coordinates are string labels.
========= ===========


.. _DVObjectSubtype_uml:

---------------
DVObjectSubtype
---------------

Description
***********

The `DVObjectSubtype` contains the enumeration literals of the dependent
variable object.

.. cssclass:: table-bordered table-hover

========= ===========
Enum      Description
========= ===========
internal  The dependent variable components are stored within the file.
external  The dependent variable components are stores as binary data at an
          external location.
========= ===========


.. _quantityType_uml:

------------
QuantityType
------------

Description
***********

An enumeration literal used in interpreting the `p`-components of the
dependent variable.

.. cssclass:: table-bordered table-hover

================== ===========
Enum               Description
================== ===========
scalar             A dependent variable with :math:`p=1` component interpret
                   as a scalar, :math:`\mathcal{S}_i=U_{0,i}`.
vector_n           A dependent variable with :math:`p=n` components
                   interpret as vector components.
matrix_n_m         A dependent variable with :math:`p=mn` components
                   interpret as a :math:`n \times m` matrix as follows,

                    .. math::
                            M_i = \left[
                                \begin{array}{cc}
                                U_{0,i} & U_{1,i}
                                \end{array}
                                \right]

symmetric_matrix_n A dependent variable with :math:`p=n^2` components interpret
                   as a symmetric matrix shown below,
================== ===========

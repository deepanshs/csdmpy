

===========
Enumeration
===========


.. _dimObjectSubtype_uml:

----------------
DimObjectSubtype
----------------

An enumeration with literals as the value of the :ref:`dimension_uml` objects'
`type` attribute.

.. cssclass:: table-bordered table-hover centered table-striped

.. list-table::
  :widths: 25 75
  :header-rows: 1

  * - Literal
    - Description

  * - linear
    - Literal specifying an instance of a :ref:`linearDimension_uml` object.

  * - monotonic
    - Literal specifying an instance of a :ref:`monotonicDimension_uml` object.

  * - labeled
    - Literal specifying an instance of a :ref:`labeledDimension_uml` object.


.. _DVObjectSubtype_uml:

---------------
DVObjectSubtype
---------------

An enumeration with literals as the values of the :ref:`dependent_var_uml`
object' `type` attribute.

.. cssclass:: table-bordered table-hover centered table-striped

.. list-table::
  :widths: 25 75
  :header-rows: 1

  * - Literal
    - Description

  * - internal
    - Literal specifying an instance of an :ref:`internal_uml` object.

  * - external
    - Literal specifying an instance of an :ref:`external_uml` object.

.. _numericType_uml:

-----------
NumericType
-----------

An enumeration with literals as the value of the :ref:`dependent_var_uml`
objects' `numeric_type` attribute.

.. cssclass:: table-bordered table-hover centered table-striped

.. list-table::
  :widths: 25 75
  :header-rows: 1

  * - Literal
    - Description

  * - uint8
    - 8-bit unsigned integer

  * - uint16
    - 16-bit unsigned integer

  * - uint32
    - 32-bit unsigned integer

  * - uint64
    - 64-bit unsigned integer

  * - int8
    - 8-bit signed integer

  * - int16
    - 16-bit signed integer

  * - int32
    - 32-bit signed integer

  * - int64
    - 64-bit signed integer

  * - float32
    - 32-bit floating point number

  * - float64
    - 64-bit floating point number

  * - complex64
    - two 32-bit floating points numbers

  * - complex128
    - two 64-bit floating points numbers


.. _quantityType_uml:

------------
QuantityType
------------

An enumeration with literals as the value of the :ref:`dependent_var_uml`
objects' `quantity_type` attribute. The value is used in interpreting the
`p`-components of the dependent variable.

- **scalar**
    A dependent variable with :math:`p=1` component interpret as
    a scalar, :math:`\mathcal{S}_i=U_{0,i}`.

- **vector_n**
    A dependent variable with :math:`p=n` components interpret
    as vector components,
    :math:`\mathcal{V}_i= \left[ U_{0,i}, U_{1,i}, ... U_{n-1,i}\right]`.

- **matrix_n_m**
    A dependent variable with :math:`p=mn` components interpret
    as a :math:`n \times m` matrix as follows,

    .. math::
      M_i = \left[
          \begin{array}{cccc}
              U_{0,i} & U_{1,i} & ... &U_{(n-1)m,i} \\
              U_{1,i} & U_{m+1,i} & ... &U_{(n-1)m+1,i} \\
              \vdots &  \vdots & \vdots & \vdots \\
              U_{m-1,i}  & U_{2m-1,i}  & ... &U_{nm-1,i}
          \end{array}
      \right]

- **symmetric_matrix_n**
    A dependent variable with :math:`p=n^2` components
    interpret as a matrix symmetric about its leading diagonal as shown below,

    .. math::
      M^{(s)}_i = \left[
          \begin{array}{cccc}
              U_{0,i} & U_{1,i} & ... & U_{n-1,i} \\
              U_{1,i} & U_{n,i} & ... &U_{2n-2,i} \\
              \vdots & \vdots  & \vdots & \vdots \\
              U_{n-1,i} & U_{2n-2,i} & ... &U_{\frac{n(n+1)}{2}-1,i}
          \end{array}
      \right]

- **pixel_n**
    A dependent variable with :math:`p=n` components interpret as
    image/pixel components,
    :math:`\mathcal{P}_i= \left[ U_{0,i}, U_{1,i}, ... U_{n-1,i}\right]`.

Here, the terms :math:`n` and :math:`m` are intergers.

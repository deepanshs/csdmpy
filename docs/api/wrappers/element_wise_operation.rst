.. _numpy_support:

Supported NumPy functions
-------------------------

The csdm object supports the use of NumPy functions, as

    >>> y = np.func(x) # doctest: +SKIP

where ``x`` and ``y`` are the csdm objects, and ``func`` is any one of the
following functions. These functions apply to each component of the dependent
variables from a given `csdm` object, `x`.

.. rubric:: Trigonometric functions

The trigonometric functions apply to the components of the dependent
variables from a csdm object.

.. note:: The components must be dimensionless quantities.

.. cssclass:: table-bordered table-striped centered

.. list-table:: A list of supported trigonometric functions.
  :widths: 25 75
  :header-rows: 1

  * - Functions
    - Description

  * - `sin <https://docs.scipy.org/doc/numpy/reference/generated/numpy.sin.html#numpy.sin>`_
    - Apply sine to the components of the dependent variables

  * - `cos <https://docs.scipy.org/doc/numpy/reference/generated/numpy.cos.html#numpy.cos>`_
    - Apply cosine to the components of the dependent variables

  * - `tan <https://docs.scipy.org/doc/numpy/reference/generated/numpy.tan.html#numpy.tan>`_
    - Apply tangent to the components of the dependent variables

  * - `arcsin <https://docs.scipy.org/doc/numpy/reference/generated/numpy.arcsin.html#numpy.arcsin>`_
    - Apply inverse sine to the components of the dependent variables

  * - `arccos <https://docs.scipy.org/doc/numpy/reference/generated/numpy.arccos.html#numpy.arccos>`_
    - Apply inverse cosine to the components of the dependent variables

  * - `arctan <https://docs.scipy.org/doc/numpy/reference/generated/numpy.arctan.html#numpy.arctan>`_
    - Apply inverse tangent to the components of the dependent variables


  * - `sinh <https://docs.scipy.org/doc/numpy/reference/generated/numpy.sinh.html#numpy.sinh>`_
    - Apply hyperbolic sine to the components of the dependent variables

  * - `cosh <https://docs.scipy.org/doc/numpy/reference/generated/numpy.cosh.html#numpy.cosh>`_
    - Apply hyperbolic cosine to the components of the dependent variables

  * - `tanh <https://docs.scipy.org/doc/numpy/reference/generated/numpy.tanh.html#numpy.tanh>`_
    - Apply hyperbolic tangent to the components of the dependent variables

  * - `arcsinh <https://docs.scipy.org/doc/numpy/reference/generated/numpy.arcsinh.html#numpy.arcsinh>`_
    - Apply inverse hyperbolic sine to the components of the dependent variables

  * - `arccosh <https://docs.scipy.org/doc/numpy/reference/generated/numpy.arccosh.html#numpy.arccosh>`_
    - Apply inverse hyperbolic cosine to the components of the dependent variables

  * - `arctanh <https://docs.scipy.org/doc/numpy/reference/generated/numpy.arctanh.html#numpy.arctanh>`_
    - Apply inverse hyperbolic tangent to the components of the dependent variables


.. rubric:: Mathematical operations

The following mathematical functions apply to the components of the dependent
variables from a csdm object.

.. note:: The components must be dimensionless quantities.
.. cssclass:: table-bordered table-striped centered
.. list-table:: A list of supported mathematical functions.
  :widths: 25 75
  :header-rows: 1

  * - Functions
    - Description
  * - `exp <https://docs.scipy.org/doc/numpy/reference/generated/numpy.exp.html#numpy.exp>`_
    - Calculate the exponential of the components of the dependent variables.

  * - `expm1 <https://docs.scipy.org/doc/numpy/reference/generated/numpy.expm1.html#numpy.expm1>`_
    - Apply :math:`e^x - 1`, where `x` are the components of the dependent variables.

  * - `exp2 <https://docs.scipy.org/doc/numpy/reference/generated/numpy.exp2.html#numpy.exp2>`_
    - Calculate :math:`2^x`, where `x` are the components of the dependent variables.

  * - `log <https://docs.scipy.org/doc/numpy/reference/generated/numpy.log.html#numpy.log>`_
    - Calculate natural logarithm of the components of the dependent variables.

  * - `log1p <https://docs.scipy.org/doc/numpy/reference/generated/numpy.log1p.html#numpy.log1p>`_
    - Calculate natural logarithm plus one on the components of the dependent variables.

  * - `log2 <https://docs.scipy.org/doc/numpy/reference/generated/numpy.log2.html#numpy.log2>`_
    - Calculate base-2 logarithm of the components of the dependent variables.

  * - `log10 <https://docs.scipy.org/doc/numpy/reference/generated/numpy.log10.html#numpy.log10>`_
    - Calculate base-10 logarithm of the components of the dependent variables.



The following mathematical functions apply to the components of the dependent
variables from a csdm object irrespective of the components' dimensionality.

.. cssclass:: table-bordered table-striped centered
.. list-table:: Arithmetic operations
  :widths: 25 75
  :header-rows: 1

  * - Functions
    - Description

  * - `reciprocal <https://docs.scipy.org/doc/numpy/reference/generated/numpy.reciprocal.html#numpy.reciprocal>`_
    - Return element-wise reciprocal.

  * - `positive <https://docs.scipy.org/doc/numpy/reference/generated/numpy.positive.html#numpy.positive>`_
    - Return element-wise numerical positive.

  * - `negative <https://docs.scipy.org/doc/numpy/reference/generated/numpy.negative.html#numpy.negative>`_
    - Return element-wise numerical negative.


.. cssclass:: table-bordered table-striped centered
.. list-table:: Miscellaneous
  :widths: 25 75
  :header-rows: 1

  * - Functions
    - Description

  * - `sqrt <https://docs.scipy.org/doc/numpy/reference/generated/numpy.sqrt.html#numpy.sqrt>`_
    - Return element-wise non-negative square-root.

  * - `cbrt <https://docs.scipy.org/doc/numpy/reference/generated/numpy.cbrt.html#numpy.cbrt>`_
    - Return element-wise cube-root.

  * - `square <https://docs.scipy.org/doc/numpy/reference/generated/numpy.square.html#numpy.square>`_
    - Return element-wise square.

  * - `absolute <https://docs.scipy.org/doc/numpy/reference/generated/numpy.absolute.html#numpy.absolute>`_
    - Return element-wise absolute value.

  * - `fabs <https://docs.scipy.org/doc/numpy/reference/generated/numpy.fabs.html#numpy.fabs>`_
    - Return element-wise absolute value.

  * - `sign <https://docs.scipy.org/doc/numpy/reference/generated/numpy.sign.html#numpy.sign>`_
    - Return element-wise sign of the values.

.. * - `clip <https://docs.scipy.org/doc/numpy/reference/generated/numpy.clip.html#numpy.clip>`_
..   - Clip the values between the limits.

.. cssclass:: table-bordered table-striped centered
.. list-table:: Handling complex numbers
  :widths: 25 75
  :header-rows: 1

  * - Functions
    - Description

  * - `angle <https://docs.scipy.org/doc/numpy/reference/generated/numpy.angle.html#numpy.angle>`_
    - Return element-wise angle of a complex value.

  * - `real <https://docs.scipy.org/doc/numpy/reference/generated/numpy.real.html#numpy.real>`_
    - Return element-wise real part of a complex value.

  * - `imag <https://docs.scipy.org/doc/numpy/reference/generated/numpy.imag.html#numpy.imag>`_
    - Return element-wise imaginary part of a complex value.å

  * - `conj <https://docs.scipy.org/doc/numpy/reference/generated/numpy.conj.html#numpy.conj>`_
    - Return element-wise conjugate.
  * - `conjugate <https://docs.scipy.org/doc/numpy/reference/generated/numpy.conjugate.html#numpy.conjugate>`_
    - Return element-wise conjugate.


.. cssclass:: table-bordered table-striped centered
.. list-table:: Sums, products, differences
  :widths: 25 75
  :header-rows: 1

  * - Functions
    - Description

  * - `prod <https://docs.scipy.org/doc/numpy/reference/generated/numpy.prod.html#numpy.prod>`_
    - Return the product of the components of a dependent variable along a dimension.

  * - `sum <https://docs.scipy.org/doc/numpy/reference/generated/numpy.sum.html#numpy.sum>`_
    - Return the sum of the components of a dependent variable along a dimension.



.. cssclass:: table-bordered table-striped centered
.. list-table:: Rounding
  :widths: 25 75
  :header-rows: 1

  * - Functions
    - Description

  * - `rint <https://docs.scipy.org/doc/numpy/reference/generated/numpy.rint.html#numpy.rint>`_
    - Round elements to the nearest integer.

  * - `around <https://docs.scipy.org/doc/numpy/reference/generated/numpy.around.html#numpy.around>`_
    - Round elements to the given number of decimals.

  * - `round <https://docs.scipy.org/doc/numpy/reference/generated/numpy.round_.html#numpy.round_>`_
    - Round elements to the given number of decimals.


Other functions

- min
- max
- mean
- var
- std


Supported NumPy functions
-------------------------

The csdm object supports the use of NumPy functions, as

    >>> y = np.func(x) # doctest: +SKIP

where ``x`` and ``y`` are the csdm objects, and ``func`` is any one of the
following functions. These functions apply to each component of the dependent
variables from a given `csdm` object, `x`.

.. rubric:: Trigonometric functions

The trigonometric functions apply to the components of the dependent
variables from a csdm object, where the components are dimensionless quantity.

- `sin <https://docs.scipy.org/doc/numpy/reference/generated/numpy.sin.html#numpy.sin>`_
- `cos <https://docs.scipy.org/doc/numpy/reference/generated/numpy.cos.html#numpy.cos>`_
- `tan <https://docs.scipy.org/doc/numpy/reference/generated/numpy.tan.html#numpy.tan>`_
- `arcsin <https://docs.scipy.org/doc/numpy/reference/generated/numpy.arcsin.html#numpy.arcsin>`_
- `arccos <https://docs.scipy.org/doc/numpy/reference/generated/numpy.arccos.html#numpy.arccos>`_
- `arctan <https://docs.scipy.org/doc/numpy/reference/generated/numpy.arctan.html#numpy.arctan>`_

- `sinh <https://docs.scipy.org/doc/numpy/reference/generated/numpy.sinh.html#numpy.sinh>`_
- `cosh <https://docs.scipy.org/doc/numpy/reference/generated/numpy.cosh.html#numpy.cosh>`_
- `tanh <https://docs.scipy.org/doc/numpy/reference/generated/numpy.tanh.html#numpy.tanh>`_
- `arcsinh <https://docs.scipy.org/doc/numpy/reference/generated/numpy.arcsinh.html#numpy.arcsinh>`_
- `arccosh <https://docs.scipy.org/doc/numpy/reference/generated/numpy.arccosh.html#numpy.arccosh>`_
- `arctanh <https://docs.scipy.org/doc/numpy/reference/generated/numpy.arctanh.html#numpy.arctanh>`_


.. rubric:: Mathematical operations

The following mathematical functions apply to the components of the dependent
variables from a csdm object, where the components are dimensionless quantity.

- `exp <https://docs.scipy.org/doc/numpy/reference/generated/numpy.exp.html#numpy.exp>`_
- `exp2 <https://docs.scipy.org/doc/numpy/reference/generated/numpy.exp2.html#numpy.exp2>`_
- `log <https://docs.scipy.org/doc/numpy/reference/generated/numpy.log.html#numpy.log>`_
- `log2 <https://docs.scipy.org/doc/numpy/reference/generated/numpy.log2.html#numpy.log2>`_
- `log10 <https://docs.scipy.org/doc/numpy/reference/generated/numpy.log10.html#numpy.log10>`_
- `expm1 <https://docs.scipy.org/doc/numpy/reference/generated/numpy.expm1.html#numpy.expm1>`_
- `log1p <https://docs.scipy.org/doc/numpy/reference/generated/numpy.log1p.html#numpy.log1p>`_

The following mathematical functions apply to the components of the dependent
variables from a csdm object irrespective of the components' dimensionality.

- `negative <https://docs.scipy.org/doc/numpy/reference/generated/numpy.negative.html#numpy.negative>`_
- `positive <https://docs.scipy.org/doc/numpy/reference/generated/numpy.positive.html#numpy.positive>`_
- `absolute <https://docs.scipy.org/doc/numpy/reference/generated/numpy.absolute.html#numpy.absolute>`_
- `fabs <https://docs.scipy.org/doc/numpy/reference/generated/numpy.fabs.html#numpy.fabs>`_
- `rint <https://docs.scipy.org/doc/numpy/reference/generated/numpy.rint.html#numpy.rint>`_
- `sign <https://docs.scipy.org/doc/numpy/reference/generated/numpy.sign.html#numpy.sign>`_
- `conj <https://docs.scipy.org/doc/numpy/reference/generated/numpy.conj.html#numpy.conj>`_
- `conjugate <https://docs.scipy.org/doc/numpy/reference/generated/numpy.conjugate.html#numpy.conjugate>`_


- `sqrt <https://docs.scipy.org/doc/numpy/reference/generated/numpy.sqrt.html#numpy.sqrt>`_
- `square <https://docs.scipy.org/doc/numpy/reference/generated/numpy.square.html#numpy.square>`_
- `cbrt <https://docs.scipy.org/doc/numpy/reference/generated/numpy.cbrt.html#numpy.cbrt>`_
- `reciprocal <https://docs.scipy.org/doc/numpy/reference/generated/numpy.reciprocal.html#numpy.reciprocal>`_


- clip
- round

- real
- imag

Reduction
- min
- max
- mean
- var
- std
- prod

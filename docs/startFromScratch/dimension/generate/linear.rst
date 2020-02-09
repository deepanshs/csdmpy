---------------
LinearDimension
---------------

A LinearDimension is where the coordinates are regularly spaced along the
dimension. This type of dimension is frequently encountered in many scientific
datasets. There are several ways to generate LinearDimension.

**Using the** :class:`~csdmpy.Dimension` **class.**

.. doctest::

    >>> import csdmpy as cp
    >>> x = cp.Dimension(type='linear', count=10, increment="0.1 s", label="time", description="A temporal dimension.")
    >>> print(x)
    LinearDimension([0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] s)

**Using the** :class:`~csdmpy.LinearDimension` **class.**

.. doctest::

    >>> import csdmpy as cp
    >>> x1 = cp.LinearDimension(count=10, increment="0.1 s", label="time",
    ...                          description="A temporal dimension.")
    >>> print(x1)
    LinearDimension([0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] s)

**Using NumPy array**

You may also create a LinearDimesion object from a one-dimensional NumPy array
using the :meth:`~csdmpy.as_dimension` method.

.. doctest::

    >>> import numpy as np
    >>> array = np.arange(10) * 0.1
    >>> x2 = cp.as_dimension(array)
    >>> print(x2)
    LinearDimension([0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9])

Note, the Dimension object ``x2`` is dimensionless. You can create a physical
dimension by either providing an appropriate unit as the argument to the
:meth:`~csdmpy.as_dimension` method,

.. doctest::

    >>> x3 = cp.as_dimension(array, unit='s')
    >>> print(x3)
    LinearDimension([0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] s)

or appropriately multiplying the dimension object ``x2`` with a
:class:`~csdmpy.ScalarQuantity`.

.. doctest::

    >>> x2 *= cp.ScalarQuantity('s')
    >>> print(x2)
    LinearDimension([0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] s)

The coordinates of the ``x2`` LinearDimension object,
.. doctest::

    >>> x2.coordinates
    <Quantity [0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] s>

where ``x2.coordinates`` is a `Quantity <http://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity>`_
array. The value and the unit of the quantity instance are

.. doctest::

    >>> # To access the numpy array
    >>> numpy_array = x.coordinates.value
    >>> print('numpy array =', numpy_array)
    numpy array = [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9]

    >>> # To access the astropy.unit
    >>> unit = x.coordinates.unit
    >>> print('unit =', unit)
    unit = s

respectively.

.. Note:: When generating LinearDimension objects from NumPy array, the NumPy
            array must be one-dimensional and regularly spaced.

.. doctest::

    >>> cp.as_dimension(np.arange(20).reshape(2, 10))  # doctest: +SKIP
    ValueError: Cannot convert a 2 dimensional array to a Dimension object.

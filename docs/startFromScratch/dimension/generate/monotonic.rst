------------------
MonotonicDimension
------------------

A MonotonicDimension is one where the coordinates along the dimension are
sampled monotonically, that is, either strictly increasing or decreasing
coordinates. Like the LinearDimension, there are several ways to generate
a MonotonicDimension.

**Using the** :class:`~csdmpy.Dimension` **class.**

.. doctest::

    >>> import csdmpy as cp
    >>> x = cp.Dimension(type='monotonic',
    ...                  coordinates=['10ns', '100ns', '1µs', '10µs', '100µs',
    ...                               '1ms', '10ms', '100ms', '1s', '10s'])
    >>> print(x)
    MonotonicDimension([1.e+01 1.e+02 1.e+03 1.e+04 1.e+05 1.e+06 1.e+07 1.e+08 1.e+09 1.e+10] ns)

**Using the** :class:`~csdmpy.MonotonicDimension` **class.**

.. doctest::

    >>> import numpy as np
    >>> array = np.asarray([-0.28758166, -0.22712233, -0.19913859, -0.17235106,
    ...                     -0.1701172, -0.10372635, -0.01817061, 0.05936719,
    ...                     0.18141424, 0.34758913])
    >>> x = cp.MonotonicDimension(coordinates=array)*cp.ScalarQuantity('cm')
    >>> print(x)
    MonotonicDimension([-0.28758166 -0.22712233 -0.19913859 -0.17235106 -0.1701172  -0.10372635
     -0.01817061  0.05936719  0.18141424  0.34758913] cm)

In the above example, we generate a dimensionless MonotonicDimension from
the NumPy array and scale its dimensionality by multiplying the object with an
appropriate :class:`~csdmpy.ScalarQuantity`.

**From numpy arrays.**

Use the :meth:`~csdmpy.as_dimension` method to convert a numpy array as a
Dimension object.

.. doctest::

    >>> numpy_array = 10 ** (np.arange(10)/10)
    >>> x_dim = cp.as_dimension(numpy_array, unit='A')
    >>> print(x_dim)
    MonotonicDimension([1.         1.25892541 1.58489319 1.99526231 2.51188643 3.16227766
     3.98107171 5.01187234 6.30957344 7.94328235] A)


When generating MonotonicDimension object using the Numpy array, the array
must be monotonic, that is, either strictly increasing or decreasing.
An exception will be raised otherwise.

.. doctest::

    >>> numpy_array = np.random.rand(10)
    >>> x_dim = cp.as_dimension(numpy_array) # doctest: +SKIP
    Exception: Invalid array for Dimension object.

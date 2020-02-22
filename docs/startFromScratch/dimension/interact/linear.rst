---------------
LinearDimension
---------------

There are several attributes and methods associated with the LinearDimension,
each controlling the coordinates along the dimension. The following section
demonstrates the effect of these attributes and methods on the coordinates of
the LinearDimension.

.. doctest::

    >>> import csdmpy as cp
    >>> x = cp.LinearDimension(count=10, increment="0.1 s", label="time",
    ...                          description="A temporal dimension.")
    >>> print(x)
    LinearDimension([0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] s)


Attributes
""""""""""

:attr:`~csdmpy.Dimension.type`
    This attribute returns the type of the instance.

    .. doctest::

        >>> print(x.type)
        linear

**The attributes that modify the coordinates**


:attr:`~csdmpy.Dimension.count`
    The number of points along the dimension

    .. doctest::

        >>> print('number of points =', x.count)
        number of points = 10

    To update the number of points, update the value of this attribute,

    .. doctest::

        >>> x.count = 12
        >>> print('new number of points =', x.count)
        new number of points = 12

        >>> print('new coordinates =', x.coordinates)
        new coordinates = [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.  1.1] s

:attr:`~csdmpy.Dimension.increment`
    .. doctest::

        >>> print('old increment =', x.increment)
        old increment = 0.1 s

        >>> x.increment = "10 s"
        >>> print('new increment =', x.increment)
        new increment = 10.0 s

        >>> print('new coordinates =', x.coordinates)
        new coordinates = [  0.  10.  20.  30.  40.  50.  60.  70.  80.  90. 100. 110.] s

:attr:`~csdmpy.Dimension.coordinates_offset`
    .. doctest::

        >>> print('old reference offset =', x.coordinates_offset)
        old reference offset = 0.0 s

        >>> x.coordinates_offset = "1 s"
        >>> print('new reference offset =', x.coordinates_offset)
        new reference offset = 1.0 s

        >>> print('new coordinates =', x.coordinates)
        new coordinates = [  1.  11.  21.  31.  41.  51.  61.  71.  81.  91. 101. 111.] s

:attr:`~csdmpy.Dimension.origin_offset`
    .. doctest::

        >>> print('old origin offset =', x.origin_offset)
        old origin offset = 0.0 s

        >>> x.origin_offset = "1 day"
        >>> print ('new origin offset =', x.origin_offset)
        new origin offset = 1.0 d

        >>> print('new coordinates =', x.coordinates)
        new coordinates = [  1.  11.  21.  31.  41.  51.  61.  71.  81.  91. 101. 111.] s

    The last operation updates the value of the origin offset, however,
    the coordinates remain unaffected. This is because the
    :attr:`~csdmpy.Dimension.coordinates` attribute refers to the
    reference coordinates. You may access the absolute coordinates through the
    :attr:`~csdmpy.Dimension.absolute_coordinates` attribute.

    .. doctest::

        >>> print('absolute coordinates =', x.absolute_coordinates)
        absolute coordinates = [86401. 86411. 86421. 86431. 86441. 86451. 86461. 86471. 86481. 86491.
         86501. 86511.] s


.. _lsgd_order_attributes:

**The attributes that modify the order of coordinates**

:attr:`~csdmpy.Dimension.complex_fft`
    If true, orders the coordinates along the dimension according to the output
    of a complex Fast Fourier Transform (FFT) routine.

    .. doctest::

        >>> print('old coordinates =', x.coordinates)
        old coordinates = [  1.  11.  21.  31.  41.  51.  61.  71.  81.  91. 101. 111.] s

        >>> x.complex_fft = True
        >>> print('new coordinates =', x.coordinates)
        new coordinates = [-59. -49. -39. -29. -19.  -9.   1.  11.  21.  31.  41.  51.] s


**Other attributes**

:attr:`~csdmpy.Dimension.period`
    The period of the dimension.

    .. doctest::

        >>> print('old period =', x.period)
        old period = inf s

        >>> x.period = '10 s'
        >>> print('new period =', x.period)
        new period = 10.0 s

:attr:`~csdmpy.Dimension.quantity_name`
    Returns the quantity name.

    .. doctest::

        >>> print('quantity name is', x.quantity_name)
        quantity name is time

:attr:`~csdmpy.Dimension.label`
    .. doctest::

        >>> x.label
        'time'

        >>> x.label = 't1'
        >>> x.label
        't1'

:attr:`~csdmpy.Dimension.axis_label`
    Returns a formatted string for labeling axis.

    .. doctest::

        >>> x.label
        't1'
        >>> x.axis_label
        't1 / (s)'

Methods
"""""""

:meth:`~csdmpy.Dimension.to`:
This method is used for unit conversions.

.. doctest::

    >>> print('old unit =', x.coordinates.unit)
    old unit = s

    >>> print('old coordinates =', x.coordinates)
    old coordinates = [-59. -49. -39. -29. -19.  -9.   1.  11.  21.  31.  41.  51.] s

    >>> ## unit conversion
    >>> x.to('min')

    >>> print ('new coordinates =', x.coordinates)
    new coordinates = [-0.98333333 -0.81666667 -0.65       -0.48333333 -0.31666667 -0.15
      0.01666667  0.18333333  0.35        0.51666667  0.68333333  0.85      ] min

.. note::

    In the above examples, the coordinates are ordered according to the FFT output
    order, based on the previous set of operations.

The argument of this method is a string containing the unit, in this case,
`min`, whose dimensionality is be consistent with the dimensionality of the
coordinates. An exception will be raised otherwise.

.. doctest::

    >>> x.to('km/s')  # doctest: +SKIP
    Exception: The unit 'km / s' (speed) is inconsistent with the unit 'min' (time).


Changing the dimensionality
"""""""""""""""""""""""""""

You may scale the dimension object by multiplying the object with the
appropriate ScalarQuantity, as follows,

.. doctest::

    >>> print(x)
    LinearDimension([-0.98333333 -0.81666667 -0.65       -0.48333333 -0.31666667 -0.15
      0.01666667  0.18333333  0.35        0.51666667  0.68333333  0.85      ] min)
    >>> x *= cp.ScalarQuantity('m/s')
    >>> print(x)
    LinearDimension([-59. -49. -39. -29. -19.  -9.   1.  11.  21.  31.  41.  51.] m)

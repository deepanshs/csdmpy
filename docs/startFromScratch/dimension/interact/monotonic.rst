------------------
MonotonicDimension
------------------

There are several attributes and methods associated with a MonotonicDimension,
controlling the coordinates along the dimension. The following section
demonstrates the effect of these attributes and methods on the coordinates.


.. doctest::

    >>> import numpy as np
    >>> array = np.asarray([-0.28758166, -0.22712233, -0.19913859, -0.17235106,
    ...                     -0.1701172, -0.10372635, -0.01817061, 0.05936719,
    ...                     0.18141424, 0.34758913])
    >>> x = cp.MonotonicDimension(coordinates=array)*cp.ScalarQuantity('cm')

Attributes
""""""""""

The following are the attributes of the :class:`~csdmpy.MonotonicDimension`
instance.


:attr:`~csdmpy.Dimension.type`
    This attribute returns the type of the instance.

    .. doctest::

        >>> print(x.type)
        monotonic


**The attributes that modify the coordinates**

:attr:`~csdmpy.Dimension.count`
    The number of points along the dimension

    .. doctest::

        >>> print ('number of points =', x.count)
        number of points = 10

    You may update the number of points with this attribute, however, you can
    only lower the number of points.

    .. doctest::

        >>> x.count = 6
        >>> print('new number of points =', x.count)
        new number of points = 6
        >>> print(x.coordinates)
        [-0.28758166 -0.22712233 -0.19913859 -0.17235106 -0.1701172  -0.10372635] cm


:attr:`~csdmpy.Dimension.origin_offset`
    .. doctest::

        >>> print('old origin offset =', x.origin_offset)
        old origin offset = 0.0 cm

        >>> x.origin_offset = "1 km"
        >>> print('new origin offset =', x.origin_offset)
        new origin offset = 1.0 km

        >>> print(x.coordinates)
        [-0.28758166 -0.22712233 -0.19913859 -0.17235106 -0.1701172  -0.10372635] cm

    The last operation updates the value of the origin offset, however,
    the value of the ``coordinates`` attribute remains unchanged.
    This is because the ``coordinates`` refer to the reference coordinates.
    The absolute coordinates are accessed through the ``absolute_coordinates``
    attribute.

    .. doctest::

        >>> print('absolute coordinates =', x.absolute_coordinates)
        absolute coordinates = [99999.71241834 99999.77287767 99999.80086141 99999.82764894
         99999.8298828  99999.89627365] cm


**Other attributes**

:attr:`~csdmpy.Dimension.label`
    .. doctest::

        >>> x.label = 't1'
        >>> print('new label =', x.label)
        new label = t1

:attr:`~csdmpy.Dimension.period`
    .. doctest::

        >>> print('old period =', x.period)
        old period = inf cm

        >>> x.period = '10 m'
        >>> print('new period =', x.period)
        new period = 10.0 m

:attr:`~csdmpy.Dimension.quantity_name`
    Returns the quantity name.

    .. doctest::

        >>> print ('quantity is', x.quantity_name)
        quantity is length



Methods
"""""""

:meth:`~csdmpy.Dimension.to()`

The method is used for unit conversions. It follows,

.. doctest::

    >>> print('old unit =', x.coordinates.unit)
    old unit = cm
    >>> print('old coordinates =', x.coordinates)
    old coordinates = [-0.28758166 -0.22712233 -0.19913859 -0.17235106 -0.1701172  -0.10372635] cm

    >>> ## unit conversion
    >>> x.to('mm')

    >>> print('new coordinates =', x.coordinates)
    new coordinates = [-2.8758166 -2.2712233 -1.9913859 -1.7235106 -1.701172  -1.0372635] mm

The argument of this method is a unit, in this case, 'mm', whose
dimensionality must be consistent with the dimensionality of the
coordinates.  An exception will be raised otherwise,

.. doctest::

    >>> x.to('km/s')  # doctest: +SKIP
    Exception("Validation Failed: The unit 'km / s' (speed) is inconsistent with the unit 'mm' (length).")



Changing the dimensionality
"""""""""""""""""""""""""""

You may scale the dimension object by multiplying the object with the
appropriate ScalarQuantity, as follows,

.. doctest::

    >>> print(x)
    MonotonicDimension([-2.8758166 -2.2712233 -1.9913859 -1.7235106 -1.701172  -1.0372635] mm)
    >>> x *= cp.ScalarQuantity('2 s/mm')
    >>> print(x)
    MonotonicDimension([-0.57516332 -0.45424466 -0.39827718 -0.34470212 -0.3402344  -0.2074527 ] cm s / mm)

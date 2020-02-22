
-----------------------------
Interacting with CSDM objects
-----------------------------

Basic math operations
"""""""""""""""""""""

The csdm object supports basic mathematical operations such as additive and
multiplicative operations.

.. note:: All operations applied to or involving the csdm objects apply only to
    the components of the dependent variables within the csdm object. These
    operations do not apply to the dimensions within the csdm object.

Consider the following csdm data object.

.. doctest::

    >>> arr1 = np.arange(6, dtype=np.float32).reshape(2, 3)
    >>> csdm_obj1 = cp.as_csdm(arr1)
    >>> # converting the dimension to proper physical dimensions.
    >>> csdm_obj1.dimensions[0]*=cp.ScalarQuantity('2.64 m')
    >>> csdm_obj1.dimensions[0].coordinates_offset = '1 km'
    >>> # converting the dimension to proper physical dimensions.
    >>> csdm_obj1.dimensions[1]*=cp.ScalarQuantity('10 µs')
    >>> csdm_obj1.dimensions[1].coordinates_offset = '-0.5 ms'
    >>> print(csdm_obj1)
    CSDM(
    DependentVariable(
    [[[0. 1. 2.]
      [3. 4. 5.]]], quantity_type=scalar, numeric_type=float32),
    LinearDimension([1000.   1002.64 1005.28] m),
    LinearDimension([-500. -490.] us)
    )

**Additive operations involving a scalar**

**Example 1**

.. doctest::

    >>> csdm_obj1 += np.pi
    >>> print(csdm_obj1)
    CSDM(
    DependentVariable(
    [[[3.1415927 4.141593  5.141593 ]
      [6.141593  7.141593  8.141593 ]]], quantity_type=scalar, numeric_type=float32),
    LinearDimension([1000.   1002.64 1005.28] m),
    LinearDimension([-500. -490.] us)
    )

**Example 2**

.. doctest::

    >>> csdm_obj2 = csdm_obj1 + (2 - 4j)
    >>> print(csdm_obj2)
    CSDM(
    DependentVariable(
    [[[ 5.141593-4.j  6.141593-4.j  7.141593-4.j]
      [ 8.141593-4.j  9.141593-4.j 10.141593-4.j]]], quantity_type=scalar, numeric_type=complex64),
    LinearDimension([1000.   1002.64 1005.28] m),
    LinearDimension([-500. -490.] us)
    )

**Multiplicative operations involving scalar / ScalarQuantity**

**Example 3**

.. doctest::

    >>> csdm_obj1 = cp.as_csdm(np.ones(6).reshape(2, 3))
    >>> csdm_obj2 = csdm_obj1 * 4.693
    >>> print(csdm_obj2)
    CSDM(
    DependentVariable(
    [[[4.693 4.693 4.693]
      [4.693 4.693 4.693]]], quantity_type=scalar, numeric_type=float64),
    LinearDimension([0. 1. 2.]),
    LinearDimension([0. 1.])
    )

**Example 4**

.. doctest::

    >>> csdm_obj2 = csdm_obj1 * 3j/2.4
    >>> print(csdm_obj2)
    CSDM(
    DependentVariable(
    [[[0.+1.25j 0.+1.25j 0.+1.25j]
      [0.+1.25j 0.+1.25j 0.+1.25j]]], quantity_type=scalar, numeric_type=complex128),
    LinearDimension([0. 1. 2.]),
    LinearDimension([0. 1.])
    )

You may change the dimensionality of the dependent variables by multiplying the
csdm object with the appropriate scalar quantity, for example,

**Example 5**

.. doctest::

    >>> csdm_obj1 *= cp.ScalarQuantity('3.23 m')
    >>> print(csdm_obj1)
    CSDM(
    DependentVariable(
    [[[3.23 3.23 3.23]
      [3.23 3.23 3.23]]] m, quantity_type=scalar, numeric_type=float64),
    LinearDimension([0. 1. 2.]),
    LinearDimension([0. 1.])
    )

**Example 6**

.. doctest::

    >>> csdm_obj1 /= cp.ScalarQuantity('3.23 m')
    >>> print(csdm_obj1)
    CSDM(
    DependentVariable(
    [[[1. 1. 1.]
      [1. 1. 1.]]], quantity_type=scalar, numeric_type=float64),
    LinearDimension([0. 1. 2.]),
    LinearDimension([0. 1.])
    )


**Additive operations involving two csdm objects**

The additive operations are supported between two csdm objects only when the
two objects have identical sets of Dimension objects and DependentVariable
objects with the same dimensionality. For examples,

**Example 7**

.. doctest::

    >>> csdm1 = cp.as_csdm(np.ones((2,3)), unit='m/s')
    >>> csdm2 = cp.as_csdm(np.ones((2,3)), unit='cm/s')
    >>> csdm_obj = csdm1 + csdm2
    >>> print(csdm_obj)
    CSDM(
    DependentVariable(
    [[[1.01 1.01 1.01]
      [1.01 1.01 1.01]]] m / s, quantity_type=scalar, numeric_type=float64),
    LinearDimension([0. 1. 2.]),
    LinearDimension([0. 1.])
    )

An exception will be raised if the DependentVariable objects of the two
csdm objects have different dimensionality.

**Example 8**

.. doctest::

    >>> csdm1 = cp.as_csdm(np.ones((2,3)), unit='m/s')
    >>> csdm2 = cp.as_csdm(np.ones((2,3)))
    >>> csdm_obj = csdm1 + csdm2 # doctest: +SKIP
    Exception: Cannot operate on dependent variables with physical types: speed and dimensionless.

Similarly, an exception will be raised if the dimension objects of the two
csdm objects are different.

**Example 9**

.. doctest::

    >>> csdm1 = cp.as_csdm(np.ones((2,3)), unit='m/s')
    >>> csdm1.dimensions[1] = cp.MonotonicDimension(coordinates=['1 ms', '1 s'])
    >>> csdm2 = cp.as_csdm(np.ones((2,3)), unit='cm/s')
    >>> csdm_obj = csdm1 + csdm2 # doctest: +SKIP
    Exception: Cannot operate on CSDM objects with different dimensions.


Basic Slicing and Indexing
""""""""""""""""""""""""""

The CSDM objects support NumPy basic slicing and indexing and follow the same
rules as the NumPy array. Consider the following 3D{1} csdm object.

.. doctest::

    >>> csdm1 = cp.as_csdm(np.zeros((5, 10, 20)), unit='s')
    >>> csdm1.dimensions[0] = cp.as_dimension(np.arange(20)*0.5+4.3, unit='kg')
    >>> csdm1.dimensions[1] = cp.as_dimension([1, 2, 3, 5, 7, 11, 13, 17, 19, 23], unit='mm')
    >>> csdm1.dimensions[2] = cp.LabeledDimension(labels=list('abcde'))
    >>> print(csdm1.shape)
    (20, 10, 5)
    >>> print(csdm1.dimensions)
    [LinearDimension(count=20, increment=0.5 kg, coordinates_offset=4.3 kg, quantity_name=mass),
    MonotonicDimension(coordinates=[ 1.  2.  3.  5.  7. 11. 13. 17. 19. 23.] mm, quantity_name=length, reciprocal={'quantity_name': 'wavenumber'}),
    LabeledDimension(labels=['a', 'b', 'c', 'd', 'e'])]

The above object ``csdm1`` has three dimensions, each with different
dimensionality and dimension type.
To retrieve a sub-grid of this 3D{1} dataset, use the NumPy indexing scheme.

**Example 10**

.. doctest::

    >>> sub_csdm = csdm1[0]
    >>> print(sub_csdm.shape)
    (10, 5)
    >>> print(sub_csdm.dimensions)
    [MonotonicDimension(coordinates=[ 1.  2.  3.  5.  7. 11. 13. 17. 19. 23.] mm, quantity_name=length, reciprocal={'quantity_name': 'wavenumber'}),
    LabeledDimension(labels=['a', 'b', 'c', 'd', 'e'])]

The above example returns a 2D{1} cross-section of the 3D{1} datasets
corresponding to the index 0 along the first dimension of the ``csdm1``
object as a ``sub_csdm`` csdm object. The two dimensions in ``sub_csdm`` are
the MonotonicDimension and LabeledDimension.

**Example 11**

.. doctest::

    >>> sub_csdm = csdm1[::5, 2::2, :]
    >>> print(sub_csdm.shape)
    (4, 4, 5)
    >>> print(sub_csdm.dimensions)
    [LinearDimension(count=4, increment=2.5 kg, coordinates_offset=4.3 kg, quantity_name=mass),
    MonotonicDimension(coordinates=[ 3.  7. 13. 19.] mm, quantity_name=length, reciprocal={'quantity_name': 'wavenumber'}),
    LabeledDimension(labels=['a', 'b', 'c', 'd', 'e'])]

The above example returns a 3D{1} dataset, ``sub_csdm``, which contains a
sub-grid of the 3D{1} datasets in ``csdm1``. In ``sub_csdm``, the first
dimension is a sub-grid of the first dimension from the ``csdm1`` object,
where only every fifth grid point is selected. Similarly, the second dimension
of the ``sub_csdm`` object is sampled from the second dimension of the
``csdm1`` object, where every second grid point is selected, starting with the
entry at the grid index two. The third dimension of the ``sub_csdm`` object
is the same as the third object of the ``csdm1`` object. The values of the
corresponding linear, monotonic, and labeled dimensions are accordingly
adjusted, for example, notice the value of the `count` and `increment`
attribute of the linear dimension in ``sub_csdm`` object.

**Example 12**

.. doctest::

    >>> sub_csdm = csdm1[::5, 2::2, -3::-1]
    >>> print(sub_csdm.shape)
    (4, 4, 3)
    >>> print(sub_csdm.dimensions)
    [LinearDimension(count=4, increment=2.5 kg, coordinates_offset=4.3 kg, quantity_name=mass),
    MonotonicDimension(coordinates=[ 3.  7. 13. 19.] mm, quantity_name=length, reciprocal={'quantity_name': 'wavenumber'}),
    LabeledDimension(labels=['c', 'b', 'a'])]

The above example is similar to the previous examples, except the third
dimension indexed in reversed starting at the third index from the end.


.. seealso::

    `Basic Slicing and Indexing <https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html#basic-slicing-and-indexing>`_

Support for Numpy methods
"""""""""""""""""""""""""

In most cases, the csdm object may be used as if it were a NumPy array.
See the list of all supported :ref:`numpy_support`.

Method that only operate on dimensionless dependent variables
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

**Example 13**

.. doctest::

    >>> csdm_obj1 = cp.as_csdm(10**(np.arange(10)/10))
    >>> new_csdm1 = np.log10(csdm_obj1)
    >>> print(new_csdm1)
    CSDM(
    DependentVariable(
    [[0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9]], quantity_type=scalar, numeric_type=float64),
    LinearDimension([0. 1. 2. 3. 4. 5. 6. 7. 8. 9.])
    )

**Example 14**

.. doctest::

    >>> new_csdm2 = np.cos(2*np.pi*new_csdm1)
    >>> print(new_csdm2)
    CSDM(
    DependentVariable(
    [[ 1.          0.80901699  0.30901699 -0.30901699 -0.80901699 -1.
      -0.80901699 -0.30901699  0.30901699  0.80901699]], quantity_type=scalar, numeric_type=float64),
    LinearDimension([0. 1. 2. 3. 4. 5. 6. 7. 8. 9.])
    )

**Example 15**

.. doctest::

    >>> new_csdm2 = np.exp(new_csdm1 * cp.ScalarQuantity('K')) # doctest: +SKIP
    ValueError: Cannot apply `exp` to quantity with physical type `temperature`.

An exception is raised for csdm object with non-dimensionless dependent
variables.

Method that are independent of the dependent variable dimensionality
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

**Example 16**

.. doctest::

    >>> new_csdm2 = np.square(new_csdm1 * cp.ScalarQuantity('K'))
    >>> print(new_csdm2)
    CSDM(
    DependentVariable(
    [[0.   0.01 0.04 0.09 0.16 0.25 0.36 0.49 0.64 0.81]] K2, quantity_type=scalar, numeric_type=float64),
    LinearDimension([0. 1. 2. 3. 4. 5. 6. 7. 8. 9.])
    )

**Example 17**

.. doctest::

    >>> new_csdm1 = np.sqrt(new_csdm2)
    >>> print(new_csdm1)
    CSDM(
    DependentVariable(
    [[0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9]] K, quantity_type=scalar, numeric_type=float64),
    LinearDimension([0. 1. 2. 3. 4. 5. 6. 7. 8. 9.])
    )

Dimension reduction methods
'''''''''''''''''''''''''''

**Example 18**

.. doctest::

    >>> csdm1 = cp.as_csdm(np.ones((10,20,30)), unit='µG')
    >>> csdm1.shape
    (30, 20, 10)
    >>> new = np.sum(csdm1, axis=1)
    >>> new.shape
    (30, 10)
    >>> print(new.dimensions)
    [LinearDimension(count=30, increment=1.0),
    LinearDimension(count=10, increment=1.0)]

**Example 19**

.. doctest::

    >>> csdm1 = cp.as_csdm(np.ones((10,20,30)), unit='µG')
    >>> csdm1.shape
    (30, 20, 10)
    >>> new = np.sum(csdm1, axis=(1, 2))
    >>> new.shape
    (30,)
    >>> print(new.dimensions)
    [LinearDimension(count=30, increment=1.0)]

**Example 20**

.. doctest::

    >>> minimum = np.min(new_csdm1)
    >>> print(minimum)
    0.0 K
    >>> np.min(new_csdm1) == new_csdm1.min()
    True

.. note:: See the list of all supported :ref:`numpy_support`.

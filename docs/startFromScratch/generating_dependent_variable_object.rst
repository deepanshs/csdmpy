.. _generate_dependent_variable_objects:

------------------------------------
Generating DependentVariable objects
------------------------------------

A DependentVariable is where the responses of the multi-dimensional dataset
reside. There are two types of DependentVariable objects, `internal` and
`external`. In this section, we show how to generate DependentVariable objects
of both types.

InternalDependentVariable
"""""""""""""""""""""""""

Single component dependent variable
'''''''''''''''''''''''''''''''''''

**Using the** :class:`~csdmpy.DependentVariable` **class.**

.. doctest::

    >>> dv1 = cp.DependentVariable(type='internal', quantity_type='scalar',
    ...                            components=np.arange(10000), unit='J',
    ...                            description='A sample internal dependent variable.')
    >>> print(dv1)
    DependentVariable(
    [[   0    1    2 ... 9997 9998 9999]] J, quantity_type=scalar, numeric_type=int64)

**Using NumPy array**

Use the :meth:`~csdmpy.as_dependent_variable` method to convert a NumPy array
into a DependentVariable object. Note, this method returns a view of the NumPy
array as the DependentVariable object.

.. doctest::

    >>> dv1 = cp.as_dependent_variable(np.arange(10000).astype(np.complex64), unit='J')
    >>> print(dv1)
    DependentVariable(
    [[0.000e+00+0.j 1.000e+00+0.j 2.000e+00+0.j ... 9.997e+03+0.j
      9.998e+03+0.j 9.999e+03+0.j]] J, quantity_type=scalar, numeric_type=complex64)

You may additionally provide the quantity_type for the dependent variable,

.. doctest::

    >>> dv2 = cp.as_dependent_variable(np.arange(10000).astype(np.complex64), quantity_type='pixel_1')
    >>> print(dv2)
    DependentVariable(
    [[0.000e+00+0.j 1.000e+00+0.j 2.000e+00+0.j ... 9.997e+03+0.j
      9.998e+03+0.j 9.999e+03+0.j]], quantity_type=pixel_1, numeric_type=complex64)

Multi-component dependent variable
''''''''''''''''''''''''''''''''''

To generate a multi-component DependentVariable object, add an appropriate
`quantity_type` value, see :ref:`quantityType_uml` for details.

**Using the** :class:`~csdmpy.DependentVariable` **class.**

.. doctest::

    >>> dv1 = cp.DependentVariable(type='internal', quantity_type='vector_2',
    ...                            components=np.arange(10000), unit='J',
    ...                            description='A sample internal dependent variable.')
    >>> print(dv1)
    DependentVariable(
    [[   0    1    2 ... 4997 4998 4999]
     [5000 5001 5002 ... 9997 9998 9999]] J, quantity_type=vector_2, numeric_type=int64)

The above example generates a two-component dependent variable.

**Using NumPy array**

.. doctest::

    >>> dv1 = cp.as_dependent_variable(np.arange(9000).astype(np.complex64),
    ...                                unit='m/s', quantity_type='symmetric_matrix_3')
    >>> print(dv1)
    DependentVariable(
    [[0.000e+00+0.j 1.000e+00+0.j 2.000e+00+0.j ... 1.497e+03+0.j
      1.498e+03+0.j 1.499e+03+0.j]
     [1.500e+03+0.j 1.501e+03+0.j 1.502e+03+0.j ... 2.997e+03+0.j
      2.998e+03+0.j 2.999e+03+0.j]
     [3.000e+03+0.j 3.001e+03+0.j 3.002e+03+0.j ... 4.497e+03+0.j
      4.498e+03+0.j 4.499e+03+0.j]
     [4.500e+03+0.j 4.501e+03+0.j 4.502e+03+0.j ... 5.997e+03+0.j
      5.998e+03+0.j 5.999e+03+0.j]
     [6.000e+03+0.j 6.001e+03+0.j 6.002e+03+0.j ... 7.497e+03+0.j
      7.498e+03+0.j 7.499e+03+0.j]
     [7.500e+03+0.j 7.501e+03+0.j 7.502e+03+0.j ... 8.997e+03+0.j
      8.998e+03+0.j 8.999e+03+0.j]] m / s, quantity_type=symmetric_matrix_3, numeric_type=complex64)

The above example generates a six-component dependent variable.

.. note::
    For multi-component DependentVariable objects, the size of the NumPy array
    must be an integer multiple of the total number of components.

    .. doctest::

        >>> d1 = cp.as_dependent_variable(np.arange(127), quantity_type='pixel_2') # doctest: +SKIP
        ValueError: cannot reshape array of size 127 into shape (2,63)

Notice in the above examples, we use a one-dimensional NumPy array to generate
a DependentVariable object. If a multi-dimensional NumPy array is given as the
argument, the array will be raveled (flattened) before returning the
DependentVariable object. Note, in the core scientific dataset model, the
DependentVariable objects only contain information about the number of
components and not the dimensions. For example, consider the following.

.. doctest::

    >>> d2 = cp.as_dependent_variable(np.arange(6000).reshape(10,20,30), quantity_type='vector_2')
    >>> print(d2)
    DependentVariable(
    [[   0    1    2 ... 2997 2998 2999]
     [3000 3001 3002 ... 5997 5998 5999]], quantity_type=vector_2, numeric_type=int64)

Here, a three-dimensional Numpy array is given as the argument with a
quantity_type of `vector_2`. The DependentVariable object generated from this
array contains two-components by appropriately flattening the input array.


ExternalDependentVariable
"""""""""""""""""""""""""

The ExternalDependentVariable objects are generated similar to the
InternalDependentVariable object. The only difference is that the components
of the dependent variable are located at a remote and local address.

**Using the** :class:`~csdmpy.DependentVariable` **class.**

.. doctest::

    >>> dv = cp.DependentVariable(type='external', quantity_type='scalar', unit='J',
    ...                           components_url='address to the binary file.',
    ...                           numeric_type='int64',
    ...                           description='A sample internal dependent variable.') # doctest: +SKIP


A DependentVariable of type `external` is useful for data serialization. When
using with `csdmpy`, all instances of the `external` dependent variable objects
are set as `internal` after downloading the components from the
`components_url`.

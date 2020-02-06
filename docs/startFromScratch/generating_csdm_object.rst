
-----------------------
Generating CSDM objects
-----------------------

An empty csdm object
""""""""""""""""""""

To create a new empty csdm object, import the `csdmpy` module and create a new
instance of the CSDM class following,

.. doctest::

    >>> import csdmpy as cp
    >>> new_data = cp.new(description='A new test dataset')

The :meth:`~csdmpy.new` method returns an instance of the CSDM class with zero
dimensions and dependent variables. respectively, `i.e.`, a 0D{0} dataset.
In the above example, this instance is assigned to the ``new_data`` variable.
Optionally, a description may also be provided as an argument of the
:meth:`~csdmpy.new` method.
The data structure from the above example is

.. doctest::

    >>> print(new_data.data_structure)
    {
      "csdm": {
        "version": "1.0",
        "description": "A new test dataset",
        "dimensions": [],
        "dependent_variables": []
      }
    }

From a NumPy array
""""""""""""""""""

Perhaps the easiest way to convert a dataset into a csdm object is to convert
the NumPy array holding the dataset into a csdm object. The NumPy array is
assigned as the dependent variable of the csdm object of the given
`quantity_type`. The dimensions of this csdm object are assumed as
LinearDimension objects with unit increment. The number of points
along each dimension is determined from the shape of the NumPy array.

.. doctest::

    >>> array = np.arange(30).reshape(3, 10)
    >>> csdm_obj = cp.as_csdm_object(array)
    >>> print(csdm_obj)
    CSDM(
    DependentVariable([[[ 0  1  2  3  4  5  6  7  8  9]
      [10 11 12 13 14 15 16 17 18 19]
      [20 21 22 23 24 25 26 27 28 29]]], quantity_type=scalar),
    LinearDimension([0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]),
    LinearDimension([0. 1. 2.])
    )

The required argument of the :meth:`~csdmpy.as_csdm_object` method is the NumPy
array, here referred to as the ``array``. The ``quantity_type`` of the
dependent variable from the ``csdm_obj`` object is set to `scalar` by default.
Notice, the ``csdm_obj`` object has two LinearDimension objects corresponding
to the two-dimensional array of shape (3, 10).

Additionally, a quantity type may be provided as the argument of the
:meth:`~csdmpy.as_csdm_object` method,

.. doctest::

    >>> csdm_obj1 = cp.as_csdm_object(array, quantity_type='pixel_3')
    >>> print(csdm_obj1)
    CSDM(
    DependentVariable([[ 0  1  2  3  4  5  6  7  8  9]
     [10 11 12 13 14 15 16 17 18 19]
     [20 21 22 23 24 25 26 27 28 29]], quantity_type=pixel_3),
    LinearDimension([0. 1. 2. 3. 4. 5. 6. 7. 8. 9.])
    )

In this case, the ``csdm_obj1`` object has one dimension with 10 points.
This time, the first axis of the NumPy array, `3`, is the number of
components in the `pixel_3` dataset.

Note, when providing the `quantity_type`, the number of points
along the first axis of the NumPy array must be consistent with the desired
number of components for the `quantity_type` key, see :ref:`quantityType_uml`.
An exception will be raised otherwise.

    >>> csdm_obj_err = cp.as_csdm_object(array, quantity_type='vector_2')  # doctest: +SKIP
    ValueError: Expecting exactly 2 components for quantity type, `vector_2`, found 3.
    Make sure `array.shape[0]` is equal to the number of components supported by vector_2.

.. note::
    Only csdm object with a single dependent variable may be created from a NumPy array.


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

Perhaps the easiest way to generate a csdm object is to convert the NumPy array
holding the dataset as a csdm object using the :meth:`~csdmpy.as_csdm` method,
which returns a view of the array as a CSDM object.
Here, the NumPy array becomes the dependent variable of the CSDM object of the
given `quantity_type`.
Unlike the :meth:`~csdmpy.as_dependent_variable` method, however, the
:meth:`~csdmpy.as_csdm` method retains the shape of the Numpy array and uses
this information to generate the dimensions of the CSDM object. By default,
the dimensions are of a `linear` subtype with unit increment. Consider
the following example.

.. doctest::

    >>> array = np.arange(30).reshape(3, 10)
    >>> csdm_obj = cp.as_csdm(array)
    >>> print(csdm_obj)
    CSDM(
    DependentVariable(
    [[[ 0  1  2  3  4  5  6  7  8  9]
      [10 11 12 13 14 15 16 17 18 19]
      [20 21 22 23 24 25 26 27 28 29]]], quantity_type=scalar, numeric_type=int64),
    LinearDimension([0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]),
    LinearDimension([0. 1. 2.])
    )

Here, a two-dimensional NumPy array of shape (3, 10) is given as the argument
of the :meth:`~csdmpy.as_csdm` method. The resulting CSDM object, ``csdm_obj``,
contains a 2D{1} datasets, with two linear dimensions of unit increment and
10 and 3 points, respectively, and a single one-component dependent variable of
quantity_type `scalar`.

.. note:: The order of the dimensions in the CSDM object is the reverse of the
    order of axes from the corresponding Numpy array. Thus, the dimension at index
    0 of the CSDM object is the last axis of the Numpy array.

You may additionally provide a quantity type as the argument of the
:meth:`~csdmpy.as_csdm` method. When the quantity type requires more than one
component, see :ref:`quantityType_uml`, the first axis of the NumPy array must
be the number of components. For example,

.. doctest::

    >>> csdm_obj1 = cp.as_csdm(array, quantity_type='pixel_3')
    >>> print(csdm_obj1)
    CSDM(
    DependentVariable(
    [[ 0  1  2  3  4  5  6  7  8  9]
     [10 11 12 13 14 15 16 17 18 19]
     [20 21 22 23 24 25 26 27 28 29]], quantity_type=pixel_3, numeric_type=int64),
    LinearDimension([0. 1. 2. 3. 4. 5. 6. 7. 8. 9.])
    )

Here, the ``csdm_obj1`` object is a 1D{3} datasets, with a single
three-component dependent variable. In this case, the length of the NumPy array
along axis 0, i.e., 3, is consistent with the number of components required
by the quantity type `pixel_3`. The remaining axes of the NumPy array are used
in generating the dimensions of the csdm object. In this example, this
corresponds to a single dimension of `linear` type with 10 points.

The following example generates a 3D{2} vector dataset. Here, the first axis of
the four-dimensional Numpy array is the components of the vector dataset, and
the remaining three axes become the respective dimensions.

.. doctest::

    >>> array2 = np.arange(12000).reshape(2,30,20,10)
    >>> csdm_obj2 = cp.as_csdm(array2, quantity_type='vector_2')
    >>> print(len(csdm_obj2.dimensions), len(csdm_obj2.dependent_variables[0].components))
    3 2

An exception will be raised if the `quantity_type` and the number of points
along the first axis of the NumPy array are inconsistent, for example,

    >>> csdm_obj_err = cp.as_csdm(array, quantity_type='vector_2')  # doctest: +SKIP
    ValueError: Expecting exactly 2 components for quantity type, `vector_2`, found 3.
    Make sure `array.shape[0]` is equal to the number of components supported by vector_2.

.. note::
    Only a csdm object with a single dependent variable may be created from a NumPy array.

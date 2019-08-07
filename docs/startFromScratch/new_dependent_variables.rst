
-----------------------------------------------
How to add instances of DependentVariable class
-----------------------------------------------

In the previous two sections, we learnt how to create a new dataset and add
dimensions to a dataset. In this example, we will see how to add
dependent variables to the dataset. Let's start by creating a new dataset,

.. doctest::

    >>> import csdmpy as cp
    >>> new_data = cp.new(description='A new test dependent variables dataset')

An instance of the DependentVariable class is added using the
:meth:`~csdmpy.csdm.CSDM.add_dependent_variable` method of the :ref:`csdm_api`
instance. There are two subtypes of DependentVariable class:

- **InternalDependentVariable**:
  We refer an instance of the DependentVariable as *internal* when the
  components of the dependent variable are listed along with the other
  metadata specifying the dependent variable.
- **ExternalDependentVariable**:
  We refer an instance of the DependentVariable as *external* when the
  components of the dependent variable are stored in an external file as
  binary data either locally or at a remote server.

In version 1.0, the CSD model allows dependent variables with quantity types
as

- scalar
- vector_n
- pixel_n
- matrix_n_m
- symmetric_matrix_n

.. seeAlso::
    Read more about :ref:`DependentVariable API <dv_api>`.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Adding a scalar dependent variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A dependent variable with quantity type `scalar` is a one-component dependent
variable. Consider the following python dictionary

.. doctest::

    >>> d0 = {
    ...     'type': 'internal',
    ...     'quantity_type': 'scalar',
    ...     'description': 'This is an internal scalar dependent variable',
    ...     'unit': 'cm',
    ...     'components': [np.arange(100)]
    ... }

Here, the components are listed as the value of the
:attr:`~csdmpy.dependent_variables.DependentVariable.components` keyword, and
therefore, the value of the `type` keyword is specified as `internal`.

.. note::
    The value of the components attribute is listed as a list of numpy array.
    In csdmpy, the first dimension is reserved for the components. Since this
    example has only one component, we specify it as a list of numpy array.
    Alternatively, one could also assign
    ``np.arange(100).reshape(np.newaxis, 100)`` as the value of the components
    attribute.

To add a dependent variable to the ``new_data`` instance, use the
:meth:`~csdmpy.csdm.CSDM.add_dependent_variable` method as

.. doctest::

    >>> new_data.add_dependent_variable(d0)

This will generate and add a :ref:`dv_api` object to the list of
dependent variables, thereby creating a 0D{1} dataset. The data structure
after adding the dependent variable is

.. doctest::

    >>> print(new_data.data_structure)
    {
      "csdm": {
        "version": "1.0",
        "description": "A new test dependent variables dataset",
        "dimensions": [],
        "dependent_variables": [
          {
            "type": "internal",
            "description": "This is an internal scalar dependent variable",
            "unit": "cm",
            "quantity_name": "length",
            "numeric_type": "int64",
            "quantity_type": "scalar",
            "components": [
              [
                "0, 1, ..., 98, 99"
              ]
            ]
          }
        ]
      }
    }

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Adding a multi-component dependent variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this next example, we demostrate how to add a dependent variable with
multiple components. This time we use keywords as the argument of the
:meth:`~csdmpy.csdm.CSDM.add_dependent_variable` method to add a new
dependent variable.

.. doctest::

    >>> new_data.add_dependent_variable(
    ...     type='internal',
    ...     description='This is an internal vector dependent variable',
    ...     quantity_type='vector_3',
    ...     unit='kg * m / s^2',
    ...     components=np.arange(300, dtype='complex64').reshape(3,100)
    ... )

Notice, the value of the `components` keyword is a numpy array of shape
3 x 100, where 3 is the number of components and 100 is the number of points
per component. Here, we specify, `vector_3` as the value of the
`quantity_type`, indicating that the three components of the dependent variable
should be interpretted as vector dataset. Users may, however, substitute this
value with any valid `quantity_type` consistent with the number of components.
For example, the above dataset may also be interpretted as an image data
if quantity type is given as `pixel_3`.

The data structure after adding the above dependent variable is

.. doctest::

    >>> print(new_data.data_structure)
    {
      "csdm": {
        "version": "1.0",
        "description": "A new test dependent variables dataset",
        "dimensions": [],
        "dependent_variables": [
          {
            "type": "internal",
            "description": "This is an internal scalar dependent variable",
            "unit": "cm",
            "quantity_name": "length",
            "numeric_type": "int64",
            "quantity_type": "scalar",
            "components": [
              [
                "0, 1, ..., 98, 99"
              ]
            ]
          },
          {
            "type": "internal",
            "description": "This is an internal vector dependent variable",
            "unit": "kg * m * s^-2",
            "quantity_name": "force",
            "numeric_type": "complex64",
            "quantity_type": "vector_3",
            "components": [
              [
                "0j, (1+0j), ..., (98+0j), (99+0j)"
              ],
              [
                "(100+0j), (101+0j), ..., (198+0j), (199+0j)"
              ],
              [
                "(200+0j), (201+0j), ..., (298+0j), (299+0j)"
              ]
            ]
          }
        ]
      }
    }

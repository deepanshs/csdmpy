
-------------------------------------------
Adding instances of DependentVariable class
-------------------------------------------

In the previous two sections, we create a new dataset and populated it with
dimension objects. In this example, we will create a new dataset and
populate it with the dependent variables.

.. doctest::

    >>> import csdfpy as cp
    >>> new_data = cp.new(description='A new test dependent variables dataset')

In this section, we will add dimension objects to this dataset.
An instance of the Dimension class is added using the
:meth:`~csdfpy.csdm.CSDModel.add_dimension` method of the :ref:`csdm_api`
instance. See :ref:`dim_api` API for further detail.

^^^^^^^^
Internal
^^^^^^^^
**Scalar type**
We refer dependent variable type as *internal* when the components of the data
are provided along with the dependent variable metadata. For example, consider
the following python dictionary

.. doctest::

    >>> d0 = {
    ...     'type': 'internal',
    ...     'description': 'This is an internal scalar dependent variable',
    ...     'unit': 'cm',
    ...     'components': [np.arange(100)]
    ... }

where the components are listed as the value of the components keyword.

.. note::
    The value of the components attribute is listed as a list of numpy array.
    In csdfpy, the first dimension is reserved for the components. Since this
    example has only one component, we specify it as a list of numpy array.
    Alternatively, one could also assign
    ``np.arange(100).reshape(np.newaxis, 100)`` as the value of the components
    attribute.

To add a dependent variable to the ``new_data`` instance, use the
:meth:`~csdfpy.csdm.CSDModel.add_dependent_variable` method as

.. doctest::

    >>> new_data.add_dependent_variable(d0)

This will generate and add a :ref:`dv_api` object to the list of
dependent variables, thereby creating a 0D{1} dataset. The data structure
after adding the dependent variable is

.. doctest::

    >>> print(new_data.data_structure)
    {
      "csdm": {
        "version": "0.0.12",
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

**Vector type**
In this next example, we add a dependent variable of vector quantity type.
This time we use the keyword arguments to add a new dependent variable.

.. doctest::

    >>> new_data.add_dependent_variable(
    ...     type='internal',
    ...     description='This is an internal vector dependent variable',
    ...     quantity_type='vector_3',
    ...     unit='kg * m / s^2',
    ...     components=np.arange(300, dtype='complex64').reshape(3,100)
    ... )

The data structure after adding the above dependent variable is

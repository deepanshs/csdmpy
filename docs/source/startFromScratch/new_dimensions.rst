
-----------------------------------
Adding instances of Dimension class
-----------------------------------

In the previous example, we create a new dataset using,

.. doctest::

    >>> import csdfpy as cp
    >>> new_data = cp.new(description='A new test dataset')

In this section, we will add dimension objects to this dataset.
An instance of the :ref:`dim_api` class is added using the
:meth:`~csdfpy.csdm.CSDModel.add_dimension` method of the :ref:`csdm_api`
instance. See :ref:`dim_api` API for further detail.

^^^^^^^^^^^^^^^
LinearDimension
^^^^^^^^^^^^^^^

A linear dimension is where the coordinates along the dimension are
uniformly spaced. Let's make use of the Python dictionary object to create
and add a new dimension to the `new_data` variable.
The Python dictionary for a LinearDimension follows,

.. doctest::

    >>> d0 = {
    ...     'type': 'linear',
    ...     'description': 'This is a linear dimension',
    ...     'count': 10,
    ...     'increment': '0.1 s'
    ... }

Here, we define the dimension type as `linear` and provide an `increment` value
along with the total number of points, `count`, along the dimension. To add
this dimension to the dataset use

.. doctest::

    >>> new_data.add_dimension(d0)

This will generate and add a LinearDimension object to the list of dimensions.
The dataset is now a 1D{0} dataset with the data structure,

.. doctest::

    >>> print(new_data.data_structure)
    {
      "csdm": {
        "version": "0.0.12",
        "description": "A new test dataset",
        "dimensions": [
          {
            "type": "linear",
            "description": "This is a linear dimension",
            "count": 10,
            "increment": "0.1 s",
            "quantity_name": "time",
            "reciprocal": {
              "quantity_name": "frequency"
            }
          }
        ],
        "dependent_variables": []
      }
    }

^^^^^^^^^^^^^^^^^^
MonotonicDimension
^^^^^^^^^^^^^^^^^^

Try adding another :ref:`dim_api` object to the dataset.
This time add a monotonic dimension. A monotonic dimension is where the
coordinates along the dimension are spaced strictly increasing or strictly
decreasing. In the following example, we use a different approach for
adding dimension objects, `i.e.`, by using keywords as the arguments of the
:meth:`~csdfpy.csdm.CSDModel.add_dimension` method.

.. doctest::

    >>> new_data.add_dimension(
    ...     type='monotonic',
    ...     description='This is a monotonic dimension',
    ...     coordinates=['1 µG', '2.1 mG', '12.4 G', '0.5 T', '2 T'])

The above operation generates an instance of the MonotonicDimension and adds
it to the `new_dataset` instance, thereby, creating a 2D{0} dataset. The data
structure form the updated `new_dataset` instance follows

.. doctest::

    >>> print(new_data.data_structure)
    {
      "csdm": {
        "version": "0.0.12",
        "description": "A new test dataset",
        "dimensions": [
          {
            "type": "linear",
            "description": "This is a linear dimension",
            "count": 10,
            "increment": "0.1 s",
            "quantity_name": "time",
            "reciprocal": {
              "quantity_name": "frequency"
            }
          },
          {
            "type": "monotonic",
            "description": "This is a monotonic dimension",
            "coordinates": [
              "1 µG",
              "2.1 mG",
              "12.4 G",
              "0.5 T",
              "2 T"
            ],
            "quantity_name": "magnetic flux density"
          }
        ],
        "dependent_variables": []
      }
    }

Notice, every time a new physical dimension is added, the value of the
:attr:`~csdfpy.dimensions.Dimension.quantity_name` attribute is
appropriately added, if possible.

^^^^^^^^^^^^^^^^
LabeledDimension
^^^^^^^^^^^^^^^^

The third type of dimensions are the labeled dimension. As the name suggests,
this dimension consists of labels. This type of dimension is useful for
datasets describing, for example, the ionization energy as a function of atomic
symbols or the population against the country name.

Try adding a labeled dimension to the `new_data` instance.
This time pass an instance of the :ref:`dim_api` class as the argument of the
:meth:`~csdfpy.csdm.CSDModel.add_dimension` method. To create an instance of
the Dimension class follow,

.. doctest::

    >>> from csdfpy import Dimension
    >>> d1 = Dimension(
    ...     type = 'labeled',
    ...     description = 'This is a labeled dimensions.',
    ...     labels = ['Cu', 'Ag', 'Au']
    ... )

In the above code, the variable `d1` is an instance of :ref:`dim_api`. Now
add this instance to the :meth:`~csdfpy.csdm.CSDModel.add_dimension` method.

.. doctest::

    >>> new_data.add_dimension(d1)

This generates a 3D{0} dataset with the data structure -

.. doctest::

    >>> print(new_data.data_structure)
    {
      "csdm": {
        "version": "0.0.12",
        "description": "A new test dataset",
        "dimensions": [
          {
            "type": "linear",
            "description": "This is a linear dimension",
            "count": 10,
            "increment": "0.1 s",
            "quantity_name": "time",
            "reciprocal": {
              "quantity_name": "frequency"
            }
          },
          {
            "type": "monotonic",
            "description": "This is a monotonic dimension",
            "coordinates": [
              "1 µG",
              "2.1 mG",
              "12.4 G",
              "0.5 T",
              "2 T"
            ],
            "quantity_name": "magnetic flux density"
          },
          {
            "type": "labeled",
            "description": "This is a labeled dimensions.",
            "labels": [
              "Cu",
              "Ag",
              "Au"
            ]
          }
        ],
        "dependent_variables": []
      }
    }

.. note::

    When using a :ref:`dim_api` instance as an argument of the
    :meth:`~csdfpy.csdm.CSDModel.add_dimension` method, one
    must be aware that instances in Python are passed by reference. Therefore,
    any changes to the instance `d1`, in the above example, will affect the
    corresponding dimension instance in the `new_data` instance.
    To be safe, as a general
    recommendation, one should always pass a copy of the instance to the
    :meth:`~csdfpy.csdm.CSDModel.add_dimension` method. We allow the use of
    :ref:`dim_api` objects as arguments because it provides an easy alternative
    for copying an instance of the :ref:`dim_api` class from one
    :ref:`csdm_api` instance to another.

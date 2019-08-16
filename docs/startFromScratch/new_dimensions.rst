
---------------------------------------
How to add instances of Dimension class
---------------------------------------

In the previous section, we create a new dataset using,

.. doctest::

    >>> import csdmpy as cp
    >>> new_data = cp.new(description='A new test dimension dataset')

In this section, we will add dimension objects to this dataset.
An instance of the Dimension class is added using the
:meth:`~csdmpy.csdm.CSDM.add_dimension` method of the :ref:`csdm_api`
instance.
There are three subtypes of Dimension objects,

- LinearDimension
- MonotonicDimension
- LabeledDimension

.. seeAlso::
    :ref:`Dimension API <dim_api>` for further detail.

^^^^^^^^^^^^^^^
LinearDimension
^^^^^^^^^^^^^^^

A linear dimension is where the coordinates along the dimension are uniformly
spaced. Let's add a LinearDimension instance to the ``new_data`` instance.
For this, we make use of the Python dictionary object which follows

.. doctest::

    >>> d0 = {
    ...     'type': 'linear',
    ...     'description': 'This is a linear dimension',
    ...     'count': 10,
    ...     'increment': '0.1 s'
    ... }

Here, we define the dimension type as `linear` and provide an `increment`,
along with the total number of points, `count`, along the dimension. Now, add
this dictionary to the ``new_data`` instance using

.. doctest::

    >>> new_data.add_dimension(d0)

This will generate and add a LinearDimension object to the list of dimensions.
The dataset is now a 1D{0} dataset with the following data structure,

.. doctest::

    >>> print(new_data.data_structure)
    {
      "csdm": {
        "version": "1.0",
        "description": "A new test dimension dataset",
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

Try adding another :ref:`dim_api` object to this dataset.
This time add a monotonic dimension. A monotonic dimension is where the
coordinates along the dimension are spaced either strictly increasing or
strictly decreasing. In the following example, we use a different approach for
adding the dimension object, that is, using the keyword arguments as follows,

.. doctest::

    >>> new_data.add_dimension(
    ...     type='monotonic',
    ...     description='This is a monotonic dimension',
    ...     coordinates=['1 µG', '2.1 mG', '12.4 G', '0.5 T', '2 T'])

The above operation generates an instance of the MonotonicDimension and adds
it to the ``new_data`` instance, thereby, creating a 2D{0} dataset. The data
structure form the updated ``new_data`` instance follows,

.. doctest::

    >>> print(new_data.data_structure)
    {
      "csdm": {
        "version": "1.0",
        "description": "A new test dimension dataset",
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
:attr:`~csdmpy.dimensions.Dimension.quantity_name` attribute is
appropriately added, if applicable.

^^^^^^^^^^^^^^^^
LabeledDimension
^^^^^^^^^^^^^^^^

The third type of dimensions are the labeled dimensions. As the name suggests,
this dimension consists of labels. This type of dimension is useful for
datasets describing, for example, the ionization energy as a function of atomic
symbols or the population of different countries.

Let's add a labeled dimension to the ``new_data`` instance.
This time pass an instance of the :ref:`dim_api` class as the argument of the
:meth:`~csdmpy.csdm.CSDM.add_dimension` method. To create an instance of
the Dimension class follow,

.. doctest::

    >>> from csdmpy import Dimension
    >>> d1 = Dimension(
    ...     type = 'labeled',
    ...     description = 'This is a labeled dimensions.',
    ...     labels = ['Cu', 'Ag', 'Au']
    ... )

In the above code, the variable ``d1`` is an instance of :ref:`dim_api` class.
Now add this instance to the :meth:`~csdmpy.csdm.CSDM.add_dimension`
method.

.. doctest::

    >>> new_data.add_dimension(d1)

This generates a 3D{0} dataset with the data structure ---

.. doctest::

    >>> print(new_data.data_structure)
    {
      "csdm": {
        "version": "1.0",
        "description": "A new test dimension dataset",
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

.. Attention::

    When using a :ref:`dim_api` instance as an argument of the
    :meth:`~csdmpy.csdm.CSDM.add_dimension` method, one
    must be aware that instances in Python are passed by reference. Therefore,
    any changes to the instance ``d1``, in the above example, will affect the
    corresponding dimension instance in the ``new_data`` instance.
    To be safe, as a general
    recommendation, one should always pass a copy of the instance to the
    :meth:`~csdmpy.csdm.CSDM.add_dimension` method. We allow the use of
    :ref:`dim_api` objects as arguments because it provides an easy alternative
    for copying an instance of the :ref:`dim_api` class from one
    :ref:`csdm_api` instance to another.


.. --------------------
.. Removing a dimension
.. --------------------

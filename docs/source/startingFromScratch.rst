
=====================
Starting from scratch
=====================

An instance of the :ref:`csdm_api` class can also be used to create a new
data file. This is particularly useful when writing the raw or the processed
data to a `.csdf` or `.csdfe` file.

First, import the `csdfpy` module and then create a new instance of the
CSDModel class following,

.. doctest::

    >>> import csdfpy as cp
    >>> new = cp.new(description='A new test dataset')

The variable ``new`` is an instance of the CSDModel class with no
independent or dependent variables, `i.e.`, a 0D{0} dataset.
The data structure of this instance is

.. doctest::

    >>> print(new.data_structure)
    {
      "csdm": {
        "version": "0.0.11",
        "description": "A new test dataset",
        "dimensions": [],
        "dependent_variables": []
      }
    }

-------------------------------------------
Adding instances of the :ref:`iv_api` class
-------------------------------------------

An instance of the Dimension class is added using the
:meth:`~csdfpy.CSDModel.add_dimension` method of the :ref:`csdm_api`
instance, in this case, the variable ``new``. There are three ways to add an
independent variable instance. See :ref:`iv_api` API for further detail.

^^^^^^^^^^^^^^^
LinearDimension
^^^^^^^^^^^^^^^

Start by adding a dimension where the coordinates along the dimension are
uniformly spaced. Let's make use of the Python dictionary object to create
and add a new dimension using its :meth:`~csdfpy.Dimension.add_dimension`
method. The Python dictionary for a LinearDimension follows,

.. doctest::

    >>> d0 = {
    ...     'type': 'linear',
    ...     'description': 'This is a linear dimension',
    ...     'count': 10,
    ...     'increment': '0.1 s'
    ... }

Here, we define the `type` as `linear` and provide an increment value
along with the total number of points along the dimension. Add
this dictionary as an argument of the
:meth:`~csdfpy.Dimension.add_dimension` method.

.. doctest::

    >>> new.add_dimension(d0)

This creates and adds a new dimension to the ``new`` instance. The
dataset is now a 1D{0} dataset with the data structure as

.. doctest::

    >>> print(new.data_structure)
    {
      "csdm": {
        "version": "0.0.11",
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

Try adding another :ref:`iv_api` instance to the ``new`` instance.
This time add a dimension where the coordinates along the dimension are spaced
strictly monotonically, that is, either strictly increasing or strictly
decreasing. This time we use the second approach for adding dimensions, `i.e.`,
by using keywords as the arguments of the
:meth:`~csdfpy.Dimension.add_dimension` method as shown below.

.. doctest::

    >>> new.add_dimension(
    ...     type='monotonic',
    ...     description='This is a monotonic dimension',
    ...     values=['1 µG', '2.1 mG', '12.4 G', '0.5 T', '2 T'])

The above operation creates and adds another dimension instance,
thereby generating a 2D{0} dataset. The data structure form the updated ``new``
instance is

.. doctest::

    >>> print(new.data_structure)
    {
      "csdm": {
        "version": "0.0.11",
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
            "values": [
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

Notice, every time a new independent variable corresponding to a physical
dimension is added, the value of the
:attr:`~csdfp.Dimension.quantity_name` attribute is self-generated, if
possible.

^^^^^^^^^^^^^^^^
LabeledDimension
^^^^^^^^^^^^^^^^

The third type of dimensions are the labeled dimension. As the name suggests,
this dimension consists of labeled coordinates. The dimension is useful for
datasets such as describing the human population as a function of the country's
name or the ionization energy as a function of atomic symbols.

Try adding a labeled dimension to the ``new`` instance.
This time pass an instance of the :ref:`iv_api` class as the argument of the
:meth:`~csdfpy.Dimension.add_dimension` method.
But before, create an instance of the Dimension class as follows,

.. doctest::

    >>> from csdfpy import Dimension
    >>> d1 = Dimension(
    ...     type = 'labeled',
    ...     description = 'This is a labeled dimensions.',
    ...     values = ['Cu', 'Ag', 'Au']
    ... )

In the above code, the variable ``d1`` is an instance of :ref:`iv_api`. Now
add this instance to the
:meth:`~csdfpy.Dimension.add_dimension` method.

.. doctest::

    >>> new.add_dimension(d1)

This generates a 3D{0} dataset with the data structure -

.. doctest::

    >>> print(new.data_structure)
    {
      "csdm": {
        "version": "0.0.11",
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
            "values": [
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
            "values": [
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

    When using an :ref:`iv_api` instance as an argument of the
    :meth:`~csdfpy.Dimension.add_dimension` method, one
    must be aware that instances in Python are passed by reference. Therefore,
    any change to the instance ``d1``, in the above example, will affect the
    corresponding independent variable instance from the ``new`` instance.
    To be safe, as a general
    recommendation, one should always pass a copy of the instance to the
    :meth:`~csdfpy.Dimension.add_dimension` method. This
    method is useful when copying an instance of the :ref:`iv_api` class from one
    :ref:`csdm_api` instance to another.

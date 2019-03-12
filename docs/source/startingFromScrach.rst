
====================
Starting from scrach
====================

An instance of the :ref:`csdm_api` class can also be used to create a new
data file. This is particularly useful when writing the raw or the processed
data to a `.csdf` or `.csdfe` file.

First, import the `csdfpy` module and then create a new instance of the
CSDModel class following,

.. doctest::

    >>> import csdfpy as cp
    >>> new = cp.new()

The variable ``new`` is an instance of the CSDModel class with no
independent or dependent variables, `i.e.`, a 0D{0} dataset.
The data structure of this instance is

.. doctest::

    >>> print(new.data_structure)
    {
      "CSDM": {
        "version": "0.0.9",
        "independent_variables": [],
        "dependent_variables": []
      }
    }

-------------------------------------------
Adding instances of the :ref:`iv_api` class
-------------------------------------------

An instance of the IndependentVariable class is added using the
:meth:`~csdfpy.CSDModel.add_independent_variable` method of the :ref:`csdm_api`
instance, in this case, the variable ``new``. There are three ways to add an
independent variable instance. See :ref:`iv_api` API for further detail.

^^^^^^^^^^^^^^^^^^^^^^^^^^
Linearly Sampled Dimension
^^^^^^^^^^^^^^^^^^^^^^^^^^

Start by adding an independent variable where the coordinates along the
dimension are linearly spaced. Let's make use of the
Python dictionary to create and add a new independent variable
``new`` using its :meth:`~csdfpy.IndependentVariable.add_independent_variable`
method. The Python dictionary corresponding to a linearly spaced dimension
coordinates follows,

.. doctest::

    >>> d0 = {'type': 'linearly_sampled',
    ...       'number_of_points': 10,
    ...       'sampling_interval': '0.1 s'
    ...      }

Here, we define the `type` as `linearly_sampled` and provide a sampling
interval and number of points along the independent variable dimension. Add
this dictionary as an argument of the
:meth:`~csdfpy.IndependentVariable.add_independent_variable` method.

.. doctest::

    >>> new.add_independent_variable(d0)

This creates and adds a new independent variable to the ``new`` instance. The
dataset is now a 1D{0} dataset with the data structure -

.. doctest::

    >>> print(new.data_structure)
    {
      "CSDM": {
        "version": "0.0.9",
        "independent_variables": [
          {
            "type": "linearly_sampled",
            "number_of_points": 10,
            "sampling_interval": "0.1 s",
            "quantity": "time",
            "reciprocal": {
              "quantity": "frequency"
            }
          }
        ],
        "dependent_variables": []
      }
    }

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Arbitrarily Sampled Dimension
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Try adding another :ref:`iv_api` instance to the ``new`` instance.
This time add an
independent variable where the coordinates along the dimension are spaced
arbitrarily. Also, try the second approach for adding independent
variables, `i.e.`, by using keywords as the arguments of the
:meth:`~csdfpy.IndependentVariable.add_independent_variable` method as
shown below.

.. doctest::

    >>> new.add_independent_variable(type='arbitrarily_sampled',
    ...                              values=['1 µG', '2.1 mG', '12.4 G', '0.5 T', '2 T'])

The above operation creates and adds another independent variable instance,
thereby generating a 2D{0} dataset. The data structure form the updated ``new``
instance is

.. doctest::

    >>> print(new.data_structure)
    {
      "CSDM": {
        "version": "0.0.9",
        "independent_variables": [
          {
            "type": "linearly_sampled",
            "number_of_points": 10,
            "sampling_interval": "0.1 s",
            "quantity": "time",
            "reciprocal": {
              "quantity": "frequency"
            }
          },
          {
            "type": "arbitrarily_sampled",
            "values": [
              "1 µG",
              "2.1 mG",
              "12.4 G",
              "0.5 T",
              "2 T"
            ],
            "quantity": "magnetic flux density"
          }
        ],
        "dependent_variables": []
      }
    }

Notice, every time a new independent variable corresponding to a physical
dimension is added, the value of the
:attr:`~csdfp.IndependentVariable.quantity` attribute is self-generated, if
possible.

^^^^^^^^^^^^^^^^^
Labeled Dimension
^^^^^^^^^^^^^^^^^

The third type of dimensions are the labeled dimension. As the name suggests,
this dimension consists of labeled coordinates. The dimension is useful for
datasets such as describing the human population as a function of the country's
name or the ionization energy as a function of atomic symbols.

Try adding a labeled dimension to the ``new`` instance.
This time pass an instance of the :ref:`iv_api` class as the argument of the
:meth:`~csdfpy.IndependentVariable.add_independent_variable` method.
But before, create an instance of the IndependentVariable class as follows,

.. doctest::

    >>> from csdfpy import IndependentVariable
    >>> d1 = IndependentVariable(type = 'labeled',
    ...                          values = ['Cu', 'Ag', 'Au'])

In the above code, the variable ``d1`` is an instance of :ref:`iv_api`. Now
add this instance to the
:meth:`~csdfpy.IndependentVariable.add_independent_variable` method.

.. doctest::

    >>> new.add_independent_variable(d1)

This generates a 3D{0} dataset with the data structure -

.. doctest::

    >>> print(new.data_structure)
    {
      "CSDM": {
        "version": "0.0.9",
        "independent_variables": [
          {
            "type": "linearly_sampled",
            "number_of_points": 10,
            "sampling_interval": "0.1 s",
            "quantity": "time",
            "reciprocal": {
              "quantity": "frequency"
            }
          },
          {
            "type": "arbitrarily_sampled",
            "values": [
              "1 µG",
              "2.1 mG",
              "12.4 G",
              "0.5 T",
              "2 T"
            ],
            "quantity": "magnetic flux density"
          },
          {
            "type": "labeled",
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
    :meth:`~csdfpy.IndependentVariable.add_independent_variable` method, one
    must be aware that instances in Python are passed by reference. Therefore,
    any change to the instance ``d1``, in the above example, will affect the
    corresponding independent variable instance from the ``new`` instance.
    To be safe, as a general
    recommendation, one should always pass a copy of the instance to the
    :meth:`~csdfpy.IndependentVariable.add_independent_variable` method. This
    method is useful when copying an instance of the :ref:`iv_api` class from one
    :ref:`csdm_api` instance to another.

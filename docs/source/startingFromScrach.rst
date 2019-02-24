

====================
Starting from scrach
====================

The ``CSDModel`` allow the users to create the data file from scrach.
This is particularly useful when converting the raw or processed
data to ``.csdf`` or ``.csdfx`` files.

First, import the ``csdfpy`` module and then create a new
``CSDModel`` object, ::

    >>> import csdfpy as cp
    >>> new = cp.new()

The variable ``new`` is an object of class ``CSDModel`` with no
controlled and uncontrolled variables. The structure of the
this object follows, ::

    >>> print (new_object.data_structure())
    {
      "CSDM": {
        "uncontrolled_variables": [],
        "controlled_variables": [],
        "version": "0.1.0"
      }
    }

-----------------------------------
Adding the ``controlled_variables``
-----------------------------------

The ``controlled_variables`` are added using the ``add_controlled_variable``
method of the :ref:`csdm_api` class. There are two ways to add controlled
variables. The first approach is to employ the Python dictionary. The
dictionary comprises of an unordered set of permitted key-value pairs. The
other approach is to use the keys as the arguments to the
``add_controlled_variable`` method. In the following, we provide examples of
both schemes for the three classes of controlled variables.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The linearly sampled grid dimension
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the Python dictionary ::

    >>> d0 = {'number_of_points': 10,
    >>>       'sampling_interval': '0.1 s'}
    >>> new.add_controlled_variable(d0)
    >>> print (new.data_structure())
    {
      "CSDM": {
        "uncontrolled_variables": [],
        "controlled_variables": [
          {
            "reciprocal": {
              "quantity": "frequency"
            },
            "number_of_points": 10,
            "sampling_interval": "0.1 s",
            "quantity": "time"
          }
        ],
        "version": "0.1.0"
      }
    }

Using keywords as arguments ::

    >>> new2 = csdfpy.create_new()
    >>> new2.add_controlled_variable(number_of_points=10, sampling_interval='0.1 s')
    >>> print (new.data_structure())
    {
      "CSDM": {
        "uncontrolled_variables": [],
        "controlled_variables": [
          {
            "reciprocal": {
              "quantity": "frequency"
            },
            "number_of_points": 10,
            "sampling_interval": "0.1 s",
            "quantity": "time"
          }
        ],
        "version": "0.1.0"
      }
    }

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The arbitrarily sampled grid dimension
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

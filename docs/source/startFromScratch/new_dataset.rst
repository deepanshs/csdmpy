
----------------------
Creating a new dataset
----------------------

To create a new dataset, import the `csdmpy` module and create a new
instance of the CSDM class using,

.. doctest::

    >>> import csdmpy as cp
    >>> new_data = cp.new(description='A new test dataset')

The :meth:`~csdmpy.new` method returns an instance of the CSDM class
with zero dimensions and zero dependent variables, `i.e.`, a 0D{0} dataset.
In the above example, this instance is assigned to the ``new_data`` variable.
Optionally, a description may also be provided as an argument of the
:meth:`~csdmpy.new` method.
The data structure from the above example is

.. doctest::

    >>> print(new_data.data_structure)
    {
      "csdm": {
        "version": "0.0.12",
        "description": "A new test dataset",
        "dimensions": [],
        "dependent_variables": []
      }
    }


-------------------
An emoji 😁 example
-------------------

Let's make use of what we learned so far and create a simple 1D{1} dataset.
To make it interesting, let's create an emoji dataset.

Start by importing the `csdmpy` package.

.. doctest::

    >>> import csdmpy as cp

Create a new dataset with the :meth:`~csdmpy.new` method.

.. doctest::

    >>> fun_data = cp.new(description='An emoji dataset')

Here, `fun_data` is an instance of the :ref:`csdm_api` class with a 0D{0} dataset.
The data structure of this instance is

.. doctest::

    >>> print(fun_data.data_structure)
    {
      "csdm": {
        "version": "1.0",
        "description": "An emoji dataset"
      }
    }

Add a labeled dimension to the `fun_data` instance. Here, we'll make use of
python dictionary.

.. doctest::

    >>> x = dict(type='labeled', labels=['🍈','🍉','🍋','🍌','🥑','🍍'])

The above python dictionary contains two keys. The `type` key identifies the
dimension as a labeled dimension while the `labels` key holds an
array of labels. In this example, the labels are emojis. Add this dictionary
as an argument of the :meth:`~csdmpy.CSDM.add_dimension` method
of the `fun_data` instance.

.. doctest::

    >>> fun_data.add_dimension(x)
    >>> print(fun_data.data_structure)
    {
      "csdm": {
        "version": "1.0",
        "description": "An emoji dataset",
        "dimensions": [
          {
            "type": "labeled",
            "labels": [
              "🍈",
              "🍉",
              "🍋",
              "🍌",
              "🥑",
              "🍍"
            ]
          }
        ]
      }
    }

We have successfully added a labeled dimension to the `fun_data`
instance.

Next, add a dependent variable. Set up a python dictionary corresponding to the
dependent variable object and add this dictionary as an argument of the
:meth:`~csdmpy.CSDM.add_dependent_variable` method of the `fun_data`
instance.

.. doctest::

    >>> y =dict(type='internal', numeric_type='float32', quantity_type='scalar',
    ...     components=[[0.5, 0.25, 1, 2, 1, 0.25]])
    >>> fun_data.add_dependent_variable(y)

Here, the python dictionary contains `type`, `numeric_type`, and `components`
key. The value of the `components` key holds an array of data values
corresponding to the labels from the labeled dimension.

Now, we have a 😂 dataset...

.. doctest::

    >>> print(fun_data.data_structure)
    {
      "csdm": {
        "version": "1.0",
        "description": "An emoji dataset",
        "dimensions": [
          {
            "type": "labeled",
            "labels": [
              "🍈",
              "🍉",
              "🍋",
              "🍌",
              "🥑",
              "🍍"
            ]
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "numeric_type": "float32",
            "quantity_type": "scalar",
            "components": [
              [
                "0.5, 0.25, ..., 1.0, 0.25"
              ]
            ]
          }
        ]
      }
    }

To serialize this file, use the :meth:`~csdmpy.CSDM.save` method of the
`fun_data` instance as

.. doctest::

    >>> fun_data.dependent_variables[0].encoding = 'base64'
    >>> fun_data.save('my_file.csdf')

.. testcleanup::

    import os
    os.remove('csdmpy/my_file.csdf')

In the above code, the components from the
:attr:`~csdmpy.CSDM.dependent_variables` attribute at index zero, are
encoded as `base64` strings before serializing to the `my_file.csdf` file.

You may also save the components as a binary file, in which case, the file is
serialized with a `.csdfe` file extension.

.. doctest::

  >>> fun_data.dependent_variables[0].encoding = 'raw'
  >>> fun_data.save('my_file_raw.csdfe')

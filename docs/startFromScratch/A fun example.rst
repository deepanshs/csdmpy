
-------------------
An emoji 😁 example
-------------------

Let's make use of what we learned so far and create a simple 1D{1} dataset.
To make it interesting, let's create an emoji dataset.

Start by importing the `csdmpy` package.

.. doctest::

    >>> import csdmpy as cp

Create a labeled dimension. Here, we make use of python dictionary.

.. doctest::

    >>> x = dict(type="labeled", labels=["🍈", "🍉", "🍋", "🍌", "🥑", "🍍"])

The above python dictionary contains two keys. The `type` key identifies the
dimension as a labeled dimension while the `labels` key holds an
array of labels. In this example, the labels are emojis. Add this dictionary
to the list of dimensions.

Next, create a dependent variable. Similarly, set up a python dictionary corresponding
to the dependent variable object.

.. doctest::

    >>> y = dict(
    ...     type="internal",
    ...     numeric_type="float32",
    ...     quantity_type="scalar",
    ...     components=[[0.5, 0.25, 1, 2, 1, 0.25]],
    ... )

Here, the python dictionary contains `type`, `numeric_type`, and `components`
key. The value of the `components` key holds an array of data values
corresponding to the labels from the labeled dimension.

Create a csdm object from the dimensions and dependent variables and we have a 😂 dataset...

.. doctest::

    >>> fun_data = cp.CSDM(
    ...     dimensions=[x], dependent_variables=[y], description="An emoji dataset"
    ... )
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

    >>> fun_data.dependent_variables[0].encoding = "base64"
    >>> fun_data.save("my_file.csdf")


In the above code, the components from the
:attr:`~csdmpy.CSDM.dependent_variables` attribute at index zero, are
encoded as `base64` strings before serializing to the `my_file.csdf` file.

You may also save the components as a binary file, in which case, the file is
serialized with a `.csdfe` file extension.

.. doctest::

    >>> fun_data.dependent_variables[0].encoding = "raw"
    >>> fun_data.save("my_file_raw.csdfe")

.. testcleanup::

    import os

    os.remove("my_file.csdf")
    os.remove("my_file_raw.csdfe")
    os.remove("my_file_raw_0.dat")

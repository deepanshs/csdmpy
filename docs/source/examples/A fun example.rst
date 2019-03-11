

----------------
A fun 🤪 example
----------------

Previously, we looked at datasets from various scientific fields which were
already saved in the CSD model format. In this section we'll go through the steps
on how one can create a new dataset. Let's start with a simple example. To make
it interesting let's create an emoji dataset.

Start with importing the ``csdfpy`` package.

.. doctest::

    >>> import csdfpy as cp

To create a new dataset, use the :meth:`~csdfpy.new` method of the `csdfpy`
package.

.. doctest::

    >>> fundata = cp.new()

This will create an instance of the :ref:`csdm_api` class with a 0D{0} dataset,
`i.e.`, a dataset with no dependent or independent variables.

.. doctest::

    >>> print(fundata.data_structure)
    {
      "CSDM": {
        "version": "1.0.0",
        "independent_variables": [],
        "dependent_variables": []
      }
    }
  
There are three ways to add an independent variable to an instance of the
:ref:`csdm_api` class. Here, we'll make use a python dictionary to create a
:ref:`iv_api` instance. 

.. doctest::

    >>> x = {
    ...     'type': 'labeled',
    ...     'values': ['🍈','🍉','🍋','🍌','🥑','🍍'] 
    ... }

The above python dictionary contains two keys. The `type` key identifies the
independent variable as a labeled dimension while the `values` key holds an
array of labels. In this example, the labels are emoji. To create an instance
of the independent variable, simply add this dictionary as an argument of the
:meth:`~csdfpy.CSDModel.add_independent_variable` method of the ``fundata``
instance.

.. doctest::

    >>> fundata.add_independent_variable(x)
    >>> print(fundata.data_structure)
    {
      "CSDM": {
        "version": "1.0.0",
        "independent_variables": [
          {
            "type": "labeled",
            "values": [
              "🍈",
              "🍉",
              "🍋",
              "🍌",
              "🥑",
              "🍍"
            ]
          }
        ],
        "dependent_variables": []
      }
    }

We have successfully added one independent variable to the ``fundata``
instance. To add more independent variable dimensions, simply write a python
dictionary corresponding to each independent variable and sequentially add it
to the ``fundata`` instance using the
:meth:`~csdfpy.CSDModel.add_independent_variable` method.
In this example, we'll limit to one independent dimension.

Similary, to add a dependent variable, again write a python dictionary
corresponding to the dependent variable. Only this the dictionary is pass as an
arguament to the :meth:`~csdfpy.CSDModel.add_dependent_variable` method.

.. doctest::

    >>> y ={
    ...     'components': [[0.5, 0.25, 1, 2, 1, 0.25]]
    ... }

Here, the python dictionary only contains a `components` key containing values
corresponding to the labels from the independent variable dimension.
Let's add this dictionary to the ``fundata`` instance,

.. doctest::

    >>> fundata.add_dependent_variable(y)

Now, we have a 😂 dataset...

.. doctest::

    >>> print(fundata.data_structure)
    {
      "CSDM": {
        "version": "1.0.0",
        "independent_variables": [
          {
            "type": "labeled",
            "values": [
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
            "numeric_type": "float64",
            "components": "[0.5, 0.5, ...... 1.0, 1.0]"
          }
        ]
      }
    }

.. To plot,

..  todo:: add plot
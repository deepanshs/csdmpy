

----------------
A fun 🤪 example
----------------

We have looked at datasets from various scientific fields. Let's create a
fun dataset. As usual, we start by importing the ``csdfpy`` package. ::

    >>> import csdfpy as cp

Let's create a new :ref:`CSDM_api` object. ::

    >>> fundata = cp.new()

Let's also write a python dictionary for generating a :ref:`cv_api` object ::

    >>> x = {
    ...     'values': ['🍈','🍉','🍋','🍌','🥑','🍍'],
    ...     'non_quantitative': True
    ... }

and another for the :ref:`uv_api` object, ::

    >>> y ={
    ...     'components': [[0.5, 0.25, 1, 2, 1, 0.25]]
    ... }

Let's add the two dictionaries to the ``fundata`` object, ::

    >>> fundata.add_controlled_variable(x)
    >>> fundata.add_uncontrolled_variable(y)

Now, we have a 😂 dataset... ::

    >>> print(fundata.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "numeric_type": "float64",
            "components": "[0.5, 0.5, ...... 1.0, 1.0]"
          }
        ],
        "controlled_variables": [
          {
            "values": [
              "🍈",
              "🍉",
              "🍋",
              "🍌",
              "🥑",
              "🍍"
            ],
            "non_quantitative": true
          }
        ],
        "version": "0.0.9"
      }
    }

To plot,

.. todo:: add plot

.. testsetup::

    >>> import matplotlib
    >>> font = {'family': 'normal', 'weight': 'light', 'size': 9};
    >>> matplotlib.rc('font', **font)
    >>> from os import path

Scatter, 0D{1,1} dataset
^^^^^^^^^^^^^^^^^^^^^^^^

We start with a correlated dataset without a coordinate grid such as
a 0D{1,1} dataset which has no dimensions, d = 0, and two
single-component dependent variables.
In the following example, the two `correlated` dependent variables are
the :math:`^{29}\text{Si}` - :math:`^{29}\text{Si}` nuclear spin couplings,
:math:`^2J`, across a Si-O-Si linkage and the `s`-character product on the
O and two Si along the Si-O bond across the Si-O-Si linkage.

Let's import the dataset.

.. doctest::

    >>> import csdmpy as cp
    >>> filename = 'Test Files/correlatedDataset/0D_dataset/J_vs_s.csdf'
    >>> zero_d_dataset = cp.load(filename)

Since the dataset has no dimensions, the value of the
:attr:`~csdmpy.csdm.CSDM.dimensions` attribute of the :attr:`~csdmpy.csdm.CSDM`
class is an empty tuple,

.. doctest::

    >>> print(zero_d_dataset.dimensions)
    ()

The :attr:`~csdmpy.csdm.CSDM.dependent_variables` attribute, however, holds
two dependent-variable objects. The data structure from the two dependent
variables is,

.. doctest::

    >>> print(zero_d_dataset.dependent_variables[0].data_structure)
    {
      "type": "internal",
      "name": "Gaussian computed J-couplings",
      "unit": "Hz",
      "quantity_name": "frequency",
      "numeric_type": "float32",
      "quantity_type": "scalar",
      "component_labels": [
        "J-coupling"
      ],
      "components": [
        [
          "-1.87378, -1.42918, ..., 25.1742, 26.0608"
        ]
      ]
    }

and

.. doctest::

    >>> print(zero_d_dataset.dependent_variables[1].data_structure)
    {
      "type": "internal",
      "name": "product of s-characters",
      "unit": "%",
      "numeric_type": "float32",
      "quantity_type": "scalar",
      "component_labels": [
        "s-character product"
      ],
      "components": [
        [
          "0.8457453, 0.8534185, ..., 1.5277092, 1.5289451"
        ]
      ]
    }

respectively.

The correlation plot of the dependent-variables from the dataset is
shown below.

.. tip:: Plotting a scatter plot.

  .. doctest::

      >>> import matplotlib.pyplot as plt
      >>> def plot_scatter():
      ...     plt.figure(figsize=(4,3))
      ...
      ...     y0 = zero_d_dataset.dependent_variables[0]
      ...     y1 = zero_d_dataset.dependent_variables[1]
      ...
      ...     plt.scatter(y1.components[0], y0.components[0], s=2, c='k')
      ...     plt.xlabel(y1.axis_label[0])
      ...     plt.ylabel(y0.axis_label[0])
      ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
      ...     plt.show()

.. doctest::

    >>> plot_scatter()

.. figure:: ../../_images/0D{1,1}_dataset.*
    :figclass: figure-polaroid

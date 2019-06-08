

--------------
2D{2} datasets
--------------

The 2D{2} datasets is two-dimensional, :math:`d=2`, dataset
with one two-component dependent variable, :math:`p=2`.

Vector dataset
^^^^^^^^^^^^^^

The following is an example of a simulated electric field dataset of a dipole
as a function of two spatial dimensions.

.. doctest::

    >>> import csdfpy as cp

    >>> filename = '../test-datasets0.0.11/vector/electricField/electric_field_raw.csdfe'
    >>> vector_data = cp.load(filename)
    >>> print (vector_data.data_structure)
    {
      "csdm": {
        "version": "0.0.11",
        "description": "A simulated electric field dataset from an electric dipole.",
        "dimensions": [
          {
            "type": "linear",
            "number_of_points": 64,
            "increment": "0.0625 cm",
            "index_zero_value": "-2.0 cm",
            "quantity": "length",
            "label": "x",
            "reciprocal": {
              "quantity": "wavenumber"
            }
          },
          {
            "type": "linear",
            "number_of_points": 64,
            "increment": "0.0625 cm",
            "index_zero_value": "-2.0 cm",
            "quantity": "length",
            "label": "y",
            "reciprocal": {
              "quantity": "wavenumber"
            }
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "name": "Electric field lines",
            "unit": "C^-1 * N",
            "quantity": "electrical field strength",
            "numeric_type": "float32",
            "quantity_type": "vector_2",
            "components": [
              [
                "3.7466873e-07, 3.7466873e-07, ..., 3.5343004e-07, 3.5343004e-07"
              ],
              [
                "1.6129676e-06, 1.6129676e-06, ..., 1.846712e-06, 1.846712e-06"
              ]
            ]
          }
        ]
      }
    }

The spatial dimensions are sampled linearly along the two independent
variables. The tuples of independent and dependent variable instances
from this example are

.. doctest::

    >>> x = vector_data.dimensions
    >>> y = vector_data.dependent_variables

with the respective coordinates (viewed only up to five values).

.. doctest::

    >>> print(x[0].coordinates[:5])
    [-2.     -1.9375 -1.875  -1.8125 -1.75  ] cm

    >>> print(x[1].coordinates[:5])
    [-2.     -1.9375 -1.875  -1.8125 -1.75  ] cm

respectively.
The components of the dependent variable are of a vector dataset. This is
also seen from the :attr:`~csdfpy.DependentVariable.quantity_type`
attribute of the corresponding dependent variable instance.

.. doctest::

    >>> print(y[0].quantity_type)
    vector_2

Let's plot the vector data. To do this, we use the *streamplot* method
from the matplotlib package. Before we could visualize, however, there
is an initial processing step. We use the methods from the Numpy library for
processing.

.. doctest::

    >>> import numpy as np

    >>> X, Y = np.meshgrid(x[0].coordinates, x[1].coordinates)
    >>> U, V = y[0].components[0], y[0].components[1]
    >>> R = np.sqrt(U**2 + V**2)
    >>> R/=R.min()
    >>> Rlog=np.log10(R)

And now, the plot.

.. doctest::

    >>> import matplotlib.pyplot as plt

    >>> fig, ax = plt.subplots(1,1, figsize=(5.4,5))
    >>> ax.streamplot(X.value, Y.value, U, V, density =1,
    ...               linewidth=Rlog, color=Rlog, cmap='viridis')  # doctest: +SKIP

    >>> ax.set_xlim([x[0].coordinates[0].value,
    ...             x[0].coordinates[-1].value])  # doctest: +SKIP
    >>> ax.set_ylim([x[1].coordinates[0].value,
    ...             x[1].coordinates[-1].value])  # doctest: +SKIP

    >>> # Set axes labels and figure title.
    >>> ax.set_xlabel(x[0].axis_label)  # doctest: +SKIP
    >>> ax.set_ylabel(x[1].axis_label)  # doctest: +SKIP
    >>> ax.set_title(y[0].name) # doctest: +SKIP

    >>> # Set grid lines.
    >>> ax.grid(color='gray', linestyle='--', linewidth=0.5)

    >>> plt.tight_layout(pad=0., w_pad=0., h_pad=0.)
    >>> plt.subplots_adjust(wspace=0.025, hspace=0.05)
    >>> plt.savefig(vector_data.filename+'.pdf')

.. image:: /_static/electric_field_raw.csdfe.pdf

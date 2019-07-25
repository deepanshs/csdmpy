

--------------
2D{2} datasets
--------------

The 2D{2} datasets are two-dimensional, :math:`d=2`,
with one two-component dependent variable, :math:`p=2`.

Vector dataset
^^^^^^^^^^^^^^

The following is an example of a simulated electric field dataset of a dipole
as a function of two spatial dimensions.

.. doctest::

    >>> import csdmpy as cp

    >>> filename = '../test-datasets0.0.12/vector/electricField/electric_field_raw.csdfe'
    >>> vector_data = cp.load(filename)
    >>> print (vector_data.data_structure)
    {
      "csdm": {
        "version": "0.0.12",
        "description": "A simulated electric field dataset from an electric dipole.",
        "dimensions": [
          {
            "type": "linear",
            "count": 64,
            "increment": "0.0625 cm",
            "coordinates_offset": "-2.0 cm",
            "quantity_name": "length",
            "label": "x",
            "reciprocal": {
              "quantity_name": "wavenumber"
            }
          },
          {
            "type": "linear",
            "count": 64,
            "increment": "0.0625 cm",
            "coordinates_offset": "-2.0 cm",
            "quantity_name": "length",
            "label": "y",
            "reciprocal": {
              "quantity_name": "wavenumber"
            }
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "name": "Electric field lines",
            "unit": "C^-1 * N",
            "quantity_name": "electrical field strength",
            "numeric_type": "float32",
            "quantity_type": "vector_2",
            "components": [
              [
                "3.7466873e-07, 3.3365018e-07, ..., 3.5343004e-07, 4.0100363e-07"
              ],
              [
                "1.6129676e-06, 1.6765767e-06, ..., 1.846712e-06, 1.7754871e-06"
              ]
            ]
          }
        ]
      }
    }

The spatial dimensions are sampled linearly along the two dimensions.
The tuples of the dimension and dependent variable instances from this example
are

.. doctest::

    >>> x = vector_data.dimensions
    >>> y = vector_data.dependent_variables

with the respective coordinates (viewed only up to five values).

.. doctest::

    >>> print(x[0].coordinates[:5])
    [-2.     -1.9375 -1.875  -1.8125 -1.75  ] cm

    >>> print(x[1].coordinates[:5])
    [-2.     -1.9375 -1.875  -1.8125 -1.75  ] cm

respectively. In this example, the components of the dependent variable are
vectors as seen from the
:attr:`~csdmpy.dependent_variables.DependentVariable.quantity_type`
attribute of the corresponding dependent variable instance.

.. doctest::

    >>> print(y[0].quantity_type)
    vector_2

Let's plot the vector data. To do this, we use the *streamplot* method
from the matplotlib package. Before we could visualize, however, there
is an initial processing step. We use the Numpy library for processing.

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
    >>> def plot_vector():
    ...     fig, ax = plt.subplots(1,1, figsize=(5.4,5))
    ...     ax.streamplot(X.value, Y.value, U, V, density =1,
    ...                   linewidth=Rlog, color=Rlog, cmap='viridis')
    ...
    ...     ax.set_xlim([x[0].coordinates[0].value,
    ...                 x[0].coordinates[-1].value])
    ...     ax.set_ylim([x[1].coordinates[0].value,
    ...                 x[1].coordinates[-1].value])
    ...
    ...     # Set axes labels and figure title.
    ...     ax.set_xlabel(x[0].axis_label)
    ...     ax.set_ylabel(x[1].axis_label)
    ...     ax.set_title(y[0].name)
    ...
    ...     # Set grid lines.
    ...     ax.grid(color='gray', linestyle='--', linewidth=0.5)
    ...
    ...     plt.tight_layout()
    ...     plt.show()

.. doctest::

    >>> plot_vector()

.. image:: electric_field_raw.png
   :align: center

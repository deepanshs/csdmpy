
.. testsetup::

    >>> import matplotlib
    >>> font = {'family': 'normal', 'weight': 'light', 'size': 9};
    >>> matplotlib.rc('font', **font)
    >>> from os import path

----------------------
Vector, 2D{2} datasets
----------------------

The 2D{2} datasets are two-dimensional, :math:`d=2`,
with one two-component dependent variable, :math:`p=2`.

Vector dataset
^^^^^^^^^^^^^^

The following is an example of a simulated electric field vector dataset of a
dipole as a function of two linearly sampled spatial dimensions.

.. doctest::

    >>> import csdmpy as cp

    >>> filename = 'Test Files/vector/electric_field/electric_field_raw.csdfe'
    >>> vector_data = cp.load(filename)
    >>> print (vector_data.data_structure)
    {
      "csdm": {
        "version": "1.0",
        "read_only": true,
        "timestamp": "2014-09-30T11:16:33Z",
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
            "quantity_name": "electric field strength",
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


The tuples of the dimension and dependent variable instances from this example
are

.. doctest::

    >>> x = vector_data.dimensions
    >>> y = vector_data.dependent_variables

with the respective coordinates (viewed only up to five values),

.. doctest::

    >>> print(x[0].coordinates[:5])
    [-2.     -1.9375 -1.875  -1.8125 -1.75  ] cm

    >>> print(x[1].coordinates[:5])
    [-2.     -1.9375 -1.875  -1.8125 -1.75  ] cm

In this example, the components of the dependent variable are
vectors as seen from the
:attr:`~csdmpy.dependent_variables.DependentVariable.quantity_type`
attribute of the corresponding dependent variable instance.

.. doctest::

    >>> print(y[0].quantity_type)
    vector_2

From the value `vector_2`, `vector` indicates a vector dataset while `2`
indicates the number of vector components.

**Visualizing the dataset**

Let's visualize the vector data using the *streamplot* method
from the matplotlib package. Before we could visualize, however, there
is an initial processing step. We use the Numpy library for processing.

.. doctest::

    >>> import numpy as np

    >>> X, Y = np.meshgrid(x[0].coordinates, x[1].coordinates)
    >>> U, V = y[0].components[0], y[0].components[1]
    >>> R = np.sqrt(U**2 + V**2)
    >>> R/=R.min()
    >>> Rlog=np.log10(R)

In the above processing, we calculate the X-Y grid points along with a
scaled magnitude of the vector dataset. The magnitude is scaled such that the
minimum value is one. This scaled magnitude is stored in ``R``.
Next, we calculate the log of ``R`` to visualize the intensity of the plot on
a logarithmic scale.

And now, the plot.

.. tip:: **Plotting a streamplot vector data**

  .. doctest::

      >>> import matplotlib.pyplot as plt
      >>> def plot_vector():
      ...     plt.figure(figsize=(4,3.5))
      ...     plt.streamplot(X.value, Y.value, U, V, density =1,
      ...                   linewidth=Rlog, color=Rlog, cmap='viridis')
      ...
      ...     plt.xlim([x[0].coordinates[0].value, x[0].coordinates[-1].value])
      ...     plt.ylim([x[1].coordinates[0].value, x[1].coordinates[-1].value])
      ...
      ...     # Set axes labels and figure title.
      ...     plt.xlabel(x[0].axis_label)
      ...     plt.ylabel(x[1].axis_label)
      ...     plt.title(y[0].name)
      ...
      ...     # Set grid lines.
      ...     plt.grid(color='gray', linestyle='--', linewidth=0.5)
      ...
      ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
      ...     plt.show()

.. doctest::

    >>> plot_vector()


.. testsetup::

    >>> def plot_vector_save(dataObject):
    ...     plt.figure(figsize=(4,3.5))
    ...     plt.streamplot(X.value, Y.value, U, V, density =1,
    ...                   linewidth=Rlog, color=Rlog, cmap='viridis')
    ...
    ...     plt.xlim([x[0].coordinates[0].value, x[0].coordinates[-1].value])
    ...     plt.ylim([x[1].coordinates[0].value, x[1].coordinates[-1].value])
    ...
    ...     # Set axes labels and figure title.
    ...     plt.xlabel(x[0].axis_label)
    ...     plt.ylabel(x[1].axis_label)
    ...     plt.title(y[0].name)
    ...
    ...     # Set grid lines.
    ...     plt.grid(color='gray', linestyle='--', linewidth=0.5)
    ...
    ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    ...     filename = path.split(dataObject.filename)[1]
    ...     filepath = './docs/_images'
    ...     pth = path.join(filepath, filename)
    ...     plt.savefig(pth+'.pdf')
    ...     plt.savefig(pth+'.png', dpi=100)
    ...     plt.close()

.. testsetup::

    >>> plot_vector_save(vector_data)


.. figure:: ../../_images/electric_field_raw.csdfe.*
    :figclass: figure-polaroid

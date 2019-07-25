


Transmission Electron Microscopy (TEM) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following `TEM dataset <https://doi.org/10.1371/journal.pbio.1000502>`_ is
a section of an early larval brain of *Drosophila melanogaster* used in the
analysis of neuronal microcircuitry. The dataset was obtained
from the `TrakEM2 tutorial <http://www.ini.uzh.ch/~acardona/data.html>`_ and
subsequently converted to the CSD model file-format.

Let's import the CSD model data-file and look at its data structure.

.. doctest::

    >>> import csdmpy as cp
    >>> import matplotlib.pyplot as plt

    >>> filename = '../test-datasets0.0.12/ssTEM/TEM.csdf'
    >>> TEM = cp.load(filename)
    >>> print(TEM.data_structure)
    {
      "csdm": {
        "version": "0.0.12",
        "description": "TEM image of the early larval brain of Drosophila melanogaster used in the analysis of neuronal microcircuitry.",
        "dimensions": [
          {
            "type": "linear",
            "count": 512,
            "increment": "4.0 nm",
            "quantity_name": "length",
            "reciprocal": {
              "quantity_name": "wavenumber"
            }
          },
          {
            "type": "linear",
            "count": 512,
            "increment": "4.0 nm",
            "quantity_name": "length",
            "reciprocal": {
              "quantity_name": "wavenumber"
            }
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "numeric_type": "uint8",
            "quantity_type": "scalar",
            "components": [
              [
                "126, 107, ..., 164, 171"
              ]
            ]
          }
        ]
      }
    }

This dataset contains two uniformly spaced linear dimensions and one
single-component dependent variable.
The tuples of the dimension and the dependent variable instances from this
example are

.. doctest::

    >>> x = TEM.dimensions
    >>> y = TEM.dependent_variables

with the respective coordinates (viewed only for the first ten coordinates),

.. doctest::

    >>> x0 = x[0].coordinates
    >>> print(x0[:10])
    [ 0.  4.  8. 12. 16. 20. 24. 28. 32. 36.] nm

    >>> x1 = x[1].coordinates
    >>> print(x1[:10])
    [ 0.  4.  8. 12. 16. 20. 24. 28. 32. 36.] nm

For convenience, let's convert the coordinate from `nm` to `µm` using the
:meth:`~csdmpy.dimensions.Dimension.to` method of the respective :ref:`dim_api`
instance,

.. doctest::

    >>> x[0].to('µm')
    >>> x[1].to('µm')

and plot the data.

.. doctest::

    >>> def plot_image(data_object):
    ...     fig, ax = plt.subplots(1,1)
    ...
    ...     # Set the extents of the image plot.
    ...     extent = [x0[0].value, x0[-1].value,
    ...               x1[0].value, x1[-1].value]
    ...
    ...     # Add the image plot.
    ...     im = ax.imshow(y[0].components[0], extent=extent, cmap='bone')
    ...
    ...     # Add a colorbar.
    ...     cbar = fig.colorbar(im)
    ...     cbar.ax.set_ylabel(y[0].axis_label[0])
    ...
    ...     # Set up the axes label and figure title.
    ...     ax.set_xlabel(x[0].axis_label)
    ...     ax.set_ylabel(x[1].axis_label)
    ...     ax.set_title(y[0].name)
    ...
    ...     # Set up the grid lines.
    ...     ax.grid(color='k', linestyle='--', linewidth=0.5)
    ...
    ...     plt.tight_layout()
    ...     plt.show()

.. doctest::

    >>> plot_image(TEM)

.. figure:: TEM.pdf
   :align: center

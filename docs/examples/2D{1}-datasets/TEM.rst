
.. testsetup::

    >>> import matplotlib
    >>> font = {'family': 'normal', 'weight': 'light', 'size': 9};
    >>> matplotlib.rc('font', **font)
    >>> from os import path

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

    >>> filename = 'Test Files/TEM/TEM.csdf'
    >>> TEM = cp.load(filename)
    >>> print(TEM.data_structure)
    {
      "csdm": {
        "version": "1.0",
        "read_only": true,
        "timestamp": "2016-03-12T16:41:00Z",
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

    >>> print(x[0].coordinates[:10])
    [ 0.  4.  8. 12. 16. 20. 24. 28. 32. 36.] nm

    >>> print(x[1].coordinates[:10])
    [ 0.  4.  8. 12. 16. 20. 24. 28. 32. 36.] nm

For convenience, let's convert the coordinate from `nm` to `µm` using the
:meth:`~csdmpy.dimensions.Dimension.to` method of the respective :ref:`dim_api`
instance,

.. doctest::

    >>> x[0].to('µm')
    >>> x[1].to('µm')

and plot the data.

.. doctest::

    >>> def plot_image():
    ...     plt.figure(figsize=(4,3))
    ...
    ...     # Set the extents of the image plot.
    ...     extent = [x[0].coordinates[0].value, x[0].coordinates[-1].value,
    ...               x[1].coordinates[0].value, x[1].coordinates[-1].value]
    ...
    ...     # Add the image plot.
    ...     im = plt.imshow(y[0].components[0], origin='lower', extent=extent, cmap='gray')
    ...
    ...     # Add a colorbar.
    ...     cbar = plt.gca().figure.colorbar(im)
    ...     cbar.ax.set_ylabel(y[0].axis_label[0])
    ...
    ...     # Set up the axes label and figure title.
    ...     plt.xlabel(x[0].axis_label)
    ...     plt.ylabel(x[1].axis_label)
    ...     plt.title(y[0].name)
    ...
    ...     # Set up the grid lines.
    ...     plt.grid(color='k', linestyle='--', linewidth=0.5)
    ...
    ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    ...     plt.show()

.. doctest::

    >>> plot_image()

.. testsetup::

    >>> def plot_image_save(dataObject):
    ...     plt.figure(figsize=(4,3))
    ...
    ...     # Set the extents of the image plot.
    ...     extent = [x[0].coordinates[0].value, x[0].coordinates[-1].value,
    ...               x[1].coordinates[0].value, x[1].coordinates[-1].value]
    ...
    ...     # Add the image plot.
    ...     im = plt.imshow(y[0].components[0], origin='lower', extent=extent, cmap='gray')
    ...
    ...     # Add a colorbar.
    ...     cbar = plt.gca().figure.colorbar(im)
    ...     cbar.ax.set_ylabel(y[0].axis_label[0])
    ...
    ...     # Set up the axes label and figure title.
    ...     plt.xlabel(x[0].axis_label)
    ...     plt.ylabel(x[1].axis_label)
    ...     plt.title(y[0].name)
    ...
    ...     # Set up the grid lines.
    ...     plt.grid(color='k', linestyle='--', linewidth=0.5)
    ...
    ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    ...
    ...     filename = path.split(dataObject.filename)[1]
    ...     filepath = './docs/_images'
    ...     pth = path.join(filepath, filename)
    ...     plt.savefig(pth+'.pdf')
    ...     plt.savefig(pth+'.png', dpi=100)
    ...     plt.close()

.. testsetup::

    >>> plot_image_save(TEM)

.. figure:: ../../_images/TEM.csdf.*
    :figclass: figure-polaroid

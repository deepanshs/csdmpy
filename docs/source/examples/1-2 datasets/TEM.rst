

TEM dataset
^^^^^^^^^^^

The following `TEM dataset <https://doi.org/10.1371/journal.pbio.1000502>`_ is
a section of early larval brain of *Drosophila melanogaster* used in the
analysis of neuronal microcircuitry. The dataset was obtained
from the `TrakEM2 tutorial <http://www.ini.uzh.ch/~acardona/data.html>`_ and
subsequently converted to the CSD model format. 

Let's import the file and look at the data structure.

.. doctest::

    >>> import csdfpy as cp
    >>> import matplotlib.pyplot as plt
    >>> filename = '../../test-datasets/ssTEM/TEM.csdf'
    >>> TEM = cp.load(filename)
    >>> print(TEM.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "numeric_type": "uint8",
            "components": "[126, 126, ...... 164, 164]"
          }
        ],
        "controlled_variables": [
          {
            "reciprocal": {
              "quantity": "wavenumber"
            },
            "number_of_points": 512,
            "sampling_interval": "4.0 nm",
            "quantity": "length"
          },
          {
            "reciprocal": {
              "quantity": "wavenumber"
            },
            "number_of_points": 512,
            "sampling_interval": "4.0 nm",
            "quantity": "length"
          }
        ],
        "version": "0.0.9"
      }
    }

The tuples of controlled and the uncontrolled variable instances are

.. doctest::

    >>> x = TEM.controlled_variables
    >>> y = TEM.uncontrolled_variables

with the respective coordinates (previewed only for the first ten coordinates),

.. doctest::

    >>> x0 = x[0].coordinates
    >>> print(x0[:10])
    [ 0.  4.  8. 12. 16. 20. 24. 28. 32. 36.] nm

    >>> x1 = x[1].coordinates
    >>> print(x1[:10])
    [ 0.  4.  8. 12. 16. 20. 24. 28. 32. 36.] nm

For convenience, let's convert the coordinate unit from nm to µm using the
:py:meth:`~csdfpy.ControlledVariable.to` method of the :ref:`cv_api` class,

.. doctest::

    >>> x[0].to('µm')
    >>> x[1].to('µm')

and plot the data.

.. doctest::

    >>> fig, ax = plt.subplots(1,1,figsize=(5, 5))

    >>> # Set the extents of the image plot.
    >>> extent = [x0[0].value, x0[-1].value,
    ...           x1[0].value, x1[-1].value]

    >>> # Add the image plot.
    >>> im = ax.imshow(y[0].components[0], extent=extent, cmap='bone')  # doctest: +SKIP

    >>> # Add a colorbar.
    >>> cbar = fig.colorbar(im)
    >>> cbar.ax.set_ylabel(y[0].axis_label[0])

    >>> # Set up the axes label and figure title.
    >>> ax.set_xlabel(x[0].axis_label)  # doctest: +SKIP
    >>> ax.set_ylabel(x[1].axis_label)  # doctest: +SKIP
    >>> ax.set_title(y[0].name)  # doctest: +SKIP

    >>> # Set up the grid lines.
    >>> ax.grid(color='k', linestyle='--', linewidth=0.5)
    
    >>> plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    >>> plt.savefig(TEM.filename+'.pdf')
    >>> plt.show()

.. image:: /_static/TEM.csdf.pdf
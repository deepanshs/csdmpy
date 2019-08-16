
.. testsetup::

    >>> import matplotlib
    >>> import matplotlib.pyplot as plt
    >>> font = {'family': 'normal', 'weight': 'light', 'size': 9};
    >>> matplotlib.rc('font', **font)
    >>> from os import path


Astronomy dataset
^^^^^^^^^^^^^^^^^

The following dataset is a new observation of the Bubble Nebula
acquired by
`The Hubble Heritage Team <https://archive.stsci.edu/prepds/heritage/bubble/introduction.html>`_,
on February 2016. The original dataset was obtained in the FITS format
and subsequently converted to the CSD model file-format. For the convenience of
illustration, we have downsampled the original dataset.

Let's load the `.csdfe` file and look at its data structure.

.. doctest::

    >>> import csdmpy as cp
    >>> bubble_nebula = cp.load('Test Files/BubbleNebula/Bubble.csdfe')
    >>> print(bubble_nebula.data_structure)
    {
      "csdm": {
        "version": "1.0",
        "read_only": true,
        "timestamp": "2016-02-26T16:41:00Z",
        "description": "The dataset is a new observation of the Bubble Nebula acquired by The Hubble Heritage Team, in February 2016.",
        "dimensions": [
          {
            "type": "linear",
            "count": 1024,
            "increment": "-0.0002581136196 °",
            "coordinates_offset": "350.311874957 °",
            "quantity_name": "plane angle",
            "label": "Right Ascension"
          },
          {
            "type": "linear",
            "count": 1024,
            "increment": "0.0001219957797701109 °",
            "coordinates_offset": "61.12851494969163 °",
            "quantity_name": "plane angle",
            "label": "Declination"
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "name": "Bubble Nebula, 656nm",
            "numeric_type": "float32",
            "quantity_type": "scalar",
            "components": [
              [
                "0.0, 0.0, ..., 0.0, 0.0"
              ]
            ]
          }
        ]
      }
    }

Here, the variable ``bubble_nebula`` is an instance of the :ref:`csdm_api`
class. From the data structure, one finds two dimensions, labeled as
*Right Ascension* and *Declination*, and a single one-component dependent
variable named as *Bubble Nebula, 656nm*.


Let's get the tuples of the dimension and dependent variable instances from
the ``bubble_nebula`` instance following,

.. doctest::

    >>> x = bubble_nebula.dimensions
    >>> y = bubble_nebula.dependent_variables

Because there are two dimension instances in ``x``, let's look
at the coordinates along each dimensions, using the
:attr:`~csdmpy.dimensions.Dimension.coordinates` attribute of the
respective instances.

.. doctest::

    >>> print(x[0].coordinates[:10])
    [350.31187496 350.31161684 350.31135873 350.31110062 350.3108425
     350.31058439 350.31032628 350.31006816 350.30981005 350.30955193] deg

    >>> print(x[1].coordinates[:10])
    [61.12851495 61.12863695 61.12875894 61.12888094 61.12900293 61.12912493
     61.12924692 61.12936892 61.12949092 61.12961291] deg

Here, we only print the first 10 coordinates along the respective dimensions.

The component of the dependent variable is accessed through the
:attr:`~csdmpy.dependent_variables.DependentVariable.components` attribute.

.. doctest::

    >>> y00 = y[0].components[0]

**Visualizing the dataset**

Now, to plot the dataset.

.. tip:: **Plotting an intensity data**

  .. doctest::

      >>> import matplotlib.pyplot as plt
      >>> from matplotlib.colors import LogNorm
      >>> import numpy as np

      >>> def plot():
      ...     # Figure setup.
      ...     fig, ax = plt.subplots(1,1, figsize=(4,3))
      ...     ax.set_facecolor('w')
      ...
      ...     x0 = x[0].coordinates
      ...     x1 = x[1].coordinates
      ...
      ...     # Set the extents of the image.
      ...     extent=[x0[0].value, x0[-1].value, x1[0].value, x1[-1].value]
      ...
      ...     # Log intensity image plot.
      ...     im = ax.imshow(np.abs(y00), origin='lower', cmap='bone_r',
      ...                    norm=LogNorm(vmax=y00.max()/10, vmin=7.5e-3, clip=True),
      ...                    extent=extent, aspect='auto')
      ...
      ...     # Set the axes labels and the figure tile.
      ...     ax.set_xlabel(x[0].axis_label)
      ...     ax.set_ylabel(x[1].axis_label)
      ...     ax.set_title(y[0].name)
      ...     ax.locator_params(nbins=5)
      ...
      ...     # Add a colorbar.
      ...     cbar = fig.colorbar(im)
      ...     cbar.ax.set_ylabel(y[0].axis_label[0])
      ...
      ...     # Set the x and y limits.
      ...     ax.set_xlim([350.25, 350.1])
      ...     ax.set_ylim([61.15, 61.22])
      ...
      ...     # Add grid lines.
      ...     ax.grid(color='gray', linestyle='--', linewidth=0.5)
      ...
      ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
      ...     plt.show()

.. doctest::

    >>> plot()

.. testsetup::

    >>> def plot_save(dataObject):
    ...     # Figure setup.
    ...     fig, ax = plt.subplots(1,1, figsize=(4,3))
    ...     ax.set_facecolor('w')
    ...
    ...     x0 = x[0].coordinates
    ...     x1 = x[1].coordinates
    ...
    ...     # Set the extents of the image.
    ...     extent=[x0[0].value, x0[-1].value, x1[0].value, x1[-1].value]
    ...
    ...     # Log intensity image plot.
    ...     im = ax.imshow(np.abs(y00), origin='lower', cmap='bone_r',
    ...                    norm=LogNorm(vmax=y00.max()/10, vmin=7.5e-3, clip=True),
    ...                    extent=extent, aspect='auto')
    ...
    ...     # Set the axes labels and the figure tile.
    ...     ax.set_xlabel(x[0].axis_label)
    ...     ax.set_ylabel(x[1].axis_label)
    ...     ax.set_title(y[0].name)
    ...     ax.locator_params(nbins=5)
    ...
    ...     # Add a colorbar.
    ...     cbar = fig.colorbar(im)
    ...     cbar.ax.set_ylabel(y[0].axis_label[0])
    ...
    ...     # Set the x and y limits.
    ...     ax.set_xlim([350.25, 350.1])
    ...     ax.set_ylim([61.15, 61.22])
    ...
    ...     # Add grid lines.
    ...     ax.grid(color='gray', linestyle='--', linewidth=0.5)
    ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    ...
    ...     filename = path.split(dataObject.filename)[1]
    ...     filepath = './docs/_images'
    ...     pth = path.join(filepath, filename)
    ...     plt.savefig(pth+'.pdf')
    ...     plt.savefig(pth+'.png', dpi=100)
    ...     plt.close()

.. testsetup::

    >>> plot_save(bubble_nebula)

.. figure:: ../../_images/Bubble.csdfe.*
    :figclass: figure-polaroid

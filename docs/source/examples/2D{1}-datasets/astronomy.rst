


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

    >>> import csdfpy as cp
    >>> bubble_nebula = cp.load('../test-datasets0.0.12/astronomy/source/Bubble Nebula/bubble.csdm')
    >>> print(bubble_nebula.data_structure)
    {
      "csdm": {
        "version": "0.0.12",
        "timestamp": "2019-06-25T01:29:53Z",
        "read_only": true,
        "description": "The dataset is a new observation of the Bubble Nebula acquired by The Hubble Heritage Team, in February 2016.",
        "dimensions": [
          {
            "type": "linear",
            "count": 1024,
            "increment": "-2.279306196154649e-05 °",
            "coordinates_offset": "350.311874957 °",
            "quantity_name": "angle",
            "label": "Right Ascension"
          },
          {
            "type": "linear",
            "count": 1024,
            "increment": "0.0001219957797701109 °",
            "coordinates_offset": "-61.12851494969163 °",
            "quantity_name": "angle",
            "label": "Declination"
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "name": "hlsp_heritage_hst_wfc3-uvis_bubble_nebula_f656n_v1_drc",
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
variable named as *hlsp_heritage_hst_wfc3-uvis_bubble_nebula_f656n_v1_drc*.
During the file conversion to the CSD model, we retained the original FITS
standard naming convention.


Let's get the tuples of the dimension and dependent variable instances from
the `bubble_nebula` instance following,

.. doctest::

    >>> x = bubble_nebula.dimensions
    >>> y = bubble_nebula.dependent_variables

Because there are two dimension instances in `x`, let's look
at the coordinates along each dimension, `x0`, and `x1` respectively,
using the :py:attr:`~csdfpy.dimensions.Dimension.coordinates` attribute of the
respective instances.

.. doctest::

    >>> x0 = x[0].coordinates[:10]
    >>> print(x0)
    [350.31187496 350.31185216 350.31182937 350.31180658 350.31178378
     350.31176099 350.3117382  350.31171541 350.31169261 350.31166982] deg

    >>> x1 = x[1].coordinates[:10]
    >>> print(x1)
    [-61.12851495 -61.12839295 -61.12827096 -61.12814896 -61.12802697
     -61.12790497 -61.12778298 -61.12766098 -61.12753898 -61.12741699] deg

Here, we only print the first 10 coordinates along the respective dimensions.

The component of the dependent variable is accessed through the
:py:attr:`~csdfpy.dependent_variables.DependentVariable.components` attribute.

.. doctest::

    >>> y00 = y[0].components[0]

We plot this dataset using the plot method.

    >>> from matplotlib.colors import LogNorm
    >>> cp.plot(bubble_nebula, cmap='cubehelix', vmin=0, vmax=0.55)

.. .. doctest::

..     >>> import matplotlib.pyplot as plt
..     >>> from matplotlib.colors import LogNorm
..     >>> import numpy as np

..     >>> # Figure setup.
..     >>> fig, ax = plt.subplots(1,1,figsize=(6, 5))
..     >>> ax.set_facecolor('w')

..     >>> # Set the extents of the image.
..     >>> extent=[x0[0].value, x0[-1].value,
..     ...         x1[0].value, x1[-1].value]

..     >>> # Log intensity image plot.
..     >>> im = ax.imshow(np.abs(y00), origin='lower', cmap='bone_r',
..     ...                norm=LogNorm(vmax=y00.max()/10, vmin=7.5e-3, clip=True),
..     ...                extent=extent, aspect='auto')

..     >>> # Set the axes labels and the figure tile.
..     >>> ax.set_xlabel(x[0].axis_label)  # doctest: +SKIP
..     >>> ax.set_ylabel(x[1].axis_label)  # doctest: +SKIP
..     >>> ax.set_title(y[0].name)  # doctest: +SKIP

..     >>> # Add a colorbar.
..     >>> cbar = fig.colorbar(im)
..     >>> cbar.ax.set_ylabel(y[0].axis_label[0])  # doctest: +SKIP

..     >>> # Set the x and y limits.
..     >>> ax.set_xlim([350.25, 350.1])  # doctest: +SKIP
..     >>> ax.set_ylim([61.15, 61.22])  # doctest: +SKIP

..     >>> # Add grid lines.
..     >>> ax.grid(color='gray', linestyle='--', linewidth=0.5)

..     >>> plt.tight_layout(pad=0, w_pad=0, h_pad=0)
..     >>> plt.savefig(bubble_nebula.filename+'.pdf', dpi=450)

.. figure:: bubble.png

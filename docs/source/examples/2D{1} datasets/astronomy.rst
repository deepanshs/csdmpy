


Astronomy dataset
^^^^^^^^^^^^^^^^^

The following dataset is a new observation of the Bubble Nebula 
acquired by
`The Hubble Heritage Team <https://archive.stsci.edu/prepds/heritage/bubble/introduction.html>`_,
on February 2016. The original dataset was downloaded in the FITS format
and then converted to the CSD model file-format.

Let's load the `.csdfe` file and take a quick look at its data structure.

.. doctest::

    >>> import csdfpy as cp

    >>> bubble_data = cp.load('../../test-datasets0.0.9/astronomy/source/Bubble Nebula/Bubble.csdfe')
    >>> print(bubble_data.data_structure)
    {
      "CSDM": {
        "version": "0.0.9",
        "independent_variables": [
          {
            "type": "linearly_sampled",
            "number_of_points": 11596,
            "sampling_interval": "2.279306196154649e-05 °",
            "reference_offset": "-350.04758940351087 °",
            "quantity": "angle",
            "reverse": true,
            "label": "Right Ascension"
          },
          {
            "type": "linearly_sampled",
            "number_of_points": 11351,
            "sampling_interval": "1.1005521846938031e-05 °",
            "reference_offset": "-61.128514949691635 °",
            "quantity": "angle",
            "label": "Declination"
          }
        ],
        "dependent_variables": [
          {
            "name": "hlsp_heritage_hst_wfc3-uvis_bubble_nebula_f656n_v1_drc",
            "numeric_type": "float32",
            "components": "[0.0, 0.0, ...... 0.0, 0.0]"
          }
        ]
      }
    }

Here, the variable ``bubble_data`` is an instance of the :ref:`csdm_api` class.
From the data structure, one finds two independent variables, labeled as
*Right Ascension* and *Declination*, and a single one-component dependent
variable named as *hlsp_heritage_hst_wfc3-uvis_bubble_nebula_f656n_v1_drc*.
During the file conversion to the CSD model, we retained the original FITS
standard naming convention.


Let's get the tuples of the independent and dependent variable instances from
the ``bubble_data`` instance following,

.. doctest::

    >>> x = bubble_data.independent_variables
    >>> y = bubble_data.dependent_variables

Because there are two independent variable instances in `x`, let's take a look
at the coordinates of each independent variable, `x0`, and `x1` respectively, 
using the :py:attr:`~csdfpy.IndependentVariable.coordinates` attribute of the
respective instances.

.. doctest::

    >>> x0 = x[0].coordinates
    >>> print(x0)
    [350.31187496 350.31185216 350.31182937 ... 350.04763499 350.0476122
     350.0475894 ] deg

    >>> x1 = x[1].coordinates
    >>> print(x1)
    [61.12851495 61.12852596 61.12853696 ... 61.25340561 61.25341662
     61.25342762] deg
 
Notice, the descending order of coordinates in `x0` which is a
consequence of  the :py:attr:`~csdfpy.IndependentVariable.reverse` attribute set
to `True` for the corresponding :ref:`iv_api` instance. This is also
observed from the data structure view shown above. As before, the component of the
dependent variable is accessed through the 
:py:attr:`~csdfpy.DependentVariable.components` attribute.

.. doctest::

     >>> y00 = y[0].components[0]

Now, to plot the data.

.. doctest::

    >>> import matplotlib.pyplot as plt
    >>> from matplotlib.colors import LogNorm
    >>> import numpy as np

    >>> # Figure setup.
    >>> fig, ax = plt.subplots(1,1,figsize=(6, 5))
    >>> ax.set_facecolor('w')

    >>> # Set the extents of the image.
    >>> extent=[x0[0].value, x0[-1].value,
    ...         x1[0].value, x1[-1].value]

    >>> # Log intensity image plot.
    >>> im = ax.imshow(np.abs(y00), origin='lower', cmap='bone_r',
    ...                norm=LogNorm(vmax=y00.max()/10, vmin=7.5e-3, clip=True),
    ...                extent=extent, aspect='auto')

    >>> # Set the axes labels and the figure tile.
    >>> ax.set_xlabel(x[0].axis_label)  # doctest: +SKIP
    >>> ax.set_ylabel(x[1].axis_label)  # doctest: +SKIP
    >>> ax.set_title(y[0].name)  # doctest: +SKIP
    
    >>> # Add a colorbar.
    >>> cbar = fig.colorbar(im)
    >>> cbar.ax.set_ylabel(y[0].axis_label[0])  # doctest: +SKIP

    >>> # Set the x and y limits.
    >>> ax.set_xlim([350.25, 350.1])  # doctest: +SKIP
    >>> ax.set_ylim([61.15, 61.22])  # doctest: +SKIP

    >>> # Add grid lines.
    >>> ax.grid(color='gray', linestyle='--', linewidth=0.5)

    >>> plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    >>> plt.savefig(bubble_data.filename+'.pdf', dpi=450)
    >>> plt.show()

.. image:: /_static/Bubble.csdfx.png


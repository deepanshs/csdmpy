


Nuclear Magnetic Resonance (NMR) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following example is a :math:`^{29}\mathrm{Si}` NMR time domain
saturation recovery measurement of a highly siliceous zeolite Silicalite-I.
Usually, the spin recovery measurements are acquired over a rectilinear grid
where the grid spacing along one dimension is non-linear.

Let's load the file and look at its data structure.

.. doctest::

    >>> import csdfpy as cp

    >>> filename = '../../test-datasets0.0.9/NMR/satrec/satRec_raw.csdfe'
    >>> NMR2Ddata = cp.load(filename)
    >>> print(NMR2Ddata.data_structure)
    {
      "CSDM": {
        "version": "0.0.9",
        "independent_variables": [
          {
            "type": "linearly_sampled",
            "number_of_points": 1024,
            "sampling_interval": "8e-05 s",
            "reference_offset": "0.04104 s",
            "quantity": "time",
            "label": "$t_2$",
            "reciprocal": {
              "origin_offset": "79578822.26202029 Hz",
              "quantity": "frequency",
              "reverse": true,
              "label": "$^{29}$ frequency shift"
            }
          },
          {
            "type": "arbitrarily_sampled",
            "values": [
              "1.0 s",
              "5.0 s",
              "10.0 s",
              "20.0 s",
              "40.0 s",
              "80.0 s"
            ],
            "quantity": "time",
            "label": "$t_1$",
            "reciprocal": {
              "quantity": "frequency"
            }
          }
        ],
        "dependent_variables": [
          {
            "numeric_type": "complex64",
            "components": "[(182.26953+136.4989j), (182.26953+136.4989j), ...... (-1765.7441-375.72888j), (-1765.7441-375.72888j)]"
          }
        ]
      }
    }

The tuples of the independent and dependent variable instances from
the ``NMR2Ddata`` instance are

.. doctest::

    >>> x = NMR2Ddata.independent_variables
    >>> y = NMR2Ddata.dependent_variables

respectively.
There are two independent variable instances in this example. The coordinates
of the first independent variable, labeled as `$t_2$`, are spaced linearly
while the coordinate spacing is non-linear, or arbitrary, for the second
independent variable, labeled as `$t_1$`.
The coordinates of the two independent variables are

.. doctest::

    >>> x0 = x[0].coordinates
    >>> print(x0)
    [-0.04104 -0.04096 -0.04088 ...  0.04064  0.04072  0.0408 ] s

    >>> x1 = x[1].coordinates
    >>> print(x1)
    [ 1.  5. 10. 20. 40. 80.] s

Notice, the unit of `x0` is in seconds. Since all the values are less than one
second, it might be convenient to convert the unit to milliseconds.
Use the :py:meth:`~csdfpy.IndependentVariable.to` method of the respective
:ref:`iv_api` instance for the unit conversion. In this case,
it follows

.. doctest::

    >>> x[0].to('ms')
    >>> print(x[0].coordinates)
    [-41.04 -40.96 -40.88 ...  40.64  40.72  40.8 ] ms
    

As before, the components of the dependent variable is accessed using the
:py:attr:`~csdfpy.DependentVariable.components` attribute.

.. doctest::

    >>> y00 = y[0].components[0]
    >>> print(y00)
    [[  182.26953   +136.4989j    -530.45996   +145.59097j
       -648.56055   +296.6433j   ... -1034.6655    +123.473114j
        137.29883   +144.3381j    -151.75049    -18.316727j]
     [  -80.799805  +138.63733j   -330.4419    -131.69786j
       -356.23877   +463.6406j   ...   854.9712    +373.60577j
        432.64648   +525.6024j     -35.51758   -141.60239j ]
     [ -215.80469   +163.03308j   -330.6836    -308.8578j
      -1313.7393   -1557.9144j   ...  -979.9209    +271.06757j
       -667.6211     +61.262817j   150.32227    -41.081024j]
     [    6.2421875 -163.0319j    -654.5654    +372.27518j
      -1209.3877    -217.7103j   ...   202.91211   +910.0657j
       -163.88281   +343.41882j     27.354492   +21.467224j]
     [  -86.03516   -129.40945j   -461.1875     -74.49284j
         68.13672   -641.11975j  ...   803.3242    -423.6355j
       -267.3672    -226.39514j     77.77344    +80.2041j  ]
     [ -436.0664    -131.52814j    216.32812   +441.56696j
       -577.0254    -658.17645j  ... -1780.457     +454.20862j
      -1765.7441    -375.72888j    407.0703    +162.24716j ]]


**Plotting the dataset**

More often than not, the code required to plot the data become 
exhaustingly long. Here is one such example.

.. doctest::

    >>> import matplotlib.pyplot as plt
    >>> from matplotlib.image import NonUniformImage
    >>> import numpy as np

    >>> """ 
    ... Set the extents of the image.
    ... To set the independent variable coordinates at the center of each image
    ... pixel, subtract and add half the sampling interval from the first
    ... and the last coordinate, respectively, of the linearly sampled
    ... dimension, i.e., x0.
    ... """  # doctest: +SKIP
    >>> si=x[0].sampling_interval
    >>> extent = ((x0[0]-0.5*si).value, 
    ...           (x0[-1]+0.5*si).value, 
    ...           x1[0].value,
    ...           x1[-1].value)
    
    >>> """
    ... Create a 2x2 subplot grid. The subplot at the lower-left corner is for
    ... the image intensity plot. The subplots at the top-left and bottom-right
    ... are for the data slice at the horizontal and vertical cross-section,
    ... respectively. The subplot at the top-right corner is empty.
    ... """  # doctest: +SKIP
    >>> fig, axi = plt.subplots(2,2, gridspec_kw = {'width_ratios':[4,1], 
    ...                                             'height_ratios':[1,4]})

    >>> """
    ... The image subplot quadrant.
    ... Add an image over a rectilinear grid. Here, only the real part of the
    ... data values is used.
    ... """  # doctest: +SKIP
    >>> ax = axi[1,0]
    >>> im = NonUniformImage(ax, interpolation='nearest', 
    ...                      extent=extent, cmap='bone_r')
    >>> im.set_data(x0, x1, y00.real/y00.real.max())

    >>> """Add the colorbar and the component label."""  # doctest: +SKIP
    >>> cbar = fig.colorbar(im)
    >>> cbar.ax.set_ylabel(y[0].axis_label[0])  # doctest: +SKIP

    >>> """Set up the grid lines."""  # doctest: +SKIP
    >>> ax.images.append(im)
    >>> for i in range(x1.size):  # doctest: +SKIP
    ...     ax.plot(x0, np.ones(x0.size)*x1[i], 'k--', linewidth=0.5)  # doctest: +SKIP
    >>> ax.grid(axis='x', color='k', linestyle='--', linewidth=0.5, which='both')

    >>> """Setup the axes, add the axes labels, and the figure title."""  # doctest: +SKIP
    >>> ax.set_xlim([extent[0], extent[1]])  # doctest: +SKIP
    >>> ax.set_ylim([extent[2], extent[3]])  # doctest: +SKIP
    >>> ax.set_xlabel(x[0].axis_label)  # doctest: +SKIP
    >>> ax.set_ylabel(x[1].axis_label)  # doctest: +SKIP
    >>> ax.set_title(y[0].name)  # doctest: +SKIP

    >>> """Add the horizontal data slice to the top-left subplot."""  # doctest: +SKIP
    >>> ax0 = axi[0,0]
    >>> top = y00[-1].real
    >>> ax0.plot(x0, top, 'k', linewidth=0.5)  # doctest: +SKIP
    >>> ax0.set_xlim([extent[0], extent[1]])  # doctest: +SKIP
    >>> ax0.set_ylim([top.min(), top.max()])  # doctest: +SKIP
    >>> ax0.axis('off')  # doctest: +SKIP

    >>> """Add the vertical data slice to the bottom-right subplot."""  # doctest: +SKIP
    >>> ax1 = axi[1,1]
    >>> right = y00[:,513].real
    >>> ax1.plot(right, x1, 'k', linewidth=0.5)  # doctest: +SKIP
    >>> ax1.set_ylim([extent[2], extent[3]])  # doctest: +SKIP
    >>> ax1.set_xlim([right.min(),  right.max()])  # doctest: +SKIP
    >>> ax1.axis('off')  # doctest: +SKIP

    >>> """Turn off the axis system for the top-right subplot."""  # doctest: +SKIP
    >>> axi[0,1].axis('off')  # doctest: +SKIP

    >>> plt.tight_layout(pad=0., w_pad=0., h_pad=0.)
    >>> plt.subplots_adjust(wspace=0.025, hspace=0.05)
    >>> plt.savefig(NMR2Ddata.filename+'.pdf')
    >>> plt.show()

.. image:: /_static/satRec_raw.csdfx.pdf

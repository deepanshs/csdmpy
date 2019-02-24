
NMR dataset
^^^^^^^^^^^

The following is a :math:`(1,2)`-D NMR dataset. Start by loading the
file. ::

    >>> filename = 'test/NMR/satrec/satRec_raw.csdfx'
    >>> NMR2Ddata = cp.load(filename)
    >>> print (NMR2Ddata.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "numeric_type": "complex64",
            "components": "[(182.26953+136.4989j), (182.26953+136.4989j), ...... (-1765.7441-375.72888j), (-1765.7441-375.72888j)]"
          }
        ],
        "controlled_variables": [
          {
            "reciprocal": {
              "origin_offset": "79578822.26202029 Hz",
              "reverse": true,
              "quantity": "frequency",
              "label": "$^{29}$ frequency shift"
            },
            "number_of_points": 1024,
            "sampling_interval": "8e-05 s",
            "reference_offset": "0.04104 s",
            "quantity": "time",
            "label": "t$_2$"
          },
          {
            "reciprocal": {
              "quantity": "frequency"
            },
            "values": [
              "1.0 s",
              "5.0 s",
              "10.0 s",
              "20.0 s",
              "40.0 s",
              "80.0 s"
            ],
            "quantity": "time",
            "label": "t$_1$"
          }
        ],
        "version": "0.0.9"
      }
    }

Let's get the tuples of the controlled and uncontrolled variable objects from
the ``NMR2Ddata`` object following, ::

    >>> x = NMR2Ddata.controlled_variables
    >>> y = NMR2Ddata.uncontrolled_variables

and look at the coordinates of each variable using the
:py:attr:`~csdfpy.ControlledVariable.coordinates` attribute of the respective
objects. ::

    >>> x[0].coordinates
    [-0.04104 -0.04096 -0.04088 ...  0.04064  0.04072  0.0408 ] s

    >>> x[1].coordinates
    [ 1.  5. 10. 20. 40. 80.] s

Notice, the unit of ``x[0].coordinates`` is in second. Since all the values are
less than one second, it might be convenient to convert the unit to ms.
We use the :py:meth:`~csdfpy.ControlledVariable.to` method of the 
:ref:`cv_api` class to perform the unit conversion, which follows, ::

    >>> x[0].to('ms')
    >>> x[0].coordinates
    [-41.04 -40.96 -40.88 ...  40.64  40.72  40.8 ] ms
    

Similarly, the components of the data is accessed using the 
:py:attr:`~csdfpy.UncontrolledVariable.components` attribute. ::

    >>> y[0].components[0]
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
exhaustingly long. Here is one such example. ::

    >>> from matplotlib.image import NonUniformImage
    >>> import numpy as np

    >>> x0 = x[0].coordinates
    >>> x1 = x[1].coordinates
    >>> y00 = y[0].components[0].real
    >>> si=x[0].sampling_interval

    >>> extent = ((x0[0]-0.5*si).value, 
    ...           (x0[-1]+0.5*si).value, 
    ...           x1[0].value,
    ...           x1[-1].value)
    
    >>> fig, axi = plt.subplots(2,2, gridspec_kw = {'width_ratios':[4,1], 
    ...                                             'height_ratios':[1,4]})

    >>> ax = axi[1,0]
    >>> im = NonUniformImage(ax, interpolation='nearest',  extent=extent, cmap='gray_r')
    >>> im.set_data(x0, x1, y00/y00.max())

    >>> ax.images.append(im)
    >>> for i in range(x1.size):
    ...     ax.plot(x0, np.ones(x0.size)*x1[i], 'k--', linewidth=0.5)

    >>> ax.set_xlim([extent[0], extent[1]])
    >>> ax.set_ylim([extent[2], extent[3]])
    >>> ax.set_xlabel(x[0].axis_label)
    >>> ax.set_ylabel(x[1].axis_label)
    >>> ax.set_title(y[0].name)

    >>> ax.grid(axis='x', color='k', linestyle='--', linewidth=0.5, which='both')
    >>> ax.spines['right'].set_visible(False)
    >>> ax.spines['top'].set_visible(False)
    >>> ax.yaxis.set_ticks_position('left')
    >>> ax.xaxis.set_ticks_position('bottom')

    >>> ax0 = axi[0,0]
    >>> top = y00.sum(axis=0).real
    >>> ax0.plot(x0, top, 'k', linewidth=0.5)
    >>> ax0.set_xlim([extent[0], extent[1]])
    >>> ax0.set_ylim([top.min(), top.max()])
    >>> ax0.axis('off')

    >>> ax1 = axi[1,1]
    >>> right = y00[:,513].real
    >>> ax1.plot(right, x1, 'k', linewidth=0.5)
    >>> ax1.set_ylim([extent[2], extent[3]])
    >>> ax1.set_xlim([right.min(),  right.max()])
    >>> ax1.axis('off')
    >>> axi[0,1].axis('off')
    >>> plt.tight_layout(pad=0., w_pad=0., h_pad=0.)
    >>> plt.subplots_adjust(wspace=0.025, hspace=0.05)
    >>> plt.show()

.. image:: /resource/satRec_raw.csdfx.pdf



Astronomy dataset
^^^^^^^^^^^^^^^^^
The following dataset is a new observations of the Bubble Nebula 
acquired by
`The Hubble Heritage Team <https://archive.stsci.edu/prepds/heritage/bubble/introduction.html>`_,
in February 2016. The dataset was downloded and then converted to
the CSD model `.csdfx` format.

Let's import the `csdfx` file and take a quick look at the data structure, ::

    >>> bubble_data = cp.load('test/astronomy/source/Bubble Nebula/Bubble.csdfx')
    >>> print(bubble_data.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "name": "hlsp_heritage_hst_wfc3-uvis_bubble_nebula_f656n_v1_drc",
            "numeric_type": "float32",
            "components": "[0.0, 0.0, ...... 0.0, 0.0]"
          }
        ],
        "controlled_variables": [
          {
            "number_of_points": 11596,
            "sampling_interval": "2.279306196154649e-05 °",
            "reference_offset": "-350.04758940351087 °",
            "reverse": true,
            "quantity": "angle",
            "label": "Right Ascension"
          },
          {
            "number_of_points": 11351,
            "sampling_interval": "1.1005521846938031e-05 °",
            "reference_offset": "-61.128514949691635 °",
            "quantity": "angle",
            "label": "Declination"
          }
        ],
        "version": "0.0.9"
      }
    }

Here, the ``bubble_data`` is an instance of the :ref:`csdm_api` class.
From the data structure, one sees two control variables, labeled as
*Right Ascension* and *Declination*, and a single one-component uncontrol
variable named *hlsp_heritage_hst_wfc3-uvis_bubble_nebula_f656n_v1_drc*.
During the file conversion to the CSD model, we choose to retain the FITS
naming convension.


Let's get the tuples of the controlled and uncontrolled variable objects from
the ``bubble_data`` instance following, ::

    >>> x = bubble_data.controlled_variables
    >>> y = bubble_data.uncontrolled_variables

Because there are two controlled variable objects in ``x``, let's look at the
coordinates of each variable using the
:py:attr:`~csdfpy.ControlledVariable.coordinates` attribute of the respective
objects. ::

    >>> x[0].coordinates
    [350.31187496 350.31185216 350.31182937 ... 350.04763499 350.0476122 350.0475894 ] deg

    >>> x[1].coordinates
    [61.12851495 61.12852596 61.12853696 ... 61.25340561 61.25341662 61.25342762] deg

Notice, the descending order of coordinates along ``x[0]`` which is a
consequence of  the :py:attr:`~csdfpy.ControlledVariable.reverse` attribute set
to True for the corresponding :ref:`cv_api` object. This is also observed in
the data structure view shown above. The component of the uncontrolled variable
is accessed through the :py:attr:`~csdfpy.UncontrolledVariable.components`
attribute. ::

     >>> y00 = y[0].components[0]

Now, to plot the data, ::

    >>> fig, ax = plt.subplots(1,1,figsize=(6, 5))
    >>> extent=[x0[0].value, x0[-1].value,
    ...         x1[0].value, x1[-1].value]
    >>> im = ax.imshow(np.abs(y00), origin='lower', cmap='Greys_r',
    ...                norm=LogNorm(vmax=y00.max(), vmin=7.5e-3, clip=True),
    ...                extent=extent, aspect='auto')
    >>> ax.set_xlabel(x[0].axis_label)
    >>> ax.set_ylabel(x[1].axis_label)
    >>> ax.set_facecolor('k')
    >>> cbar = fig.colorbar(im)
    >>> cbar.ax.set_ylabel(y[0].axis_label[0])
    >>> ax.grid(color='gray', linestyle='--', linewidth=0.5)
    >>> plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    >>> plt.savefig(bubble_data.filename+'.pdf', dpi=1600)
    >>> plt.show()

.. image:: /resource/Bubble.csdfx.pdf


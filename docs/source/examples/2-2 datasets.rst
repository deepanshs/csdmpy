
------------------------
:math:`(2,2)`-D datasets
------------------------

This group of datasets has two controlled variables, as well as two
uncontrolled variables.

Vector dataset
^^^^^^^^^^^^^^

Start by importing the :guilabel:`csdfpy` package and loading the file. ::

    >>> filename = 'test/vector/electricField/electric_field_raw.csdfx'
    >>> vectordata = cp.load(filename)
    >>> print (vectordata.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "name": "Electric field lines",
            "unit": " C^-1 * N",
            "quantity": "electrical field strength",
            "numeric_type": "float32",
            "dataset_type": "vector_2",
            "components": "[3.7466873e-07, 3.7466873e-07, ...... 3.5343004e-07, 3.5343004e-07], [1.6129676e-06, 1.6129676e-06, ...... 1.846712e-06, 1.846712e-06]"
          }
        ],
        "controlled_variables": [
          {
            "reciprocal": {
              "quantity": "wavenumber"
            },
            "number_of_points": 64,
            "sampling_interval": "0.0625 cm",
            "reference_offset": "2.0 cm",
            "quantity": "length",
            "label": "x"
          },
          {
            "reciprocal": {
              "quantity": "wavenumber"
            },
            "number_of_points": 64,
            "sampling_interval": "0.0625 cm",
            "reference_offset": "2.0 cm",
            "quantity": "length",
            "label": "y"
          }
        ],
        "version": "0.0.9"
      }
    }

and the corresponding tuples of controlled and uncontrolled variable
objects. ::

    >>> x = vectordata.controlled_variables
    >>> y = vectordata.uncontrolled_variables

Let's plot the vector data. In the follwing code, we use the streamplot
from matplotlib package. This requires a initial setup before we can plot
the vector data. ::

    >>> import numpy as np

    >>> n=2
    >>> X, Y =  np.meshgrid(x[0].coordinates[::n], x[1].coordinates[::n])
    >>> U, V = y[0].components[0][::n,::n], y[0].components[1][::n,::n]
    >>> R = np.sqrt(U**2 + V**2)
    >>> lw = np.sqrt(R)
    >>> lw/=lw.max()

And now, the plot. ::

    >>> fig, ax = plt.subplots(1,1)
    >>> ax.streamplot(X.value, Y.value, U, V, density =1 , linewidth=8*lw, color=np.sqrt(lw), cmap='viridis')
    >>> ax.set_xlim([x[0].coordinates[0].value,
    ...             x[0].coordinates[-1].value])
    >>> ax.set_ylim([x[1].coordinates[0].value,
    ...             x[1].coordinates[-1].value])
    >>> ax.set_xlabel(x[0].axis_label)
    >>> ax.set_ylabel(x[1].axis_label)
    >>> ax.set_title(y[0].name)
    >>> plt.tight_layout(pad=0., w_pad=0., h_pad=0.)
    >>> plt.subplots_adjust(wspace=0.025, hspace=0.05)
    >>> plt.show()

.. image:: /resource/electric_field_raw.csdfx.pdf
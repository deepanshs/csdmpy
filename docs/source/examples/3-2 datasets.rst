

------------------------
:math:`(3,2)`-D datasets
------------------------

Image datasets
^^^^^^^^^^^^^^

In this example, we present an image dataset. An image dataset is a
`(3,2)`-D datasets with two spatial controlled variables and one
uncontrolled variable with three components. 
To load an image data file follow, ::

    >>> import csdfpy as cp
    >>>
    >>> filename = 'test/image/raccoon_raw.csdfx'
    >>> ImageData = cp.load(filename)
    >>> print (ImageData.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "name": "raccoon face",
            "component_labels": [
              "red",
              "green",
              "blue"
            ],
            "encoding": "raw",
            "numeric_type": "uint8",
            "dataset_type": "RGB",
            "components_URI": "file:./raccoon_raw.dat"
          }
        ],
        "controlled_variables": [
          {
            "number_of_points": 1024,
            "sampling_interval": "1.0 "
          },
          {
            "number_of_points": 768,
            "sampling_interval": "1.0 "
          }
        ],
        "version": "0.0.9"
      }
    }

Here, ``ImageData`` is an instance of the :ref:`CSDModel <csdm_api>` class. 
As before, to access the uncontrolled and controlled variables, follow ::

    >>> x = ImageData.controlled_variables
    >>> y = ImageData.uncontrolled_variables

Since there are two controlled variables, to access the coordinates
along the each dimensions, use the respective ``coordinates``
attribute. Here, we illustrate this by printing the first ten coordinates
along both controlled variables. ::

    >>> print('x0 =', x[0].coordinates[:10])
    >>> print('x1 =', x[1].coordinates[:10])
    x0 = [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]
    x1 = [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]

To access the three components of the uncontrolled variable components,
use the ``components`` attribute. As an example, we print the shape of
each component array for the three components, along with their
respective labels. ::

    >>> print (y[0].component_labels[0], y[0].components[0].shape)
    >>> print (y[0].component_labels[1], y[0].components[1].shape)
    >>> print (y[0].component_labels[2], y[0].components[2].shape)
    red (768, 1024)
    green (768, 1024)
    blue (768, 1024)

.. note::
        In this example, we do not increment the index of `y`. The
        indices of y span through the uncontrolled variables. Since
        we only have one uncontrolled variable, the index of `y`, that
        is ``y[0]``, is set to zero. The indices for the
        ``components`` and ``component_label`` span through the number of
        components and are, therefore, incremented.

Now, to plot the dataset. ::

    >>> import matplotlib.pyplot as plt
    >>> import numpy as np

    >>> fig, ax = plt.subplots(1,1)
    >>> ax.imshow(np.moveaxis(y[0].components, 0, -1 ))
    >>> ax.set_axis_off()
    >>> plt.tight_layout(pad=0., w_pad=0., h_pad=0.)
    >>> plt.subplots_adjust(wspace=0.025, hspace=0.05, left=0., right=1, top=1, bottom=0)
    >>> plt.savefig(ImageData.filename+'.pdf')
    >>> plt.show()

.. image:: /resource/raccoon_raw.csdfx.pdf
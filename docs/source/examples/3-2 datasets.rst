

----------------
(3,2)-D datasets
----------------

The following subset of datasets has two control variables, :math:`d=2` and
one three-component uncontrol variable, :math:`p_0=3`.

Image datasets
^^^^^^^^^^^^^^

A common example from this subset is perhaps the RGB image dataset.
An image dataset has two spatially controlled variables and one uncontrolled
variable with three components corresponding to the red, green, and blue color
intensities.
 
Take a look at an example data structure of an image data file.

.. doctest::

    >>> import csdfpy as cp
    >>>
    >>> filename = '../../test-datasets/image/raccoon_raw.csdfx'
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
            "numeric_type": "uint8",
            "dataset_type": "RGB",
            "components": "[121, 121, ...... 119, 119], [112, 112, ...... 155, 155], [131, 131, ...... 93, 93]"
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
As before, to access the uncontrolled and controlled variables, follow

.. doctest::

    >>> x = ImageData.controlled_variables
    >>> y = ImageData.uncontrolled_variables

Since there are two controlled variables, to access the coordinates
along each control variable, use the respective
:py:attr:`~csdfpy.ControlledVariable.coordinates`
attribute. Here, only the first ten coordinates
along each control variable are displayed.

.. doctest::

    >>> print('x0 =', x[0].coordinates[:10])
    x0 = [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]

    >>> print('x1 =', x[1].coordinates[:10])
    x1 = [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]

To access the three components of the uncontrolled variable,
use the :py:attr:`~csdfpy.UncontrolledVariable.components` attribute.
As an example, we print the shape of
each component array for the three components, along with their
respective labels.

.. doctest::

    >>> print (y[0].component_labels[0], y[0].components[0].shape)
    red (768, 1024)

    >>> print (y[0].component_labels[1], y[0].components[1].shape)
    green (768, 1024)

    >>> print (y[0].component_labels[2], y[0].components[2].shape)
    blue (768, 1024)

.. note::
        In this example, we do not increase the index of `y` because the
        indices of y span through the uncontrolled variables. Since
        there is only one uncontrolled variable, the index of `y`, that
        is ``y[0]``, is set to zero. The indices for the
        :py:attr:`~csdfpy.UncontrolledVariable.components` and the
        :py:attr:`~csdfpy.UncontrolledVariable.component_labels`,
        on the other hand, span through the number of components.

Now, to visualize the dataset.

.. doctest::

    >>> import matplotlib.pyplot as plt
    >>> import numpy as np

    >>> fig, ax = plt.subplots(1,1)
    >>> ax.imshow(np.moveaxis(y[0].components, 0, -1 ))  # doctest: +SKIP
    >>> ax.set_axis_off()  # doctest: +SKIP
    >>> plt.tight_layout(pad=0., w_pad=0., h_pad=0.)
    >>> plt.subplots_adjust(wspace=0.025, hspace=0.05, left=0., right=1, top=1, bottom=0)
    >>> plt.savefig(ImageData.filename+'.pdf')
    >>> plt.show()

.. image:: /_static/raccoon_raw.csdfx.pdf


--------------
2D{3} datasets
--------------

The 2D{3} datasets have two independent variables, :math:`d=2` and
one three-component dependent variable, :math:`p=3`.

Image datasets
^^^^^^^^^^^^^^

A common example from this subset is perhaps the RGB image dataset.
An image dataset has two spatially independent variables and one dependent
variable with three components corresponding to the red, green, and blue color
intensities.
 
The following is an example of the RGB image dataset.

.. doctest::

    >>> import csdfpy as cp

    >>> filename = '../../test-datasets0.0.9/image/raccoon_raw.csdfe'
    >>> ImageData = cp.load(filename)
    >>> print (ImageData.data_structure)
    {
      "CSDM": {
        "version": "0.0.9",
        "independent_variables": [
          {
            "type": "linearly_sampled",
            "number_of_points": 1024,
            "sampling_interval": "1.0 "
          },
          {
            "type": "linearly_sampled",
            "number_of_points": 768,
            "sampling_interval": "1.0 "
          }
        ],
        "dependent_variables": [
          {
            "name": "raccoon face",
            "numeric_type": "uint8",
            "quantity_type": "RGB",
            "component_labels": [
              "red",
              "green",
              "blue"
            ],
            "components": "[121, 121, ...... 119, 119], [112, 112, ...... 155, 155], [131, 131, ...... 93, 93]"
          }
        ]
      }
    }

The tuples of the independent and dependent variable instances from
``ImageData`` instance are

.. doctest::

    >>> x = ImageData.independent_variables
    >>> y = ImageData.dependent_variables

resepctively.
Since there are two independent variables, the coordinates
along each independent variable are

.. doctest::

    >>> print('x0 =', x[0].coordinates[:10])
    x0 = [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]

    >>> print('x1 =', x[1].coordinates[:10])
    x1 = [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]

respectively, where both independent variable coordinates are spaced linearly.
In the above expression, only the first ten coordinates along each
independent variable are displayed.

The dependent variable is an RGB image as also seen from the
:attr:`~csdfpy.DependentVariable.quantity_type` attribute of the corresponding
:ref:`dv_api` instance.

.. doctest::

    >>> print(y[0].quantity_type)
    RGB

As usual, the components of the dependent variable are accessed through
the :attr:`~csdfpy.DependentVariable.components` attribute.
To access the individual components use the appropriate array indexing.
For example,

.. doctest::

    >>> print (y[0].components[0])
    [[121 138 153 ... 119 131 139]
     [ 89 110 130 ... 118 134 146]
     [ 73  94 115 ... 117 133 144]
     ...
     [ 87  94 107 ... 120 119 119]
     [ 85  95 112 ... 121 120 120]
     [ 85  97 111 ... 120 119 118]]

will return an array with the first component of all data values. Here, these
components correspond to the red color intensity. The label corresponding to
this component array is accessed through the
:attr:`~csdfpy.DependentVariable.component_labels` attrbibute with appropriate
indexing, that is

.. doctest::

    >>> print (y[0].component_labels[0])
    red

To avoid displaying larger output, as an example, we print the shape of
each component array (using Numpy array's `shape` attribute) for the three
components along with their respective labels.

.. doctest::

    >>> print (y[0].component_labels[0], y[0].components[0].shape)
    red (768, 1024)

    >>> print (y[0].component_labels[1], y[0].components[1].shape)
    green (768, 1024)

    >>> print (y[0].component_labels[2], y[0].components[2].shape)
    blue (768, 1024)

The shape (768, 1024) corresponds to the number of points from the list of the
independent variable instances.

.. note::
        In this example, we do not increase the index of `y` because the
        indices of y span through the dependent variables. Since
        there is only one dependent variable, the index of `y`, that
        is ``y[0]``, is set to zero. The indices for the
        :py:attr:`~csdfpy.DependentVariable.components` and the
        :py:attr:`~csdfpy.DependentVariable.component_labels`,
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

.. image:: /_static/raccoon_raw.csdfx.png

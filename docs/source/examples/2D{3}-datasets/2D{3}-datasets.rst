

--------------
2D{3} datasets
--------------

The 2D{3} datasets is two dimensional, :math:`d=2`, with
a single three-component dependent variable, :math:`p=3`.

Image datasets
^^^^^^^^^^^^^^

A common example from this subset is perhaps the RGB image dataset.
An image dataset has two spatial dimensions and one dependent
variable with three components corresponding to the red, green, and blue color
intensities.

The following is an example of the RGB image dataset.

.. doctest::

    >>> import csdmpy as cp

    >>> filename = '../test-datasets0.0.12/image/raccoon_raw.csdfe'
    >>> ImageData = cp.load(filename)
    >>> print (ImageData.data_structure)
    {
      "csdm": {
        "version": "0.0.12",
        "description": "An RBG image of a raccoon face.",
        "dimensions": [
          {
            "type": "linear",
            "count": 1024,
            "increment": "1.0"
          },
          {
            "type": "linear",
            "count": 768,
            "increment": "1.0"
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "name": "raccoon face",
            "numeric_type": "uint8",
            "quantity_type": "pixel_3",
            "component_labels": [
              "red",
              "green",
              "blue"
            ],
            "components": [
              [
                "121, 138, ..., 119, 118"
              ],
              [
                "112, 129, ..., 155, 154"
              ],
              [
                "131, 148, ..., 93, 92"
              ]
            ]
          }
        ]
      }
    }

The tuples of the dimension and dependent variable instances from
``ImageData`` instance are

.. doctest::

    >>> x = ImageData.dimensions
    >>> y = ImageData.dependent_variables

respectively.
Since there are two dimensions, the coordinates along each dimension are

.. doctest::

    >>> print('x0 =', x[0].coordinates[:10])
    x0 = [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]

    >>> print('x1 =', x[1].coordinates[:10])
    x1 = [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]

respectively, where coordinates along both dimensions are spaced uniformly.
In the above example, only the first ten coordinates along each dimension
are displayed.

The dependent variable is an RGB image as also seen from the
:attr:`~csdmpy.dependent_variables.DependentVariable.quantity_type` attribute
of the corresponding :ref:`dv_api` instance.

.. doctest::

    >>> print(y[0].quantity_type)
    pixel_3

As usual, the components of the dependent variable are accessed through
the :attr:`~csdmpy.dependent_variables.DependentVariable.components` attribute.
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
:attr:`~csdmpy.dependent_variables.DependentVariable.component_labels`
attribute with appropriate indexing, that is

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

The shape (768, 1024) corresponds to the number of points from the each
dimension instances.

.. note::
        In this example, since there is only one dependent variable, the index
        of `y` is set to zero, that is ``y[0]``. We do not increase the index
        of `y`.  The indices for the
        :attr:`~csdmpy.dependent_variables.DependentVariable.components` and the
        :attr:`~csdmpy.dependent_variables.DependentVariable.component_labels`,
        on the other hand, span through the number of components and are
        incremented.

Now, to visualize the dataset.

.. doctest::

    >>> import matplotlib.pyplot as plt
    >>> import numpy as np

    >>> def image_data():
    ...     fig, ax = plt.subplots(1,1)
    ...     ax.imshow(np.moveaxis(y[0].components, 0, -1 ))
    ...     ax.set_axis_off()
    ...     plt.tight_layout()
    ...     plt.show()

    >>> image_data()

.. figure:: raccoon_raw.png
   :align: center

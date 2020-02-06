# -*- coding: utf-8 -*-
"""
Image, 2D{3} datasets
^^^^^^^^^^^^^^^^^^^^^
"""
#%%
# The 2D{3} dataset is two dimensional, :math:`d=2`, with
# a single three-component dependent variable, :math:`p=3`.
# A common example from this subset is perhaps the RGB image dataset.
# An RGB image dataset has two spatial dimensions and one dependent
# variable with three components corresponding to the red, green, and blue color
# intensities.
#
# The following is an example of an RGB image dataset.
import csdmpy as cp

filename = "https://osu.box.com/shared/static/vdxdaitsa9dq45x8nk7l7h25qrw2baxt.csdf"
ImageData = cp.load(filename)
print(ImageData.data_structure)

#%%
# The tuple of the dimension and dependent variable instances from
# ``ImageData`` instance are

x = ImageData.dimensions
y = ImageData.dependent_variables

#%%
# respectively. There are two dimensions, and the coordinates along each
# dimension are

print("x0 =", x[0].coordinates[:10])

#%%
print("x1 =", x[1].coordinates[:10])

#%%
# respectively, where only first ten coordinates along each dimension is displayed.

#%%
# The dependent variable is the image data, as also seen from the
# :attr:`~csdmpy.DependentVariable.quantity_type` attribute
# of the corresponding :ref:`dv_api` instance.

print(y[0].quantity_type)

#%%
# From the value `pixel_3`, `pixel` indicates a pixel data, while `3`
# indicates the number of pixel components.

#%%
# As usual, the components of the dependent variable are accessed through
# the :attr:`~csdmpy.DependentVariable.components` attribute.
# To access the individual components, use the appropriate array indexing.
# For example,

print(y[0].components[0])

#%%
# will return an array with the first component of all data values. In this case,
# the components correspond to the red color intensity, also indicated by the
# corresponding component label. The label corresponding to
# the component array is accessed through the
# :attr:`~csdmpy.DependentVariable.component_labels`
# attribute with appropriate indexing, that is

print(y[0].component_labels[0])

#%%
# To avoid displaying larger output, as an example, we print the shape of
# each component array (using Numpy array's `shape` attribute) for the three
# components along with their respective labels.

#%%
print(y[0].component_labels[0], y[0].components[0].shape)

#%%
print(y[0].component_labels[1], y[0].components[1].shape)

#%%
print(y[0].component_labels[2], y[0].components[2].shape)

#%%
# The shape (768, 1024) corresponds to the number of points from the each
# dimension instances.

#%%
# .. note::
#         In this example, since there is only one dependent variable, the index
#         of `y` is set to zero, which is ``y[0]``. The indices for the
#         :attr:`~csdmpy.DependentVariable.components` and the
#         :attr:`~csdmpy.DependentVariable.component_labels`,
#         on the other hand, spans through the number of components.

#%%
# Now, to visualize the dataset as an RGB image,

import matplotlib.pyplot as plt
import numpy as np

plt.imshow(np.moveaxis(y[0].components, 0, -1))
plt.xlabel(x[0].axis_label)
plt.ylabel(x[1].axis_label)
plt.tight_layout()
plt.show()

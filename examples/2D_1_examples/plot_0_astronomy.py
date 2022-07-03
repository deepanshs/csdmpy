# -*- coding: utf-8 -*-
"""
Astronomy dataset
^^^^^^^^^^^^^^^^^
"""
# %%
# The following dataset is a new observation of the Bubble Nebula
# acquired by `The Hubble Heritage Team
# <https://archive.stsci.edu/prepds/heritage/bubble/introduction.html>`_,
# in February 2016. The original dataset was obtained in the FITS format
# and subsequently converted to the CSD model file-format. For the convenience of
# illustration, we have downsampled the original dataset.
#
# Let's load the `.csdfe` file and look at its data structure.
import matplotlib.pyplot as plt

import csdmpy as cp

domain = "https://www.ssnmr.org/sites/default/files/CSDM"
filename = f"{domain}/BubbleNebula/Bubble_nebula.csdf"
bubble_nebula = cp.load(filename)
print(bubble_nebula.data_structure)

# %%
# Here, the variable ``bubble_nebula`` is an instance of the :ref:`csdm_api`
# class. From the data structure, one finds two dimensions, labeled as
# *Right Ascension* and *Declination*, and one single-component dependent
# variable named *Bubble Nebula, 656nm*.

# %%
# Let's get the tuple of the dimension and dependent variable instances from
# the ``bubble_nebula`` instance following,
x = bubble_nebula.dimensions
y = bubble_nebula.dependent_variables

# %%
# There are two dimension instances in ``x``. Let's look
# at the coordinates along each dimension, using the
# :attr:`~csdmpy.Dimension.coordinates` attribute of the
# respective instances.

# %%
print(x[0].coordinates[:10])

# %%
print(x[1].coordinates[:10])

# %%
# Here, we only print the first ten coordinates along the respective dimensions.

# %%
# The component of the dependent variable is accessed through the
# :attr:`~csdmpy.DependentVariable.components` attribute.
y00 = y[0].components[0]

# %%
# **Visualize the dataset**
from matplotlib.colors import LogNorm

plt.figure(figsize=(6, 4.5))
ax = plt.subplot(projection="csdm")
ax.imshow(bubble_nebula, norm=LogNorm(vmin=7.5e-3, clip=True), aspect="auto")
plt.tight_layout()
plt.show()

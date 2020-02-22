# -*- coding: utf-8 -*-
"""
Vector, 2D{2} dataset
^^^^^^^^^^^^^^^^^^^^^
"""
#%%
# The 2D{2} datasets are two-dimensional, :math:`d=2`,
# with one two-component dependent variable, :math:`p=2`.
# The following is an example of a simulated electric field vector dataset of a
# dipole as a function of two linearly sampled spatial dimensions.
import csdmpy as cp

filename = "https://osu.box.com/shared/static/iobasl6fx1z7rds3ovamrwueek8ver5o.csdf"
vector_data = cp.load(filename)
print(vector_data.data_structure)

#%%
# The tuple of the dimension and dependent variable instances from this example
# are

x = vector_data.dimensions
y = vector_data.dependent_variables

#%%
# with the respective coordinates (viewed only up to five values), as

print(x[0].coordinates[:5])

#%%
print(x[1].coordinates[:5])

#%%
# The components of the dependent variable are vector components as seen
# from the :attr:`~csdmpy.DependentVariable.quantity_type`
# attribute of the corresponding dependent variable instance.

print(y[0].quantity_type)

#%%
# **Visualizing the dataset**
#
# Let's visualize the vector data using the *streamplot* method
# from the matplotlib package. Before we could visualize, however, there
# is an initial processing step. We use the Numpy library for processing.

import numpy as np

X, Y = np.meshgrid(x[0].coordinates, x[1].coordinates)  # (x, y) coordinate pairs
U, V = y[0].components[0], y[0].components[1]  # U and V are the components
R = np.sqrt(U ** 2 + V ** 2)  # The magnitude of the vector
R /= R.min()  # Scaled magnitude of the vector
Rlog = np.log10(R)  # Scaled magnitude of the vector on a log scale

#%%
# In the above steps, we calculate the X-Y grid points along with a
# scaled magnitude of the vector dataset. The magnitude is scaled such that the
# minimum value is one. Next, calculate the log of the scaled magnitude to
# visualize the intensity on a logarithmic scale.

#%%
# And now, the streamplot vector plot

import matplotlib.pyplot as plt

plt.streamplot(
    X.value, Y.value, U, V, density=1, linewidth=Rlog, color=Rlog, cmap="viridis"
)

plt.xlim([x[0].coordinates[0].value, x[0].coordinates[-1].value])
plt.ylim([x[1].coordinates[0].value, x[1].coordinates[-1].value])

# Set axes labels and figure title.
plt.xlabel(x[0].axis_label)
plt.ylabel(x[1].axis_label)
plt.title(y[0].name)

# Set grid lines.
plt.grid(color="gray", linestyle="--", linewidth=0.5)

plt.tight_layout()
plt.show()

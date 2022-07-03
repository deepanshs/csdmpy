# -*- coding: utf-8 -*-
"""
Vector, 1D{2} dataset
---------------------
"""
# %%
# The 1D{2} datasets are one-dimensional, :math:`d=1`, with two-component
# dependent variable, :math:`p=2`. Such datasets are more common with the
# weather forecast, such as the wind velocity predicting at a location
# as a function of time.
#
# The following is an example of a simulated 1D vector field dataset.
import matplotlib.pyplot as plt

import csdmpy as cp

filename = "https://www.ssnmr.org/sites/default/files/CSDM/vector/1D_vector.csdf"
vector_data = cp.load(filename)
print(vector_data.data_structure)

# %%
# The tuple of the dimension and dependent variable instances from this example
# are
x = vector_data.dimensions
y = vector_data.dependent_variables

# %%
# with coordinates
print(x[0].coordinates)

# %%
# In this example, the components of the dependent variable are
# vectors as seen from the
# :attr:`~csdmpy.DependentVariable.quantity_type`
# attribute of the corresponding dependent variable instance.
print(y[0].quantity_type)

# %%
# From the value `vector_2`, `vector` indicates a vector dataset, while `2`
# indicates the number of vector components.

# %%
# **Visualizing the dataset**

plt.figure(figsize=(5, 3.5))
cp.plot(vector_data)
plt.tight_layout()
plt.show()

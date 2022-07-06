"""
1D{1,1} datasets
----------------
"""
# %%
# In the following example, we illustrate how one can covert a Numpy array into
# a CSDM object. Start by importing the Numpy and csdmpy libraries.
import matplotlib.pyplot as plt
import numpy as np

import csdmpy as cp

# %%
# Let's generate two 1D NumPy arrays as the dependent variables of as our dataset.
test_data1 = np.zeros(500)
test_data1[250] = 1

test_data2 = np.zeros(500)
test_data2[150] = 1

# %%
# Create the two DependentVariable objects from the numpy objects.
dv1 = cp.as_dependent_variable(test_data1, unit="%")
dv2 = cp.as_dependent_variable(test_data2, unit="J")

# %%
# Create the corresponding dimension object. Here, we create a LinearDimension object.
dim = cp.LinearDimension(count=500, increment="43 cm", coordinates_offset="-0.1 km")

# %%
# Creating the CSDM object.
csdm_object = cp.CSDM(dependent_variables=[dv1, dv2], dimensions=[dim])

# %%
# Plot of the dataset.
plt.figure(figsize=(5, 3.5))
ax = plt.subplot(projection="csdm")
ax.plot(csdm_object)
plt.tight_layout()
plt.show()

# %%
# To serialize the file, use the save method.
csdm_object.save("1D_11_dataset.csdf")

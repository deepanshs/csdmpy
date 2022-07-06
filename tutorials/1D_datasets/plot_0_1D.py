"""
1D{1} datasets
--------------
"""
# %%
# In the following example, we illustrate how one can covert a Numpy array into
# a CSDM object. Start by importing the Numpy and csdmpy libraries.
import matplotlib.pyplot as plt
import numpy as np

import csdmpy as cp

# %%
# Let's generate a 1D NumPy array of as our dataset.
test_data = np.zeros(500)
test_data[250] = 1

# %%
# Create a DependentVariable object from the numpy object
dv = cp.as_dependent_variable(test_data, unit="%")

# %%
# Create the corresponding dimensions object. Here, we create a LinearDimension object
dim = cp.LinearDimension(count=500, increment="1 m")

# %%
# Creating the CSDM object.
csdm_object = cp.CSDM(dependent_variables=[dv], dimensions=[dim])

# %%
# Plot of the dataset.
plt.figure(figsize=(5, 3.5))
ax = plt.subplot(projection="csdm")
ax.plot(csdm_object)
plt.tight_layout()
plt.show()

# %%
# To serialize the file, use the save method.
csdm_object.save("1D_1_dataset.csdf")

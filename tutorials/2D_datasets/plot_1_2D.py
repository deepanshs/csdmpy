"""
2D{1} dataset with linear and monotonic dimensions
--------------------------------------------------
"""
# %%
# In the following example, we illustrate how one can covert a Numpy array into
# a CSDM object. Start by importing the Numpy and csdmpy libraries.
import matplotlib.pyplot as plt
import numpy as np

import csdmpy as cp

# %%
# Let's generate a 2D NumPy array of random numbers as our dataset.
data = np.random.rand(8192).reshape(32, 256)


# %%
# Create the DependentVariable object from the numpy object.
dv = cp.as_dependent_variable(data, unit="J/(mol K)")

# %%
# Create the two Dimension objects.
d0 = cp.LinearDimension(
    count=256, increment="15.23 µs", coordinates_offset="-1.95 ms", label="t1"
)

# %%
# Here, ``d0`` is a LinearDimension with 256 points and 15.23 µs increment. You
# may similarly set the second dimension as a LinearDimension, however, in this
# example, let's set it as a MonotonicDimension.
#
array = 10 ** (np.arange(32) / 8)
d1 = cp.as_dimension(array, unit="µs", label="t2")

# %%
# The variable ``array`` is a NumPy array that is uniformly sampled on a log
# scale. To convert this array into a Dimension object, we use the
# :meth:`~csdmpy.as_dimension` method.
#
# Creating the CSDM object.
csdm_object = cp.CSDM(dependent_variables=[dv], dimensions=[d0, d1])
print(csdm_object.dimensions)

# %%
# Plot of the dataset.
plt.figure(figsize=(5, 3.5))
cp.plot(csdm_object)
plt.tight_layout()
plt.show()

# %%
# To serialize the file, use the save method.
csdm_object.save("2D_1_dataset.csdf")

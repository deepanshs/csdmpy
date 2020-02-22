# -*- coding: utf-8 -*-
"""
Linear and Monotonic dimensions
-------------------------------
"""
#%%
# In the following example, we illustrate how one can covert a Numpy array into
# a CSDM object. Start by importing the Numpy and csdmpy libraries.
import numpy as np

import csdmpy as cp

#%%
# Let's generate a 2D NumPy array of random numbers as our dataset.
data = np.random.rand(8192).reshape(32, 256)

#%%
# To convert this array into a csdm object, use the :meth:`~csdmpy.as_csdm`
# method,
data_csdm = cp.as_csdm(data)
print(data_csdm.dimensions)

#%%
# This generates a 2D{1} dataset, that is, a two-dimensional dataset with a
# single one-component dependent variable. The two dimensions are, by default,
# set as the LinearDimensions of the unit interval.
#
# You may set the proper dimensions by generating the appropriate Dimension
# objects and replacing the default dimensions in the ``data_csdm`` object.
d0 = cp.LinearDimension(
    count=256, increment="15.23 µs", coordinates_offset="-1.95 ms", label="t1"
)

#%%
# Here, ``d0`` is a LinearDimension with 256 points and 15.23 µs increment. You
# may similarly set the second dimension as a LinearDimension, however, in this
# example, let's set it as a MonotonicDimension.
#
array = 10 ** (np.arange(32) / 8)
d1 = cp.as_dimension(array, unit="µs", label="t2")

#%%
# The variable ``array`` is a NumPy array that is uniformly sampled on a log
# scale. To convert this array into a Dimension object, we use the
# :meth:`~csdmpy.as_dimension` method.
#
# Now, replace the dimension objects in ``data_csdm`` with the new ones.
data_csdm.dimensions[0] = d0
data_csdm.dimensions[1] = d1

#%%
print(data_csdm.dimensions)

#%%
# Plot of the dataset.
cp.plot(data_csdm)

#%%
# To serialize the file, use the save method.
data_csdm.save("filename.csdf")

# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

import csdmpy as cp

# Create a test 1D{1} dataset. ================================================
# Step-1: Create a new csdm object
csdm = cp.new()

# Step-2: Create dimension objects and add it to the CSDM object.
x = cp.as_dimension(np.arange(10) * 0.1 + 15, unit="s", label="t1")
csdm.add_dimension(x)

# Step-3: Create dependent variable objects and add it to the CSDM object.
y = cp.as_dependent_variable(np.random.rand(10), unit="cm", name="test-0")
csdm.add_dependent_variable(y)


# Plot ========================================================================
plt.figure(figsize=(5, 3.5))
# create the axes with `projection="csdm"`
ax = plt.subplot(projection="csdm")
# use matplotlib plot function with csdm object.
ax.plot(csdm)
plt.tight_layout()
plt.show()


# Scatter =====================================================================
plt.figure(figsize=(5, 3.5))
# create the axes with `projection="csdm"`
ax = plt.subplot(projection="csdm")
# use matplotlib plot function with csdm object.
ax.scatter(csdm, marker="x", color="red")
plt.tight_layout()
plt.show()

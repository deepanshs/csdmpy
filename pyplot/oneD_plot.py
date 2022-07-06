import matplotlib.pyplot as plt
import numpy as np

import csdmpy as cp

# Create a test 1D{1} dataset. ================================================

# Step-1: Create dimension objects.
x = cp.as_dimension(np.arange(10) * 0.1 + 15, unit="s", label="t1")

# Step-2: Create dependent variable objects.
y = cp.as_dependent_variable(np.random.rand(10), unit="cm", name="test-0")

# Step-3: Create the CSDM object with Dimension and Dependent variable objects.
csdm = cp.CSDM(dimensions=[x], dependent_variables=[y])


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

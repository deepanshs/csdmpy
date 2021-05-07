# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

import csdmpy as cp

# Create a test 2D{1} dataset. ================================================

# Step-1: Create dimension objects.
x1 = cp.as_dimension(np.arange(10) * 0.1 + 15, unit="s", label="t1")
x2 = cp.as_dimension(np.arange(10) * 12.5, unit="s", label="t2")

# Step-2: Create dependent variable objects.
y = cp.as_dependent_variable(np.diag(np.ones(10)), name="body-diagonal")

# Step-3: Create the CSDM object with Dimension and Dependent variable objects.
csdm = cp.CSDM(dimensions=[x1, x2], dependent_variables=[y])

# Plot imshow =================================================================
plt.figure(figsize=(5, 3.5))
# create the axes with `projection="csdm"`
ax = plt.subplot(projection="csdm")
# use matplotlib imshow function with csdm object.
ax.imshow(csdm, origin="upper", aspect="auto")
plt.tight_layout()
plt.show()

# Plot contour ================================================================
plt.figure(figsize=(5, 3.5))
# create the axes with `projection="csdm"`
ax = plt.subplot(projection="csdm")
# use matplotlib contour function with csdm object.
ax.contour(csdm)
plt.tight_layout()
plt.show()

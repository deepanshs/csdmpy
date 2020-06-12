# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

import csdmpy as cp

# Create a test 2D{1} dataset. ================================================
# Step-1: Create a new csdm object
csdm = cp.new()

# Step-2: Create dimension objects and add it to the CSDM object.
x1 = cp.as_dimension(np.arange(10) * 0.1 + 15, unit="s", label="t1")
csdm.add_dimension(x1)
x2 = cp.as_dimension(np.arange(10) * 12.5, unit="s", label="t2")
csdm.add_dimension(x2)

# Step-3: Create dependent variable objects and add it to the CSDM object.
y = cp.as_dependent_variable(np.diag(np.ones(10)), name="body-diagonal")
csdm.add_dependent_variable(y)
y = cp.as_dependent_variable(np.diag(np.ones(5), 5), name="off-body-diagonal")
csdm.add_dependent_variable(y)


# Plot imshow =================================================================
plt.figure(figsize=(5, 3.5))
# create the axes with `projection="csdm"`
ax = plt.subplot(projection="csdm")
# use matplotlib imshow function with csdm object.
ax.imshow(csdm, origin="upper", aspect="auto", cmaps=["Blues", "Reds"], alpha=0.5)
plt.tight_layout()
plt.show()


# Plot contourf ===============================================================
plt.figure(figsize=(5, 3.5))
# create the axes with `projection="csdm"`
ax = plt.subplot(projection="csdm")
# use matplotlib contourf function with csdm object.
ax.contourf(csdm, cmaps=["Blues", "Reds"], alpha=0.5)
plt.tight_layout()
plt.show()

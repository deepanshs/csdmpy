# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

import csdmpy as cp

# Create a test 1D{1, 1, 1, 1, 1} dataset. ====================================

# Step-1: Create a new csdm object
csdm = cp.new()

# %%
# Step-2: Create dimension objects and add it to the CSDM object.
x = cp.as_dimension(np.arange(40) * 0.5 - 10, unit="µm", label="x")
csdm.add_dimension(x)

# %%
# Step-3: Create dependent variable objects and add it to the CSDM object.
units = ["cm", "s", "m/s", ""]
for i in range(4):
    y = cp.as_dependent_variable(
        np.random.rand(40) + 10, unit=units[i], name=f"test-{i}"
    )
    csdm.add_dependent_variable(y)


# The plot on same axes =======================================================
plt.figure(figsize=(6, 4))
# create the ax with `projection="csdm"``
ax = plt.subplot(projection="csdm")
# use matplotlib plot function with csdm object.
ax.plot(csdm)
plt.title("Data plotted on the same figure")
plt.tight_layout()
plt.show()


# The plot on separate axes ===================================================

# Split the CSDM object into multiple single dependent-variable CSDM objects.
sub_type = csdm.split()

# create the axes with `projection="csdm"``
_, ax = plt.subplots(2, 2, figsize=(8, 6), subplot_kw={"projection": "csdm"})
# now use matplotlib plot function with csdm object.
ax[0, 0].plot(sub_type[0])
ax[0, 1].plot(sub_type[1])
ax[1, 0].plot(sub_type[2])
ax[1, 1].plot(sub_type[3])
plt.title("Data plotted separately")
plt.tight_layout()
plt.show()

# -*- coding: utf-8 -*-
"""
Sparse along two dimensions, 2D{1,1} dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
# %%
# The following is an example [#f2]_ of a 2D{1,1} sparse dataset with two-dimensions,
# :math:`d=2`, and two, :math:`p=2`, sparse single-component dependent-variables,
# where the component is sparsely sampled along two dimensions. The following is an
# example of a hypercomplex acquisition of the NMR dataset.
#
# Let's import the CSD model data-file and look at its data structure.
import csdmpy as cp

filename = "https://www.ssnmr.org/sites/default/files/CSDM/sparse/iglu_2d.csdf"
sparse_2d = cp.load(filename)

# %%
# There are two linear dimensions and two single-component sparse dependent variables.
# The tuple of the dimension and the dependent variable instances are
x = sparse_2d.dimensions
y = sparse_2d.dependent_variables

# %%
# The coordinates, viewed only for the first ten coordinates, are
print(x[0].coordinates[:10])

# %%
print(x[1].coordinates[:10])

# %%
# Converting the coordinates to `ms`.
x[0].to("ms")
x[1].to("ms")

# %%
# **Visualize the dataset**
import matplotlib.pyplot as plt

# split the CSDM object with two dependent variables into two CSDM objects with single
# dependent variables.

cos, sin = sparse_2d.split()

# cosine data
plt.figure(figsize=(5, 3.5))
ax = plt.subplot(projection="csdm")
cb = ax.contourf(cos.real)
plt.colorbar(cb, ax=ax)
plt.tight_layout()
plt.show()

# %%

# sine data
plt.figure(figsize=(5, 3.5))
ax = plt.subplot(projection="csdm")
cb = ax.contourf(sin.real)
plt.colorbar(cb, ax=ax)
plt.tight_layout()
plt.show()

# %%
# .. rubric:: Citation
#
# .. [#f2] Balsgart NM, Vosegaard T., Fast Forward Maximum entropy reconstruction
#          of sparsely sampled data., J Magn Reson. 2012, 223, 164-169.
#          doi: 10.1016/j.jmr.2012.07.002

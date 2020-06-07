# -*- coding: utf-8 -*-
"""
Diffusion tensor MRI, 3D{6} dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
# %%
# The following is an example of a 3D{6} diffusion tensor MRI dataset with three
# spatial dimensions, :math:`d=3`, and one, :math:`p=1`, dependent-variable
# with six components. For illustration, we have reduced the size of the dataset.
# The complete diffusion tensor MRI dataset, in the CSDM format, is available
# `online <https://osu.box.com/shared/static/i7pwedo7sjabzr9qfn5q2gnjffqabp0p.csdf>`_.
# The original dataset [#f1]_ is also available.
#
# Let's import the CSDM data-file and look at its data structure.
import csdmpy as cp

filename = "https://osu.box.com/shared/static/x5d1hgqjgo01wguyzwbv6e256erxejtx.csdf"
diff_mri = cp.load(filename)

# %%
# There are three linear dimensions in this dataset, corresponding to the x, y, and z
# spatial dimensions,
x = diff_mri.dimensions
print(x[0].label, x[1].label, x[2].label)

# %%
# and one six-component dependent variables holding the diffusion tensor components.
# Because the diffusion tensor is a symmetric second-rank tensor, we only need six
# tensor components. The components of the tensor are ordered as
y = diff_mri.dependent_variables
print(y[0].component_labels)

# %%
# The symmetric matrix information is also found with the
# :attr:`~csdmpy.DependentVariable.quantity_type` attribute,
y[0].quantity_type

# %%
# which implies a 3x3 symmetric matrix.

# %%
# **Visualize the dataset**
#
# In the following, we visualize the isotropic diffusion coefficient, that is, the
# average of the :math:`d_{xx}`, :math:`d_{yy}`, and :math:`d_{zz}` tensor components.
# Since it's a three-dimensional dataset, we'll visualize the projections onto the
# three dimensions.

# the isotropic diffusion coefficient.
# component at index 0 = dxx
# component at index 3 = dyy
# component at index 5 = dzz
isotropic_diffusion = (y[0].components[0] + y[0].components[3] + y[0].components[5]) / 3

# %%
# In the following, we use certain features of the csdmpy module.
# Please refer to :ref:`generating_csdm_objects` for  further details.

# Create a new csdm object from the isotropic diffusion coefficient array.
new_csdm = cp.as_csdm(isotropic_diffusion, quantity_type="scalar")

# Add the dimensions from `diff_mri` object to the `new_csdm` object.
for i, dim in enumerate(x):
    new_csdm.dimensions[i] = dim

# %%
# Now, we can plot the projections of the isotropic diffusion coefficients along
# the respective dimensions as
import matplotlib.pyplot as plt

# projection along the x-axis.
plt.figure(figsize=(5, 4))
cp.plot(new_csdm.sum(axis=0), cmap="gray_r", origin="upper")
plt.tight_layout()
plt.show()

# %%

# projection along the y-axis.
plt.figure(figsize=(5, 4))
cp.plot(new_csdm.sum(axis=1), cmap="gray_r", origin="upper")
plt.tight_layout()
plt.show()

# %%

# projection along the z-axis.
plt.figure(figsize=(5, 4))
cp.plot(new_csdm.sum(axis=2), cmap="gray_r", origin="upper")
plt.tight_layout()
plt.show()

# %%
# .. rubric:: Citation
#
# .. [#f1] Diffusion tensor MRI `dataset <http://www.sci.utah.edu/~gk/DTI-data/>`_; 2000.

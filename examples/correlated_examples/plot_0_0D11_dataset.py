# -*- coding: utf-8 -*-
"""
Scatter, 0D{1,1} dataset
^^^^^^^^^^^^^^^^^^^^^^^^
"""
#%%
# We start with a 0D{1,1} correlated dataset, that is, a dataset
# without a coordinate grid. A 0D{1,1} dataset has no dimensions, d = 0, and
# two single-component dependent variables.
# In the following example [#f3]_, the two `correlated` dependent variables are
# the :math:`^{29}\text{Si}` - :math:`^{29}\text{Si}` nuclear spin couplings,
# :math:`^2J`, across a Si-O-Si linkage, and the `s`-character product on the
# O and two Si along the Si-O bond across the Si-O-Si linkage.
#
# Let's import the dataset.
import csdmpy as cp

filename = "https://osu.box.com/shared/static/h1nxth6gs94fthfmvip5vchp3zh4zd6o.csdf"
zero_d_dataset = cp.load(filename)

#%%
# Since the dataset has no dimensions, the value of the
# :attr:`~csdmpy.CSDM.dimensions` attribute of the :attr:`~csdmpy.CSDM`
# class is an empty tuple,

print(zero_d_dataset.dimensions)

#%%
# The :attr:`~csdmpy.CSDM.dependent_variables` attribute, however, holds
# two dependent-variable objects. The data structure from the two dependent
# variables is

#%%
print(zero_d_dataset.dependent_variables[0].data_structure)

#%%
# and

print(zero_d_dataset.dependent_variables[1].data_structure)

#%%
# respectively.

#%%
# **Visualizing the dataset**
#
# The correlation plot of the dependent-variables from the dataset is
# shown below.

import matplotlib.pyplot as plt

y0 = zero_d_dataset.dependent_variables[0]
y1 = zero_d_dataset.dependent_variables[1]

plt.scatter(y1.components[0], y0.components[0], s=2, c="k")
plt.xlabel(y1.axis_label[0])
plt.ylabel(y0.axis_label[0])
plt.tight_layout()
plt.show()

#%%
# .. rubric:: Citation
#
# .. [#f3]
#       Srivastava DJ, Florian P, Baltisberger JH, Grandinetti PJ. Correlating geminal
#       couplings to structure in framework silicates. Phys Chem Chem Phys. 2018;20:562–571.
#       DOI:10.1039/C7CP06486A

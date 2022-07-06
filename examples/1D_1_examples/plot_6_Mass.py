"""
Mass spectrometry (sparse) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
# %%
# The following mass spectrometry data of acetone is an example of a sparse dataset.
# Here, the CSDM data file holds a sparse dependent variable. Upon import, the
# components of the dependent variable sparsely populates the coordinate grid. The
# remaining unpopulated coordinates are assigned a zero value.
import matplotlib.pyplot as plt

import csdmpy as cp

filename = "https://www.ssnmr.org/sites/default/files/CSDM/MassSpec/acetone.csdf"
mass_spec = cp.load(filename)
print(mass_spec.data_structure)

# %%
# Here, the coordinates along the dimension are
print(mass_spec.dimensions[0].coordinates)

# %%
# and the corresponding components of the dependent variable,
print(mass_spec.dependent_variables[0].components[0])

# %%
# Note, only eight values were listed in the dependent variable's `components`
# attribute in the `.csdf` file. The remaining component values were set to zero.
plt.figure(figsize=(5, 3.5))
ax = plt.subplot(projection="csdm")
ax.plot(mass_spec)
plt.tight_layout()
plt.show()

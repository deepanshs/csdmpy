# -*- coding: utf-8 -*-
"""
Ultraviolet–visible (UV-vis) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
# %%
# The following
# `UV-vis dataset <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_
# was obtained as a JCAMP-DX file, and subsequently converted to the CSD model
# file-format. The data structure of the UV-vis dataset follows,
import matplotlib.pyplot as plt

import csdmpy as cp

domain = "https://www.ssnmr.org/sites/default/files/CSDM"
filename = f"{domain}/UV-vis/benzeneVapour_base64.csdf"
UV_data = cp.load(filename)
print(UV_data.data_structure)

# %%
# and the corresponding plot
plt.figure(figsize=(5, 3.5))
ax = plt.subplot(projection="csdm")
ax.plot(UV_data)
plt.tight_layout()
plt.show()

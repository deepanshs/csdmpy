# -*- coding: utf-8 -*-
"""
Gas Chromatography dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
# %%
# The following
# `Gas Chromatography dataset  <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_
# was obtained as a JCAMP-DX file, and subsequently converted to the CSD model
# file-format. The data structure of the gas chromatography dataset follows,
import matplotlib.pyplot as plt

import csdmpy as cp

filename = "https://www.ssnmr.org/sites/default/files/CSDM/GC/cinnamon_base64.csdf"
GCData = cp.load(filename)
print(GCData.data_structure)

# %%
# and the corresponding plot
plt.figure(figsize=(5, 3.5))
ax = plt.subplot(projection="csdm")
ax.plot(GCData)
plt.tight_layout()
plt.show()

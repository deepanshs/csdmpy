# -*- coding: utf-8 -*-
"""
Electron Paramagnetic Resonance (EPR) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
# %%
# The following is a simulation of the
# `EPR dataset <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_,
# originally obtained as a JCAMP-DX file, and subsequently converted to the
# CSD model file-format. The data structure of this dataset follows,
import matplotlib.pyplot as plt

import csdmpy as cp

domain = "https://www.ssnmr.org/sites/default/files/CSDM"
filename = f"{domain}/EPR/AmanitaMuscaria_base64.csdf"
EPR_data = cp.load(filename)
print(EPR_data.data_structure)

# %%
# and the corresponding plot.
plt.figure(figsize=(5, 3.5))
ax = plt.subplot(projection="csdm")
ax.plot(EPR_data)
plt.tight_layout()
plt.show()

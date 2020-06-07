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

filename = "https://osu.box.com/shared/static/0dh8mwnjr600lh1ufpsmt5780yp7wi99.csdf"
EPR_data = cp.load(filename)
print(EPR_data.data_structure)

# %%
# and the corresponding plot.
plt.figure(figsize=(6, 4))
cp.plot(EPR_data)
plt.tight_layout()
plt.show()

# -*- coding: utf-8 -*-
"""
Gas Chromatography dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
#%%
# The following
# `Gas Chromatography dataset  <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_
# was obtained as a JCAMP-DX file, and subsequently converted to the CSD model
# file-format. The data structure of the gas chromatography dataset follows,
import csdmpy as cp

filename = "https://osu.box.com/shared/static/zt452x7p3plbnjqt2898dy8px6hkhkd8.csdf"
GCData = cp.load(filename)
print(GCData.data_structure)

#%%
# and the corresponding plot

cp.plot(GCData)

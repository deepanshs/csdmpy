# -*- coding: utf-8 -*-
"""
Fourier Transform Infrared Spectroscopy (FTIR) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
#%%
# The following
# `FTIR dataset <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_,
# was obtained as a JCAMP-DX file, and subsequently converted to the CSD model
# file-format. The data structure of the FTIR dataset follows,
import csdmpy as cp

filename = "https://osu.box.com/shared/static/0iw0egupb1hkulkbdq4hagzzhkbvqjkv.csdf"
FTIR_data = cp.load(filename)

#%%
print(FTIR_data.data_structure)

#%%
# and the corresponding plot

cp.plot(FTIR_data)

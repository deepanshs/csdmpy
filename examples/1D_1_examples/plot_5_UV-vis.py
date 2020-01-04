# -*- coding: utf-8 -*-
"""
Ultraviolet–visible (UV-vis) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
#%%
# The following
# `UV-vis dataset <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_
# was obtained as a JCAMP-DX file, and subsequently converted to the CSD model
# file-format. The data structure of the UV-vis dataset follows,
import csdmpy as cp

filename = "https://osu.box.com/shared/static/c9wg59hya5ohc083qi2jgd7wk5emmlmu.csdf"
UV_data = cp.load(filename)
print(UV_data.data_structure)

#%%
# and the corresponding plot

cp.plot(UV_data)

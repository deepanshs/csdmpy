"""
Fourier Transform Infrared Spectroscopy (FTIR) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
# %%
# The following
# `FTIR dataset <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_,
# was obtained as a JCAMP-DX file, and subsequently converted to the CSD model
# file-format. The data structure of the FTIR dataset follows,
import matplotlib.pyplot as plt

import csdmpy as cp

filename = "https://www.ssnmr.org/sites/default/files/CSDM/ir/caffeine_base64.csdf"
FTIR_data = cp.load(filename)
print(FTIR_data.data_structure)

# %%
# and the corresponding plot.
plt.figure(figsize=(5, 3.5))
ax = plt.subplot(projection="csdm")
ax.plot(FTIR_data)
ax.invert_xaxis()
plt.tight_layout()
plt.show()

# %%
# Because, FTIR spectrum is conventionally displayed on a reverse axis, an
# optional `reverse_axis` argument is provided to the :meth:`~csdmpy.plot` method.
# Its value is an order list of boolean, corresponding to the order of the
# dimensions.

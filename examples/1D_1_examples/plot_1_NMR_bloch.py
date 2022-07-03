# -*- coding: utf-8 -*-
"""
Nuclear Magnetic Resonance (NMR) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
# %%
# The following dataset is a :math:`^{13}\mathrm{C}` time-domain NMR Bloch decay
# signal of ethanol.
# Let's load this data file and take a quick look at its data
# structure. We follow the steps described in the previous example.
import matplotlib.pyplot as plt

import csdmpy as cp

domain = "https://www.ssnmr.org/sites/default/files/CSDM"
filename = f"{domain}/NMR/blochDecay/blochDecay.csdf"
NMR_data = cp.load(filename)
print(NMR_data.data_structure)

# %%
# This particular example illustrates two additional attributes of the CSD model,
# namely, the :attr:`~csdmpy.CSDM.geographic_coordinate` and
# :attr:`~csdmpy.CSDM.tags`. The `geographic_coordinate` described the
# location where the CSDM file was last serialized. You may access this
# attribute through,

# %%
print(NMR_data.geographic_coordinate)

# %%
# The `tags` attribute is a list of keywords that best describe the dataset.
# The `tags` attribute is accessed through,

# %%
print(NMR_data.tags)

# %%
# You may add additional tags, if so desired, using the `append`
# method of python's list class, for example,

# %%
NMR_data.tags.append("Bloch decay")
print(NMR_data.tags)

# %%
# The coordinates along the dimension are
x = NMR_data.dimensions
x0 = x[0].coordinates
print(x0)

# %%
# Unlike the previous example, the data structure of an NMR measurement is
# a complex-valued dependent variable. The numeric type of the components from
# a dependent variable is accessed through the
# :attr:`~csdmpy.DependentVariable.numeric_type` attribute.

# %%
y = NMR_data.dependent_variables
print(y[0].numeric_type)

# %%
# Visualizing the dataset
# -----------------------
#
# In the previous example, we illustrated a matplotlib script for plotting 1D data.
# Here, we use the csdmpy :meth:`~csdmpy.plot` method, which is a supplementary method
# for plotting 1D and 2D datasets only.
plt.figure(figsize=(5, 3.5))
ax = plt.subplot(projection="csdm")
ax.plot(NMR_data.real, label="real")
ax.plot(NMR_data.imag, label="imag")
plt.grid()
plt.tight_layout()
plt.show()

# %%
# Reciprocal dimension object
# ---------------------------
#
# When observing the dimension instance of `NMR_data`,
print(x[0].data_structure)

# %%
# notice, the reciprocal keyword. The :attr:`~csdmpy.Dimension.reciprocal`
# attribute is useful for datasets that frequently transform to a reciprocal domain,
# such as the NMR dataset. The value of the reciprocal attribute is the reciprocal
# object, which contains metadata for describing the reciprocal coordinates, such as
# the `coordinates_offset`, `origin_offset` of the reciprocal dimension.
#
# You may perform a fourier transform to visualize the NMR spectrum. Use the
# :meth:`~csdmpy.CSDM.fft` method on the csdm object ``NMR_data`` as follows
fft_NMR_data = NMR_data.fft()

# %%
# By default, the unit associated with a dimension after FFT is the reciprocal of the
# unit associated with the dimension before FFT. In this case, the dimension unit after
# FFT is Hz. NMR datasets are often visualized as a dimension frequency scale. To
# convert the dimension’s unit to ppm use,
fft_NMR_data.dimensions[0].to("ppm", "nmr_frequency_ratio")

# plot of the frequency domain data after FFT.
fig, ax = plt.subplots(1, 2, figsize=(8, 3), subplot_kw={"projection": "csdm"})
ax[0].plot(fft_NMR_data.real, label="real")
plt.grid()
ax[1].plot(fft_NMR_data.imag, label="imag")
plt.grid()
plt.tight_layout()
plt.show()

# %%
# In the above plot, the plot metadata is taken from the reciprocal object such as
# the x-axis label.

# %%
# To return to time domain signal, once again use the :meth:`~csdmpy.CSDM.fft` method
# on the ``fft_NMR_data`` object. We use the CSDM object's
# :attr:`~csdmpy.CSDM.complex_fft` attribute to determine the FFT ot iFFT operation.
NMR_data_2 = fft_NMR_data.fft()

# plot of the frequency domain data.
fig, ax = plt.subplots(1, 2, figsize=(8, 3), subplot_kw={"projection": "csdm"})
ax[0].plot(NMR_data_2.real, label="real")
plt.grid()
ax[1].plot(NMR_data_2.imag, label="imag")
plt.grid()
plt.tight_layout()
plt.show()

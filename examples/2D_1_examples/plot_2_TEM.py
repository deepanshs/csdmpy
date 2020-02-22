# -*- coding: utf-8 -*-
"""
Transmission Electron Microscopy (TEM) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
#%%
# The following `TEM dataset <https://doi.org/10.1371/journal.pbio.1000502>`_ is
# a section of an early larval brain of *Drosophila melanogaster* used in the
# analysis of neuronal microcircuitry. The dataset was obtained
# from the `TrakEM2 tutorial <http://www.ini.uzh.ch/~acardona/data.html>`_ and
# subsequently converted to the CSD model file-format.
#
# Let's import the CSD model data-file and look at its data structure.
import csdmpy as cp

filename = "https://osu.box.com/shared/static/3w5iqkx15fayan1u6g6sn5woc2ublkyh.csdf"
TEM = cp.load(filename)
print(TEM.data_structure)

#%%
# This dataset consists of two linear dimensions and one single-component
# dependent variable. The tuple of the dimension and the dependent variable
# instances from this example are

x = TEM.dimensions
y = TEM.dependent_variables

#%%
# and the respective coordinates (viewed only for the first ten coordinates),

print(x[0].coordinates[:10])

#%%
print(x[1].coordinates[:10])

#%%
# For convenience, let's convert the coordinates from `nm` to `µm` using the
# :meth:`~csdmpy.Dimension.to` method of the respective :ref:`dim_api`
# instance,

x[0].to("µm")
x[1].to("µm")

#%%
# and plot the data.

cp.plot(TEM)

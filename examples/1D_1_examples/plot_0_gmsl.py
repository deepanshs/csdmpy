# -*- coding: utf-8 -*-
"""
Global Mean Sea Level rise dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
#%%
# The following dataset is the Global Mean Sea Level (GMSL) rise from the late
# 19th to the Early 21st Century [#f0]_. The
# `original dataset <http://www.cmar.csiro.au/sealevel/sl_data_cmar.html>`_ was
# downloaded as a CSV file and subsequently converted to the CSD model format.
#
# Let's import this file.
import csdmpy as cp

filename = "https://osu.box.com/shared/static/vetjm3cndxdps05ijvv603ajth3jocck.csdf"
sea_level = cp.load(filename)

#%%
# The variable `filename` is a string with the address to the `.csdf` file.
# The :meth:`~csdmpy.load` method of the `csdmpy` module reads the
# file and returns an instance of the :ref:`csdm_api` class, in
# this case, as a variable ``sea_level``. For a quick preview of the data
# structure, use the :attr:`~csdmpy.CSDM.data_structure` attribute of this
# instance.

print(sea_level.data_structure)

#%%
# .. warning::
#     The serialized string from the :attr:`~csdmpy.CSDM.data_structure`
#     attribute is not the same as the JSON serialization on the file.
#     This attribute is only intended for a quick preview of the data
#     structure and avoids displaying large datasets. Do not use
#     the value of this attribute to save the data to the file. Instead, use the
#     :meth:`~csdmpy.CSDM.save` method of the :ref:`CSDM <csdm_api>`
#     class.

#%%
# The tuple of the dimensions and dependent variables, from this example, are

x = sea_level.dimensions
y = sea_level.dependent_variables

#%%
# respectively. The coordinates along the dimension and the
# component of the dependent variable are
print(x[0].coordinates)

#%%
# and
print(y[0].components[0])

#%%
# respectively.

#%%
# **Plotting the data**
#
# .. note::
#     The following code is only for illustrative purposes. The users may use
#     any plotting library to visualize their datasets.

import matplotlib.pyplot as plt

plt.plot(x[0].coordinates, y[0].components[0].real)
plt.xlim(x[0].coordinates[0].value, x[0].coordinates[-1].value)

# The axes labels and figure title.
plt.xlabel(x[0].axis_label)
plt.ylabel(y[0].axis_label[0])
plt.title(y[0].name)

plt.grid(color="gray", linestyle="--", linewidth=0.3)
plt.tight_layout()
plt.show()


#%%
#   The following is a quick description of the above code. Within the code, we
#   make use of the csdm instance's attributes in addition to the matplotlib
#   functions. The first line is an import call for the matplotlib functions.
#   The following line generates a plot of the coordinates along the
#   dimension verse the component of the dependent variable.
#   The next line sets the x-range. For labeling the axes,
#   use the :attr:`~csdmpy.Dimension.axis_label` attribute
#   of both dimension and dependent variable instances. For the figure title,
#   use the :attr:`~csdmpy.DependentVariable.name` attribute
#   of the dependent variable instance. The next statement adds the grid lines.
#   For additional information, refer to `Matplotlib <https://matplotlib.org>`_
#   documentation.

#%%
# .. seealso::
#     :ref:`getting_started`
#

#%%
# .. rubric:: Citation
#
# .. [#f0] Church JA, White NJ. Sea-Level Rise from the Late 19th to the Early 21st Century.
#          Surveys in Geophysics. 2011;32:585–602. DOI:10.1007/s10712-011-9119-1

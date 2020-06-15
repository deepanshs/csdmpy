
====================================
Plotting CSDM object with matplotlib
====================================

As you may have noticed by now, a CSDM object holds basic metadata such as the label,
unit, and physical quantity of the dimensions and dependent-variables, which is enough
to visualize the CSDM datasets on proper coordinate axes. In the following section, we
illustrate how you may use the CSDM object with the matplotlib plotting library.

When plotting CSDM objects with matplotlib, we make use of the CSDM object's metadata
to produce a `matplotlib Axes <https://matplotlib.org/api/axes_api.html>`_  object with
basic formattings, such as the coordinate axes label, dependent variable labels, and
legends. You may still additionally customize your figures. Please refer to the
`matplotlib documentation <https://matplotlib.org/index.html>`_ for further details.

To enable plotting CSDM objects with matplotlib, add a ``projection="csdm"`` to the
matplotlib's Axes instance, as follows,

.. code-block:: python

   ax = plt.subplot(projection="csdm")
   # now add the matplotlib plotting functions to this axes.
   # ax.plot(csdm_object) or
   # ax.imshow(csdm_object) ... etc

See the following examples.

.. toctree::
   :maxdepth: 2

   plotting_with_pyplot/one_D_plots
   plotting_with_pyplot/two_D_plots

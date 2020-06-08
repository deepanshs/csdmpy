
====================================
Plotting CSDM object with matplotlib
====================================

As you may have noticed by now, a CSDM object holds basic metadata such as the label,
unit, and physical quantity of the dimensions and dependent-variables, which is enough
to visualize the CSDM dataset. In the following section, we illustrate how to use the
CSDM object with the matplotlib plotting library.

To plot the content of a csdm object, add a ``projection="csdm"`` to the matplotlib's
Axes instance, as follows,

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


=================================
Using CSDM object with matplotlib
=================================

As you may have noticed by now, a CSDM object holds basic metadata such as the label,
unit, and physical quantity of the dimensions and dependent-variables, which is enough
to visualize the CSDM dataset. In the following section, we illustrate how to use the
CSDM object with the matplotlib plotting library.

To plot the content of a csdm object, add a ``projection='csdm`` to the Axes instance
of matplotlib, as follows,

.. code-block:: python

   ax = plt.subplot(projection="csdm")
   # now add the matplotlib plotting functions to this axes.
   # ax.plot(csdm_object) or
   # ax.imshow(csdm_object) ... etc

Part 1: Plotting 1D datasets
----------------------------------

Example-1: 1D{1} datasets
'''''''''''''''''''''''''

.. plot:: ../pyplot/oneD_plot.py
   :include-source:


Example-1: 1D{1, 1, ...} datasets
'''''''''''''''''''''''''''''''''

Plotting on the same Axes.
""""""""""""""""""""""""""

When multiple single-component dependent variables are present within the CSDM object,
the data from all dependent-variables are plotted on the same axes. The name of each
dependent variable is displayed within the legend.

Plotting on separate Axes.
""""""""""""""""""""""""""

To plot the data from individual dependent variables onto a separate axes, use the
:meth:`~csdmpy.CSDM.split` method to first split the CSDM object with `n` dependent
variables into `n` CSDM objects with single dependent variables, and then plot them
separately.

.. plot:: ../pyplot/oneD111_plot.py
   :include-source:

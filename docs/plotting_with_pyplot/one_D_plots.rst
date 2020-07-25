
1D CSDM objects with ``plot()|scatter()``
-----------------------------------------

1D{1} datasets
''''''''''''''

.. plot:: ../pyplot/oneD_plot.py
   :include-source:


1D{1, 1, ...} datasets
''''''''''''''''''''''

Plotting on the same Axes
"""""""""""""""""""""""""

When multiple single-component dependent variables are present within the CSDM object,
the data from all dependent-variables is plotted on the same axes. The name of each
dependent variable is displayed within the legend.

Plotting on separate Axes
"""""""""""""""""""""""""

To plot the data from individual dependent variables onto separate axes, use the
:meth:`~csdmpy.CSDM.split` method to first split the CSDM object with `n` dependent
variables into `n` CSDM objects with single dependent variables, and then plot them
separately.

.. plot:: ../pyplot/oneD111_plot.py
   :include-source:

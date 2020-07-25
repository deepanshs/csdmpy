
2D CSDM objects with ``imshow()|contour()|contourf()``
------------------------------------------------------

2D{1} datasets
''''''''''''''

.. plot:: ../pyplot/twoD_plot.py
   :include-source:


2D{1, 1, ..} datasets
'''''''''''''''''''''

Plotting on the same Axes
"""""""""""""""""""""""""

When multiple single-component dependent variables are present within the CSDM object,
the data from all dependent-variables is plotted on the same axes. The name of each
dependent variable is displayed along the color bar.

.. plot:: ../pyplot/twoD111_plot.py
   :include-source:

Plotting on separate Axes
"""""""""""""""""""""""""

To plot the data from individual dependent variables onto separate axes, use the
:meth:`~csdmpy.CSDM.split` method to first split the CSDM object with `n` dependent
variables into `n` CSDM objects with single dependent variables, and then plot them
separately.

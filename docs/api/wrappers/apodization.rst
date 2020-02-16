Dimension specific Apodization methods
--------------------------------------

The following methods of form

.. math::
    y = f(a x),

where :math:`a` is the function argument, and :math:`x` are the coordinates
along the dimension, apodize the components of the dependent variables along
the respective dimensions. The dimensionality of :math:`a` must be the
reciprocal of that of :math:`x`.
The resulting CSDM object has the same number of dimensions as the original
object.

.. currentmodule:: csdmpy.apodize

.. rubric:: Method Summary
.. autosummary::
    ~sin
    ~cos
    ~tan
    ~arcsin
    ~arccos
    ~arctan
    ~exp

.. rubric:: Method Documentation
.. autofunction:: sin
.. autofunction:: cos
.. autofunction:: tan
.. autofunction:: arcsin
.. autofunction:: arccos
.. autofunction:: arctan
.. autofunction:: exp

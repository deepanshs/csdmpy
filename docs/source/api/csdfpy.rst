

------
csdfpy
------

The `csdfpy` is a python module for importing and exporting the CSD model
file exchange formats.
The module is based on the core scientific dataset (CSD) model which is
designed as a building block in the development of a more sophisticated
portable scientific dataset file standard.
The CSD model supports :math:`p`-component independent variable, :math:`y`,
which is discretely sampled at :math:`N` points in a :math:`d`-dimensional
independent variable space :math:`(x_0, x_1, ... x_k, ... x_{d-1})`.
The model also supports multiple dependent variables that are
simultaneously sampled over the :math:`d`-dimensional independent variable
space.

In the `csdfpy` module, every instance of the :ref:`csdm_api` class holds a
list of independent and dependent variables. Every independent variable,
:math:`x_k`, is an instance of the :ref:`iv_api` class while every dependent
variable, :math:`y`, is an instance of the :ref:`dv_api` class.
A UML class diagram of the `csdfpy` module is shown below.

.. image:: /_static/classes_csdfpy.png

Methods
^^^^^^^

.. currentmodule:: csdfpy

.. autofunction:: load
.. autofunction:: new



------
csdmpy
------

The `csdmpy` is a python package for importing and exporting core scientific
dataset model file formats.
The package is based on the core scientific dataset (CSD) model which is
designed as a re-usable building block in the development of a more
sophisticated portable scientific dataset file standards.
The `csdmpy` package supports :math:`p`-component dependent variable,
:math:`\mathbf{U} \equiv \{\mathbf{U}_{0}, \ldots,\mathbf{U}_{q},
\ldots,\mathbf{U}_{p-1} \}`,
which is discretely sampled at :math:`N` unique points in a :math:`d`-
dimensional space
:math:`(\mathbf{X}_0, \ldots \mathbf{X}_k, \ldots \mathbf{X}_{d-1})`. In
addition, the package also supports multiple dependent variables,
:math:`\mathbf{U}_i`, sharing the same :math:`n`-dimensional space.

Here, every instance of the :ref:`csdm_api` class holds a
list of dimensions and dependent variables. Every dimension,
:math:`\mathbf{X}_k`, is an instance of the :ref:`dim_api` class while every
dependent variable, :math:`\mathbf{U}_i`, is an instance of the
:ref:`dv_api` class.
A UML class diagram of the `csdmpy` module is shown below.

.. image:: /_static/classes_csdmpy.png

Methods
^^^^^^^

.. currentmodule:: csdmpy

.. autofunction:: load
.. autofunction:: new
.. autofunction:: plot

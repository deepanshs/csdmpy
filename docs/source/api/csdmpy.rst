

------
csdmpy
------

The `csdmpy` is a python package for importing and exporting files serialized
with the core scientific dataset model file format. The package supports
:math:`p`-component dependent variable,
:math:`\mathbf{U} \equiv \{\mathbf{U}_{0}, \ldots,\mathbf{U}_{q},
\ldots,\mathbf{U}_{p-1} \}`, which is discretely sampled at :math:`M` unique
points in a :math:`d`-dimensional space
:math:`(\mathbf{X}_0, \ldots \mathbf{X}_k, \ldots \mathbf{X}_{d-1})`. In
addition, the package also supports multiple dependent variables,
:math:`\mathbf{U}_i`, sharing the same :math:`d`-dimensional space.

Here, every dataset is an instance of the :ref:`csdm_api` class which holds a
list of dimensions and dependent variables. Every dimension,
:math:`\mathbf{X}_k`, is an instance of the :ref:`dim_api` class while every
dependent variable, :math:`\mathbf{U}_i`, is an instance of the
:ref:`dv_api` class.
.. A UML class diagram of the `csdmpy` module is shown below.


Methods
^^^^^^^

.. currentmodule:: csdmpy

.. rubric:: Methods Summary

.. autosummary::
    load
    new

.. rubric:: Method Documentation
.. autofunction:: load
.. autofunction:: new

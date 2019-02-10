
Controlled variables
====================

Based on the sampling type and the types of coordinates, 
there are three types of controlled variable objects
associated with,

* :ref:`lsgd`
* :ref:`asgd`
* :ref:`nqd`



.. _lsgd:

Linearly sampled quantitative grid dimension
--------------------------------------------

The ``CSDModel`` is not just designed to read a scientific data file.
In this section, we describe the features of a linearly
sampled quantitative grid dimension. We illustrate this with 
the following example. ::

    >>> from MRData import csdfpy
    >>> filename = csdfpy.test_file['test01']
    >>> testdata1 = csdfpy.open(filename)

This creates an object ``testdata1``, an instance of the ``CSDModel`` class.
Here, we focus on the controlled variable, ::

    >>> x = testdata1.controlled_variables
    >>> print(x)
    (<MRData.csdfpy.controlled_variables._linearlySampledGrid object at 0xa0bc86150>,)

where ``x`` is a tuple with a single object, that is a ``_linearlySampledGrid`` object. 
    >>> print ('number of points = ', x[0].number_of_points)
    
This can also be used to assign/update the sampling
interval of the dimension.

    >>> x[0].number_of_points = 5
    >>> print ('new number of points = ', x[0].number_of_points)
    >>> print ('new coordinates = ', x[0].coordinates)


.. _asgd:

Arbitrarily sampled quantitative grid dimension
-----------------------------------------------


.. _nqd:

Non-quantitative dimension
--------------------------
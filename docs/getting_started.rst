.. _getting_started:

=====================================
Getting started with `csdmpy` package
=====================================

We have put together a set of guidelines for importing the `csdmpy`
package and related methods and attributes. We encourage the users
to follow these guidelines to promote consistency, amongst others.
Import the package using

.. doctest::

    >>> import csdmpy as cp

To load a `.csdf` or a `.csdfe` file, use the :meth:`~csdmpy.load`
method of the `csdmpy` module. In the following example, we load a
sample test file.

.. doctest::

    >>> filename = cp.tests.test01 # replace this with your file's name.
    >>> testdata1 = cp.load(filename)

Here, ``testdata1`` is an instance of the CSDM class.

At the root level, the :ref:`csdm_api` object includes various useful optional
attributes that may contain additional information about the dataset. One such
useful attribute is the :attr:`~csdmpy.CSDM.description` key, which briefs
the end-users on the contents of the dataset. To access the value of this
attribute use,

.. doctest::

    >>> testdata1.description
    'A simulated sine curve.'

---------------------------------------------------------------
Accessing the dimensions and dependent variables of the dataset
---------------------------------------------------------------

An instance of the CSDM object may include multiple dimensions and
dependent variables. Collectively, the dimensions form a multi-dimensional grid
system, and the dependent variables populate this grid.
In `csdmpy`,
dimensions and dependent variables are structured as list object.
To access these lists, use the :attr:`~csdmpy.CSDM.dimensions` and
:attr:`~csdmpy.CSDM.dependent_variables` attribute of the CSDM object,
respectively. For example,

.. doctest::

    >>> x = testdata1.dimensions
    >>> y = testdata1.dependent_variables

In this example, the dataset contains one dimension and one dependent variable.

You may access the instances of individual dimension and dependent variable by
using the proper indexing. For example, the dimension and dependent variable
at index 0 may be accessed using ``x[0]`` and ``y[0]``, respectively.

Every instance of the :ref:`dim_api` object has its own set of attributes
that further describe the respective dimension. For example, a Dimension object
may have an optional :attr:`~csdmpy.Dimension.description`
attribute,

.. doctest::

    >>> x[0].description
    'A temporal dimension.'

Similarly, every instance of the :ref:`dv_api` object has its own set of
attributes. In this example, the
:attr:`~csdmpy.DependentVariable.description`
attribute from the dependent variable is

    >>> y[0].description
    'A response dependent variable.'

Coordinates along the dimension
*******************************

Every dimension object contains a list of coordinates associated with every
grid index along the dimension. To access these coordinates, use
the :attr:`~csdmpy.Dimension.coordinates` attribute of the
respective :ref:`dim_api` instance. In this example, the coordinates are

.. doctest::

    >>> x[0].coordinates
    <Quantity [0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] s>

.. note::
    ``x[0].coordinates`` returns a
    `Quantity <http://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity>`_
    instance from the
    `Astropy <http://docs.astropy.org/en/stable/units/>`_ package.
    The `csdmpy` module utilizes the units library from
    `astropy.units <http://docs.astropy.org/en/stable/units/>`_ module
    to handle physical quantities. The numerical `value` and the
    `unit` of the physical quantities are accessed through the Quantity
    instance, using the ``value`` and the ``unit`` attributes, respectively.
    Please refer to the `astropy.units <http://docs.astropy.org/en/stable/units/>`_
    documentation for details.
    In the `csdmpy` module, the ``Quantity.value`` is a
    `Numpy array <https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.ndarray.html>`_.
    For instance, in the above example, the underlying Numpy array from the
    coordinates attribute is accessed as

    .. doctest::

        >>> x[0].coordinates.value
        array([0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])

Components of the dependent variable
************************************

Every dependent variable object has at least one component. The number of
components of the dependent variable is determined from the
:attr:`~csdmpy.DependentVariable.quantity_type` attribute
of the dependent variable object. For example, a scalar quantity has
one-component, while a vector quantity may have multiple components. To access
the components of the dependent variable, use the
:attr:`~csdmpy.DependentVariable.components`
attribute of the respective :ref:`dv_api` instance. For example,

.. doctest::

    >>> y[0].components
    array([[ 0.0000000e+00,  5.8778524e-01,  9.5105654e-01,  9.5105654e-01,
             5.8778524e-01,  1.2246469e-16, -5.8778524e-01, -9.5105654e-01,
            -9.5105654e-01, -5.8778524e-01]], dtype=float32)

The :attr:`~csdmpy.DependentVariable.components` attribute
is a Numpy array. Note, the number of dimensions of this array is :math:`d+1`,
where :math:`d` is the number of :ref:`dim_api` objects from the
:attr:`~csdmpy.CSDM.dimensions` attribute. The additional dimension in the
Numpy array corresponds to the number of components of the dependent variable.
For instance, in this example, there is a single dimension, `i.e.`, :math:`d=1`
and, therefore, the value of the
:attr:`~csdmpy.DependentVariable.components`
attribute holds a two-dimensional Numpy array of shape

.. doctest::

    >>> y[0].components.shape
    (1, 10)

where the first element of the shape tuple, `1`, is the number of
components of the dependent variable and the second element, `10`, is the
number of points along the dimension, `i.e.`, ``x[0].coordinates``.


--------------------
Plotting the dataset
--------------------

It is always helpful to represent a scientific dataset with visual aids
such as a plot or a figure instead of columns of numbers. As such, throughout
this documentation, we provide a figure or two for every example dataset.
We make use of Python's `Matplotlib library <https://matplotlib.org>`_
for generating these figures. The users may, however, use their favorite
plotting library.

.. Attention::

    Although we show code for visualizing the dataset, this documentation is not
    a guide for data visualization.

The following snippet plots the dataset from this example. Here, the
`axis_label` is an attribute of both Dimension and DependentVariable
instances, and the `name` is an attribute of the DependentVariable instance.

.. doctest::

    >>> import matplotlib.pyplot as plt
    >>> plt.plot(x[0].coordinates, y[0].components[0])  # doctest: +SKIP
    >>> plt.xlabel(x[0].axis_label)  # doctest: +SKIP
    >>> plt.ylabel(y[0].axis_label[0])  # doctest: +SKIP
    >>> plt.title(y[0].name)  # doctest: +SKIP
    >>> plt.show()

.. figure:: _images/test.*
    :figclass: figure-polaroid

.. seealso::

    :ref:`csdm_api`, :ref:`dim_api`, :ref:`dv_api`,
    `Quantity <http://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity>`_,
    `numpy array <https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.ndarray.html>`_,
    `Matplotlib library <https://matplotlib.org>`_

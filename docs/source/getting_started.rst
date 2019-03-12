
=====================================
Getting Started With `csdfpy` package
=====================================

If you prefer Jupyter notebooks, start a new notebook and follow the
instructions below. If you are new to Jupyter notebooks, first refer to the
`Installing Jupyter Notebook documentation <https://jupyter.readthedocs.io/en/latest/install.html>`_
to set up a Jupyter notebook. Not a fan of Jupyter notebooks, simply start
with a new python file.

------------------------------
Importing the `csdfpy` package
------------------------------

We have put together a set of guidelines for importing the `csdfpy`
module and the related methods and attributes. We encourage the users
to follow these guidelines to promote consistency amongst others.
Import the module using

.. doctest::

    >>> import csdfpy as cp

To load a `.csdf` or a `.csdfe` file, use the :py:meth:`~csdfpy.load`
method of the `csdfpy` module. In the following example, we load a
sample test file.

.. doctest::

    >>> filename = cp.test_file['test01']  # replace this with the filename.
    >>> testdata1 = cp.load(filename)

Here, ``testdata1`` is an instance of the :ref:`csdm_api` class.


-------------------------------------------------
Accessing the independent and dependent variables
-------------------------------------------------

To access the dependent and independent variables of the dataset, use the
:py:attr:`~csdfpy.CSDModel.dependent_variables` and the
:py:attr:`~csdfpy.CSDModel.independent_variables` attribute,
respectively, of the ``testdata1`` instance. For example,

.. doctest::

    >>> x = testdata1.independent_variables
    >>> y = testdata1.dependent_variables

where `x` and `y` are the tuples of :ref:`iv_api` and :ref:`dv_api` instances.
In the above example, both `x` and `y` are tuples with a single instance.

.. doctest::

    >>> print('x is a {0} of length {1}.'.format(type(x).__name__, len(x)))
    x is a tuple of length 1.
    >>> print('y is a {0} of length {1}.'.format(type(y).__name__, len(y)))
    y is a tuple of length 1.

To access the list of coordinates along the independent variable dimension, use
the :py:attr:`~csdfpy.IndependentVariable.coordinates` attribute of the
respective :ref:`iv_api` instance. In this example, the coordinates are

.. doctest::

    >>> print(x[0].coordinates)
    [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] s

.. note::
    ``x[0].coordinates`` returns a
    `Quantity <http://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity>`_
    instance from the
    `Astropy <http://docs.astropy.org/en/stable/units/>`_ package.
    The `csdfpy` module utilizes the units library from
    `astropy.units <http://docs.astropy.org/en/stable/units/>`_ module
    to handle physical quantities. The numerical `value` and the
    `unit` of the physical quantities are accessed through the Quantity
    instance, using the ``value`` and the ``unit`` attributes, respectively.
    Please refer to the `astropy.units <http://docs.astropy.org/en/stable/units/>`_
    documentation for details.
    In the `csdfpy` module, the ``Quantity.value`` is a
    `Numpy array <https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.ndarray.html>`_.


Similarly, to access the list of components of the dependent variable, use the
:py:attr:`~csdfpy.DependentVariable.components` attribute of the
respective :ref:`dv_api` instance. For example,

.. doctest::

    >>> print(y[0].components)
    [[ 0.0000000e+00  5.8778524e-01  9.5105654e-01  9.5105654e-01
       5.8778524e-01  1.2246469e-16 -5.8778524e-01 -9.5105654e-01
      -9.5105654e-01 -5.8778524e-01]]

    >>> type(y[0].components)
    <class 'numpy.ndarray'>

The value of the :py:attr:`~csdfpy.DependentVariable.components` attribute
is a Numpy array. Note, the number of dimensions of this array is :math:`d+1`
where :math:`d` is the number of independent variables.
The additional dimension corresponds to
the number of components of the dependent variable. For instance, in this
example, there is a single independent variable, `i.e.`, :math:`d=1` and
therefore the value of the :py:attr:`~csdfpy.DependentVariable.components`
attribute holds a two-dimensional array.
The shape of this array is

.. doctest::

    >>> print(y[0].components.shape)
    (1, 10)

where the first element of the shape tuple, `1`, is the number of
components of the dependent variable and the second element, `10`, is the
number of points along the independent variable, `i.e.`, ``x[0].coordinates``.


--------------------
Plotting the dataset
--------------------

.. "A picture is worth a thousand words" is an English language idiom and it
.. applies to the scientific dataset as well, that is, a plot of a scientific
.. dataset is more informative than just the series of number.

It is always helpful to present the scientific datasets with visual aids
such as plots and figures rather than columns of numbers. As such, throughout
this documentation, we provide a figure or two for every example dataset.
We make use of Python's `Matplotlib library <https://matplotlib.org>`_
for generating the figures. The users may, however, use their favorite plotting
library.

.. note::

    This documentation is not a guide for data visualization, and the `csdfpy`
    module does not include any plotting library.

The following snippet plots the dataset from this example. Here, the
`axis_label` is an attribute of both IndependentVariable and DependentVariable
instances and `name` is an attribute of the DependentVariable instance.

.. doctest::

    >>> import matplotlib.pyplot as plt
    >>> plt.plot(x[0].coordinates, y[0].components[0])  # doctest: +SKIP
    >>> plt.xlabel(x[0].axis_label)  # doctest: +SKIP
    >>> plt.ylabel(y[0].axis_label[0])  # doctest: +SKIP
    >>> plt.title(y[0].name)  # doctest: +SKIP
    >>> plt.show()

.. image:: /_static/test.pdf

.. seealso::

    :ref:`iv_api`, :ref:`dv_api`,
    `Quantity <http://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity>`_,
    `numpy array <https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.ndarray.html>`_,
    `Matplotlib library <https://matplotlib.org>`_

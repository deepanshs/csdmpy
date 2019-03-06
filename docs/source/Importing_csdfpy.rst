

===============================================
Getting Started With `csdfpy` package
===============================================

----------------------------------------
Importing the `csdfpy` package
----------------------------------------

We have put together a set of guidelines for importing the `csdfpy`
package and related functionalities. We encourage the users to follow these
guidelines to promote consistency amongst others.
Import the package using

.. doctest::

    >>> import csdfpy as cp

To load a `.csdf` or a `.csdfx` file, use the :py:meth:`~csdfpy.load`
method of the `csdfpy` package. In the following example, we use a
sample test file.

.. doctest::

    >>> filename = cp.test_file['test01']  # replace this with the filename.
    >>> testdata1 = cp.load(filename)

Here, ``testdata1`` is an instance of the :ref:`CSDModel <csdm_api>` class.


---------------------------------------------------
Accessing the controlled and uncontrolled variables
---------------------------------------------------

To access the controlled and the uncontrolled variables of the dataset, use the
:py:attr:`~csdfpy.CSDModel.controlled_variables` and the
:py:attr:`~csdfpy.CSDModel.uncontrolled_variables` attribute,
respectively, of the ``testdata1`` instance,

.. doctest::

    >>> x = testdata1.controlled_variables
    >>> y = testdata1.uncontrolled_variables

where x and y are the tuples of :ref:`cv_api` and :ref:`uv_api` instances. In
the above example, both x and y are tuples with a single object.

.. doctest::

    >>> print('x is a {0} of length {1}.'.format(type(x).__name__, len(x)))
    x is a tuple of length 1.
    >>> print('y is a {0} of length {1}.'.format(type(y).__name__, len(y)))
    y is a tuple of length 1.

Access the list of coordinates of the controlled variables through the
:py:attr:`~csdfpy.ControlledVariable.coordinates` attribute of the respective
:ref:`cv_api` instance. In this example, the coordinates are

.. doctest::

    >>> print(x[0].coordinates)
    [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] s

.. note::
    ``x[0].coordinates`` returns a
    `Quantity <http://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity>`_
    instance from the
    `Astropy <http://docs.astropy.org/en/stable/units/>`_ package.
    The `csdfpy` package utilizes the units library from
    `astropy.units <http://docs.astropy.org/en/stable/units/>`_ package
    to handle the physical quantities. The numerical `value` and the
    `unit` of the physical quantities are accessed through the Quantity
    instance, using the ``value`` and the ``unit`` attributes, respectively.
    Please refer to the `astropy.units <http://docs.astropy.org/en/stable/units/>`_
    documentation for details.
    In the `csdfpy` package, the ``Quantity.value`` is a
    `Numpy array <https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.ndarray.html>`_.


Similarly, access the list of components of the uncontrolled variables through
the :py:attr:`~csdfpy.UncontrolledVariable.components` attribute of the
respective :ref:`uv_api` instance. For instance,

.. doctest::

    >>> print(y[0].components)
    [[ 0.0000000e+00  5.8778524e-01  9.5105654e-01  9.5105654e-01
       5.8778524e-01  1.2246469e-16 -5.8778524e-01 -9.5105654e-01
      -9.5105654e-01 -5.8778524e-01]]

    >>> type(y[0].components)
    <class 'numpy.ndarray'>

This attribute returns a Numpy array. Note, the Numpy array from the
:py:attr:`~csdfpy.UncontrolledVariable.components` attribute has :math:`d+1`
dimensions, where :math:`d` is the number of controlled variables.
In this example, there is only one controlled variable, and
therefore, ``y[0].components`` holds a two-dimensional array of shape,

.. doctest::

    >>> print(y[0].components.shape)
    (1, 10)

The first element of the shape tuple, ``(1,10)``, is the number of components
of the uncontrolled variable. In this case, the number of components is one.
The second element, `10`, is the number of points along the
``x[0].coordinates``.


--------------------
Plotting the dataset
--------------------

For an illustrative purpose, we will use Python's
`Matplotlib library <https://matplotlib.org>`_ for rendering plots.
The users may, however, use their favorite plotting library.

.. doctest::

    >>> import matplotlib.pyplot as plt
    >>> plt.plot(x[0].coordinates, y[0].components[0])  # doctest: +SKIP
    >>> plt.xlabel(x[0].axis_label)  # doctest: +SKIP
    >>> plt.ylabel(y[0].axis_label[0])  # doctest: +SKIP
    >>> plt.title(y[0].name)  # doctest: +SKIP
    >>> plt.show()

.. image:: /_static/test.pdf



.. seealso::

    :ref:`Controlled variables <controlled_variables>`,
    `Quantity <http://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity>`_,
    `numpy array <https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.ndarray.html>`_,
    `Matplotlib library <https://matplotlib.org>`_

..    :ref:`Uncontrolled variables <uncontrolled_variables>`,

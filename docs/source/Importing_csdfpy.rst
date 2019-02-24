

===============================================
Getting Satrted With :guilabel:`csdfpy` package
===============================================

----------------------------------------
Importing the :guilabel:`csdfpy` package
----------------------------------------

We have put together a set of guidelines for importing :guilabel:`csdfpy`
package and the related functionality. We encourage the users to follow these
guidelines to promote consistency amongst others.
The package is imported as, ::

    >>> import csdfpy as cp  # doctest: +SKIP

To load a ``.csdf`` or a ``.csdfx`` file, use the :py:meth:`~csdfpy.load`
method of the :guilabel:`csdfpy` package. In the following example, we use a
sample test file. ::

    >>> filename = cp.test_file['test01']  # replace this with the filename.
    >>> testdata1 = cp.load(filename) # doctest: +SKIP

Here, ``testdata1`` is an instance of the :ref:`CSDModel <csdm_api>` class.


-----------------------------------------------
Accessing controlled and uncontrolled variables
-----------------------------------------------

To access the controlled and uncontrolled variables, use the
:py:attr:`~csdfpy.CSDModel.controlled_variables` and the
:py:attr:`~csdfpy.CSDModel.uncontrolled_variables` attributes,
respectively, of the ``testdata1`` instance, ::

    >>> x = testdata1.controlled_variables
    >>> y = testdata1.uncontrolled_variables

where x and y are the tuples of :ref:`cv_api` and :ref:`uv_api` objects. In the
above example, both x and y are tuples with a single object ::

    >>> print ('x is an {0} of length {1}.'.format(type(x).__name__, len(x)))
    >>> print ('y is an {0} of length {1}.'.format(type(y).__name__, len(y)))
    x is an tuple of length 1.
    y is an tuple of length 1.

The list of controlled variable coordinates is accessed through the
:py:attr:`~csdfpy.ControlledVariable.coordinates` attribute of the
:ref:`cv_api` object, which follows ::

    >>> x[0].coordinates # doctest: +SKIP
    [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] s

.. note::
    ``x[0].coordinates`` returns a
    `Quantity <http://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity>`_
    object from the
    `Astropy <http://docs.astropy.org/en/stable/units/>`_ module.
    The :guilabel:`csdfpy` module uses the units library from
    `astropy.units <http://docs.astropy.org/en/stable/units/>`_
    to handle the physical quantities. The `value` and the
    `unit` of the physical quantities are accessed through the Quantity
    object, using the ``value`` and the ``unit`` attributes, respectively.
    Please refer to the `astropy.units <http://docs.astropy.org/en/stable/units/>`_
    documentation for details.
    In :guilabel:`csdfpy` module, the ``Quantity.value`` is a
    `numpy array <https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.ndarray.html>`_.


The list of uncontrolled variables is accessed through the
:py:attr:`~csdfpy.UncontrolledVariable.components`
attribute of the :ref:`uv_api` object. This returns a numpy array. ::

    >>> y[0].components
    [[ 0.0000000e+00  5.8778524e-01  9.5105654e-01  9.5105654e-01
    5.8778524e-01  1.2246469e-16 -5.8778524e-01 -9.5105654e-01
    -9.5105654e-01 -5.8778524e-01]]
    >>> type(y[0].components)
    <class 'numpy.ndarray'>

.. note::
    The numpy array from the :py:attr:`~csdfpy.UncontrolledVariable.components`
    attribute has :math:`d+1` dimensions, where :math:`d` is the number of
    controlled variables.


In this example, there is only one controlled variable object, and
therefore, ``y[0].components`` holds a two dimensional array of shape, ::

    >>> y[0].components.shape
    (1, 10)

The first element of the shape tuple, ``(1,10)``, is the number of components
of the uncontrolled variable. In this case, the number of components is one.
The second element, `10`, is the number of points along the
``x[0].coordinates``.


-----------------
Plotting the data
-----------------

For a demonstrative purpose, we will use Python's
`Matplotlib library <https://matplotlib.org>`_ for producing plots.
The users may, however, use their favorite plotting library. ::

    >>> import matplotlib.pyplot as plt
    >>> plt.plot(x[0].coordinates, y[0].components[0])
    >>> plt.xlabel(x[0].axis_label)
    >>> plt.ylabel(y[0].axis_label[0])
    >>> plt.title(y[0].name)
    >>> plt.show()

.. image:: /resource/test.pdf



.. seealso::

    :ref:`Controlled variables <controlled_variables>`,
    `Quantity <http://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity>`_,
    `numpy array <https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.ndarray.html>`_,
    `Matplotlib library <https://matplotlib.org>`_

..    :ref:`Uncontrolled variables <uncontrolled_variables>`,

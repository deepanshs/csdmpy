=================
Importing csdfpy 
=================

We have put together a set of guidelines for importing ``csdfpy`` module and related functionality.
We encourage the users to follow these guidelines to promote consistency amongst other users. 
The module is imported as ::

    >>> from MRData import csdfpy # doctest: +SKIP

To load a ``.csdf`` or a ``.csdfx`` file, use the ``open`` method of the ``csdfpy`` module.
In the following example, we use a sample test file. ::

    >>> filename = csdfpy.test_file['test01'] # Replace this with the file address
    >>> testdata1 = csdfpy.open(filename) # doctest: +SKIP

Here, ``testdata1`` is an instance of the ``CSDModel`` class. 


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Accessing controlled and uncontrolled variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To access the uncontrolled and uncontrolled variables, use the ``uncontrolled_variables`` 
and the ``controlled_variables`` attributes of the ``testdata1`` instance, ::

    >>> x = testdata1.controlled_variables
    >>> y = testdata1.uncontrolled_variables

where ``x`` and ``y`` are the tuples of controlled and uncontrolled variables objects. 
In the above example, both ``x`` and ``y`` are tuples with a single object ::

    >>> print ('x', len(x), type(x))
    >>> print ('y', len(y), type(y))  # doctest: +SKIP
    x 1 <class 'tuple'>
    y 1 <class 'tuple'>

The list of controlled variable coordinates is accessed through the ``coordinates``
attribute of the controlled variable object. In the above example, the controlled
variable coordinates are ::

    >>> print (x[0].coordinates) # doctest: +SKIP
    [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] s

.. note::
    ``x[0].coordinates`` return an instance of the 
    `Quantity <http://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity>`_
    class from 
    `Astropy <http://docs.astropy.org/en/stable/units/>`_ module.
    The ``csdfpy`` module uses the units library from the astropy module to handle 
    the physical quantities.
    The value and the unit of the physical quantity are accessed through the 
    Quantity instance, using the ``value`` and the ``unit`` attributes. In ``csdfpy``,
    the ``value`` attribute is always a 
    `numpy array <https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.ndarray.html>`_.


The list of uncontrolled variables is accessed through the ``components`` attribute
of the uncontrolled variable object. This returns a numpy array. ::

    >>> print (y[0].components) 
    >>> print (type( y[0].components ))  # doctest: +SKIP
    [[ 0.0000000e+00  5.8778524e-01  9.5105654e-01  9.5105654e-01
    5.8778524e-01  1.2246469e-16 -5.8778524e-01 -9.5105654e-01
    -9.5105654e-01 -5.8778524e-01]]
    <class 'numpy.ndarray'>

.. note::
    The numpy array from the ``components`` attribute has M+1 dimensions, 
    where M is the number of controlled variables.


In the above example, there is only one controlled variable object, therefore
``y[0].components`` holds a two dimensional array of shape ::

    >>> print (y[0].components.shape)  # doctest: +SKIP
    (1, 10)

The first element of the shape tuple, ``(1,10)``, is the number of components of 
the uncontrolled variable. In this case, the number of components is one.


^^^^^^^^^^^^^^^^^
Plotting the data
^^^^^^^^^^^^^^^^^

We show the plot using python's Matplotlib library, however, the users may 
use their favorite plotting library.  :: 

    >>> import matplotlib.pyplot as plt
    >>> plt.plot(x[0].coordinates, y[0].components[0])
    >>> plt.xlabel(x[0].label)
    >>> plt.ylabel(y[0].component_labels[0])
    >>> plt.title(y[0].name)
    >>> plt.show()

.. image:: /resource/test.pdf


^^^^^^^^
See also
^^^^^^^^

* controlled_variables
* uncontrolled_variables
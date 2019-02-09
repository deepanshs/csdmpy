-----------------
Importing csdfpy 
-----------------

We have put together a set of guidelines for importing ``csdfpy`` module and related functionality.
We encourage the users to follow these guidelines to promote consistency amongst other users. 
The module is imported as ::

    >>> from MRData import csdfpy # doctest: +SKIP

To load a ``.csdf`` or a ``.csdfx`` file, use the ``open`` method of the ``csdfpy`` module.
In the following example, we use a sample test file. ::

    >>> filename = csdf.test_file['test01'] # Replace this with the file address
    >>> testdata1 = csdf.open(filename) # doctest: +SKIP

Here, ``testdata1`` is an instance of the ``CSDModel`` class. 
The print function will display a python dictonary with keywords describing
the contents ``testdata1``. ::

    >>> print (testdata1) # doctest: +SKIP

    {
    "CSDM": {
        "uncontrolled_variables": [
            {
                "encoding": "none",
                "numeric_type": "float32",
                "components": "[[ 0.0000000e+00  5. ... -01 -5.8778524e-01]]"
            }
        ],
        "controlled_variables": [
            {
                "reciprocal": {
                    "quantity": "frequency"
                },
                "number_of_points": 10,
                "sampling_interval": "0.1 s",
                "quantity": "time"
            }
        ],
        "version": "0.1.0"
        }
    }


To access the uncontrolled and uncontrolled variables, use the ``uncontrolled_variables`` 
and the ``controlled_variables`` attribure of the ``testdata1`` instance, ::

    >>> x = testdata1.controlled_variables
    >>> y = testdata1.uncontrolled_variables

where ``x`` and ``y`` are tuples of controlled and uncontrolled variables objects. 
In the above example, both ``x`` and ``y`` are tuples with a single object ::

    >>> print ('x', len(x), type(x))
    >>> print ('y', len(y), type(y))  # doctest: +SKIP
    x 1 <class 'tuple'>
    y 1 <class 'tuple'>

The list of controlled variable coordinates are accessed throught the ``coordinates``
attribute of the controlled variable object. In the above example, the controlled
variable coordinates are ::

    >>> print (x[0].coordinates) # doctest: +SKIP
    [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] s

.. note::
    ``x[0].coordinates`` returns an instance of Quantity calss from Astropy.
    ``csdfpy`` used the astropy units library to handle physical quantities.
    The value and the unit of the physical quantity can be accessed from the 
    Quantity instance using the ``value``and the ``unit`` attributes. The 
    ``value`` attributes return a numpy array.

>>> coordinate = x[0].coordinates.value
>>> unit = x[0].coordinates.unit
>>> print (coordinate)
>>> print (type(coordinate))
>>> print (unit)
    [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9]
    <class 'numpy.ndarray'>
    s

Similarly, the list of uncontrolled variables are accessed through the ``components`` attribute
of the uncontrolled valiable object. This returns a numpy array. ::

    >>> print (y[0].components) 
    >>> print (type( y[0].components ))  # doctest: +SKIP
    [[ 0.0000000e+00  5.8778524e-01  9.5105654e-01  9.5105654e-01
    5.8778524e-01  1.2246469e-16 -5.8778524e-01 -9.5105654e-01
    -9.5105654e-01 -5.8778524e-01]]
    <class 'numpy.ndarray'>

.. note::
    The numpy array from the ``components`` attribute has M+1 dimensions, 
    where M is the number of controlled variables.


In the above example, there is only one controlled variable object. The shape of ``y``
is ::

    >>> print (y[0].components.shape)  # doctest: +SKIP
    (1, 10)

where the first element, ``1``, is the number of components of uncontrolled variable.

    >>> print ('old number of points = ', x[0].number_of_points)
    >>> x[0].number_of_points = 5
    >>> print ('new number of points = ', x[0].number_of_points)
    >>> print ('new coordinates = ', x[0].coordinates) # doctest: +SKIP

    old number of points =  10
    new number of points =  5
    new coordinates =  [0.  0.1 0.2 0.3 0.4] s
    
    """
********************************
Importing csdfpy and subpackages
********************************

We have put together a set of guidelines for importing ``csdfpy`` module and related functionality.
We encourage the users to follow these guidelines to promote consistency amongst other users.

    >>> from MRData import csdf

To load a ``.csdf`` or a ``.csdfx`` file, use the ``open`` method of the ``csdf`` module.
In the following example, we use the sample test file.

    >>> filename = csdf.test_file['test01'] # Replace this with the file address
    >>> testdata1 = csdf.open(filename)

Here ``testdata1`` is an instance of the ``CSDModel`` class. 
The print function will display a python dictonary with keywords describing the content of data file.

    >>> print (testdata1)

.. testoutput::
    {
        "CSDM": {
            "uncontrolled_variables": [
            {
                "encoding": "none",
                "numeric_type": "float32",
                "components": "[[ 0.0000000e+00  5.8778524e-01  9.5105654e-01  9.5105654e-01   5.8778524e-01  1.2246469e-16 -5.8778524e-01 -9.5105654e-01  -9.5105654e-01 -5.8778524e-01]]"
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


To access the uncontrolled variables and uncontrolled variables, use the ``uncontrolled_variables`` 
and the ``controlled_variables`` attribure of the 
.. testcode::  
    >>> x = dO.controlled_variables
    >>> y = dO.uncontrolled_variables
.. sourcecode:: ipython

    >>> print ('old number of points = ', x[0].number_of_points)
    >>> x[0].number_of_points = 5
    >>> print ('new number of points = ', x[0].number_of_points)
    >>> print ('new coordinates = ', x[0].coordinates)
    old number of points =  10
    new number of points =  5
    new coordinates =  [0.  0.1 0.2 0.3 0.4] s
    
    """
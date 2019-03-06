

.. _lsgd:

-----------------------------------------
Linearly sampled grid controlled variable
-----------------------------------------

In this subsection, we describe the methods and attributes of a linearly
sampled grid controlled variable class. We illustrate this with an example.
The following snippet downloads and loads a test file containing a linearly
sampled grid controlled variable dimension. ::

    >>> import csdfpy as cp
    >>> url = 'https://raw.githubusercontent.com/DeepanshS/csdfpy-doc/master/test_files/test1.csdf?token=AUYEl2qKFBHjoZcy5nhkP0Ajo0syO5t2ks5cgSD2wA%3D%3D'
    >>> testdata1 = cp.load(url)
    Downloading '/DeepanshS/csdfpy-doc/master/test_files/test1.csdf' from 'raw.githubusercontent.com' to file 'test1_1.csdf'.
    [█████████████████████████████████████████████████]

.. testsetup:: test1.csdf

    import csdfpy as cp
    url = 'https://raw.githubusercontent.com/DeepanshS/csdfpy-doc/master/test_files/test1.csdf?token=AUYEl2qKFBHjoZcy5nhkP0Ajo0syO5t2ks5cgSD2wA%3D%3D'
    testdata1 = cp.load(url)

When the argument of the :py:meth:`~csdfpy.load` method is an URL, the
corresponding file is first downloaded to the working directory and then
read as a local file.

Let's look at the data structure.

.. doctest::

    >>> print(testdata1.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "numeric_type": "float32",
            "components": "[0.0, 0.0, ...... -0.95105654, -0.95105654]"
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
        "version": "0.0.9"
      }
    }

Here, the `testdata1` is an instance of the :ref:`CSDModel <csdm_api>` class.
For the remainder of this example, we will focus on the
:py:attr:`~csdfpy.CSDModel.controlled_variables` attribute of this
instance.

.. doctest::

    >>> x = testdata1.controlled_variables

The variable `x` is a tuple containing an instance of the :ref:`cv_api` class.
The controlled variable coordinates of this instance are

.. doctest::

    >>> print(x[0].coordinates)
    [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] s

where ``x[0].coordinates`` is a
`Quantity <http://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity>`_
object. The value and the unit of this object are

.. doctest::

    >>> # To access the numpy array
    >>> numpy_array = x[0].coordinates.value
    >>> print('numpy array =', numpy_array)
    numpy array = [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9]

    >>> # To access the astropy.unit
    >>> unit = x[0].coordinates.unit
    >>> print('unit =', unit)
    unit = s

respectively.



Attributes
^^^^^^^^^^

We go through the attributes of the :ref:`cv_api` class and demonstrate its
effects on the coordinates along the dimension.

The attributes that modify the coordinates
""""""""""""""""""""""""""""""""""""""""""

**The** :py:attr:`~csdfpy.ControlledVariable.number_of_points`:
The number of points along the grid dimension is accessed through the
:py:attr:`~csdfpy.ControlledVariable.number_of_points` attribute.

.. doctest::

    >>> print('number of points =', x[0].number_of_points)
    number of points = 10

To update the number of points, simply update the value of this attribute,

.. doctest::

    >>> x[0].number_of_points = 12
    >>> print('new number of points =', x[0].number_of_points)
    new number of points = 12

    >>> print('new coordinates =', x[0].coordinates)
    new coordinates = [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.  1.1] s

**The** :py:attr:`~csdfpy.ControlledVariable.sampling interval`: Similarly,

.. doctest::

    >>> print('old sampling interval =', x[0].sampling_interval)
    old sampling interval = 0.1 s

    >>> x[0].sampling_interval = "10 s"
    >>> print('new sampling interval =', x[0].sampling_interval)
    new sampling interval = 10.0 s

    >>> print('new coordinates =', x[0].coordinates)
    new coordinates = [  0.  10.  20.  30.  40.  50.  60.  70.  80.  90. 100. 110.] s

**The** :py:attr:`~csdfpy.ControlledVariable.reference_offset`

.. doctest::

    >>> print('old reference offset =', x[0].reference_offset)
    old reference offset = 0.0 s

    >>> x[0].reference_offset = "-1 s"
    >>> print('new reference offset =', x[0].reference_offset)
    new reference offset = -1.0 s

    >>> print('new coordinates =', x[0].coordinates)
    new coordinates = [  1.  11.  21.  31.  41.  51.  61.  71.  81.  91. 101. 111.] s

**The** :py:attr:`~csdfpy.ControlledVariable.origin_offset`

.. doctest::

    >>> print('old origin offset =', x[0].origin_offset)
    old origin offset = 0.0 s

    >>> x[0].origin_offset = "1 day"
    >>> print ('new origin offset =', x[0].origin_offset)
    new origin offset = 1.0 d

    >>> print('new coordinates =', x[0].coordinates)
    new coordinates = [  1.  11.  21.  31.  41.  51.  61.  71.  81.  91. 101. 111.] s

The last operation updates the value of the origin offset, however,
the coordinates remain unaffected. This is because the
:py:attr:`~csdfpy.ControlledVariable.coordinates` attribute refers to the
reference coordinates. Access the absolute coordinates through the
:py:attr:`~csdfpy.ControlledVariable.absolute_coordinates` attribute.

.. doctest::

    >>> print('absolute coordinates =', x[0].absolute_coordinates)
    absolute coordinates = [86401. 86411. 86421. 86431. 86441. 86451. 86461. 86471. 86481. 86491.
     86501. 86511.] s


.. _lsgd_order_attributes:

The attributes that modify the order of coordinates
"""""""""""""""""""""""""""""""""""""""""""""""""""

**The** :py:attr:`~csdfpy.ControlledVariable.fft_output_order` **option**:
Orders the coordinates according to the output of a Fast Fourier Transform
(FFT) routine.

.. doctest::

    >>> print('old coordinates =', x[0].coordinates)
    old coordinates = [  1.  11.  21.  31.  41.  51.  61.  71.  81.  91. 101. 111.] s

    >>> x[0].fft_output_order = True
    >>> print('new coordinates =', x[0].coordinates)
    new coordinates = [  1.  11.  21.  31.  41.  51. -59. -49. -39. -29. -19.  -9.] s

**The** :py:attr:`~csdfpy.ControlledVariable.reverse` **option**:
Reverse the order of the coordinates.

.. doctest::

    >>> print('old coordinates =', x[0].coordinates)
    old coordinates = [  1.  11.  21.  31.  41.  51. -59. -49. -39. -29. -19.  -9.] s

    >>> x[0].reverse = True
    >>> print('new coordinates =', x[0].coordinates)
    new coordinates = [ -9. -19. -29. -39. -49. -59.  51.  41.  31.  21.  11.   1.] s



Other attributes
""""""""""""""""

**The** :py:attr:`~csdfpy.ControlledVariable.label`

.. doctest::

    >>> x[0].label
    ''

    >>> x[0].label = 't1'
    >>> x[0].label
    't1'

**The** :py:attr:`~csdfpy.ControlledVariable.period`

.. doctest::

    >>> print('old period =', x[0].period)
    old period = inf s

    >>> x[0].period = '10 s'
    >>> print('new period =', x[0].period)
    new period = 10.0 s

**The** :py:attr:`~csdfpy.ControlledVariable.quantity`:
Returns the quantity name.

.. doctest::

    >>> print ('quantity is', x[0].quantity)
    quantity is time



Methods
^^^^^^^

**The** :py:meth:`~csdfpy.ControlledVariable.to` **method**:
The method is used for unit conversions. It follows

.. doctest::

    >>> print('old unit =', x[0].coordinates.unit)
    old unit = s

    >>> print('old coordinates =', x[0].coordinates)
    old coordinates = [ -9. -19. -29. -39. -49. -59.  51.  41.  31.  21.  11.   1.] s

    >>> ## unit conversion
    >>> x[0].to('min')

    >>> print ('new coordinates =', x[0].coordinates)
    new coordinates = [-0.15       -0.31666667 -0.48333333 -0.65       -0.81666667 -0.98333333
      0.85        0.68333333  0.51666667  0.35        0.18333333  0.01666667] min

.. note::

    In the above examples, the coordinates are ordered according to FFT output
    order and are also reversed based on the previous set of operations.

The argument of this method is a unit, in this case, `min`, whose
dimensionality must be consistent with the dimensionality of the
coordinates.  An exception will be raised otherwise.

.. doctest::

    >>> x[0].to('km/s')  # doctest: +SKIP
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/deepansh/anaconda3/lib/python3.6/site-packages/csdfpy-0.0.9-py3.6.egg/csdfpy/cv.py", line 1238, in to
        1.0*string_to_unit(unit), self.gcv.unit
      File "/Users/deepansh/anaconda3/lib/python3.6/site-packages/csdfpy-0.0.9-py3.6.egg/csdfpy/_utils.py", line 290, in _check_unit_consistency
        raise Exception(message.format(*options))
    Exception: The unit 'km / s' (speed) is inconsistent with the unit 'min' (time).

Also see :ref:`cv_api`

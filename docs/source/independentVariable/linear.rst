

.. _lsgd:

--------------------------
DimensionWithLinearSpacing
--------------------------

The coordinates along an independent variable with subtype :ref:`dwls_api` is
frequently encountered in scientific datasets.
Consider :math:`m_k` as the sampling interval, :math:`N_k \ge 1` as the
number of points, :math:`c_k` as the reference offset, and
:math:`o_k` as the origin offset from the :math:`k^{th}`
:ref:`iv_api` instance with the subtype of `DimensionWithLinearSpacing`,
then the corresponding coordinates along the dimension are evaluated as,

.. math::

    \begin{align}
    \mathbf{X}_k &= [m_k j ]_{j=0}^{N_k-1} - c_k \mathbf{1}, \\
    \mathbf{X}_k^\mathrm{abs} &= \mathbf{X}_k + o_k \mathbf{1}.
    \end{align}

Here :math:`\mathbf{X}_k` and :math:`\mathbf{X}_k^\mathrm{abs}` are the
ordered arrays of the reference and absolute independent variable
coordinates, respectively, and :math:`\mathbf{1}` is an array of ones.

In this section, we describe the methods and attributes of an independent
variable dimension with the `DimensionWithLinearSpacing` subtype. As an
example, we consider a test file.
The following snippet downloads and loads a test file with a linearly
spaced independent variable dimension coordinates.

.. doctest::

    >>> import csdfpy as cp
    >>> url = 'https://github.com/DeepanshS/NMRLineshape/raw/master/test1.csdf'
    >>> testdata1 = cp.load(url)
    Downloading '/DeepanshS/NMRLineshape/raw/master/NMR_CSA_lineshape_simulation.csdf' from 'github.com' to file 'NMR_CSA_lineshape_simulation.csdf'.
    [█████████████████████████████████████████]


When the argument of the :py:meth:`~csdfpy.load` method is an URL, the
corresponding file is first downloaded to the working directory and then
read in as a local file.

Here, the `testdata1` is an instance of the :ref:`CSDModel <csdm_api>` class.
Let's look at the data structure.

.. doctest::

    >>> print(testdata1.data_structure)
    {
      "CSDM": {
        "version": "1.0.0",
        "independent_variables": [
          {
            "type": "linear_spacing",
            "number_of_points": 10,
            "sampling_interval": "0.1 s",
            "quantity": "time",
            "reciprocal": {
              "quantity": "frequency"
            }
          }
        ],
        "dependent_variables": [
          {
            "numeric_type": "float32",
            "components": "[0.0, 0.0, ...... -0.95105654, -0.95105654]"
          }
        ]
      }
    }

For the remainder of this example, we focus only on the
:py:attr:`~csdfpy.CSDModel.independent_variables` attribute of the
``testdata1`` instance.

.. doctest::

    >>> x = testdata1.independent_variables

The variable `x` is a tuple containing an instance of the :ref:`iv_api` class.
This instance is a dimension with `linear_spacing` as seen from the value of
the :attr:`~csdfpy.IndependentVariable.dimension_type` attribute.

The coordinates of the independent variable from this instance are

.. doctest::

    >>> print(x[0].coordinates)
    [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] s

where ``x[0].coordinates`` is a
`Quantity <http://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity>`_
instance. The value and the unit of this object are

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

We go through different attributes of the :ref:`iv_api` instance and show
how it affects the coordinates along the independent variable dimension.

The attributes that modify the coordinates
""""""""""""""""""""""""""""""""""""""""""

**The** :py:attr:`~csdfpy.IndependentVariable.number_of_points`:
The number of points along the dimension is accessed through the
:py:attr:`~csdfpy.IndependentVariable.number_of_points` attribute.

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

**The** :py:attr:`~csdfpy.IndependentVariable.sampling interval`: Similarly,

.. doctest::

    >>> print('old sampling interval =', x[0].sampling_interval)
    old sampling interval = 0.1 s

    >>> x[0].sampling_interval = "10 s"
    >>> print('new sampling interval =', x[0].sampling_interval)
    new sampling interval = 10.0 s

    >>> print('new coordinates =', x[0].coordinates)
    new coordinates = [  0.  10.  20.  30.  40.  50.  60.  70.  80.  90. 100. 110.] s

**The** :py:attr:`~csdfpy.IndependentVariable.reference_offset`

.. doctest::

    >>> print('old reference offset =', x[0].reference_offset)
    old reference offset = 0.0 s

    >>> x[0].reference_offset = "-1 s"
    >>> print('new reference offset =', x[0].reference_offset)
    new reference offset = -1.0 s

    >>> print('new coordinates =', x[0].coordinates)
    new coordinates = [  1.  11.  21.  31.  41.  51.  61.  71.  81.  91. 101. 111.] s

**The** :py:attr:`~csdfpy.IndependentVariable.origin_offset`

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
:py:attr:`~csdfpy.IndependentVariable.coordinates` attribute refers to the
reference coordinates. Access the absolute coordinates through the
:py:attr:`~csdfpy.IndependentVariable.absolute_coordinates` attribute.

.. doctest::

    >>> print('absolute coordinates =', x[0].absolute_coordinates)
    absolute coordinates = [86401. 86411. 86421. 86431. 86441. 86451. 86461. 86471. 86481. 86491.
     86501. 86511.] s


.. _lsgd_order_attributes:

The attributes that modify the order of coordinates
"""""""""""""""""""""""""""""""""""""""""""""""""""

**The** :py:attr:`~csdfpy.IndependentVariable.fft_output_order` **option**:
Orders the coordinates according to the output of a Fast Fourier Transform
(FFT) routine.

.. doctest::

    >>> print('old coordinates =', x[0].coordinates)
    old coordinates = [  1.  11.  21.  31.  41.  51.  61.  71.  81.  91. 101. 111.] s

    >>> x[0].fft_output_order = True
    >>> print('new coordinates =', x[0].coordinates)
    new coordinates = [  1.  11.  21.  31.  41.  51. -59. -49. -39. -29. -19.  -9.] s

**The** :py:attr:`~csdfpy.IndependentVariable.reverse` **option**:
Reverse the order of the coordinates.

.. doctest::

    >>> print('old coordinates =', x[0].coordinates)
    old coordinates = [  1.  11.  21.  31.  41.  51. -59. -49. -39. -29. -19.  -9.] s

    >>> x[0].reverse = True
    >>> print('new coordinates =', x[0].coordinates)
    new coordinates = [ -9. -19. -29. -39. -49. -59.  51.  41.  31.  21.  11.   1.] s



Other attributes
""""""""""""""""

**The** :py:attr:`~csdfpy.IndependentVariable.label`

.. doctest::

    >>> x[0].label
    ''

    >>> x[0].label = 't1'
    >>> x[0].label
    't1'

**The** :py:attr:`~csdfpy.IndependentVariable.period`

.. doctest::

    >>> print('old period =', x[0].period)
    old period = inf s

    >>> x[0].period = '10 s'
    >>> print('new period =', x[0].period)
    new period = 10.0 s

**The** :py:attr:`~csdfpy.IndependentVariable.quantity`:
Returns the quantity name.

.. doctest::

    >>> print ('quantity is', x[0].quantity)
    quantity is time



Methods
^^^^^^^

**The** :py:meth:`~csdfpy.IndependentVariable.to` **method**:
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

Also see :ref:`iv_api`

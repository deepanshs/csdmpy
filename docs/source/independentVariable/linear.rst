
.. _lsgd:

--------------------------
Linearly Sampled Dimension
--------------------------

For a linearly sampled dimension, the coordinates of the independent variable
are spaced linearly along the dimension and are frequently encountered in many
scientific datasets.
In this case, the instance of the corresponding :ref:`dim_api`
class has a subtype called `linearly_sampled`.

Consider that the :math:`k^{th}` :ref:`dim_api` instance from
a :ref:`csdm_api` instance has a `linearly_sampled` subtype.
Let :math:`m_k`, :math:`N_k \ge 1`, :math:`c_k`, and :math:`o_k` be the
sampling interval, number of points, reference offset, and the origin offset,
respectively, from the corresponding Dimension instance,
then the coordinates along this dimension are evaluated as,

.. math::

    \begin{align}
    \mathbf{X}_k &= [m_k j ]_{j=0}^{N_k-1} - c_k \mathbf{1}, \\
    \mathbf{X}_k^\mathrm{abs} &= \mathbf{X}_k + o_k \mathbf{1}.
    \end{align}

where :math:`\mathbf{X}_k` and :math:`\mathbf{X}_k^\mathrm{abs}` are the
ordered arrays of the reference and absolute independent variable
coordinates, respectively, and :math:`\mathbf{1}` is an array of ones.

Methods and attributes
^^^^^^^^^^^^^^^^^^^^^^

There are several attributes and methods associated with a linearly sampled
dimension, each controlling the coordinates along the dimension in a unique
way. The following section describes these attributes and methods and
demonstrates their effect on the coordinates of the independent variable along
the dimension using examples. Consider the following test file.

.. doctest::

    >>> import csdmpy as cp
    >>> url = 'https://github.com/DeepanshS/csdmpy-doc/raw/master/test_files/test1.csdf'
    >>> filename = cp.tests.test01
    >>> testdata1 = cp.load(filename)


The above snippet downloads and loads a test file containing a linearly
sampled independent variable.
When the argument of the :meth:`~csdmpy.load` method is an URL, the
corresponding file is first downloaded to the working directory and then
read in as a local file.
In the above example, ``testdata1`` is an instance of the
:ref:`CSDM <csdm_api>` class with the following data structure.

.. doctest::

    >>> print(testdata1.data_structure)
    {
      "csdm": {
        "version": "1.0",
        "timestamp": "1994-11-05T13:15:30Z",
        "geographic_coordinate": {
          "latitude": "10 deg",
          "longitude": "93.2 deg",
          "altitude": "10 m"
        },
        "description": "A simulated sine curve.",
        "dimensions": [
          {
            "type": "linear",
            "description": "A temporal dimension.",
            "count": 10,
            "increment": "0.1 s",
            "quantity_name": "time",
            "label": "time",
            "reciprocal": {
              "quantity_name": "frequency"
            }
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "description": "A response dependent variable.",
            "name": "sine curve",
            "numeric_type": "float32",
            "quantity_type": "scalar",
            "component_labels": [
              "response"
            ],
            "components": [
              [
                "0.0, 0.58778524, ..., -0.95105654, -0.58778524"
              ]
            ]
          }
        ]
      }
    }

This a 1D{1} dataset with one independent variable of subtype
`linearly_sampled` and one single-component dependent variable.
For the remainder of this example, we only focus on the independent variable
instance `i.e` the member of the
:attr:`~csdmpy.CSDM.dimensions` attribute's tuple from the
``testdata1`` instance.

.. doctest::

    >>> x0 = testdata1.dimensions[0]

The variable `x0` is an instance of the :ref:`dim_api` class.
The coordinates of the independent variable from this instance are

.. doctest::

    >>> print(x0.coordinates)
    [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] s

where ``x0.coordinates`` is a
`Quantity <http://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity>`_
instance. The value and the unit of the quantity instance are

.. doctest::

    >>> # To access the numpy array
    >>> numpy_array = x0.coordinates.value
    >>> print('numpy array =', numpy_array)
    numpy array = [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9]

    >>> # To access the astropy.unit
    >>> unit = x0.coordinates.unit
    >>> print('unit =', unit)
    unit = s

respectively.



Attributes
""""""""""

The following are the attributes of the :ref:`dim_api` instance along with
examples demonstrating its effect on the coordinates along the dimension.

* :attr:`~csdmpy.dimensions.Dimension.type`
    This attribute returns the subtype of the instance.

    .. doctest::

        >>> print(x0.type)
        linear

**The attributes that modify the coordinates**


* :attr:`~csdmpy.dimensions.Dimension.count`
    The number of points along the dimension

    .. doctest::

        >>> print('number of points =', x0.count)
        number of points = 10

    To update the number of points, update the value of this attribute,

    .. doctest::

        >>> x0.count = 12
        >>> print('new number of points =', x0.count)
        new number of points = 12

        >>> print('new coordinates =', x0.coordinates)
        new coordinates = [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.  1.1] s

* :attr:`~csdmpy.dimensions.Dimension.increment`
    Similarly, the increment

    .. doctest::

        >>> print('old increment =', x0.increment)
        old increment = 0.1 s

        >>> x0.increment = "10 s"
        >>> print('new increment =', x0.increment)
        new increment = 10.0 s

        >>> print('new coordinates =', x0.coordinates)
        new coordinates = [  0.  10.  20.  30.  40.  50.  60.  70.  80.  90. 100. 110.] s

* :attr:`~csdmpy.dimensions.Dimension.coordinates_offset`

    .. doctest::

        >>> print('old reference offset =', x0.coordinates_offset)
        old reference offset = 0.0 s

        >>> x0.coordinates_offset = "1 s"
        >>> print('new reference offset =', x0.coordinates_offset)
        new reference offset = 1.0 s

        >>> print('new coordinates =', x0.coordinates)
        new coordinates = [  1.  11.  21.  31.  41.  51.  61.  71.  81.  91. 101. 111.] s

* :attr:`~csdmpy.dimensions.Dimension.origin_offset`

    .. doctest::

        >>> print('old origin offset =', x0.origin_offset)
        old origin offset = 0.0 s

        >>> x0.origin_offset = "1 day"
        >>> print ('new origin offset =', x0.origin_offset)
        new origin offset = 1.0 d

        >>> print('new coordinates =', x0.coordinates)
        new coordinates = [  1.  11.  21.  31.  41.  51.  61.  71.  81.  91. 101. 111.] s

    The last operation updates the value of the origin offset however
    the coordinates remain unaffected. This is because the
    :attr:`~csdmpy.dimensions.Dimension.coordinates` attribute refers to the
    reference coordinates. Access the absolute coordinates through the
    :attr:`~csdmpy.dimensions.Dimension.absolute_coordinates` attribute.

    .. doctest::

        >>> print('absolute coordinates =', x0.absolute_coordinates)
        absolute coordinates = [86401. 86411. 86421. 86431. 86441. 86451. 86461. 86471. 86481. 86491.
         86501. 86511.] s


.. _lsgd_order_attributes:

**The attributes that modify the order of coordinates**

* :attr:`~csdmpy.dimensions.Dimension.complex_fft`
    Orders the coordinates along the dimension according to the output of a
    complex Fast Fourier Transform (FFT) routine.

    .. doctest::

        >>> print('old coordinates =', x0.coordinates)
        old coordinates = [  1.  11.  21.  31.  41.  51.  61.  71.  81.  91. 101. 111.] s

        >>> x0.complex_fft = True
        >>> print('new coordinates =', x0.coordinates)
        new coordinates = [-59. -49. -39. -29. -19.  -9.   1.  11.  21.  31.  41.  51.] s


**Other attributes**

* :attr:`~csdmpy.dimensions.Dimension.period`

    .. doctest::

        >>> print('old period =', x0.period)
        old period = inf s

        >>> x0.period = '10 s'
        >>> print('new period =', x0.period)
        new period = 10.0 s

* :attr:`~csdmpy.dimensions.Dimension.quantity_name`
    Returns the quantity name.

    .. doctest::

        >>> print('quantity name is', x0.quantity_name)
        quantity name is time

* :attr:`~csdmpy.dimensions.Dimension.label`

    .. doctest::

        >>> x0.label
        'time'

        >>> x0.label = 't1'
        >>> x0.label
        't1'

* :attr:`~csdmpy.dimensions.Dimension.axis_label`
    Returns a formatted string for axis labeling.

    .. doctest::

        >>> x0.label
        't1'
        >>> x0.axis_label
        't1 / (s)'

Methods
"""""""

:meth:`~csdmpy.dimensions.Dimension.to`:
This method is used for unit conversions.

.. doctest::

    >>> print('old unit =', x0.coordinates.unit)
    old unit = s

    >>> print('old coordinates =', x0.coordinates)
    old coordinates = [-59. -49. -39. -29. -19.  -9.   1.  11.  21.  31.  41.  51.] s

    >>> ## unit conversion
    >>> x0.to('min')

    >>> print ('new coordinates =', x0.coordinates)
    new coordinates = [-0.98333333 -0.81666667 -0.65       -0.48333333 -0.31666667 -0.15
      0.01666667  0.18333333  0.35        0.51666667  0.68333333  0.85      ] min

.. note::

    In the above examples, the coordinates are ordered according to FFT output
    order and are also reversed based on the previous set of operations.

The argument of this method is a string containing the unit, in this case,
`min`, whose dimensionality must be consistent with the dimensionality of the
coordinates.  An exception will be raised otherwise.

.. doctest::

    >>> x0.to('km/s')  # doctest: +SKIP
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/deepansh/anaconda3/lib/python3.6/site-packages/csdmpy-0.0.9-py3.6.egg/csdmpy/cv.py", line 1238, in to
        1.0*string_to_unit(unit), self.gcv.unit
      File "/Users/deepansh/anaconda3/lib/python3.6/site-packages/csdmpy-0.0.9-py3.6.egg/csdmpy/_utils.py", line 290, in _check_unit_consistency
        raise Exception(message.format(*options))
    Exception: The unit 'km / s' (speed) is inconsistent with the unit 'min' (time).

Also see :ref:`dim_api`

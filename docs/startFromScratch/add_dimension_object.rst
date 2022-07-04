.. _how_to_add_dimension:

---------------------------------------
Adding Dimension objects to CSDM object
---------------------------------------

There are three subtypes of Dimension objects,

- LinearDimension
- MonotonicDimension
- LabeledDimension

**Using an instance of the Dimension class**

Please read the topic :ref:`generate_dimension_objects` for details on how to
generate an instance of the Dimension class. Once created, use the dimensions
to generate a CSDM object.


.. doctest::

    >>> linear_dim = cp.LinearDimension(count=10, increment="0.1 C/V")
    >>> new_data = cp.CSDM(dimensions=[linear_dim])
    >>> print(new_data)
    CSDM(
    LinearDimension([0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9] C / V)
    )

**Using Python's dictionary objects**

When using python dictionaries, the key-value pairs of the dictionary must
be a valid collection for the given Dimension subtype. For example,

.. doctest::

    >>> # dictionary representation of a linear dimension.
    >>> d0 = {
    ...     "type": "linear",
    ...     "description": "This is a linear dimension",
    ...     "count": 5,
    ...     "increment": "0.1 rad",
    ... }
    >>> # dictionary representation of a monotonic dimension.
    >>> d1 = {
    ...     "type": "monotonic",
    ...     "description": "This is a monotonic dimension",
    ...     "coordinates": ["1 m/s", "2 cm/s", "4 mm/s"],
    ... }
    >>> # dictionary representation of a labeled dimension.
    >>> d2 = {
    ...     "type": "labeled",
    ...     "description": "This is a labeled dimension",
    ...     "labels": ["Cu", "Ag", "Au"],
    ... }
    >>> # add the dictionaries to the CSDM object.
    >>> new_data = cp.CSDM(dimensions=[d0, d1, d2])
    >>> print(new_data)
    CSDM(
    LinearDimension([0.  0.1 0.2 0.3 0.4] rad),
    MonotonicDimension([1.    0.02  0.004] m / s),
    LabeledDimension(['Cu' 'Ag' 'Au'])
    )

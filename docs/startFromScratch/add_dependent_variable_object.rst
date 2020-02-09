
----------------------------------------------------------
Adding instances of DependentVariable class to CSDM object
----------------------------------------------------------

Create a new empty CSDM object following,

.. doctest::

    >>> import csdmpy as cp
    >>> new_data = cp.new(description='A new test dependent variables dataset')

Add an instance of the DependentVariable class using the
:meth:`~csdmpy.CSDM.add_dependent_variable` method of the :ref:`csdm_api`
instance.

There are two subtypes of DependentVariable class:

- **InternalDependentVariable**:
  We refer to an instance of the DependentVariable as *internal* when the
  components of the dependent variable are listed along with the other
  metadata specifying the dependent variable.
- **ExternalDependentVariable**:
  We refer to an instance of the DependentVariable as *external* when the
  components of the dependent variable are stored in an external file as
  binary data either locally or at a remote server.


**Using an instance of the DependentVariable class**

Please read the topic :ref:`generate_dependent_variable_objects` for details
on how to generate an instance of the DependentVariable class. Once created,
use the :meth:`~csdmpy.CSDM.add_dependent_variable` method of the CSDM object
to add the dependent variable, for example,

.. doctest::

    >>> dv = cp.as_dependent_variable(np.arange(10))
    >>> new_data.add_dependent_variable(dv)
    >>> print(new_data)
    CSDM(
    DependentVariable(
    [[0 1 2 3 4 5 6 7 8 9]], quantity_type=scalar, numeric_type=int64)
    )


**Using Python's dictionary objects**

When using python dictionaries, the key-value pairs of the dictionary must
be a valid collection for the given DependentVariable subtype. For example,

.. doctest::

    >>> d0 = {
    ...     'type': 'internal',
    ...     'quantity_type': 'scalar',
    ...     'description': 'This is an internal scalar dependent variable',
    ...     'unit': 'cm',
    ...     'components': np.arange(100)
    ... }
    >>> new_data.add_dependent_variable(d0)
    >>> print(new_data)
    CSDM(
    DependentVariable(
    [[0 1 2 3 4 5 6 7 8 9]], quantity_type=scalar, numeric_type=int64),
    DependentVariable(
    [[ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
      24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47
      48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71
      72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95
      96 97 98 99]] cm, quantity_type=scalar, numeric_type=int64)
    )

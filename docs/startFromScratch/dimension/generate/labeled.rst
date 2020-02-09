----------------
LabeledDimension
----------------

A LabeledDimension is one where the coordinates along the dimension are
string labels. You can similarly generate a labeled dimension.

**Using the** :class:`~csdmpy.Dimension` **class.**

.. doctest::

    >>> import csdmpy as cp
    >>> x = cp.Dimension(type='labeled',
    ...                  labels=['The', 'great', 'circle'])
    >>> print(x)
    LabeledDimension(['The' 'great' 'circle'])

**Using the** :class:`~csdmpy.LabeledDimension` **class.**

.. doctest::

    >>> x = cp.LabeledDimension(labels=['The', 'great', 'circle'])
    >>> print(x)
    LabeledDimension(['The' 'great' 'circle'])

**From numpy arrays or python list.**

Use the :meth:`~csdmpy.as_dimension` method to convert a numpy array as a
Dimension object.

.. doctest::

    >>> array = ['The', 'great', 'circle']
    >>> x = cp.as_dimension(array)
    >>> print(x)
    LabeledDimension(['The' 'great' 'circle'])

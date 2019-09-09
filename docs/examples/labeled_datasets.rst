

.. testsetup::

    >>> import matplotlib
    >>> font = {'family': 'normal', 'weight': 'light', 'size': 9};
    >>> matplotlib.rc('font', **font)
    >>> from os import path

---------------
Labeled Dataset
---------------

The CSD model also supports labeled dimensions. In the following example, we
present a mixed `linear` and `labeled` two-dimensional dataset representing
the population of the country as a function of year. The dataset is
obtained from `The World Bank <https://data.worldbank.org/indicator/SP.POP.TOTL?view=chart>`_.


Import the `csdmpy` model and load the dataset.

.. doctest::

    >>> import csdmpy as cp
    >>> import matplotlib.pyplot as plt

    >>> filename = 'Test Files/labeled/population.csdf'
    >>> labeled_data = cp.load(filename)

Let's get the tuple of dimension and dependent variable objects from
``labeled_data`` instance.

.. doctest::

    >>> x = labeled_data.dimensions
    >>> y = labeled_data.dependent_variables

Since one of the dimensions is a `labeled` dimension, let's make use of the
:attr:`~csdmpy.dimensions.Dimension.type` attribute of the dimension instances
to find out which dimension is `labeled`.

.. doctest::

    >>> x[0].type
    'linear'
    >>> x[1].type
    'labeled'

Look like the second dimension is a `labeled` dimension with [#f1]_

.. doctest::

    >>> x[1].count
    263

labels, where the first five labels are

.. doctest::

    >>> print(x[1].labels[:5])
    ['Aruba' 'Afghanistan' 'Angola' 'Albania' 'Andorra']

.. note::
    For labeled dimensions, the :attr:`~csdmpy.dimensions.Dimension.coordinates`
    attribute is an alias of the :attr:`~csdmpy.dimensions.Dimension.labels`
    attribute. Therefore,

    .. doctest::

        >>> print(x[1].coordinates[:5])
        ['Aruba' 'Afghanistan' 'Angola' 'Albania' 'Andorra']

The coordinates along the first dimension viewed up to the first ten
points are

.. doctest::

    >>> print(x[0].coordinates[:10])
    [1960. 1961. 1962. 1963. 1964. 1965. 1966. 1967. 1968. 1969.] yr

**Plotting the dataset**

You may plot this dataset however you like. Here, we use a bar graph to
represent the population of countries in the year 2017. The data
corresponding to this year is a cross-section of the dependent variable
at index 57 along the ``x[0]`` dimension.

.. doctest::

    >>> print(x[0].coordinates[57])
    2017.0 yr

To keep the plot simple, we only plot the first 20 country labels along
the ``x[1]`` dimension.

.. doctest::

    >>> def plot_bar():
    ...     plt.figure(figsize=(4,4))
    ...
    ...     x_data = x[1].coordinates[:20]
    ...     x_pos = np.arange(20)
    ...     y_data = y[0].components[0][:20, 57]
    ...
    ...     plt.bar(x_data, y_data, align='center', alpha=0.5)
    ...     plt.xticks(x_pos, x_data, rotation=90)
    ...     plt.ylabel(y[0].axis_label[0])
    ...     plt.yscale("log")
    ...     plt.title(y[0].name)
    ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    ...     plt.show()

.. doctest::

    >>> plot_bar()

.. testsetup::

    >>> def plot_bar_save(dataObject):
    ...     plt.figure(figsize=(4,4))
    ...
    ...     x_data = x[1].coordinates[:20]
    ...     x_pos = np.arange(20)
    ...     y_data = y[0].components[0][:20, 57]
    ...
    ...     plt.bar(x_data, y_data, align='center', alpha=0.5)
    ...     plt.xticks(x_pos, x_data, rotation=90)
    ...     plt.ylabel(y[0].axis_label[0])
    ...     plt.yscale("log")
    ...     plt.title(y[0].name)
    ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    ...     filename = path.split(dataObject.filename)[1]
    ...     filepath = './docs/_images'
    ...     pth = path.join(filepath, filename)
    ...     plt.savefig(pth+'.pdf')
    ...     plt.savefig(pth+'.png', dpi=100)
    ...     plt.close()

.. testsetup::

    >>> plot_bar_save(labeled_data)

.. figure:: ../_images/population.csdf.*
    :figclass: figure-polaroid

.. rubric:: Footnotes

.. [#f1] In CSD model, the attribute count is only valid for the
         :ref:`linearDimension_uml`. In `csdmpy`, however, the
         :attr:`~csdmpy.dimensions.Dimension.count` attribute is valid for all
         dimension objects and returns an integer with the number of grid
         points along the dimension.

.. Example 2
.. ---------

.. Another example is the weather prediction as a function of datetime stamp,
.. datetime stamp is the labled dimension.

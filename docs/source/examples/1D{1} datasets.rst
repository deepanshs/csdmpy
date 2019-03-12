

--------------
1D{1} datasets
--------------

The 1D{1} datasets have a one-dimensional independent, :math:`d=1`, and
one single-component, :math:`p=1`, dependent variable.

.. In this section, we
.. present examples of the 1D{1} datasets from various scientific fields.

Let's start by first importing the `csdfpy` module. Here, we
also import the `matplotlib.pyplot` module for rendering the figures.

.. doctest::

    >>> import csdfpy as cp
    >>> import matplotlib.pyplot as plt

Global Mean Sea Level rise dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following dataset is the Global Mean Sea Level (GMSL) rise from the late
19th to the Early 21st Century. The
`original dataset <http://www.cmar.csiro.au/sealevel/sl_data_cmar.html>`_ was
downloaded as a CSV file and subsequently converted to the CSD model format
with a `.csdf` file extension. Let's import this file.

.. doctest::

    >>> filename = '../../test-datasets0.0.9/gmsl/sea_level.csdf'
    >>> sea_level = cp.load(filename)

The variable `filename` is a string with the local address to the
`sea_level.csdf` file relative to the working directory.
The :py:meth:`~csdfpy.load` method of the `csdfpy` module reads the
file and returns an instance of the :ref:`csdm_api` class, in
this case, as a variable ``sea_level``. For a quick preview of the data
contents, use the :py:attr:`~csdfpy.CSDModel.data_structure` attribute of the
instance,

.. doctest::

    >>> print(sea_level.data_structure)
    {
      "CSDM": {
        "version": "0.0.9",
        "independent_variables": [
          {
            "type": "linearly_sampled",
            "number_of_points": 1608,
            "sampling_interval": "0.08333333333333333 yr",
            "reference_offset": "-1880.0417 yr",
            "quantity": "time",
            "label": "Time",
            "reciprocal": {
              "quantity": "frequency"
            }
          }
        ],
        "dependent_variables": [
          {
            "name": "Global Mean Sea Level",
            "unit": "mm",
            "quantity": "length",
            "numeric_type": "float16",
            "component_labels": [
              "GMSL"
            ],
            "components": "[-183.0, -183.0, ...... 59.7, 59.7]"
          }
        ]
      }
    }

which returns a JSON object.

.. warning::
    The JSON output from the :py:attr:`~csdfpy.CSDModel.data_structure`
    attribute is not the same as the JSON serialization on the file.
    This attribute is only intended for a quick preview of the data 
    structure and avoids displaying large datasets. Do not use
    the value of this attribute to save the data to the file. Instead, use the
    :py:meth:`~csdfpy.CSDModel.save` method of the :ref:`CSDModel <csdm_api>`
    class.

The tuples of the independent and dependent variables from this example are

.. doctest::

    >>> x = sea_level.independent_variables
    >>> y = sea_level.dependent_variables

respectively. The coordinates of the independent variable, `x0`, and the
component of the dependent variable, `y00`, are

.. doctest::

    >>> x0 = x[0].coordinates
    >>> print(x0)
    [1880.0417     1880.12503333 1880.20836667 ... 2013.7917     2013.87503333
     2013.95836667] yr

    >>> y00 = y[0].components[0]
    >>> print(y00)
    [-183.  -171.1 -164.2 ...   66.4   59.7   58.5]

respectively. 

Before we plot the dataset, we find it convenient to write a small plotting
method. This method makes it easier, later, when we describe 1D{1}
examples form a variety of scientific datasets. The method follows-

.. doctest::

    >>> def plot1D(dataObject):
    ...     fig, ax = plt.subplots(1,1,  figsize=(3.4,2.1))

    ...     # tuples of dependent and independent variables instances.
    ...     x = dataObject.independent_variables
    ...     y = dataObject.dependent_variables

    ...     # The coordinates of the independent variable.
    ...     x0 = x[0].coordinates

    ...     # The component of the dependent variable.
    ...     y00 = y[0].components[0]

    ...     ax.plot(x0, y00.real, color='k', linewidth=0.75)

    ...     # The axes labels and figure title.
    ...     ax.set_xlabel(x[0].axis_label)
    ...     ax.set_ylabel(y[0].axis_label[0])
    ...     ax.set_title(y[0].name)

    ...     if x[0].reverse:
    ...         ax.invert_xaxis()

    ...     ax.grid(color='gray', linestyle='--', linewidth=0.5)
    ...     ax.set_xlim([x0[0].value, x0[-1].value])
    ...     plt.tight_layout(pad=0., w_pad=0., h_pad=0.)
    ...     plt.savefig(dataObject.filename+'.pdf')
    ...     plt.show()

A quick walk-through of the ``plot1D`` method. The method accepts an
instance of the :ref:`csdm_api` class as an argument. Within the method, we
make use of the instance's attributes in addition to the matplotlib
functions. The first line creates a new blank figure. In the following four
lines, we define the `x`, `y`, `x0`, and `y00` as previously described. The
next line adds a plot of `y00` vs. `x0` to the figure. For labeling the
axes, we use the  :py:attr:`~csdfpy.IndependentVariable.axis_label` attribute
of both independent and dependent variable instances. For the figure title,
we use the :py:attr:`~csdfpy.DependentVariable.name` attribute of the
dependent variable instance. The following `if` statement plot the figure with
the x-axis in reverse, if the :py:attr:`~csdfpy.IndependentVariable.reverse`
attribute of the independent variable instance is True. The following two lines
add the grid lines and set the range of the x-axis, respectively.
For additional information refer to the :ref:`iv_api`, :ref:`dv_api`, and the
`Matplotlib <https://matplotlib.org>`_ documentation.

Now to plot the ``sea_level`` dataset,

.. doctest::

    >>> plot1D(sea_level)

.. image:: /_static/sea_level.csdf.pdf


Nuclear Magnetic Resonance (MNR) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following dataset is a :math:`^{13}\mathrm{C}` time domain NMR Bloch decay
signal of ethanol. Let's load the data file and take a quick look at the data
structure.

.. doctest::

    >>> filename = '../../test-datasets0.0.9/NMR/blochDecay/blochDecay_raw.csdfe'
    >>> NMRdata = cp.load(filename)
    >>> print(NMRdata.data_structure)
    {
      "CSDM": {
        "version": "0.0.9",
        "independent_variables": [
          {
            "type": "linearly_sampled",
            "number_of_points": 4096,
            "sampling_interval": "0.1 ms",
            "reference_offset": "0.3 ms",
            "quantity": "time",
            "reciprocal": {
              "reference_offset": "-3005.363 Hz",
              "origin_offset": "75426328.864 Hz",
              "quantity": "frequency",
              "reverse": true,
              "label": "$^{13}$C frequency shift"
            }
          }
        ],
        "dependent_variables": [
          {
            "numeric_type": "complex64",
            "components": "[(-8899.406-1276.7734j), (-8899.406-1276.7734j), ...... (37.548492+20.15689j), (37.548492+20.15689j)]"
          }
        ]
      }
    }

Unlike the previous example, the data structure of the NMR measurement shows
a complexed value dataset. These complex values, `y00`, are the
component of the dependent variable and are accessed as follows,

.. doctest::

    >>> y = NMRdata.dependent_variables
    >>> y00 = y[0].components[0]
    >>> print(y00)
    [-8899.406   -1276.7734j  -4606.8804   -742.4125j
      9486.438    -770.0413j  ...   -70.95386   -28.32843j
        37.548492  +20.15689j  -193.92285   -67.06525j]

Similarly, the coordinates of the independent variable, `x0`, are

.. doctest::

    >>> x = NMRdata.independent_variables
    >>> x0 = x[0].coordinates
    >>> print(x0)
    [-3.000e-01 -2.000e-01 -1.000e-01 ...  4.090e+02  4.091e+02  4.092e+02] ms

Now to the plot the dataset,

.. doctest::

    >>> plot1D(NMRdata)

.. image:: /_static/blochDecay_raw.csdfx.pdf


Electron Paramagnetic Resonance (EPR) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following simulation of the
`EPR dataset <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_
is formerly obtained as a JCAMP-DX file and subsequently converted to the
CSD model file-format. The data structure of the dataset and the corresponding
plot follows,

.. doctest::

    >>> filename = '../../test-datasets0.0.9/EPR/xyinc2_base64.csdf'
    >>> EPRdata = cp.load(filename)
    >>> print(EPRdata.data_structure)
    {
      "CSDM": {
        "version": "0.0.9",
        "independent_variables": [
          {
            "type": "linearly_sampled",
            "number_of_points": 298,
            "sampling_interval": "4.0 G",
            "reference_offset": "-2750.0 G",
            "quantity": "magnetic flux density"
          }
        ],
        "dependent_variables": [
          {
            "name": "Amanita.muscaria",
            "numeric_type": "float32",
            "component_labels": [
              "Arbitrary"
            ],
            "components": "[0.067, 0.067, ...... -0.035, -0.035]"
          }
        ]
      }
    }
    >>> plot1D(EPRdata)

.. image:: /_static/xyinc2_base64.csdf.pdf

Gas Chromatography dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^

The following
`Gas Chromatography dataset  <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_
is also obtained as a JCAMP-DX file and subsequently converted to the CSD model
file format. The data structure and the plot of the gas chromatography dataset
follows,

.. doctest::

    >>> filename = '../../test-datasets0.0.9/GC/cinnamon_none.csdf'
    >>> GCData = cp.load(filename)
    >>> print(GCData.data_structure)
    {
      "CSDM": {
        "version": "0.0.9",
        "independent_variables": [
          {
            "type": "linearly_sampled",
            "number_of_points": 6001,
            "sampling_interval": "0.0034 min",
            "quantity": "time",
            "reciprocal": {
              "quantity": "frequency"
            }
          }
        ],
        "dependent_variables": [
          {
            "name": "Headspace from cinnamon stick",
            "numeric_type": "float32",
            "component_labels": [
              "Arbitrary"
            ],
            "components": "[48453.0, 48453.0, ...... 48040.0, 48040.0]"
          }
        ]
      }
    }
    >>> plot1D(GCData)

.. image:: /_static/cinnamon_none.csdf.pdf


Fourier Transform Infrared Spectroscopy (FTIR) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the following 
`FTIR dataset  <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_,
we again convert the original JCAMP-DX file to the CSD model format. The data
structure and the plot of the FTIR dataset follows

.. doctest::

    >>> filename = '../../test-datasets0.0.9/IR/caffeine_none.csdf'
    >>> FTIRData = cp.load(filename)
    >>> print(FTIRData.data_structure)
    {
      "CSDM": {
        "version": "0.0.9",
        "independent_variables": [
          {
            "type": "linearly_sampled",
            "number_of_points": 1842,
            "sampling_interval": "1.930548614883216 cm^-1",
            "reference_offset": "-449.41 cm^-1",
            "quantity": "wavenumber",
            "reverse": true,
            "reciprocal": {
              "quantity": "length"
            }
          }
        ],
        "dependent_variables": [
          {
            "name": "Caffeine",
            "numeric_type": "float32",
            "component_labels": [
              "Transmittance"
            ],
            "components": "[100.22944, 100.22944, ...... 99.08212, 99.08212]"
          }
        ]
      }
    }
    >>> plot1D(FTIRData)

.. image:: /_static/caffeine_none.csdf.pdf

Notice, the reverse axis of the FTIR wavenumber dimension.

Ultraviolet–visible (UV-vis) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following
`UV-vis dataset <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_
is originally downloaded as a JCAMP-DX file and consequently turned to the CSD
model format. The data structure and the plot of the UV-vis dataset follows,

.. doctest::

    >>> filename = '../../test-datasets0.0.9/UV-Vis/benzeneVapour_base64.csdf'
    >>> UVdata = cp.load(filename)
    >>> print(UVdata.data_structure)
    {
      "CSDM": {
        "version": "0.0.9",
        "independent_variables": [
          {
            "type": "linearly_sampled",
            "number_of_points": 4001,
            "sampling_interval": "0.01 nm",
            "reference_offset": "-230.0 nm",
            "quantity": "length",
            "reverse": true,
            "label": "wavelength",
            "reciprocal": {
              "quantity": "wavenumber"
            }
          }
        ],
        "dependent_variables": [
          {
            "name": "Vapour of Benzene",
            "numeric_type": "float32",
            "component_labels": [
              "Absorbance"
            ],
            "components": "[0.16786034, 0.16786034, ...... 0.25923702, 0.25923702]"
          }
        ]
      }
    }
    >>> plot1D(UVdata)

.. image:: /_static/benzeneVapour_base64.csdf.pdf



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

    >>> filename = '../test-datasets0.0.11/gmsl/sea_level_none.csdf'
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
      "csdm": {
        "version": "0.0.11",
        "description": "Global Mean Sea Level (GMSL) rise from the late 19th to the Early 21st Century.",
        "dimensions": [
          {
            "type": "linear",
            "number_of_points": 1608,
            "increment": "0.08333333333 yr",
            "index_zero_value": "1880.0416666667 yr",
            "quantity": "time",
            "label": "Time",
            "reciprocal": {
              "quantity": "frequency"
            }
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "name": "Global Mean Sea Level",
            "unit": "mm",
            "quantity": "length",
            "numeric_type": "float32",
            "component_labels": [
              "Global Mean Sea Level"
            ],
            "components": [
              [
                "-183.0, -183.0, ..., 59.6875, 59.6875"
              ]
            ]
          },
          {
            "type": "internal",
            "name": "Global Mean Sea Level",
            "unit": "mm",
            "quantity": "length",
            "numeric_type": "float32",
            "component_labels": [
              "GMSL uncertainty"
            ],
            "components": [
              [
                "24.203125, 24.203125, ..., 9.0, 9.0"
              ]
            ]
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

    >>> x = sea_level.dimensions
    >>> y = sea_level.dependent_variables

respectively. The coordinates of the independent variable, `x0`, and the
component of the dependent variable, `y00`, are

.. doctest::

    >>> x0 = x[0].coordinates
    >>> print(x0)
    [1880.04166667 1880.125      1880.20833333 ... 2013.79166666 2013.87499999
     2013.95833333] yr

    >>> y00 = y[0].components[0]
    >>> print(y00)
    [-183.     -171.125  -164.25   ...   66.375    59.6875   58.5   ]

respectively.

Before we plot the dataset, we find it convenient to write a small plotting
method. This method makes it easier, later, when we describe 1D{1}
examples form a variety of scientific datasets. The method follows-

.. doctest::

    >>> def plot1D(dataObject):
    ...     fig, ax = plt.subplots(1,1,  figsize=(3.4,2.1))

    ...     # tuples of dependent and dimension instances.
    ...     x = dataObject.dimensions
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

    ...     ax.grid(color='gray', linestyle='--', linewidth=0.5)
    ...     ax.set_xlim([x0[0].value, x0[-1].value])
    ...     plt.tight_layout(pad=0., w_pad=0., h_pad=0.)
    ...     plt.savefig(dataObject.filename+'.pdf')

A quick walk-through of the ``plot1D`` method. The method accepts an
instance of the :ref:`csdm_api` class as an argument. Within the method, we
make use of the instance's attributes in addition to the matplotlib
functions. The first line creates a new blank figure. In the following four
lines, we define the `x`, `y`, `x0`, and `y00` as previously described. The
next line adds a plot of `y00` vs. `x0` to the figure. For labeling the
axes, we use the  :py:attr:`~csdfpy.Dimension.axis_label` attribute
of both independent and dependent variable instances. For the figure title,
we use the :py:attr:`~csdfpy.DependentVariable.name` attribute of the
dependent variable instance. The following two lines
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

    >>> filename = '../test-datasets0.0.11/NMR/blochDecay/blochDecay_raw.csdfe'
    >>> NMRdata = cp.load(filename)
    >>> print(NMRdata.data_structure)
    {
      "csdm": {
        "version": "0.0.11",
        "description": "A time domain NMR $^{13}$C Bloch decay signal of ethanol.",
        "dimensions": [
          {
            "type": "linear",
            "number_of_points": 4096,
            "increment": "0.1 ms",
            "index_zero_value": "-0.3 ms",
            "quantity": "time",
            "reciprocal": {
              "index_zero_value": "-3005.363 Hz",
              "origin_offset": "75426328.864 Hz",
              "quantity": "frequency",
              "label": "$^{13}$C frequency shift"
            }
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "numeric_type": "complex64",
            "components": [
              [
                "(-8899.406-1276.7734j), (-8899.406-1276.7734j), ..., (37.548492+20.15689j), (37.548492+20.15689j)"
              ]
            ]
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

    >>> x = NMRdata.dimensions
    >>> x0 = x[0].coordinates
    >>> print(x0)
    [-3.000e-01 -2.000e-01 -1.000e-01 ...  4.090e+02  4.091e+02  4.092e+02] ms

Now to the plot the dataset,

.. doctest::

    >>> plot1D(NMRdata)

.. image:: /_static/blochDecay_raw.csdfe.pdf


Electron Paramagnetic Resonance (EPR) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following simulation of the
`EPR dataset <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_
is formerly obtained as a JCAMP-DX file and subsequently converted to the
CSD model file-format. The data structure of the dataset and the corresponding
plot follows,

.. doctest::

    >>> filename = '../test-datasets0.0.11/EPR/xyinc2_base64.csdf'
    >>> EPRdata = cp.load(filename)
    >>> print(EPRdata.data_structure)
    {
      "csdm": {
        "version": "0.0.11",
        "description": "A Electron Paramagnetic Resonance simulated dataset.",
        "dimensions": [
          {
            "type": "linear",
            "number_of_points": 298,
            "increment": "4.0 G",
            "index_zero_value": "2750.0 G",
            "quantity": "magnetic flux density"
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "name": "Amanita.muscaria",
            "numeric_type": "float32",
            "component_labels": [
              "Arbitrary"
            ],
            "components": [
              [
                "0.067, 0.067, ..., -0.035, -0.035"
              ]
            ]
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

    >>> filename = '../test-datasets0.0.11/GC/cinnamon_none.csdf'
    >>> GCData = cp.load(filename)
    >>> print(GCData.data_structure)
    {
      "csdm": {
        "version": "0.0.11",
        "description": "A Gas Chromatography dataset of cinnamon stick.",
        "dimensions": [
          {
            "type": "linear",
            "number_of_points": 6001,
            "increment": "0.0034 min",
            "quantity": "time",
            "reciprocal": {
              "quantity": "frequency"
            }
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "name": "Headspace from cinnamon stick",
            "numeric_type": "float32",
            "component_labels": [
              "Arbitrary"
            ],
            "components": [
              [
                "48453.0, 48453.0, ..., 48040.0, 48040.0"
              ]
            ]
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

    >>> filename = '../test-datasets0.0.11/IR/caffeine_none.csdf'
    >>> FTIRData = cp.load(filename)
    >>> print(FTIRData.data_structure)
    {
      "csdm": {
        "version": "0.0.11",
        "description": "An IR spectrum of caffeine.",
        "dimensions": [
          {
            "type": "linear",
            "number_of_points": 1842,
            "increment": "1.930548614883216 cm^-1",
            "index_zero_value": "449.41 cm^-1",
            "quantity": "wavenumber",
            "reciprocal": {
              "quantity": "length"
            }
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "name": "Caffeine",
            "numeric_type": "float32",
            "component_labels": [
              "Transmittance"
            ],
            "components": [
              [
                "99.31053, 99.31053, ..., 100.22944, 100.22944"
              ]
            ]
          }
        ]
      }
    }
    >>> plot1D(FTIRData)

.. image:: /_static/caffeine_none.csdf.pdf


Ultraviolet–visible (UV-vis) dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following
`UV-vis dataset <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_
is originally downloaded as a JCAMP-DX file and consequently turned to the CSD
model format. The data structure and the plot of the UV-vis dataset follows,

.. doctest::

    >>> filename = '../test-datasets0.0.11/UV-Vis/benzeneVapour_base64.csdf'
    >>> UVdata = cp.load(filename)
    >>> print(UVdata.data_structure)
    {
      "csdm": {
        "version": "0.0.11",
        "description": "A UV-vis spectra of benzene vapours.",
        "dimensions": [
          {
            "type": "linear",
            "number_of_points": 4001,
            "increment": "0.01 nm",
            "index_zero_value": "230.0 nm",
            "quantity": "length",
            "label": "wavelength",
            "reciprocal": {
              "quantity": "wavenumber"
            }
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "name": "Vapour of Benzene",
            "numeric_type": "float32",
            "component_labels": [
              "Absorbance"
            ],
            "components": [
              [
                "0.25890622, 0.25890622, ..., 0.16814752, 0.16814752"
              ]
            ]
          }
        ]
      }
    }
    >>> plot1D(UVdata)

.. image:: /_static/benzeneVapour_base64.csdf.pdf


----------------
(1,1)-D datasets
----------------

In this section, we illustrate the simplest subset of datasets, the 
(1,1)-D datasets. These datasets are one-dimensional in both controlled
and uncontrolled variables.
Let's start by first importing the `csdfpy` package. Here, we
also import the `matplotlib.pyplot` package for rendering the
plots.

.. doctest::

    >>> import csdfpy as cp
    >>> import matplotlib.pyplot as plt

Global Mean Sea Level rise dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following dataset is the Global Mean Sea Level (GMSL) rise from the Late
19th to the Early 21st Century. The original
`dataset <http://www.cmar.csiro.au/sealevel/sl_data_cmar.html>`_ was obtained
as a CSV file and subsequently converted to the CSD model format. Let's start
by loading the data file,

.. doctest::

    >>> filename = '../../test-datasets/gmsl/sea_level.csdf'
    >>> sea_level = cp.load(filename)

where the `filename` is a string with the local address to the `sea_level.csdf`
file.
The :py:meth:`~csdfpy.load` method of the `csdfpy` package reads the
file and returns an instance of the :ref:`CSDModel <csdm_api>` class, in
this case, the variable ``sea_level``. For a quick preview of the data
contents, use the :py:attr:`~csdfpy.CSDModel.data_structure` attribute of the
instance,

.. doctest::

    >>> print(sea_level.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "name": "Global Mean Sea Level",
            "unit": " mm",
            "quantity": "length",
            "component_labels": [
              "GMSL"
            ],
            "numeric_type": "float16",
            "components": "[-183.0, -183.0, ...... 59.7, 59.7]"
          }
        ],
        "controlled_variables": [
          {
            "reciprocal": {
              "quantity": "frequency"
            },
            "number_of_points": 1608,
            "sampling_interval": "0.08333333333333333 yr",
            "reference_offset": "-1880.0417 yr",
            "quantity": "time",
            "label": "Time"
          }
        ],
        "version": "0.0.9"
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

To access the tuples of controlled and the uncontrolled variables follow

.. doctest::

    >>> x = sea_level.controlled_variables
    >>> y = sea_level.uncontrolled_variables

respectively. The coordinates of the controlled variable, `x0`, and the
component of the uncontrolled variable, `y00`, are

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
method. This method makes it easier, later, when we describe (1,1)-D
examples form a variety of scientific datasets. The method follows,

.. doctest::

    >>> def plot1D(dataObject):
    ...     fig, ax = plt.subplots(1,1,  figsize=(3.4,2.1))

    ...     x = dataObject.controlled_variables
    ...     y = dataObject.uncontrolled_variables

    ...     x0 = x[0].coordinates
    ...     y00 = y[0].components[0]

    ...     ax.plot(x0, y00.real, color='k', linewidth=0.75)

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

Let's take a quick look at the ``plot1D`` method. The method accepts an
instance of the
:ref:`CSDModel <csdm_api>` class as an argument. Within the method, we make
use of the instance's attributes in addition to the matplotlib
functions. The first line creates a new blank figure. In the following four
lines, we define the `x`, `y`, `x0`, and `y00` as previously described. The
next line adds a plot of `y00` vs. `x0` to the figure. For labeling the
axes, we use the 
:py:attr:`~csdfpy.ControlledVariable.axis_label` attribute of both control and
uncontrol variable instances. For the figure title, we use the
:py:attr:`~csdfpy.UncontrolledVariable.name` attribute of the
uncontrol variable instances. The following `if` statement plot the figure with
the x-axis in reverse, if the 
:py:attr:`~csdfpy.ControlledVariable.reverse` attribute of the control
variable instance is True. The following two lines add a grid and and the range
of x-axis, respectively.
For additional information refer to the :ref:`cv_api`, :ref:`uv_api`, and the
`Matplotlib <https://matplotlib.org>`_ documentation.

Now to plot the ``sea_level`` dataset,

.. doctest::

    >>> plot1D(sea_level)

.. image:: /_static/sea_level.csdf.pdf


NMR dataset
^^^^^^^^^^^

The following dataset is a :math:`^{13}\mathrm{C}` NMR Bloch decay signal of
ethanol. Let's load the file and take a quick look at the data structure.

.. doctest::

    >>> filename = '../../test-datasets/NMR/blochDecay/blochDecay_raw.csdfx'
    >>> NMRdata = cp.load(filename)
    >>> print(NMRdata.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "numeric_type": "complex64",
            "components": "[(-8899.406-1276.7734j), (-8899.406-1276.7734j), ...... (37.548492+20.15689j), (37.548492+20.15689j)]"
          }
        ],
        "controlled_variables": [
          {
            "reciprocal": {
              "reference_offset": "-3005.363 Hz",
              "origin_offset": "75426328.864 Hz",
              "reverse": true,
              "quantity": "frequency",
              "label": "$^{13}$C frequency shift"
            },
            "number_of_points": 4096,
            "sampling_interval": "0.1 ms",
            "reference_offset": "0.3 ms",
            "quantity": "time"
          }
        ],
        "version": "0.0.9"
      }
    }

Unlike the previous example, the data structure of the NMR measurement reveals
a complexed value dataset. These complex values, `y00`, are the
component of the uncontrolled variable and are accessed as follows,

.. doctest::

    >>> y = NMRdata.uncontrolled_variables
    >>> y00 = y[0].components[0]
    >>> print(y00)
    [-8899.406   -1276.7734j  -4606.8804   -742.4125j
      9486.438    -770.0413j  ...   -70.95386   -28.32843j
        37.548492  +20.15689j  -193.92285   -67.06525j]

Similarly, the coordinates of the controlled variable, `x0`, are accessed as
follows,

.. doctest::

    >>> x = NMRdata.controlled_variables
    >>> x0 = x[0].coordinates
    >>> print(x0)
    [-3.000e-01 -2.000e-01 -1.000e-01 ...  4.090e+02  4.091e+02  4.092e+02] ms

Now to the plot the dataset,

.. doctest::

    >>> plot1D(NMRdata)

.. image:: /_static/blochDecay_raw.csdfx.pdf


EPR dataset
^^^^^^^^^^^

The following simulation of the
`EPR dataset <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_
is formerly received as a JCAMP-DX file and later converted to the
CSD model format. The data structure of the dataset and the corresponding
plot follows,

.. doctest::

    >>> filename = '../../test-datasets/EPR/xyinc2_base64.csdf'
    >>> EPRdata = cp.load(filename)
    >>> print(EPRdata.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "name": "Amanita.muscaria",
            "component_labels": [
              "Arbitrary"
            ],
            "numeric_type": "float32",
            "components": "[0.067, 0.067, ...... -0.035, -0.035]"
          }
        ],
        "controlled_variables": [
          {
            "number_of_points": 298,
            "sampling_interval": "4.0 G",
            "reference_offset": "-2750.0 G",
            "quantity": "magnetic flux density"
          }
        ],
        "version": "0.0.9"
      }
    }
    >>> plot1D(EPRdata)

.. image:: /_static/xyinc2_base64.csdf.pdf

Gas Chromatography dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^

The following
`Gas Chromatography dataset  <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_
is also obtained as a JCAMP-DX file and subsequently converted to the CSD model
format. The data structure and the plot of the gas chromatography dataset
follows,

.. doctest::

    >>> filename = '../../test-datasets/GC/cinnamon_none.csdf'
    >>> GCData = cp.load(filename)
    >>> print(GCData.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "name": "Headspace from cinnamon stick",
            "component_labels": [
              "Arbitrary"
            ],
            "numeric_type": "float32",
            "components": "[48453.0, 48453.0, ...... 48040.0, 48040.0]"
          }
        ],
        "controlled_variables": [
          {
            "reciprocal": {
              "quantity": "frequency"
            },
            "number_of_points": 6001,
            "sampling_interval": "0.0034 min",
            "quantity": "time"
          }
        ],
        "version": "0.0.9"
      }
    }
    >>> plot1D(GCData)

.. image:: /_static/cinnamon_none.csdf.pdf


FTIR dataset
^^^^^^^^^^^^

For the following 
`FTIR dataset  <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_,
we convert the original JCAMP-DX file to the CSD model format. The data
structure and the plot of the FTIR dataset follows

.. doctest::

    >>> filename = '../../test-datasets/IR/caffeine_none.csdf'
    >>> FTIRData = cp.load(filename)
    >>> print(FTIRData.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "name": "Caffeine",
            "component_labels": [
              "Transmittance"
            ],
            "numeric_type": "float32",
            "components": "[100.22944, 100.22944, ...... 99.08212, 99.08212]"
          }
        ],
        "controlled_variables": [
          {
            "reciprocal": {
              "quantity": "length"
            },
            "number_of_points": 1842,
            "sampling_interval": "1.930548614883216 cm^-1",
            "reference_offset": "-449.41 cm^-1",
            "reverse": true,
            "quantity": "wavenumber"
          }
        ],
        "version": "0.0.9"
      }
    }
    >>> plot1D(FTIRData)

.. image:: /_static/caffeine_none.csdf.pdf

Notice, the reverse axis of the FTIR wavenumber axis.

UV-vis dataset
^^^^^^^^^^^^^^

The following
`UV-vis dataset <http://wwwchem.uwimona.edu.jm/spectra/index.html>`_
is originally downloaded as a JCAMP-DX file and consequently turned to the CSD
model format. The data structure and the plot of the UV-vis dataset follows,

.. doctest::

    >>> filename = '../../test-datasets/UV-Vis/benzeneVapour_base64.csdf'
    >>> UVdata = cp.load(filename)
    >>> print(UVdata.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "name": "Vapour of Benzene",
            "component_labels": [
              "Absorbance"
            ],
            "numeric_type": "float32",
            "components": "[0.16786034, 0.16786034, ...... 0.25923702, 0.25923702]"
          }
        ],
        "controlled_variables": [
          {
            "reciprocal": {
              "quantity": "wavenumber"
            },
            "number_of_points": 4001,
            "sampling_interval": "0.01 nm",
            "reference_offset": "-230.0 nm",
            "reverse": true,
            "quantity": "length",
            "label": "wavelength"
          }
        ],
        "version": "0.0.9"
      }
    }
    >>> plot1D(UVdata)

.. image:: /_static/benzeneVapour_base64.csdf.pdf

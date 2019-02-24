
------------------------
:math:`(1,1)`-D datasets
------------------------

In this section, we illustrate the simplest group of datasets, :math:`(1,1)`-D
datasets, which are both one-dimensional control and uncontrol variable dataset.
Let's start by first importing the :guilabel:`csdfpy` package. Here, we
also import the :guilabel:`matplotlib.pyplot` package for producing plots. ::

    >>> import csdfpy as cp
    >>> import matplotlib.pyplot as plt

.. Since we will be describing :math:`(1,1)`-D examples for a number of scientific
.. datasets, it is convenient to define a common function for plotting the data
.. values. ::

..     >>> def plot1D(dataObject):
..     >>>     fig, ax = plt.subplots(1,1,  figsize=(3.4,2.1))

..     >>>     x = dataObject.controlled_variables
..     >>>     y = dataObject.uncontrolled_variables

..     >>>     ax.plot(x[0].coordinates,
..     >>>             y[0].components[0].real,
..     >>>             color='k', linewidth=0.75)

..     >>>     ax.set_xlabel(x[0].axis_label)
..     >>>     ax.set_ylabel(y[0].component_labels[0])
..     >>>     ax.set_title(y[0].name)

..     >>>     plt.tight_layout(pad=0., w_pad=0., h_pad=0.)
..     >>>     plt.savefig(dataObject.filename+'.pdf')
..     >>>     plt.show()

.. In the above function, the ``plot1D`` accepts an object of the
.. :ref:`CSDModel <csdm_api>` class as an argument. Within the function, we make
.. use of a number of attribute from this object. We will describe most of these
.. attribute as we procced with the examples. For more details, please refer to
.. :ref:`cv_api` and :ref:`uv_api`.

NMR dataset
^^^^^^^^^^^

Loading the file is as simple as, ::

    >>> filename = 'test/NMR/blochDecay/blochDecay_raw.csdfx'
    >>> NMRdata = cp.load(filename)

where `filename` contains the local address to the `.csdfx` or `.csdf` file.
The :py:meth:`~csdfpy.load` method of the :guilabel:`csdfpy` package reads the
file and return an object, in this case, ``NMRdata``, of the
:ref:`CSDModel <csdm_api>` class. For a quick preview of the data contents
from this object, use the :py:attr:`~csdfpy.CSDModel.data_structure` attribute.
This returns a JSON object as shown below. ::

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

.. note::
    The JSON output from the :py:attr:`~csdfpy.CSDModel.data_structure`
    attribute is not the same as
    the JSON serialization on file. This attribute is only intended for a quick
    preview of the data structure and avoids displaying large data. Do not use
    the value of this attribute to save the data to the file. Instead, use the
    :py:meth:`~csdfpy.CSDModel.save` method of the :ref:`CSDModel <csdm_api>`
    class.

The tuples of controlled and the uncontrolled variables are accessed with ::

    >>> x = NMRdata.controlled_variables
    >>> y = NMRdata.uncontrolled_variables

respectively. The coordinates of the controlled variable, ``x0``, and the
component of the uncontrolled variable, ``y00``, are ::

    >>> x0 = x[0].cooridnates
    >>> x0
    [-3.000e-01 -2.000e-01 -1.000e-01 ...  4.090e+02  4.091e+02  4.092e+02] ms
    >>> y00 = y[0].components[0]
    >>> y00
    [-8899.406   -1276.7734j  -4606.8804   -742.4125j
     9486.438    -770.0413j  ...   -70.95386   -28.32843j
     37.548492  +20.15689j  -193.92285   -67.06525j]


respectively. 

Before we plot the dataset, we find it convenient to write a small plotting
method. This method makes it easier, later, when we describe :math:`(1,1)`-D
examples form the number of scientific fields. The method follows, ::

    >>> def plot1D(dataObject):
    >>>     fig, ax = plt.subplots(1,1,  figsize=(3.4,2.1))

    >>>     x = dataObject.controlled_variables
    >>>     y = dataObject.uncontrolled_variables

    >>>     x0 = x[0].cooridnates
    >>>     y00 = y[0].components[0]

    >>>     ax.plot(x0, y00.real, color='k', linewidth=0.75)

    >>>     ax.set_xlabel(x[0].axis_label)
    >>>     ax.set_ylabel(y[0].axis_label[0])
    >>>     ax.set_title(y[0].name)
    >>>     if x[0].reverse:
    >>>         ax.invert_xaxis()

    >>>     plt.tight_layout(pad=0., w_pad=0., h_pad=0.)
    >>>     plt.savefig(dataObject.filename+'.pdf')
    >>>     plt.show()

A quick description of the ``plot1D`` method. The method accepts an
object of the
:ref:`CSDModel <csdm_api>` class as an argument. Within the method, we make
use of a number of attributes from this object in addition to the matplotlib
functions. The first line creates a new blank figure. In the following four
lines, we define ``x``, ``y``, ``x0``, and ``y00`` as previously described. The
next line adds a plot of ``y00`` vs ``x0`` to the figure. For labeling the
axes, we use the 
:py:attr:`~csdfpy.ControlledVariable.axis_label` attribute of both control and
uncontrol variable objects. For the figure title, we use the
:py:attr:`~csdfpy.UncontrolledVariable.name` attribute of the
uncontrol variable object. The following `if` statement plot the figure with
the x-axis in reverse, if the 
:py:attr:`~csdfpy.ControlledVariable.reverse` attribute of the control
variable is True.
Please refer to the :ref:`cv_api` and :ref:`uv_api` for additional
information.

Now to plot the ``NMRdata`` contents,

    >>> plot1D(NMRdata)

.. image:: /resource/blochDecay_raw.csdfx.pdf


EPR simulated dataset
^^^^^^^^^^^^^^^^^^^^^
Similarly, ::

    >>> filename = 'test/EPR/xyinc2_base64.csdf'
    >>> EPRdata = cp.load(filename)
    >>> print(EPRdata.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "name": "Vanadyl in Amanita muscaria",
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

.. image:: /resource/xyinc2_base64.csdf.pdf


Gas Chromatography dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    >>> filename = 'test/GC/cinnamon_none.csdf'
    >>> GCData = cp.load(filename)
    >>> print(GCData.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "name": "cinnamon stick",
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

.. image:: /resource/cinnamon_none.csdf.pdf


FTIR dataset
^^^^^^^^^^^^
::

    >>> filename = 'test/IR/caffeine_none.csdf'
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

.. image:: /resource/caffeine_none.csdf.pdf


UV-vis dataset
^^^^^^^^^^^^^^

    >>> filename = 'test/UV-Vis/benzeneVapour_base64.csdf'
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
            "components": "[0.25890622, 0.25890622, ...... 0.16814752, 0.16814752]"
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

.. image:: /resource/benzeneVapour_base64.csdf.pdf

Global Mean Sea Level dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    >>> filename = 'test/gmsl/sea_level.csdf'
    >>> sea_level = cp.load(filename)
    >>> print (sea_level.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "name": "Global Mean Sea Level",
            "component_labels": [
              "GMSL (mm)"
            ],
            "numeric_type": "float64",
            "components": "[-183.0, -183.0, ...... 59.7, 59.7]"
          }
        ],
        "controlled_variables": [
          {
            "reciprocal": {
              "quantity": "frequency"
            },
            "number_of_points": 1608,
            "sampling_interval": "0.083333333 yr",
            "reference_offset": "-1880.0417 yr",
            "quantity": "time",
            "label": "Time"
          }
        ],
        "version": "0.0.9"
      }
    }

    >>> plot1D(sea_level)


.. image:: /resource/sea_level.csdf.pdf
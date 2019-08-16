
.. testsetup::

    >>> import matplotlib
    >>> font = {'family': 'normal', 'weight': 'light', 'size': 9};
    >>> matplotlib.rc('font', **font)
    >>> from os import path

Meteorological, 2D{1,1,2,1,1} dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The following dataset is obtained from `NOAA/NCEP Global Forecast System (GFS) Atmospheric Model
<https://coastwatch.pfeg.noaa.gov/erddap/griddap/NCEP_Global_Best.graph?ugrd10m[(2017-09-17T12:00:00Z)][(-4.5):(52.0)][(275.0):(331.5)]&.draw=surface&.vars=longitude%7Clatitude%7Cugrd10m&.colorBar=%7C%7C%7C%7C%7C&.bgColor=0xffccccff>`_
and subsequently converted to the CSD model file-format.
The dataset consists of two spatial dimensions describing the geographical
coordinates of the earth surface and five dependent variables with
1) surface temperature, 2) air temperature at 2 m, 3) relative humidity,
4) air pressure at sea level as the four `scalar` quantity_type dependent
variable, and 5) wind velocity as the two-component `vector`, quantity type
dependent variable.

Let's import the `csdmpy` module and load this dataset.

.. doctest::

    >>> import csdmpy as cp

    >>> filename = 'Test Files/correlatedDataset/forecast/NCEI.csdfe'
    >>> multi_dataset = cp.load(filename)

Let's get the tuple of dimension and dependent variable objects from
``multi_dataset`` instance.

.. doctest::

    >>> x = multi_dataset.dimensions
    >>> y = multi_dataset.dependent_variables

.. testsetup::

    >>> print(multi_dataset.data_structure)
    {
      "csdm": {
        "version": "1.0",
        "read_only": true,
        "timestamp": "2017-09-17T12:00:00Z",
        "description": "The dataset is obtained from NOAA/NCEP Global Forecast System (GFS) Atmospheric Model. The label for components are the standard attribute names used by the Dataset Attribute Structure (.das)",
        "dimensions": [
          {
            "type": "linear",
            "description": "The latitude are defined in the geographic coordinate system.",
            "count": 192,
            "increment": "0.5 °",
            "coordinates_offset": "-96.0 °",
            "quantity_name": "plane angle",
            "label": "longitude"
          },
          {
            "type": "linear",
            "description": "The latitude are defined in the geographic coordinate system.",
            "count": 89,
            "increment": "0.5 °",
            "coordinates_offset": "-4.0 °",
            "quantity_name": "plane angle",
            "label": "latitude"
          }
        ],
        "dependent_variables": [
          {
            "type": "internal",
            "description": "The label 'tmpsfc' is the standard attribute name for 'surface air temperature'.",
            "name": "Surface temperature",
            "unit": "K",
            "quantity_name": "temperature",
            "numeric_type": "float64",
            "quantity_type": "scalar",
            "component_labels": [
              "tmpsfc - surface air temperature"
            ],
            "components": [
              [
                "292.8152160644531, 293.0152282714844, ..., 301.8152160644531, 303.8152160644531"
              ]
            ]
          },
          {
            "type": "internal",
            "description": "The label 'tmp2m' is the standard attribute name for 'air temperature at 2m'.",
            "name": "Air temperature at 2m",
            "unit": "K",
            "quantity_name": "temperature",
            "numeric_type": "float64",
            "quantity_type": "scalar",
            "component_labels": [
              "tmp2m - air temperature at 2m"
            ],
            "components": [
              [
                "293.2685852050781, 293.36859130859375, ..., 290.0685729980469, 295.4685974121094"
              ]
            ]
          },
          {
            "type": "internal",
            "description": ". The label 'ugrd10m' is the standard attribute name for 'eastward wind velocity at 10 m above ground level', and the label 'vgrd10m', 'northward wind velocity at 10 m above ground level'.",
            "name": "Wind velocity",
            "unit": "m * s^-1",
            "quantity_name": "speed",
            "numeric_type": "float64",
            "quantity_type": "vector_2",
            "component_labels": [
              "ugrd10m - eastward wind velocity at 10m",
              "vgrd10m - northward wind velocity at 10m"
            ],
            "components": [
              [
                "-4.147548675537109, -4.427548885345459, ..., 4.262451171875, 1.7124511003494263"
              ],
              [
                "4.672541618347168, 4.622541427612305, ..., 2.7525415420532227, 3.162541389465332"
              ]
            ]
          },
          {
            "type": "internal",
            "description": "The label 'rh2m' is the standard attribute name for 'relative humidity at 2m'.",
            "name": "Relative humidity",
            "unit": "%",
            "numeric_type": "float64",
            "quantity_type": "scalar",
            "component_labels": [
              "rh2m - relative humidity at 2m"
            ],
            "components": [
              [
                "88.0, 86.80000305175781, ..., 32.60000228881836, 28.399999618530273"
              ]
            ]
          },
          {
            "type": "internal",
            "description": "The label 'prmslmsl is the standard attribute name for 'mean sea level pressure'.",
            "name": "Air pressure at sea level",
            "unit": "Pa",
            "quantity_name": "pressure",
            "numeric_type": "float64",
            "quantity_type": "scalar",
            "component_labels": [
              "prmslmsl - mean sea level pressure"
            ],
            "components": [
              [
                "101311.3515625, 101315.5546875, ..., 101779.75, 101787.1484375"
              ]
            ]
          }
        ]
      }
    }

The dataset contains two dimension objects representing the `longitude` and
`latitude` of the earth's surface. The respective dimensions are labeled as

.. doctest::

    >>> x[0].label
    'longitude'

    >>> x[1].label
    'latitude'

There are a total of five dependent variables stored in this dataset. The first
dependent variable is the surface air temperature. The data structure of this
dependent variable is

.. doctest::

    >>> print(y[0].data_structure)
    {
      "type": "internal",
      "description": "The label 'tmpsfc' is the standard attribute name for 'surface air temperature'.",
      "name": "Surface temperature",
      "unit": "K",
      "quantity_name": "temperature",
      "numeric_type": "float64",
      "quantity_type": "scalar",
      "component_labels": [
        "tmpsfc - surface air temperature"
      ],
      "components": [
        [
          "292.8152160644531, 293.0152282714844, ..., 301.8152160644531, 303.8152160644531"
        ]
      ]
    }

If you have followed all previous examples, the above data structure should
be self-explanatory. The following snippet plots a dependent variable
of scalar `quantity_type`.

.. tip:: **Plotting a scalar intensity plot**

  .. doctest::

      >>> import numpy as np
      >>> import matplotlib.pyplot as plt
      >>> from mpl_toolkits.axes_grid1 import make_axes_locatable

      >>> def plot_scalar(yx):
      ...     fig, ax = plt.subplots(1,1, figsize=(6,3))
      ...
      ...     # Set the extents of the image plot.
      ...     extent = [x[0].coordinates[0].value, x[0].coordinates[-1].value,
      ...               x[1].coordinates[0].value, x[1].coordinates[-1].value]
      ...
      ...     # Add the image plot.
      ...     im = ax.imshow(yx.components[0], origin='lower', extent=extent,
      ...                    cmap='coolwarm')
      ...
      ...     # Add a colorbar.
      ...     divider = make_axes_locatable(ax)
      ...     cax = divider.append_axes("right", size="5%", pad=0.05)
      ...     cbar = fig.colorbar(im, cax)
      ...     cbar.ax.set_ylabel(yx.axis_label[0])
      ...
      ...     # Set up the axes label and figure title.
      ...     ax.set_xlabel(x[0].axis_label)
      ...     ax.set_ylabel(x[1].axis_label)
      ...     ax.set_title(yx.name)
      ...
      ...     # Set up the grid lines.
      ...     ax.grid(color='k', linestyle='--', linewidth=0.5)
      ...
      ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
      ...     plt.show()

.. testsetup::

    >>> def plot_scalar_save(yx, dataObject):
    ...     fig, ax = plt.subplots(1,1, figsize=(6,3))
    ...
    ...     # Set the extents of the image plot.
    ...     extent = [x[0].coordinates[0].value, x[0].coordinates[-1].value,
    ...               x[1].coordinates[0].value, x[1].coordinates[-1].value]
    ...
    ...     # Add the image plot.
    ...     im = ax.imshow(yx.components[0], origin='lower', extent=extent,
    ...                    cmap='coolwarm')
    ...
    ...     # Add a colorbar.
    ...     divider = make_axes_locatable(ax)
    ...     cax = divider.append_axes("right", size="5%", pad=0.05)
    ...     cbar = fig.colorbar(im, cax)
    ...     cbar.ax.set_ylabel(yx.axis_label[0])
    ...
    ...     # Set up the axes label and figure title.
    ...     ax.set_xlabel(x[0].axis_label)
    ...     ax.set_ylabel(x[1].axis_label)
    ...     ax.set_title(yx.name)
    ...
    ...     # Set up the grid lines.
    ...     ax.grid(color='k', linestyle='--', linewidth=0.5)
    ...
    ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    ...     filename = path.split(dataObject.filename)[1]
    ...     filepath = './docs/_images'
    ...     pth = path.join(filepath, filename)
    ...     plt.savefig(pth+yx.name.replace(' ', '')+'.pdf')
    ...     plt.savefig(pth+yx.name.replace(' ', '')+'.png', dpi=100)
    ...     plt.close()

Now to plot the data from the dependent variable.

.. doctest::

    >>> plot_scalar(y[0])

.. testsetup::

    >>> plot_scalar_save(y[0], multi_dataset)

.. figure:: ../../_images/NCEI.csdfeSurfacetemperature.*
    :figclass: figure-polaroid

Similarly, other dependent variables with their respective plots are

.. doctest::

    >>> y[1].name
    'Air temperature at 2m'
    >>> plot_scalar(y[1])

.. testsetup::

    >>> plot_scalar_save(y[1], multi_dataset)

.. figure:: ../../_images/NCEI.csdfeAirtemperatureat2m.*
    :figclass: figure-polaroid

.. doctest::

    >>> y[3].name
    'Relative humidity'
    >>> plot_scalar(y[3])

.. testsetup::

    >>> plot_scalar_save(y[3], multi_dataset)

.. figure:: ../../_images/NCEI.csdfeRelativehumidity.*
    :figclass: figure-polaroid

.. doctest::

    >>> y[4].name
    'Air pressure at sea level'
    >>> plot_scalar(y[4])

.. testsetup::

    >>> plot_scalar_save(y[4], multi_dataset)

.. figure:: ../../_images/NCEI.csdfeAirpressureatsealevel.*
    :figclass: figure-polaroid

Notice, we didn't plot the dependent variable at index 2. This is because this
particular dependent variable is a vector dataset representing the wind
velocity.

.. doctest::

    >>> y[2].quantity_type
    'vector_2'
    >>> y[2].name
    'Wind velocity'

To visualize the vector data, we use matplotlib streamline plot.

.. tip:: **Plotting a vector quiver plot**

  .. doctest::

      >>> def plot_vector(yx):
      ...     fig, ax = plt.subplots(1,1, figsize=(6,3))
      ...     X, Y = np.meshgrid(x[0].coordinates, x[1].coordinates)
      ...     magnitude = np.sqrt(yx.components[0]**2 + yx.components[1]**2)
      ...
      ...     cf = ax.quiver(x[0].coordinates, x[1].coordinates,
      ...                    yx.components[0], yx.components[1],
      ...                    magnitude, pivot ='middle', cmap='inferno')
      ...     divider = make_axes_locatable(ax)
      ...     cax = divider.append_axes("right", size="5%", pad=0.05)
      ...     cbar = fig.colorbar(cf, cax)
      ...     cbar.ax.set_ylabel(yx.name+' / '+str(yx.unit))
      ...
      ...     ax.set_xlim([x[0].coordinates[0].value, x[0].coordinates[-1].value])
      ...     ax.set_ylim([x[1].coordinates[0].value, x[1].coordinates[-1].value])
      ...
      ...     # Set axes labels and figure title.
      ...     ax.set_xlabel(x[0].axis_label)
      ...     ax.set_ylabel(x[1].axis_label)
      ...     ax.set_title(yx.name)
      ...
      ...     # Set grid lines.
      ...     ax.grid(color='gray', linestyle='--', linewidth=0.5)
      ...
      ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
      ...     plt.show()

.. doctest::

    >>> plot_vector(y[2])

.. testsetup::

    >>> def plot_vector_save(yx, dataObject):
    ...     fig, ax = plt.subplots(1,1, figsize=(6,3))
    ...     X, Y = np.meshgrid(x[0].coordinates, x[1].coordinates)
    ...     magnitude = np.sqrt(yx.components[0]**2 + yx.components[1]**2)
    ...
    ...     cf = ax.quiver(x[0].coordinates, x[1].coordinates,
    ...                    yx.components[0], yx.components[1],
    ...                    magnitude, pivot ='middle', cmap='inferno')
    ...     divider = make_axes_locatable(ax)
    ...     cax = divider.append_axes("right", size="5%", pad=0.05)
    ...     cbar = fig.colorbar(cf, cax)
    ...     cbar.ax.set_ylabel(yx.name+' / '+str(yx.unit))
    ...
    ...     ax.set_xlim([x[0].coordinates[0].value, x[0].coordinates[-1].value])
    ...     ax.set_ylim([x[1].coordinates[0].value, x[1].coordinates[-1].value])
    ...
    ...     # Set axes labels and figure title.
    ...     ax.set_xlabel(x[0].axis_label)
    ...     ax.set_ylabel(x[1].axis_label)
    ...     ax.set_title(yx.name)
    ...
    ...     # Set grid lines.
    ...     ax.grid(color='gray', linestyle='--', linewidth=0.5)
    ...
    ...     plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    ...     filename = path.split(dataObject.filename)[1]
    ...     filepath = './docs/_images'
    ...     pth = path.join(filepath, filename)
    ...     plt.savefig(pth+yx.name.replace(' ', '')+'.png', dpi=100)
    ...     plt.close()

.. testsetup::

    >>> plot_vector_save(y[2], multi_dataset)

.. figure:: ../../_images/NCEI.csdfeWindvelocity.*
    :figclass: figure-polaroid

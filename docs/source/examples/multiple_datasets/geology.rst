

------------------
Correlated Dataset
------------------

The core scientific dataset model also support multiple dependent variables
that share the same coordinate grid. We call the dataset with multiple
dependent variables as correlated datasets.

In this section, we go over a few examples.


Geological dataset
^^^^^^^^^^^^^^^^^^

Import the `csdmpy` model and load the dataset. Here, we additionally import
numpy and matplotlib modules.

.. doctest::

    >>> import csdmpy as cp
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt

    >>> filename = '../test-datasets0.0.12/multipleDatasets/05/NCEP_Global05_raw.csdfe'
    >>> multi_dataset = cp.load(filename)
    >>> print(multi_dataset.data_structure)
    {
      "csdm": {
        "version": "0.0.12",
        "description": "The dataset is obtained from NOAA/NCEP Global Forecast System (GFS) Atmospheric Model. The label for components are the standard attribute names used by the Dataset Attribute Structure (.das)",
        "dimensions": [
          {
            "type": "linear",
            "description": "The latitude are defined in the geographic coordinate system.",
            "count": 192,
            "increment": "0.5 °",
            "coordinates_offset": "264.0 °",
            "quantity_name": "angle",
            "label": "longitude"
          },
          {
            "type": "linear",
            "description": "The latitude are defined in the geographic coordinate system.",
            "count": 89,
            "increment": "0.5 °",
            "coordinates_offset": "-4.0 °",
            "quantity_name": "angle",
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
              "tmpsfc"
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
              "tmp2m"
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
              "ugrd10m",
              "vgrd10m"
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
              "rh2m"
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
              "prmslmsl"
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

From the data structure one finds two dimensions labeled as `longitude`
`latitude` respectively, and five dependent variables named as
Surface temperature, Air temperature at 2m, Wind velocity, Relative humidity,
and Air pressure at sea level. Lets take a look at individual dependent
variables.

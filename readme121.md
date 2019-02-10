# MRData

`MRData` is a python module for importing and exporting data using .jsdts/.jsdtx studium data model file formats.

The studium data model is designed to encapsulate the minimum information required to correctly interpret the data coordinates of the dataset.  It is not intended to encapsulate any information on how the data might be acquired, processed or displayed.



```
from studium import dataModel as dtm

# a is the dataset object
a=dtm()

d1={'number_of_points':384,
    'sampling_interval': "1 Hz",
    'reference_offset': "0 Hz"}

a.addControlledVariable(d1) # creates a gcv-object
print (a)

class Dimension(*args, **kwds)

Parameters
----------

- number_of_points : integer. The number of points along the uniformaly sampled dimension.

- periodic: boolean. The default is false. Specify whether the dimension is treated as periodic.

- quantity: string. The default is ''. The physical quantity name specifying the dimension.

- unit: The unit associated with the dimension.

    - label
    - reverse
    - reference_offset
    - origin_offset
    - sampling_interval
    - made_dimensionless
    - inverse_label
    - inverse_reverse
    - inverse_reference_offset
    - inverse_origin_offset
    - inverse_sampling_interval
    - inverse_made_dimensionless

Methods

    - getJsonDictionary()
        Returns the dimension object as a jaon object

    
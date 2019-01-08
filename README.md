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
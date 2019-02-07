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

    
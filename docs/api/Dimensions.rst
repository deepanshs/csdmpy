.. _dim_api:

---------
Dimension
---------

.. toctree::
    :maxdepth: 2
    :caption: Dimension subtypes

    dimension/linear
    dimension/monotonic
    dimension/labeled


.. currentmodule:: csdmpy

.. autoclass:: Dimension
    :show-inheritance:

    .. rubric:: Attributes Summary

    .. autosummary::
       :nosignatures:

        ~Dimension.type
        ~Dimension.description
        ~Dimension.application
        ~Dimension.coordinates
        ~Dimension.absolute_coordinates
        ~Dimension.count
        ~Dimension.increment
        ~Dimension.coordinates_offset
        ~Dimension.origin_offset
        ~Dimension.complex_fft
        ~Dimension.quantity_name
        ~Dimension.label
        ~Dimension.labels
        ~Dimension.period
        ~Dimension.axis_label
        ~Dimension.data_structure

    .. rubric:: Methods Summary

    .. autosummary::
       :nosignatures:

        ~Dimension.to
        ~Dimension.to_dict
        ~Dimension.is_quantitative
        ~Dimension.copy
        ~Dimension.reciprocal_coordinates
        ~Dimension.reciprocal_increment


    .. rubric:: Attributes Documentation

    .. autoattribute:: type
    .. autoattribute:: description
    .. autoattribute:: application
    .. autoattribute:: coordinates
    .. autoattribute:: absolute_coordinates
    .. autoattribute:: count
    .. autoattribute:: increment
    .. autoattribute:: coordinates_offset
    .. autoattribute:: origin_offset
    .. autoattribute:: complex_fft
    .. autoattribute:: quantity_name
    .. autoattribute:: label
    .. autoattribute:: labels
    .. autoattribute:: period
    .. autoattribute:: axis_label
    .. autoattribute:: data_structure


    .. rubric:: Method Documentation

    .. automethod:: to
    .. automethod:: to_dict
    .. automethod:: is_quantitative
    .. automethod:: copy
    .. automethod:: reciprocal_coordinates
    .. automethod:: reciprocal_increment

.. _csdm_api:

----
CSDM
----

.. currentmodule:: csdmpy
.. autoclass:: CSDM
   :show-inheritance:

   .. rubric:: Attributes Summary
   .. autosummary::
      :nosignatures:

      ~CSDM.version
      ~CSDM.description
      ~CSDM.read_only
      ~CSDM.tags
      ~CSDM.timestamp
      ~CSDM.geographic_coordinate
      ~CSDM.dimensions
      ~CSDM.dependent_variables
      ~CSDM.application
      ~CSDM.data_structure
      ~CSDM.filename

   .. rubric:: Methods summary
   .. autosummary::
      :nosignatures:

      ~CSDM.add_dimension
      ~CSDM.add_dependent_variable
      ~CSDM.to_dict
      ~CSDM.dumps
      ~CSDM.astype
      ~CSDM.save
      ~CSDM.copy
      ~CSDM.split

   .. rubric:: Numpy compatible attributes summary
   .. autosummary::
      :nosignatures:

      ~CSDM.real
      ~CSDM.imag
      ~CSDM.shape
      ~CSDM.T

   .. rubric:: Numpy compatible method summary
   .. autosummary::
      :nosignatures:

      ~CSDM.max
      ~CSDM.min
      ~CSDM.clip
      ~CSDM.conj
      ~CSDM.round
      ~CSDM.sum
      ~CSDM.mean
      ~CSDM.var
      ~CSDM.std
      ~CSDM.prod

   .. rubric:: Attributes documentation

   .. autoattribute:: version
   .. autoattribute:: description
   .. autoattribute:: read_only
   .. autoattribute:: tags
   .. autoattribute:: timestamp
   .. autoattribute:: geographic_coordinate
   .. autoattribute:: dimensions
   .. autoattribute:: dependent_variables
   .. autoattribute:: application
   .. autoattribute:: data_structure
   .. autoattribute:: filename

   .. rubric:: Numpy compatible attributes documentation

   .. autoattribute:: real
   .. autoattribute:: imag
   .. autoattribute:: shape
   .. autoattribute:: T

   .. rubric:: Methods documentation

   .. automethod:: add_dimension
   .. automethod:: add_dependent_variable
   .. automethod:: to_dict
   .. automethod:: dumps
   .. automethod:: save
   .. automethod:: to_list
   .. automethod:: astype
   .. automethod:: copy
   .. automethod:: split
   .. automethod:: transpose
   .. automethod:: fft

   .. rubric:: Numpy compatible method documentation

   .. automethod:: max
   .. automethod:: min
   .. automethod:: clip
   .. automethod:: conj
   .. automethod:: round
   .. automethod:: sum
   .. automethod:: mean
   .. automethod:: var
   .. automethod:: std
   .. automethod:: prod

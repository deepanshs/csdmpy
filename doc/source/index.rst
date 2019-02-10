.. CSDM documentation master file, created by
   sphinx-quickstart on Thu Feb  7 23:05:02 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to csdfpy's documentation!
====================================

.. ``csdfpy`` is a python module for handling ``.csdf`` and ``.csdfx`` files.
.. This module is build on the idea of core scientific dataset format which
.. includes the core scientific dataset (CSD) model. The CSD model is designed 
.. to be *light-weight*, 
.. *portable*, *versatile*, and *standalone*. The CSD model only encapsulates 
.. data values and minimum metadata, to accurately describe the data coordinates 
.. and coordinates metadata. The model is not intended to encapsulate any 
.. information on how the data might be acquired, processed or visualized. 
.. The data model is versatile in allowing many use cases for any number of 
.. experiments from most spectroscopy, diffraction, and imaging measurements. 
.. As such the CSD model supports datasets associated with continuous physical 
.. quantities that are discretely sampled in a multi-dimensional space associated 
.. with other carefully controlled continuous physical quantities, for e.g., a mass 
.. as a function of temperature, a current as a function of voltage and time, a 
.. signal voltage as a function of magnetic field gradient strength, etc. It also 
.. supports datasets associated with multi-component data values. For example, the 
.. left and right audio components as a function of time, a color image with a red, 
.. green, and blue (RBG) light intensity components as a function of two independent 
.. spatial dimensions, and the six components of the symmetric second-rank diffusion 
.. tensor MRI as a function of three independent spatial dimensions. Additionally, 
.. the CSD model also supports multiple datasets when identically sampled over the 
.. same set of controlled variables. For instance, the current and voltage as a 
.. function of time where current and voltage are two datasets sampled over the 
.. same temporal coordinates. 

.. The CSD model is independent of the hardware, operating system, application 
.. software, programming language, and object-oriented file-serialization format 
.. used in writing the CSD model to the file.
.. The serialized data file is easily human readable and also easily integrable 
.. with any number of programming languages and field related application-software.


.. .. autoclass:: csdfpy.CSDModel


.. toctree::
    :maxdepth: 2
    :caption: Table of Contents
    :name: mastertoc
    :numbered:

    requirement
    CSDModel
    Importing_csdfpy
    controlled_variables
    referenceAPI






Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

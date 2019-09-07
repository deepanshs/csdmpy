
--------------------
How to save datasets
--------------------

An instance of a :ref:`csdm_api` object is serialized as a csdf/csdfe
JSON-format file with the :meth:`~csdmpy.csdm.CSDM.save` method.
While serialized a dependent-variable from a CSDM object to the data-file,
`csdmpy` module uses the value of the dependent variable's
:attr:`~csdmpy.dependent_variables.DependentVariable.encoding` attribute to
determine the encoding type before serialization. There are three types of
encoding for dependent variables:

- none
- base64
- raw

.. note:: By default, all instances of
    :attr:`~csdmpy.dependent_variables.DependentVariable` from a
    :attr:`~csdmpy.csdm.CSDM` object are serialized as
    base64 strings.

For the following examples, consider ``data`` as an instance of the
:attr:`~csdmpy.csdm.CSDM` class.

Serializing dependent-variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To serialize a dependent variable with a given encoding type, set the value
of it's encoding attribute to the respective encoding. For example,

**As ``none`` encoding**

.. code::

    >>> data.dependent_variables[0].encoding = "none"
    >>> data.save('my_file.csdf')

This will serialize the components from the dependent variable at index 0 to a
JSON file, `my_file.csdf`, where each component of the dependent variable is
serialized as an array of JSON number.

**As ``base64`` encoding**

    >>> data.dependent_variables[0].encoding = "base64"
    >>> data.save('my_file.csdf')

This will serialize the components from the dependent variable at index 0 to a
JSON file, `my_file.csdf`, where each component of the dependent variable is
serialized as a base64 string.

**As ``raw`` encoding**

    >>> data.dependent_variables[0].encoding = "raw"
    >>> data.save('my_file.csdfe')

This will serialize the metadata from the dependent variable at index 0 to a
JSON file, `my_file.csdfe`, which includes a link to an external file where the
components of the respective dependent variable are serialized as a binary
array. The binary file is named, `my_file_0.dat`, where `my_file` is the
filename from the argument of the save method, and `0` is the index number of
the dependent variable from the CSDM object.

**Multiple encoding types**

In the case of multiple dependent-variables, you may also choose to serialize
each dependent variables with a different encoding, for example,

.. code::

    >>> my_data.dependent_variables[0].encoding = "raw"
    >>> my_data.dependent_variables[1].encoding = "base64"
    >>> my_data.dependent_variables[2].encoding = "none"
    >>> my_data.dependent_variables[3].encoding = "base64"
    >>> my_data.save('my_file.csdfe')

In the above example, ``my_data`` is a CSDM object containing four
:attr:`~csdmpy.dependent_variables.DependentVariable` objects. Here, we
serialize the dependent variable at index 2 with ``none`` encoding,
the dependent variables at index 1 and 3 as ``bae64``,
and the dependent variables at index 0 as ``raw``.

.. note:: Because one instance of the dependent variable, that is, at index
    0 is set to be serialized as an external subtype, the corresponding file
    should be saved with a `.csdfe` extension.

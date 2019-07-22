
=======================================
The core scientific dataset (CSD) model
=======================================

The core scientific dataset (CSD) model is a *light-weight*, *portable*,
*versatile*, and *standalone* data model capable of handling a variety of
scientific datasets. The model only encapsulates
data values and the minimum metadata, to accurately represent a `p`-component
dependent variable,
:math:`\mathbf{U}\equiv(\mathbf{U}_0, ... \mathbf{U}_q, ... \mathbf{U}_{p-1})`,
discretely sampled at `M` unique points in a `d`-dimensional coordinate space
:math:`(\mathbf{X}_0, \mathbf{X}_1, ... \mathbf{X}_k, ... \mathbf{X}_{d-1})`.
The model is not intended to encapsulate
any information on how the data might be acquired, processed or visualized.

The data model is *versatile* in allowing many use cases for most spectroscopy,
diffraction, and imaging techniques. As
such the model supports multi-component datasets associated with continuous
physical quantities that are discretely sampled in a multi-dimensional space
associated with other carefully controlled quantities, for e.g., a mass as a
function of temperature, a current as a function of voltage and time, a signal
voltage as a function of magnetic field gradient strength, a color image with
a red, green, and blue (RBG) light intensity components as a
function of two independent spatial dimensions, or the six components of the
symmetric second-rank diffusion tensor MRI as a function of three independent
spatial dimensions. Additionally, the model supports multiple datasets sharing
the same dimensions. For instance,
the simultaneous measurement of the current and voltage as a function of time.
Another example would be the simultaneous acquisition of air temperature,
pressure, wind velocity, and
solar-flux as a function of Earth’s latitude and longitude coordinates. We
refer to these simultaneous datasets as `correlated-datasets`.

The CSD model is *standalone* because it is independent of the hardware,
operating system, application software, programming language, and the
object-oriented file-serialization format utilized in writing the CSD model to
the file. Out of numerous file serialization formats, XML, JSON, property list,
we adopt the data-exchange oriented JSON (JavaScript Object Notation) file-
serialization format because it is `human readable`, if properly organized, and
`easily integrable` with any number of programming languages and field related
application-software.

.. The serialization file names are designated with two possible extensions: .csdf
.. and .csdfe, the acronyms for Core Scientific Dataset Format and Core Scientific
.. Dataset Format External. When all data values are stored within the serialized
.. file, a `.csdf` file extension is used otherwise a `.csdfe` file extension.
.. This difference in extensions is intended to alert the
.. end user to a possible risk of failure if the external data file is
.. inaccessible when deserializing a file with the .csdfe file extensions.

.. The model allows two types of file extensions for the JSON file-serialization,
.. `.csdf` and `.csdfe`, the acronyms for the Core Scientific Dataset Format and
.. the Core Scientific Dataset Format eXternal. The two file extensions act as a
.. medium to convey the end users whether the data values are present within the
.. file (`.csdf`) or in an external file on a local or remote server (`.csdfe`).


.. toctree::
    :maxdepth: 2
    :caption: Table of Contents

    CSDmodel_uml/dimension

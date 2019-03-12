
=======================================
The core scientific dataset (CSD) model
=======================================

The core scientific dataset (CSD) model is a *light-weight*, *portable*,
*versatile*, and *standalone* data model capable of handling a variety of
scientific datasets.

The model is *light-weight* because it only encapsulates
data values and the minimum metadata, to accurately represent a `p`-component
dependent variable, :math:`y`, discretely sampled at `N` unique points in a
`d`-dimensional independent variable coordinate space
:math:`(x_0, x_1, ... x_k, ... x_{d-1})`.
The model is not intended to encapsulate
any information on how the data might be acquired, processed or visualized.

The data model is *versatile* in allowing many use cases for any number of
experiments from most spectroscopy, diffraction, and imaging techniques. As
such the model supports datasets associated with continuous physical quantities
that are discretely sampled in a multi-dimensional space associated with other
carefully controlled continuous physical quantities, for e.g., a mass as a
function of temperature, a current as a function of voltage and time, a signal
voltage as a function of magnetic field gradient strength, etc. The CSD model
also supports datasets associated with multi-component data values. For
example, a color image with a red, green, and blue (RBG) light intensity
components as a
function of two independent spatial dimensions, or the six components of the
symmetric second-rank diffusion tensor MRI as a function of three independent
spatial dimensions. Additionally, the model supports multiple datasets when
simultaneously sampled over the same set of dependent variables. For instance,
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
serialization format because it is `human readable` if properly organized and
`easily integrable` with any number of programming languages and field related
application-software.

The serialization file names are designated with two possible extensions: .csdf
and .csdfe, the acronyms for Core Scientific Dataset Format and Core Scientific
Dataset Format External. When all data values are stored within the serialized
file, a `.csdf` file extension is used otherwise a `.csdfe` file extension.
This difference in extensions is intended to alert the
end user to a possible risk of failure if the external data file is
inaccessible when deserializing a file with the .csdfe file extensions.

.. The model allows two types of file extensions for the JSON file-serialization,
.. `.csdf` and `.csdfx`, the acronyms for the Core Scientific Dataset Format and
.. the Core Scientific Dataset Format eXternal. The two file extensions act as a
.. medium to convey the end users whether the data values are present within the
.. file (`.csdf`) or in an external file on a local or remote server (`.csdfx`).

**CSD model expression**

In mathematical notations, the CSD model is expressed as,

.. math::

    y = f(x_0, x_1, ... x_k, ... x_{d-1})

where :math:`y` is the dependent variable and the :math:`x_k`,
:math:`k \in \{0, 1, ... ,d-1\}`, are the independent variables.

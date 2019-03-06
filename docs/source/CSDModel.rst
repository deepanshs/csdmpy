

=======================================
The core scientific dataset (CSD) model
=======================================

The core scientific dataset (CSD) model is a *light-weight*, *portable*,
*versatile*, and *standalone* data model capable of handling a variety of
scientific datasets. The model is *light-weight* because it only encapsulates
data values and the minimum metadata, to accurately describe the data
coordinates and coordinates metadata. The model is not intended to encapsulate
any information on how the data might be acquired, processed or visualized.
The data model is *versatile* in allowing many use cases for any number of
experiments from most spectroscopy, diffraction, and imaging techniques. As
such the model supports datasets associated with continuous physical quantities
that are discretely sampled in a multi-dimensional space associated with other
carefully controlled continuous physical quantities, for e.g., a mass as a
function of temperature, a current as a function of voltage and time, a signal
voltage as a function of magnetic field gradient strength, etc. The CSD model
also supports datasets associated with multi-component data values. For
example, the left and right audio components as a function of time, a color
image with a red, green, and blue (RBG) light intensity components as a
function of two independent spatial dimensions, or the six components of the
symmetric second-rank diffusion tensor MRI as a function of three independent
spatial dimensions. Additionally, the model supports multiple datasets when
identically sampled over the same set of controlled variables. For instance,
the current and voltage as a function of time where current and voltage are
two datasets sampled over the same temporal coordinates. Another example would
be the air temperature, pressure, wind velocity, and solar-flux as a function
of Earth’s latitude and longitude coordinates.

The CSD model is *standalone* because it is independent of the hardware,
operating system, application software, programming language, and the
object-oriented file-serialization format used in writing the CSD model to the
file. Out of numerous file serialization formats, XML, JSON, property list, we
adopt the data-exchange oriented JSON (JavaScript Object Notation)
file-serialization format because it is easily human readable and also easily
integrable with any number of programming languages and field related
application-software.

The model allows two types of file extensions for the JSON file-serialization,
`.csdf` and `.csdfx`, the acronyms for the Core Scientific Dataset Format and
the Core Scientific Dataset Format eXternal. The two file extensions act as a
medium to convey the end users whether the data values are present within the
file (`.csdf`) or in an external file on a local or remote server (`.csdfx`).

**CSD model expression**

In mathematical notations, the CSD model is expressed as,

.. math::

    y_\alpha = f_\alpha(x_0, x_1, ... x_k, ... x_{d-1})
    \forall \alpha \in \mathbb{Z}

where :math:`y_\alpha` is the uncontrolled variable and the :math:`x_k`,
:math:`k \in \{0, 1, ... ,d-1\}`, are the controlled variables. The model
supports any arbitrary :math:`d`-dimensional controlled variable space
where :math:`x_k` is its :math:`k^\mathrm{th}` dimension, and any arbitrary
:math:`p_\alpha`-dimensional uncontrolled variable space where every dimension
is a component of the uncontrolled variable.

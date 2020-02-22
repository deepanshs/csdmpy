#######################################
The core scientific dataset (CSD) model
#######################################

The core scientific dataset (CSD) model is a *light-weight*, *portable*,
*versatile*, and *standalone* data model capable of handling a variety of
scientific datasets. The model only encapsulates
data values and the minimum metadata to accurately represent a `p`-component
dependent variable,
:math:`(\mathbf{U}_0, ... \mathbf{U}_q, ... \mathbf{U}_{p-1})`,
discretely sampled at `M` unique points in a `d`-dimensional coordinate space,
:math:`(\mathbf{X}_0, \mathbf{X}_1, ... \mathbf{X}_k, ... \mathbf{X}_{d-1})`.
The model is not intended to encapsulate
any information on how the data might be acquired, processed, or visualized.

The data model is *versatile* in allowing many use cases for most spectroscopy,
diffraction, and imaging techniques. As
such the model supports multi-component datasets associated with continuous
physical quantities that are discretely sampled in a multi-dimensional space
associated with other carefully controlled quantities, for e.g., a mass as a
function of temperature, a current as a function of voltage and time, a signal
voltage as a function of magnetic field gradient strength, a color image with
a red, green, and blue (RGB) light intensity components as a function of two
independent spatial dimensions, or the six components of the symmetric
second-rank diffusion tensor MRI as a function of three independent spatial
dimensions. Additionally, the model supports multiple dependent variables
sharing the same :math:`d`-dimensional coordinate space. For example, a
simultaneous measurement of current and voltage as a function of time,
simultaneous acquisition of air temperature, pressure, wind velocity, and
solar-flux as a function of Earth’s latitude and longitude coordinates. We
refer to these dependent variables as `correlated-datasets`.

The CSD model is independent of the hardware,
operating system, application software, programming language, and the
object-oriented file-serialization format utilized in serializing the CSD model
to the file. Out of numerous file serialization formats, XML, JSON, property
list, we chose the data-exchange oriented JSON (JavaScript Object Notation)
file-serialization format because it is `human-readable` and
`easily integrable` with any number of programming languages
and field related application-software.

.. toctree::
    :maxdepth: 2
    :caption: Table of Contents

    CSDmodel_uml/csdm
    CSDmodel_uml/dimensions/dimension
    CSDmodel_uml/dependent_variables/dependent_variable
    CSDmodel_uml/enumeration
    CSDmodel_uml/scalarQuantity

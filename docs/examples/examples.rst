
========
Examples
========

In this section, we present illustrative examples for importing files
serialized with CSD model using `csdmpy` package.
Because CSD model allows multi-dimensional datasets with multiple dependent
variables, we use a shorthand notation of :math:`d\mathrm{D}\{p\}` to
indicate that a dataset has :math:`p`-component dependent variable defined
on a :math:`d`-dimensional coordinate grid.
In the case of `correlated datasets`, the number of components in each
dependent variable is given as a list within the curly braces, `i.e.`,
:math:`d\mathrm{D}\{p_0, p_1, p_2, ...\}`.

----

.. only:: latex

    **The sample CSDM compliant files used in this documentation are available**
    `online <https://osu.box.com/s/bq10pc5jyd3mu67vqvhw4xmrqgsd0x8u>`_.

.. only:: html

    **The sample CSDM compliant files used in this documentation are available online.**

    .. image:: https://img.shields.io/badge/Download-CSDM%20sample%20files-blueviolet
        :target: https://osu.box.com/s/bq10pc5jyd3mu67vqvhw4xmrqgsd0x8u

----

**Example Dataset**

.. toctree::
    :maxdepth: 2

    1D{1}-datasets/1D{1}-datasets
    2D{1}-datasets/2D{1}-datasets
    2D{2}-datasets/2D{2}-datasets
    2D{3}-datasets/2D{3}-datasets
    multiple_datasets/correlated_datasets
    labeled_datasets

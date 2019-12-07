

.. _labeledDimension_uml:


LabeledDimension
^^^^^^^^^^^^^^^^

.. only:: html

    Generalized Class
    """""""""""""""""

    .. raw:: html

        <a class="btn btn-default" href=./dimension.html#dimension-uml>
        Dimension </a>


Description
"""""""""""

A labeled dimension is a qualitative dimension where the coordinates along
the dimension are explicitly defined as labels. Let :math:`\mathbf{A}_k` be an
ordered set of unique labels along the :math:`k^{th}` dimension, then the
coordinates, :math:`\mathbf{X}_k`, along a labeled dimension are

.. math::
    \mathbf{X}_k = \mathbf{A}_k.


Attributes
""""""""""

.. cssclass:: table-bordered table-hover centered table-striped

.. list-table::
  :widths: 25 25 50
  :header-rows: 1

  * - Name
    - Type
    - Description

  * - labels
    - [String, String, ... ]
    - A `required` ordered array of labels along the dimension.


Example
"""""""

The following LabeledDimension object,

.. code::

    {
        "type": "labeled",
        "labels": ["Cu", "Fe", "Si", "H", "Li"]
    }

will generate a dimension, where the coordinates :math:`\mathbf{X}_k` are

.. code::

    ["Cu", "Fe", "Si", "H", "Li"]

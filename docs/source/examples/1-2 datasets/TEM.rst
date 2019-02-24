

TEM dataset
^^^^^^^^^^^
The following `TEM dataset <https://doi.org/10.1371/journal.pbio.1000502>`_ is
a section of early larval brain of *Drosophila melanogaster* used in the
analysis of neuronal microcircuitry. The dataset was obtained
from `TrakEM2 tutorial <http://www.ini.uzh.ch/~acardona/data.html>`_ and
converted to the CSD model *.csdfx* format. 

Let's import the file and look at the data structure ::

    >>> filename = 'test/ssTEM/TEM.csdf'
    >>> TEM = cp.load(filename)
    >>> print(TEM.data_structure)
    {
      "CSDM": {
        "uncontrolled_variables": [
          {
            "numeric_type": "uint8",
            "components": "[126, 126, ...... 164, 164]"
          }
        ],
        "controlled_variables": [
          {
            "reciprocal": {
              "quantity": "wavenumber"
            },
            "number_of_points": 512,
            "sampling_interval": "4.0 nm",
            "quantity": "length"
          },
          {
            "reciprocal": {
              "quantity": "wavenumber"
            },
            "number_of_points": 512,
            "sampling_interval": "4.0 nm",
            "quantity": "length"
          }
        ],
        "version": "0.0.9"
      }
    }

The tuples of controlled and the uncontrolled variable objects are ::

    >>> x = TEM.controlled_variables
    >>> y = TEM.uncontrolled_variables

with respective coordinates, ::

    >>> x[0].coordinates
    [ 0.  4.  8. 12. 16. ... 2028. 2032. 2036. 2040. 2044.] nm
    >>> x[1].coordinates
    [ 0.  4.  8. 12. 16. ... 2028. 2032. 2036. 2040. 2044.] nm

For convenient, let's convert the coordinte unit from nm to µm using the 
:py:meth:`~csdfpy.ControlledVariable.to` method of the :ref:`cv_api` class,

    >>> x[0].to('µm')
    >>> x[1].to('µm')

and plot the data.

    >>> fig, ax = plt.subplots(1,1,figsize=(5, 5))
    >>> extent = [x[0].coordinates[0].value, x[0].coordinates[-1].value,
    ...           x[1].coordinates[0].value, x[1].coordinates[-1].value]
    >>> ax.imshow(y[0].components[0], extent=extent, cmap='viridis')
    >>> ax.set_xlabel(x[0].axis_label)
    >>> ax.set_ylabel(x[1].axis_label)
    >>> ax.set_title(y[0].name)
    >>> ax.grid(color='k', linestyle='--', linewidth=0.5)
    
    >>> plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    >>> plt.savefig(TEM.filename+'.pdf', dpi=800)
    >>> plt.show()

.. image:: /resource/TEM.csdf.pdf
===================================
Welcome to the csdmpy documentation
===================================

.. only:: html

    .. cssclass:: table-bordered table-striped centered

    .. list-table::
      :widths: 25 75
      :header-rows: 0

      * - Deployment
        - .. image:: https://img.shields.io/pypi/v/csdmpy.svg?style=flat&logo=pypi&logoColor=white
            :target: https://pypi.python.org/pypi/csdmpy
            :alt: PyPI version

          .. image:: https://img.shields.io/pypi/pyversions/csdmpy
            :alt: PyPI - Python Version

      * - Build Status
        - .. image:: https://img.shields.io/github/workflow/status/deepanshs/csdmpy/CI%20(pip)?logo=GitHub
            :target: https://github.com/DeepanshS/csdmpy/actions
            :alt: GitHub Workflow Status

          .. image:: https://readthedocs.org/projects/csdmpy/badge/?version=stable
            :target: https://csdmpy.readthedocs.io/en/stable/
            :alt: Documentation Status

      * - License
        - .. image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
            :target: https://opensource.org/licenses/BSD-3-Clause
            :alt: License

      * - Metrics
        - .. image:: https://img.shields.io/lgtm/alerts/g/DeepanshS/csdmpy.svg?logo=lgtm
            :target: https://lgtm.com/projects/g/DeepanshS/csdmpy/alerts/
            :alt: Total alerts

          .. image:: https://img.shields.io/lgtm/grade/python/g/DeepanshS/csdmpy.svg?logo=lgtm
            :target: https://lgtm.com/projects/g/DeepanshS/csdmpy/context:python
            :alt: Language grade: Python

          .. image:: https://codecov.io/gh/DeepanshS/csdmpy/branch/master/graph/badge.svg
            :target: https://codecov.io/gh/DeepanshS/csdmpy

      * - GitHub
        - .. image:: https://img.shields.io/github/issues-raw/deepanshs/csdmpy?logo=github
            :target: https://github.com/DeepanshS/csdmpy/issues
            :alt: GitHub issues

      * - Citation
        - .. image:: https://img.shields.io/badge/DOI-PLOS%20ONE%2015(1):%20e0225953-Purple?size=large
            :target: https://doi.org/10.1371/journal.pone.0225953

.. .. image:: https://img.shields.io/github/contributors/DeepanshS/csdmpy.svg?style=flat&logo=github
..     :target: https://github.com/DeepanshS/csdmpy/graphs/contributors
..     :alt: GitHub contributors

.. .. image:: https://img.shields.io/github/release-pre/deepanshs/csdmpy
..     :alt: GitHub release

----

**About**

The ``csdmpy`` package is the Python support for the core scientific
dataset (CSD) model file exchange-format [#f10]_.
The package is based on the core scientific dataset (CSD) model, which is
designed as a building block in the development of a more sophisticated
portable scientific dataset file standard.
The CSD model is capable of handling a wide variety of
scientific datasets both within and across disciplinary fields.

The main objective of this python package is to facilitate an easy import and
export of the CSD model serialized files for Python users. The
package utilizes Numpy library and, therefore, offers the end-users versatility
to process or visualize the imported datasets with any third-party package(s)
compatible with Numpy.

----

.. only:: latex

  **View the core scientific dataset model (CSDM)**
  `examples gallery <https://csdmpy.readthedocs.io/en/stable/auto_examples/index.html>`_.

.. only:: html

  **View the core scientific dataset model (CSDM) examples gallery.**

  .. image:: https://img.shields.io/badge/View-Example%20Gallery-Purple?size=large
      :target: auto_examples/index.html

----

.. only:: latex

  `Tutorial <https://csdmpy.readthedocs.io/en/stable/auto_tutorials/index.html>`_
  **on generating and serializing CSDM objects from Numpy arrays**

.. only:: html

  **Tutorial on generating and serializing CSDM objects from Numpy arrays.**

  .. image:: https://img.shields.io/badge/View-Tutorial%20Gallery-Blue?size=large
      :target: auto_tutorials/index.html


----

.. only:: html

  Table of Contents
  -----------------

.. toctree::
    :maxdepth: 2

    CSD_model
    installation
    getting_started
    auto_examples/index
    startFromScratch/save_dataset
    startFromScratch/start
    startFromScratch/interacting_with_csdmpy_objects
    using_csdm_with_pyplot
    auto_tutorials/index
    startFromScratch/A fun example
    referenceAPI
    changelog

----

Citations
^^^^^^^^^

.. [#f10] Srivastava D.J., Vosegaard T., Massiot D., Grandinetti P.J. (2020) Core
    Scientific Dataset Model: A lightweight and portable model and file format for
    multi-dimensional scientific data.
    `PLOS ONE 15(1): e0225953. <https://doi.org/10.1371/journal.pone.0225953>`_


.. only:: html

    Media coverage
    ^^^^^^^^^^^^^^

    .. raw:: html

        <p> <a href="https://inc.cnrs.fr/fr/cnrsinfo/des-chimistes-elaborent-un-nouveau-format-pour-le-partage-de-donnees-scientifiques"><img src="https://inc.cnrs.fr/sites/institut_inc/files/styles/top_left/public/image/cnrs_20180120_0025%20%281%29.jpg?itok=i3wlyGBq" style="width:64px; height:64px" alt="Des chimistes élaborent un nouveau format pour le partage de données scientifiques"></a> <a href="https://inc.cnrs.fr/fr/cnrsinfo/des-chimistes-elaborent-un-nouveau-format-pour-le-partage-de-donnees-scientifiques"> Des chimistes élaborent un nouveau format pour le partage de données scientifiques. </a> </p>


        <p> <a href="https://www.technology.org/2020/01/03/simplifying-how-scientists-share-data/"><img src="https://www.technology.org/texorgwp/wp-content/uploads/2020/01/1920_data-1536x1024.jpg" style="width:64px; height:64px" alt="Simplifying how scientists share data"></a> <a href="https://www.technology.org/2020/01/03/simplifying-how-scientists-share-data/"> Simplifying how scientists share data. </a> </p>


.. only:: html

    Indices and tables
    ^^^^^^^^^^^^^^^^^^

    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`

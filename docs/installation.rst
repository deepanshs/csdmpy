============
Installation
============

Requirements
------------

``csdmpy`` has the following strict requirements:

- `Python <https://www.python.org>`_ 3.6 or later
- `Numpy <https://numpy.org>`_ 1.17 or later

Other requirements include:

- `requests>=2.21.0 <http://docs.python-requests.org/en/master/>`_
  (for downloading files from server)
- `astropy>=3.0 <http://www.astropy.org>`_ (for astropy units module)
- `matplotlib>=3.0 <https://matplotlib.org>`_ (for rendering plots)


Installing ``csdmpy``
---------------------

On Local machine (Using pip)
''''''''''''''''''''''''''''

PIP is a package manager for Python packages and is included with python version 3.4
and higher. PIP is the easiest way to install python packages.

.. code-block:: bash

    $ pip install csdmpy

If you get a ``PermissionError``, it usually means that you do not have the required
administrative access to install new packages to your Python installation. In this
case, you may consider adding the ``--user`` option, at the end of the statement, to
install the package into your home directory. You can read more about how to do this in
the `pip documentation <https://pip.pypa.io/en/stable/user_guide/#user-installs>`_.

.. code-block:: bash

    $ pip install csdmpy --user


Upgrading to a newer version
""""""""""""""""""""""""""""

To upgrade, type the following in the terminal/Prompt

.. code-block:: bash

    $ pip install csdmpy -U

On Google Colab Notebook
''''''''''''''''''''''''

Colaboratory is a Google research project. It is a Jupyter notebook environment that
runs entirely in the cloud. Launch a new notebook on
`Colab <http://colab.research.google.com>`_. To install the package, type

.. code-block:: shell

    !pip install csdmpy

in the first cell, and execute. All done! You may now start using the library.

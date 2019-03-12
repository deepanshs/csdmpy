
==========================
Installing `csdfpy` module
==========================

We recommend installing `anaconda <https://www.anaconda.com/distribution/>`_
distribution for python version 3.5 or higher. The anaconda distribution
comes with numerous packages and modules including Numpy, Scipy, and Matplotlib
which are required for the `csdfpy` module.
Alternatively, one can also `install python <https://www.python.org/downloads/>`_.

**Using PIP**:

PIP is a package manager for Python packages or modules and is included with
python version 3.4 and higher. The current version of the `csdfpy` module is
released as a test module. This is only a temporary release and may eventually
become unavailable after our initial release.

Before installing the test `csdfpy` module, install the requirements for the
`csdfpy` module.  If you are using an anaconda distribution for python
chances are that you already have the requirements installed.

To install the required packages type the following in the command line. ::

    >>> pip install numpy scipy requests astropy

The users may optionally install the matplotlib package if they prefer to use
this package for generating plots and figures.

.. note::

    Some of the `csdfpy` module tests may fail without the matplotlib libraries.

To install the matplotlib package type the following in the command line ::

    >>> pip install matplotlib

Now install the test `csdfpy` module using ::

    >>> pip install -i https://test.pypi.org/simple/ csdfpy==0.0.9alpha0

.. This is the recommened installation method.

.. **Using source code**:

.. Download the git repository and run ::

..     >>> python setup.py install

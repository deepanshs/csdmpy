
===========================
Installing `csdmpy` package
===========================

We recommend installing `anaconda <https://www.anaconda.com/distribution/>`_
distribution for python version 3.6 or higher. The anaconda distribution
ships with numerous packages and modules including Numpy, Scipy, and Matplotlib
which are useful packages for handling scientific datasets.

**Using PIP**:

PIP is a package manager for Python packages and modules and is included with
python version 3.4 and higher.
Before installing the `csdmpy` package, install the requirements for the
`csdmpy` module.  If you are using an anaconda distribution for python
chances are that you already have the requirements installed.

To install the required packages type the following in the command line. ::

    $ pip install -r requirements.txt

Now install the test `csdmpy` module using ::

    $ pip install -i https://test.pypi.org/simple/csdmpy==0.0.9alpha0

.. This is the recommend installation method.

.. **Using source code**:

.. Download the git repository and run ::

..     >>> python setup.py install

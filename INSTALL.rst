Install
=======

NetworkX requires Python 3.4, 3.5, or 3.6.  If you do not already
have a Python environment configured on your computer, please see the
instructions for installing the full `scientific Python stack
<https://scipy.org/install.html>`_.

.. note::
   If you are on Windows and want to install optional packages (e.g., `scipy`),
   then you will need to install a Python distribution such as
   `Anaconda <https://www.anaconda.com/download/>`_,
   `Enthought Canopy <https://www.enthought.com/product/canopy>`_,
   `Python(x,y) <http://python-xy.github.io/>`_,
   `WinPython <https://winpython.github.io/>`_, or
   `Pyzo <http://www.pyzo.org/>`_.
   If you use one of these Python distribution, please refer to their online
   documentation.

Below we assume you have the default Python environment already configured on
your computer and you intend to install ``grave`` inside of it.  If you want
to create and work with Python virtual environments, please follow instructions
on `venv <https://docs.python.org/3/library/venv.html>`_ and `virtual
environments <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_.

First, make sure you have the latest version of ``pip`` (the Python package manager)
installed. If you do not, refer to the `Pip documentation
<https://pip.pypa.io/en/stable/installing/>`_ and install ``pip`` first.

Install the released version
----------------------------

To be added.

Install the development version
-------------------------------

If you have `Git <https://git-scm.com/>`_ installed on your system, it is also
possible to install the development version of ``grave``.

Before installing the development version, you may need to uninstall the
standard version of ``grave`` using ``pip``::

    $ pip uninstall grave

Then do::

    $ git clone https://github.com/networkx/grave.git
    $ cd grave
    $ pip install -e .

The ``pip install -e .`` command allows you to follow the development branch as
it changes by creating links in the right places and installing the command
line scripts to the appropriate locations.

Then, if you want to update ``grave`` at any time, in the same directory do::

    $ git pull

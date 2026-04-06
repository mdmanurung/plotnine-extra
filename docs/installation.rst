Installation
============

Requirements
------------

* Python ≥ 3.10
* plotnine ≥ 0.15.3
* scipy ≥ 1.10.0

Install from PyPI
-----------------

The recommended way to install **plotnine-extra** is from PyPI:

.. code-block:: bash

   pip install plotnine-extra

This will also pull in the required dependencies (``plotnine`` and
``scipy``).

Install from source
-------------------

To install the latest development version directly from GitHub:

.. code-block:: bash

   pip install git+https://github.com/mdmanurung/plotnine-extra.git

Or clone the repository and install in editable mode:

.. code-block:: bash

   git clone https://github.com/mdmanurung/plotnine-extra.git
   cd plotnine-extra
   pip install -e .

Verify the installation
-----------------------

.. code-block:: python

   import plotnine_extra
   print(plotnine_extra.__version__)

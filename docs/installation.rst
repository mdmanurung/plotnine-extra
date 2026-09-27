Installation
============

Requirements
------------

* Python ≥ 3.11
* plotnine ≥ 0.16.0a14
* scipy ≥ 1.15.0
* numpy ≥ 1.25.0
* pandas ≥ 2.2.0
* matplotlib ≥ 3.10.0

.. note::

   plotnine 0.16 has no stable release yet — the latest stable is 0.15.8, and
   0.16 exists only as alphas. The dependency is therefore specified as
   ``plotnine>=0.16.0a14`` rather than ``plotnine>=0.16``: the latter is
   unsatisfiable, because no such release exists. PEP 440 permits a
   pre-release whenever the specifier itself names one, so the pinned form
   installs with a plain ``pip install`` and no ``--pre`` flag.

   In short: **installing plotnine-extra puts you on a plotnine alpha.** That
   is a deliberate trade for the composition, coordinate, contour and
   secondary-axis features it makes available. If you would rather stay on
   stable plotnine, use plotnine directly.

Install from PyPI
-----------------

The recommended way to install **plotnine-extra** is from PyPI:

.. code-block:: bash

   pip install plotnine-extra

This will also pull in the required dependencies (``plotnine``, ``scipy``,
``numpy``, ``pandas``, and ``matplotlib``).

Claude Code and Codex skills
----------------------------

The package includes bundled Claude Code and Codex skills with package-specific
notes for facets, guides, statistical annotations, composition, and animation.

Python packages should not write into user configuration directories as a side
effect of ``pip install``. After installing or upgrading the package, run:

.. code-block:: bash

   plotnine-extra-install-skills

By default this installs the skill into both
``~/.claude/skills/plotnine-extra/`` and
``~/.codex/skills/plotnine-extra/``. Use ``--target claude`` or
``--target codex`` to install for only one target, and ``--force`` to refresh an
existing installed copy after an upgrade.

To inspect the bundled skill path without copying files:

.. code-block:: bash

   plotnine-extra-install-skills --print-path

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

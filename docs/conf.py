# Configuration file for the Sphinx documentation builder.

import plotnine_extra

# -- Project information -----------------------------------------------------
project = "plotnine-extra"
copyright = "2024, plotnine-extra contributors"
author = "plotnine-extra contributors"
version = plotnine_extra.__version__
release = plotnine_extra.__version__

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "nbsphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# -- Options for autodoc -----------------------------------------------------
autodoc_member_order = "bysource"
autodoc_typehints = "description"

# -- Options for napoleon ----------------------------------------------------
napoleon_google_docstrings = True
napoleon_numpy_docstrings = True

# -- Options for nbsphinx ---------------------------------------------------
nbsphinx_execute = "always"

# -- Options for intersphinx -------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "plotnine": ("https://plotnine.org", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "pandas": ("https://pandas.pydata.org/docs", None),
}

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"

html_title = "plotnine-extra"

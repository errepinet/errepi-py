# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# set of options see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath("../errepi"))

# -- Project information -----------------------------------------------------

project = "errepi"
copyright = "2025, Errepi Net S.R.L."
author = "Valerio Faiuolo"

# The full version, including alpha/beta/rc tags
release = "0.0.1"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"
html_static_path = ["_static"]

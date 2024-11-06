# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ocfl-py'
copyright = '2018--2024, Simeon Warner and other contributors'
author = 'Simeon Warner and other contributors'

# Documentation is in docs, code is in repo root dir. Add ".." to path
# See: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#module-sphinx.ext.autodoc
import sys
from pathlib import Path
sys.path.insert(0, str(Path('..').resolve()))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser",
              "sphinx.ext.autodoc",
              "sphinx.ext.autosummary",
              "sphinx.ext.doctest",
              "sphinx.ext.napoleon",
              "sphinx_rtd_theme"]
myst_enable_extensions = ["colon_fence"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'README.md']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster' #'sphinx_rtd_theme'
html_theme_options = {
    'body_max_width' : 'none',
    'page_width': 'auto',
}
html_static_path = ['_static']

# Autodoc
autodoc_default_options = {
    "autoclass_content": "both",  # doesn't work to show __init__ docs??
    'special-members': '__init__'  # get __init__ to show explicitly
}

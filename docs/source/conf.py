# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import os
sys.path.insert(0, os.path.abspath('../../'))

project = 'PyDui-GTK'
copyright = '2022, Hiram Deng'
author = 'Hiram Deng'
release = 'https://pypi.org/project/pydui-gtk/'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
#    'sphinx.ext.autodoc',
#    'sphinx.ext.autosummary',
    'autoapi.extension',
    'myst_parser',
]

autoapi_type = 'python'
autoapi_dirs = ['../../src/pydui/']
autoapi_options = [
    "members", 
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]

autosummary_generate = True
templates_path = ['_templates']
exclude_patterns = ['_build', '_template', 'generated']
#source_suffix = {
#    '.rst': 'restructuredtext',
#    '.txt': 'markdown',
#    '.md': 'markdown',
#}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'alabaster'
# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_static_path = ['_static']

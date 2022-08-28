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
    'sphinx.ext.napoleon',
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
#    'sphinx.ext.autodoc',
#    'sphinx.ext.autosummary',
    'autoapi.extension',
    'myst_parser',
    'sphinx_rtd_theme',
]

# napolean settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# autoapi settings
autoapi_type = 'python'
autoapi_dirs = ['../../src/pydui/']
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]

# sphinx-intl settings
locale_dirs = ['locales/']
gettext_compact = False

templates_path = ['_templates']
exclude_patterns = ['build', '_template', 'generated']

# html_context settings 
try:
    html_context
except NameError:
    html_context = dict()
html_context_dict = {
    'display_lower_left': True,
    'display_github': True,
    'github_user': 'dzhsurf',
    'github_repo': 'pydui',
    'github_version': 'main',
    'conf_py_path': '/docs/source/',
}
html_context.update(html_context_dict)

html_sidebars = {
    '**': ['versions.html'],
}
html_theme_options = {
    'display_version': True,
    'vcs_pageview_mode': 'blob',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_static_path = ['_static']

if 'REPO_NAME' in os.environ:
   REPO_NAME = os.environ['REPO_NAME']
else:
   REPO_NAME = ''

# SET CURRENT_LANGUAGE
if 'current_language' in os.environ:
   # get the current_language env var set by buildDocs.sh
   current_language = os.environ['current_language']
else:
   # the user is probably doing `make html`
   # set this build's current language to english
   current_language = 'en'
html_context['current_language']  = current_language
html_context['version'] = current_language

# SET CURRENT_VERSION
from git import Repo
repo = Repo( search_parent_directories=True )

if 'current_version' in os.environ:
   # get the current_version env var set by buildDocs.sh
   current_version = os.environ['current_version']
else:
   # the user is probably doing `make html`
   # set this build's current version by looking at the branch
   current_version = repo.active_branch.name


# tell the theme which version we're currently on ('current_version' affects
# the lower-left rtd menu and 'version' affects the logo-area version)
html_context['current_version'] = current_version
html_context['version'] = current_version

# POPULATE LINKS TO OTHER LANGUAGES
html_context['languages'] = [ ('en', '/' +REPO_NAME+ '/en/' +current_version+ '/') ]
languages = [lang.name for lang in os.scandir('locales') if lang.is_dir()]
for lang in languages:
   html_context['languages'].append( (lang, '/' +REPO_NAME+ '/' +lang+ '/' +current_version+ '/') )

# POPULATE LINKS TO OTHER VERSIONS
html_context['versions'] = list()

versions = [branch.name for branch in repo.branches]
for version in versions:
   html_context['versions'].append( (version, '/' +REPO_NAME+ '/'  +current_language+ '/' +version+ '/') )


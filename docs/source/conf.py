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
    'sphinx.ext.autodoc',
    'myst_parser',
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

# sphinx-intl settings
locale_dirs = ['locales/']
gettext_compact = False

templates_path = ['_templates']
exclude_patterns = ['build', '_template', 'generated']

# # html_context settings
# try:
#     html_context
# except NameError:
#     html_context = dict()
# html_context_dict = {
#     'display_lower_left': True,
#     'display_github': True,
#     'github_user': 'dzhsurf',
#     'github_repo': 'pydui',
#     'github_version': 'main',
#     'conf_py_path': '/docs/source/',
# }
# html_context.update(html_context_dict)

# html_sidebars = {
#     '**': ['searchbox.html','press_sidetoc.html'],
# }

# html_logo = "_static/logo.png"
# html_theme_options = {
#     "logo_link": "",
#     "favicons": [
#     {
#         "rel": "icon",
#         "sizes": "16x16",
#         "href": "_static/favicons-16x16.png",
#     },
#     {
#         "rel": "icon",
#         "sizes": "32x32",
#         "href": "_static/favicons-32x32.png",
#     },
#     {
#         "rel": "apple-touch-icon",
#         "sizes": "180x180",
#         "href": "_static/apple-touch-icon-180x180.png",
#     },
#     ],
# }
#

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'piccolo_theme'
html_static_path = ['_static']

html_short_title = 'PyDui-GTK Documentation'
html_favicon = 'https://pypi.org/static/images/logo-small.95de8436.svg'
html_theme_options = {
    "source_url": 'https://github.com/dzhsurf/pydui/',
    "source_icon": "github",
    #"banner_text": 'banner text',
}
html_sidebars = {"**": ["globaltoc.html", "relations.html", "sourcelink.html", "searchbox.html"]}

# # SET CURRENT_LANGUAGE
# if 'current_language' in os.environ:
#    # get the current_language env var set by buildDocs.sh
#    current_language = os.environ['current_language']
# else:
#    # the user is probably doing `make html`
#    # set this build's current language to english
#    current_language = 'en'
# html_context['current_language']  = current_language
# html_context['version'] = current_language

# # SET CURRENT_VERSION
# from git import Repo
# repo = Repo( search_parent_directories=True )

# if 'current_version' in os.environ:
#     # get the current_version env var set by buildDocs.sh
#     current_version = os.environ['current_version']
# else:
#     # the user is probably doing `make html`
#     # set this build's current version by looking at the branch
#     current_version = repo.active_branch.name
#     if current_version == 'main':
#         current_version = 'latest'

# # tell the theme which version we're currently on ('current_version' affects
# # the lower-left rtd menu and 'version' affects the logo-area version)
# html_context['current_version'] = current_version
# html_context['version'] = current_version

# if 'REPO_NAME' in os.environ:
#    REPO_NAME = os.environ['REPO_NAME']
# else:
#    REPO_NAME = 'pydui'
# DOCS_HOST = "dzhsurf.github.io"

# # POPULATE LINKS TO OTHER LANGUAGES
# html_context['languages'] = [ ('en', f"https://{DOCS_HOST}/{REPO_NAME}/en/{current_version}/html/") ]
# languages = [lang.name for lang in os.scandir('locales') if lang.is_dir()]
# for lang in languages:
#    html_context['languages'].append( (lang, f"https://{DOCS_HOST}/{REPO_NAME}/{lang}/{current_version}/html/") )

# # POPULATE LINKS TO OTHER VERSIONS
# html_context['versions'] = list()
# versions = [branch.name for branch in repo.branches]
# for version in versions:
#     if version == 'main': version = 'latest'
#     html_context['versions'].append((version, f"https://{DOCS_HOST}/{REPO_NAME}/{current_language}/{version}/html/"))


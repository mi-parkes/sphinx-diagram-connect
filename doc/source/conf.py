project = 'sphinx-diagram-connect'
author  = 'MP'
version = '1.2'

import os, sys
import platform
import shutil

from sphinx.application import Sphinx # Import Sphinx for type hinting if desired
from sphinx.util.console import bold, colorize
from sphinx.util import logging
from sphinx.errors import ExtensionError

import sphinx
logger = sphinx.util.logging.getLogger(__name__)

def checkIfDrawIOAvailable():
    drawio_in_path = shutil.which("drawio")
    draw_dot_io_in_path = shutil.which("draw.io")
    WINDOWS_PATH = r"C:\Program Files\draw.io\draw.io.exe"
    MACOS_PATH = "/Applications/draw.io.app/Contents/MacOS/draw.io"
    LINUX_PATH = "/opt/drawio/drawio"
    LINUX_OLD_PATH = "/opt/draw.io/drawio"

    binary_path=None
    if drawio_in_path:
        binary_path = drawio_in_path
    elif draw_dot_io_in_path:
        binary_path = draw_dot_io_in_path
    elif platform.system() == "Windows" and os.path.isfile(WINDOWS_PATH):
        binary_path = WINDOWS_PATH
    elif platform.system() == "Darwin" and os.path.isfile(MACOS_PATH):
        binary_path = MACOS_PATH
    elif platform.system() == "Linux" and os.path.isfile(LINUX_PATH):
        binary_path = LINUX_PATH
    elif platform.system() == "Linux" and os.path.isfile(LINUX_OLD_PATH):
        binary_path = LINUX_OLD_PATH
    return binary_path is not None

extensions = [
    'sphinxcontrib.plantuml',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.githubpages',
    'sphinx_needs',
    'sphinx_diagram_connect',
    'myst_parser'
]

if checkIfDrawIOAvailable():
    extensions.append('sphinxcontrib.drawio')

exclude_patterns = []

language = 'en'

html_theme = 'sphinx_book_theme'

html_theme_options = {
    "path_to_docs": "doc/source",
    "repository_url": "https://github.com/mi-parkes/sphinx-diagram-connect",
    "repository_branch": "main",
    "show_navbar_depth": 2,
    "show_toc_level": 1,  
    "use_repository_button": True,
    "use_source_button": True,
    "home_page_in_toc" : True,
    "use_issues_button": True,
    "use_edit_page_button": True, 
}

env_plantuml = os.getenv("PLANTUML")

if env_plantuml != None:
    plantuml = env_plantuml
else:
    if sys.platform.startswith("linux"):
        plantuml = 'java -Djava.awt.headless=true -jar /usr/share/plantuml/plantuml.jar'
    elif sys.platform == "darwin":
        plantuml = 'java -jar /usr/local/plantuml/plantuml.jar'
plantuml_output_format = 'svg'

# SPHINX-NEEDS SETTINGS
needs_id_required = False
needs_id_regex = "^[A-Z0-9_-]*"

needs_build_json = True

needs_types = [
    dict(directive="need", title="Need", prefix="N_",color="#FDF5E6", style="rectangle")
]

#suppress_warnings = ['sphinx-diagram-connect-missing-reference']

#sphinx_diagram_connect_verbose=True

def copy_readme_md(app):
    project_root = os.path.abspath(os.path.join(app.srcdir, "..", ".."))
    ifilename = os.path.join(project_root, "README.md")
    ofilename = os.path.join(app.srcdir, "README.md")
    if os.path.exists(ifilename):
        try:
            shutil.copy2(ifilename, ofilename)
            logger.info(f"Copied '{ifilename}' to '{ofilename}'")
        except Exception as e:
            logger.error("Failed to copy README.md from '{ifilename}' to '{ofilename}': {e}")
            pass
    else:
        logger.error(f"Source file '{ifilename}' not found.")

def setup(app):
    app.connect('builder-inited', copy_readme_md)

if any(os.getenv(var) is not None for var in ["APIDOC", "APIDOC_DD"]):
    extensions.extend(
        ['sphinxcontrib.apidoc', 'sphinx.ext.autodoc']
    )
    apidoc_module_dir = '../../sphinx_diagram_connect'
    apidoc_output_dir = 'reference'
    apidoc_excluded_paths = ['tests']
    apidoc_separate_modules = False
    apidoc_extra_args = ["--no-toc"]

    if os.getenv("APIDOC_DD", None) is not None:
        apidoc_extra_args.append("-P")
        autodoc_default_options = {
            "members": True,
            "undoc-members": True,
            "private-members": True
        }

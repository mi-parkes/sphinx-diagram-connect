project = 'Demo using sphinx :ref: in PlantUML hyperlinks'
author  = 'MP'
version = '1.2'

import os, sys
import platform
import shutil

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
    'sphinx_ref_in_plantuml_hyperlinks'
]

if checkIfDrawIOAvailable():
    extensions.append('sphinxcontrib.drawio')

exclude_patterns = []

language = 'en'

html_theme = 'sphinx_book_theme'

html_theme_options = {
    "path_to_docs": "doc/source",
    "repository_url": "https://github.com/mi-parkes/sphinx-ref-in-plantuml-hyperlinks",
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

#suppress_warnings = ['sphinx-ref-in-plantuml-hyperlinks-missing-reference']

#sphinx_ref_in_plantuml_hyperlinks_verbose=True
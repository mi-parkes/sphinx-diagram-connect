
project = 'Demo using sphinx :ref: in PlantUML hyperlinks'
author  = 'MP'
version = '1.0'

import os, sys

extensions = [
    'sphinxcontrib.plantuml',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.githubpages',
    'sphinx_needs',
    'sphinx_ref_in_plantuml_hyperlinks'
]

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

#html_static_path = ['_static']

env_plantuml = os.getenv("PLANTUML")

if env_plantuml != None:
    plantuml = env_plantuml
else:
    if sys.platform.startswith("linux"):
        plantuml = 'java -jar /usr/share/plantuml/plantuml.jar'
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

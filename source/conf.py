project = 'Demo using sphinx :ref: in PlantUML hyperlinks'
author  = 'MP'
version = '1.0'

import os, sys
import sphinx
from sphinx.errors import NoUri
from docutils import nodes
import glob
import re
import xml.etree.ElementTree as ET
from sphinx.events import EventListener
from sphinx_needs.needsfile import NeedsList

logger = sphinx.util.logging.getLogger(__name__)

extensions = [
    'sphinxcontrib.plantuml',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.githubpages',
    'sphinx_needs',
]

exclude_patterns = []

language = 'en'

html_theme = 'sphinx_book_theme'

html_theme_options = {
    "path_to_docs": "source",
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

html_static_path = ['_static']

env_plantuml = os.getenv("PLANTUML")

if env_plantuml != None:
    plantuml = env_plantuml
else:
    if sys.platform.startswith("linux"):
        plantuml = 'java -jar /usr/share/plantuml/plantuml.jar'
    elif sys.platform == "darwin":
        plantuml = 'java -jar /usr/local/plantuml/plantuml.jar'
plantuml_output_format = 'svg'

def setup(app):
    app.connect('build-finished',build_finished)
    #app.connect('missing-reference', unresolved_reference)
    return {'version': '0.1', 'parallel_read_safe': True}

def unresolved_reference(env,node,contnode):
  print("unresolved_reference")

def init_needs(app):
    needs_list = NeedsList(app.env.config,app.outdir,app.srcdir)
    needs_list.load_json(os.path.join(app.builder.outdir,"needs.json"))
    if needs_list and needs_list.needs_list:
        if "versions" in needs_list.needs_list:
            keys=list(needs_list.needs_list["versions"].keys())
            if keys:
                version=keys[0]
                if "needs" in needs_list.needs_list["versions"][version]:
                    return needs_list.needs_list["versions"][version]["needs"]
    else:
        return None

def resolve_ref(app,target):
    refdomain="std"
    typ="ref"
    refdoc=os.path.join(app.builder.imagedir,"dummy.svg")
    node=nodes.literal_block("dummy","dummy")
    node['refexplicit']=False
    try:
        try:
            domain = app.env.domains[refdomain]
        except KeyError as exc:
            raise NoUri(target,typ) from exc
        newnode = domain.resolve_xref(app.env,refdoc, app.builder,typ, target.lower(),node,None)
        if newnode:
            return newnode.attributes['refuri']
        else:
            return None
    except NoUri:
        return None

def build_finished(app,docname):
    if app.builder.format=='html':
        needs_list=init_needs(app) if needs_build_json else None
        pattern = r"(:ref:`([^`]+)`)"
        for filename in glob.glob(os.path.join(app.builder.outdir,app.builder.imagedir)+"/*.svg",recursive=True):
            tree = ET.parse(filename)
            root = tree.getroot()
            modified=False
            for element in root.iter():
                if 'href' in element.attrib:
                    match = re.search(pattern,element.attrib['href'])
                    if match:
                        complete,old_href=match.groups()
                        new_href=resolve_ref(app,old_href)
                        if new_href:
                            element.attrib['href']=new_href
                            modified=True
                        elif needs_list:
                            if old_href in needs_list:
                                # TODO: the following needs to be adjusted based on app.builder.imagedir
                                element.attrib['href']=f"../{needs_list[old_href]['docname']}.html#{old_href}"
                                modified=True
            if modified:
                logger.info("Updating SVG file with resolved references:'%s'" % filename[len(os.getcwd())+1:],color='darkblue')
                with open(filename,"w") as f:
                    f.write(ET.tostring(root, encoding='utf-8').decode())
    return

# SPHINX-NEEDS SETTINGS
needs_id_required = False
needs_id_regex = "^[A-Z0-9_-]*"

needs_build_json = True

needs_types = [
    dict(directive="need", title="Need", prefix="N_",color="#FDF5E6", style="rectangle")
]

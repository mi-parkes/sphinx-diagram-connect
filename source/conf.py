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

logger = sphinx.util.logging.getLogger(__name__)

extensions = [
    'sphinxcontrib.plantuml',
    'sphinx.ext.autosectionlabel',
]

exclude_patterns = []

language = 'en'

html_theme = 'alabaster'
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

def resolve_ref(app,target):
    refdomain="std"
    typ="ref"
    refdoc="_images/dummy.svg"
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
        pattern = r"(:ref:`([^`]+)`)"
        for filename in glob.glob(os.path.join(app.builder.outdir,"_images")+"**/"+"*.svg",recursive=True):
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
            if modified:
                logger.info("Updating SVG file with resolved references:'%s'" % filename[len(os.getcwd())+1:],color='darkblue')
                with open(filename,"w") as f:
                    f.write(ET.tostring(root, encoding='utf-8').decode())
    return

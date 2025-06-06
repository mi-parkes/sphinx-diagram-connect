import os, sys
import sphinx
from sphinx.errors import NoUri
from docutils import nodes
import glob
import re
import xml.etree.ElementTree as ET
from lxml import etree
from sphinx.events import EventListener
from sphinx_needs.needsfile import NeedsList

logger = sphinx.util.logging.getLogger(__name__)

__version__ = "0.7.0"
version_info = (0,7,0)

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
    #refdoc=os.path.join(app.builder.imagedir,"dummy.svg")
    refdoc=app.builder.imagedir+"/dummy.svg"
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

def resolve_references(app,docname):
    if app.builder.format=='html':
        sphinx_ref_in_plantuml_hyperlinks_verbose=getattr(app.config,"sphinx_ref_in_plantuml_hyperlinks_verbose",False)
        needs_build_json=getattr(app.config,"needs_build_json",False)
        needs_list=init_needs(app) if needs_build_json else None
        pattern = r"(:(ref|doc):`([^`]+)`)"
        href = ""

        for filename in glob.glob(os.path.join(app.builder.outdir,app.builder.imagedir)+"/*.svg",recursive=True):
            # Read the SVG file
            with open(filename, 'rb') as file:
                svg_content = file.read()

            # Parse the SVG content
            parser = etree.XMLParser(ns_clean=True)
            root = etree.fromstring(svg_content, parser)

            modified=False
            for element in root.iter():
                keys = element.attrib.keys()
                if len(keys) > 0:
                    href = keys[0]
                    if  href.endswith('href'):
                        match = re.search(pattern,element.attrib[href])
                        if match:
                            resolved=False
                            complete,type,old_href=match.groups()
                            new_href=resolve_ref(app,old_href)
                            if new_href:
                                element.attrib[href]=new_href
                                if sphinx_ref_in_plantuml_hyperlinks_verbose:
                                    logger.info("href resolution: '%s' -> '%s'" % (old_href,new_href),color='purple')
                                resolved=True
                            elif needs_list:
                                if old_href in needs_list:
                                    # TODO: the following needs to be adjusted based on app.builder.imagedir
                                    element.attrib[href]=f"../{needs_list[old_href]['docname']}.html#{old_href}"
                                    resolved=True
                            if resolved:
                                modified=True
                            else:
                                logger.warning("Failed to resolve reference:'%s' in file:'%s'" % (old_href,filename[len(os.getcwd())+1:]),color='darkred',type='sphinx-ref-in-plantuml-hyperlinks-missing-reference')

            if modified:
                logger.info("Updating SVG file with resolved references:'%s'" % filename[len(os.getcwd())+1:],color='darkblue')
                try:
                    # Write the modified SVG content back to a file
                    with open(filename, 'wb') as file:
                        file.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
                except Exception as exc:
                    logger.error("Failed to write file:'%s' - %s" % (filename[len(os.getcwd())+1:],exc))
    return

def setup(app):
    app.connect('build-finished',resolve_references)
    app.add_config_value('sphinx_ref_in_plantuml_hyperlinks_verbose',False,"html")
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": __version__,
    }

Features
========

.. needtable::
   :columns: id,title,status,refinement
   :types: ftr

.. needflow::
   :types: ftr
   :filter: "refinement in ftr_demo_00001 or id == 'ftr_demo_00001'"

.. ftr:: Connect Sphinx References in SVGs
   :id: ftr_demo_00001
   :status: open
   :refinement: ftr_demo_00002, ftr_demo_00003

   This feature enables Sphinx documentation to automatically resolve and update
   cross-references (e.g., `:ref:`, `:doc:`) and Sphinx-Needs references within
   SVG diagrams. This allows users to create interactive, clickable diagrams that
   link directly to other parts of their documentation.

.. ftr:: Support Standard Sphinx References
   :id: ftr_demo_00002
   :status: open

   The system shall identify and resolve standard Sphinx cross-references
   (`:ref:`, `:doc:`) found within `xlink:href` attributes of SVG elements.
   Resolved references will be replaced with their absolute or relative URIs.

.. ftr:: Support Sphinx-Needs References
   :id: ftr_demo_00003
   :status: open
   :refinement: ftr_demo_00004

   The system shall identify and resolve Sphinx-Needs references (`:need:`)
   found within `xlink:href` attributes of SVG elements, provided the
   `needs_build_json` configuration is enabled.

.. ftr:: Configurable Verbose Logging
   :id: ftr_demo_00004
   :status: open

   The extension shall provide a configuration option (`sphinx_diagram_connect_verbose`)
   to enable or disable verbose logging of reference resolution operations during
   the Sphinx build process. This helps in debugging and understanding the
   extension's behavior.

.. ftr:: Handle Unresolved References Gracefully
   :id: ftr_demo_00005
   :status: open

   The extension shall log a warning for any Sphinx or Sphinx-Needs references
   within SVG files that could not be resolved to a valid URI, without
   halting the build process.

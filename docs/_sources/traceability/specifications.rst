Specifications
==============

.. needtable::
   :columns: id,title,status,refinement,satisfy
   :types: spc

.. needflow::
   :types: spc
   :filter: "refinement in spc_demo_00001 or id == 'spc_demo_00001'"

.. spc:: SVG Reference Resolution Mechanism
   :id: spc_demo_00001
   :status: open
   :refinement: spc_demo_00002, spc_demo_00003
   :satisfy: req_demo_00001

   The `DiagramConnect` class shall implement a method, `resolve_references`,
   which is triggered upon the `build-finished` Sphinx event. This method shall
   iterate through all `.svg` files located in the `app.builder.outdir` and
   `app.builder.imagedir`. It shall identify and modify `xlink:href` attributes
   that contain Sphinx cross-reference patterns (e.g., `:ref:`target`,
   `:doc:`target`) or Sphinx-Needs reference patterns (e.g., `:need:`target`).
   The modification involves replacing these patterns with their resolved URIs.

   **Component Diagram:** :ref:`Extension Architecture`

.. spc:: Standard Sphinx Reference Resolution
   :id: spc_demo_00002
   :status: open
   :satisfy: req_demo_00002

   The `_resolve_ref` internal method shall utilize `app.env.domains['std'].resolve_xref`
   to convert Sphinx reference targets (e.g., `my-section`, `my-document`) into
   their corresponding relative or absolute URIs. This process must handle
   `sphinx.errors.NoUri` by returning `None` if a reference cannot be resolved
   by Sphinx's standard mechanisms.

.. spc:: Sphinx-Needs Reference Resolution
   :id: spc_demo_00003
   :status: open
   :satisfy: req_demo_00003

   If `app.config.needs_build_json` is set to `True`, the `resolve_references`
   method shall load `needs.json` using `sphinx_needs.needsfile.NeedsList`.
   For `xlink:href` attributes matching a Sphinx-Needs reference pattern (e.g.,
   `:need:`ID`), the system shall look up the 'docname' associated with the
   'ID' in the loaded `needs.json` data. The `xlink:href` shall then be
   updated to `../<docname>.html#<ID>`.

.. spc:: Error Handling for Unresolved References
   :id: spc_demo_00004
   :status: open
   :satisfy: req_demo_00004

   The `resolve_references` method shall log a warning message using
   `sphinx.util.logging.getLogger(__name__).warning` when a Sphinx or
   Sphinx-Needs reference pattern found in an `xlink:href` attribute cannot be
   successfully resolved. The warning message shall include the unresolved
   reference and the filename where it occurred. The warning type shall be
   "sphinx-diagram-connect-missing-reference".

.. spc:: Verbose Logging Configuration
   :id: spc_demo_00005
   :status: open
   :satisfy: req_demo_00010

   The extension shall expose a configuration option,
   `sphinx_diagram_connect_verbose` (defaulting to `False`), which, when set
   to `True`, shall enable additional `logger.info` messages during the
   `resolve_references` process, specifically detailing the transformation
   of original `href` values to their resolved URIs.
   
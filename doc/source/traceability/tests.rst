Tests
=====

.. needtable::
   :columns: id,title,status,validation,verify_req,verify_spc
   :types: tsc

.. tsc:: Test Standard Sphinx Reference Resolution Success
   :id: tsc_demo_00001
   :status: open
   :verify_spc: spc_demo_00002

   **Purpose:** Verify that standard Sphinx references (`:ref:`, `:doc:`) within SVG `xlink:href` attributes are correctly resolved to their corresponding URIs when `resolve_references` is executed, primarily testing the specification for standard resolution.

                        
   **Implementation:** :meth:`tests.integration.test_diagram_connect_integration.TestDiagramConnectIntegration.test_resolve_references_html_format_success`

   **Test Steps:**

   1. Set up a mock Sphinx environment with an output directory containing an SVG file.
   2. The SVG file should contain an `<a>` element with an `xlink:href` attribute value like `:ref:`my-ref``.
   3. Configure the mock Sphinx application to return a resolved URI (e.g., `/_static/resolved_my-ref.html`) for `:ref:`my-ref``.
   4. Call `diagram_connect_instance.resolve_references(mock_sphinx_app, None)`.
   5. Assert that `builtins.open` was called to read and write the SVG.
   6. Assert that `lxml.etree.fromstring` and `lxml.etree.tostring` were called.
   7. Assert that the `xlink:href` attribute in the mock SVG element was updated to the resolved URI.
   8. Assert that the Sphinx logger recorded an "info" message about updating the SVG file.

   **Expected Result:** The `xlink:href` attribute of the SVG element is updated with the correct resolved URI, and appropriate logging occurs.

.. tsc:: Test Unresolved Standard Sphinx Reference Handling
   :id: tsc_demo_00002
   :status: open
   :verify_req: req_demo_00004

   **Purpose:** Verify that `resolve_references` logs a warning for any standard Sphinx reference in an SVG that cannot be resolved, ensuring robust error handling.
                       
   **Implementation:** :meth:`tests.integration.test_diagram_connect_integration.TestDiagramConnectIntegration.test_resolve_references_html_format_unresolved`

   **Test Steps:**

   1. Set up a mock Sphinx environment with an output directory containing an SVG file.
   2. The SVG file should contain an `<a>` element with an `xlink:href` attribute value like `:ref:`non-existent-ref``.
   3. Configure the mock Sphinx application to return `None` when attempting to resolve `:ref:`non-existent-ref``.
   4. Call `diagram_connect_instance.resolve_references(mock_sphinx_app, None)`.
   5. Assert that `builtins.open` was called to read the SVG.
   6. Assert that `lxml.etree.fromstring` was called.
   7. Assert that `lxml.etree.tostring` was *not* called (indicating no modification).
   8. Assert that the `xlink:href` attribute remains unchanged.
   9. Assert that the Sphinx logger recorded a "warning" message with the correct format and type for the unresolved reference.
   10. Assert that no "info" message about updating the SVG file was logged.

   **Expected Result:** The SVG file remains unchanged, and a warning is logged for the unresolved reference.

.. tsc:: Test Sphinx-Needs Reference Resolution Success
   :id: tsc_demo_00003
   :status: open
   :validation: usc_demo_00002

   **Purpose:** Verify that Sphinx-Needs references within SVG `xlink:href` attributes are correctly resolved when `needs_build_json` is enabled, validating the use case.
                     
   **Implementation:** :meth:`tests.integration.test_diagram_connect_integration.TestDiagramConnectIntegration.test_resolve_references_with_needs_json_success`

   **Test Steps:**

   1. Set up a mock Sphinx environment with `needs_build_json` set to `True`.
   2. Mock `sphinx_needs.needsfile.NeedsList` to return a `needs.json` structure containing a known need (e.g., `MY_NEED_001` with `docname: "specifications"`).
   3. The SVG file should contain an `<a>` element with an `xlink:href` attribute value like `:ref:`MY_NEED_001``.
   4. Call `diagram_connect_instance.resolve_references(mock_sphinx_app, None)`.
   5. Assert that `NeedsList` was initialized and `load_json` was called.
   6. Assert that the `xlink:href` attribute in the mock SVG element was updated to `../specifications.html#MY_NEED_001`.
   7. Assert that `lxml.etree.tostring` was called and an "info" message about updating the SVG was logged.

   **Expected Result:** The `xlink:href` attribute is correctly updated with the Sphinx-Needs URI, and an info message is logged.

.. tsc:: Test Verbose Logging Functionality
   :id: tsc_demo_00004
   :status: open
   :verify_req: req_demo_00010

   **Purpose:** Verify that verbose logging messages are generated as specified when `sphinx_diagram_connect_verbose` is `True`, confirming the requirement for configurable verbosity.
                        
   **Implementation:** :meth:`tests.integration.test_diagram_connect_integration.TestDiagramConnectIntegration.test_resolve_references_verbose_logging`

   **Test Steps:**

   1. Set up a mock Sphinx environment with `sphinx_diagram_connect_verbose` set to `True`.
   2. Provide a mock SVG with a resolvable Sphinx reference (e.g., `:ref:`my-ref``).
   3. Call `diagram_connect_instance.resolve_references(mock_sphinx_app, None)`.
   4. Assert that `mock_logger.info` was called with a message confirming the `href` resolution, including both the original and new URIs, and with `color="purple"`.
   5. Assert that the standard "Updating SVG file" info message is also logged.

   **Expected Result:** Both the detailed `href` resolution log and the SVG update log messages are present.

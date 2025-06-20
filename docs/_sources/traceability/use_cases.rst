Use Cases
=========

.. needtable::
   :columns: id,title,status,refinement,realization,elaboration
   :types: usc

.. needflow::
   :types: usc
   :filter: "refinement in usc_demo_00001 or id == 'usc_demo_00001'"

.. usc:: Resolve Standard Sphinx References in SVG
   :id: usc_demo_00001
   :status: open
   :refinement: usc_demo_00002
   :realization: ftr_demo_00002
   :elaboration: req_demo_00001

   **Main Flow:**

   1. The user builds Sphinx documentation that includes SVG diagrams.
   2. The extension iterates through SVG files in the output directory.
   3. For each SVG, the extension parses its content to find `xlink:href` attributes.
   4. If an `xlink:href` attribute contains a standard Sphinx reference pattern (e.g., `:ref:`my-target`), the extension attempts to resolve it.
   5. The resolved URI (e.g., `/path/to/my-target.html`) replaces the reference pattern in the `xlink:href` attribute.
   6. The modified SVG file is saved, making the link clickable in the generated HTML.

   **Preconditions:**

   * Sphinx documentation build is initiated.
   * SVG diagrams are present in the build output's image directory.
   * Sphinx cross-references used in SVGs are valid and resolvable within the Sphinx project.

   **Postconditions:**

   * SVG diagrams have clickable links where Sphinx references were present.
   * The Sphinx build completes successfully.

   **Use Case Diagram:**

   .. uml::

      left to right direction
      actor User
      boundary "Sphinx Build" as Sphinx
      control "DiagramConnect" as DC
      entity "SVG File" as SVG
      entity "Sphinx Environment" as SE

      User --> Sphinx : Build Docs
      Sphinx --> DC : Trigger resolve_references
      DC --> SVG : Read SVG files
      DC --> SE : Resolve :ref:/:doc:
      SE --> DC : Return resolved URI
      DC --> SVG : Write updated SVG
      DC --> Sphinx : Build finished
      Sphinx --> User : Provide HTML Docs

.. usc:: Resolve Sphinx-Needs References in SVG
   :id: usc_demo_00002
   :status: open
   :realization: ftr_demo_00003
   :elaboration: req_demo_00003

   **Main Flow:**

   1. The user builds Sphinx documentation with Sphinx-Needs and SVG diagrams.
   2. The `needs_build_json` configuration is enabled in `conf.py`.
   3. The extension loads the `needs.json` file generated by Sphinx-Needs.
   4. For each SVG, the extension parses its content to find `xlink:href` attributes.
   5. If an `xlink:href` attribute contains a Sphinx-Needs reference pattern (e.g., `:need:`MY_NEED_ID`), the extension attempts to resolve it using the loaded `needs.json` data.
   6. The resolved URI (e.g., `../needs_doc.html#MY_NEED_ID`) replaces the reference pattern.
   7. The modified SVG file is saved, making the link clickable in the generated HTML.

   **Alternative Flows:**

   * **No `needs.json` found:** The extension proceeds without resolving Sphinx-Needs references, logging a message if `needs_build_json` is enabled.

   **Preconditions:**

   * Sphinx documentation build is initiated.
   * SVG diagrams are present in the build output's image directory.
   * Sphinx-Needs extension is active and `needs_build_json` is set to `True`.
   * A `needs.json` file is generated and accessible.

   **Postconditions:**

   * SVG diagrams have clickable links to Sphinx-Needs where references were present.
   * The Sphinx build completes successfully.

   **Use Case Diagram:**

   .. uml::

      left to right direction
      actor User
      boundary "Sphinx Build" as Sphinx
      control "DiagramConnect" as DC
      entity "SVG File" as SVG
      entity "needs.json" as NJ

      User --> Sphinx : Build Docs (needs_build_json=True)
      Sphinx --> DC : Trigger resolve_references
      DC --> NJ : Load needs.json
      DC --> SVG : Read SVG files
      DC --> NJ : Resolve :need:
      NJ --> DC : Return resolved URI
      DC --> SVG : Write updated SVG
      DC --> Sphinx : Build finished
      Sphinx --> User : Provide HTML Docs

.. usc:: Configure Verbose Output
   :id: usc_demo_00003
   :status: open
   :realization: ftr_demo_00004
   :elaboration: req_demo_00010

   **Main Flow:**

   1. The user sets `sphinx_diagram_connect_verbose = True` in their `conf.py`.
   2. During the Sphinx build, for every successfully resolved `xlink:href` in an SVG, the extension logs an informative message indicating the original and resolved URI.

   **Preconditions:**

   * The `sphinx_diagram_connect` extension is enabled in `conf.py`.

   **Postconditions:**

   * Detailed logging messages about reference resolution are displayed during the build.

   **Use Case Diagram:**

   .. uml::

      left to right direction
      actor User
      component "conf.py" as Conf
      control "DiagramConnect" as DC
      artifact "Build Log" as Log

      User --> Conf : Set verbose = True
      Conf --> DC : Configure verbose
      DC --> Log : Log resolved hrefs

Sphinx Architecture
###################
This diagram illustrates the core components and their relationships within a typical Sphinx 
documentation project.

.. uml:: SphinxArchDiagram.puml
   :alt: Sphinx Architecture Diagram

* **Sphinx**: The central application that orchestrates the documentation build process.
* **Sphinx-Builder**: Responsible for rendering the documentation into various output formats, such as HTML, EPUB, or LaTeX. A Sphinx project can utilize one or more builders.
* **Sphinx-Extension**: Custom Python modules that extend Sphinx's functionality, allowing users to define new roles, directives, or add custom processing steps.
* **conf.py**: The primary configuration file for a Sphinx project, where settings like project metadata, extensions to load, and theme selection are defined.
* **Sphinx-Theme**: A collection of HTML templates, stylesheets, and other static files that define the visual appearance of the generated documentation. A Sphinx project typically uses one active theme.
* **Sphinx-Theme Customization**: Allows for modifications and overrides to the active Sphinx theme, providing a way to tailor the look and feel without altering the original theme files directly.
* **Documentation Sources**: The raw source files (e.g., reStructuredText `.rst` or Markdown `.md` files) that contain the actual content of the documentation. Sphinx processes these files to generate the final output.

The arrows in the diagram indicate the relationships and data flow between these components:

* Extensions implement roles and directives that Sphinx uses during processing.
* Builders are used by Sphinx to render the documentation into specific formats.
* Sphinx utilizes a theme to style the output.
* The `conf.py` file configures Sphinx and specifies the active theme and any theme customizations.
* Sphinx processes the documentation source files.
* The `conf.py` file can also reference specific source files, such as `index.rst`, which is often the starting point for the documentation.


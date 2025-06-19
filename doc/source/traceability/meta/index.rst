Meta Model
##########

This page describes the traceability structure used in this documentation. The diagram below illustrates the relationships between key artifact types—Features, Use Cases, Requirements, Specifications, and Test Cases—using Sphinx-Needs and custom link types. This model helps ensure coverage, validation, and verification across all stages of development.

.. rubric:: Traceability Relationship Diagram

.. uml:: traceability-transition-model.puml

.. rubric:: Link Type Legend

The following link types define the relationships between traceability elements:

- **refinement**: Indicates that a need is a more detailed version of another (e.g., a sub-feature or refined requirement).
- **satisfy**: Shows how a lower-level need (e.g., a Feature or Specification) fulfills a Requirement.
- **verify / verify_req / verify_spc**: Connects a Test Case to the item it verifies—either a Requirement or a Specification.
- **validation**: Connects a Test Case to a Use Case it validates.
- **realization**: Maps a Use Case to the Feature that realizes it.
- **elaboration**: Shows that a Use Case was derived from a Requirement.
- **specify**: Indicates Specification elaboration from a Requirement.

..
      :caption: Traceability Elements

.. toctree::
   :maxdepth: 2
   :hidden:

   ftr.rst
   usc.rst
   req.rst
   spc.rst
   tsc.rst

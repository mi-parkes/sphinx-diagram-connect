req
###

The ``req`` directive captures a system requirement, which can be either **functional** (defining behavior) or **non-functional** (defining constraints or quality attributes). Requirements serve as a bridge between user-level expectations and technical implementation.

.. code-block:: rst

    .. req:: TITLE
       :id: req_demo_00001
       :status: open
       :type_ext: Functional
       :reasoning:
       :test:
       :acceptance:
       :refinement: req_demo_00002, req_demo_00003
       :satisfy: ftr_demo_00001

       CONTENT_BODY

**Field Descriptions:**

- ``:id:``  
  Unique identifier for the requirement.  
  Must match the pattern: ``req_demo_[0-9]{5,5}``.

- ``:status:``  
  The current status of the requirement (e.g., ``open``, ``approved``, ``rejected``).

- ``:type_ext:``  
  Type classification: either ``Functional`` or ``Nonfunctional``.

- ``:reasoning:``  
  (Optional) Rationale or justification for this requirement.

- ``:test:``  
  (Optional) A brief summary or reference to how this requirement will be tested.

- ``:acceptance:``  
  (Optional) Criteria that define when the requirement is considered fulfilled.

- ``:refinement:``  
  (Optional) A comma-separated list of other ``req`` IDs that refine this requirement.

- ``:satisfy:``  
  A ``ftr`` ID (or multiple, comma-separated IDs) that this requirement satisfies.

- ``CONTENT_BODY``  
  A clear and concise description of the requirement, including any relevant context, constraints, or assumptions.

**Example:**

.. code-block:: rst

    .. req:: Support export to PNG
       :id: req_demo_00001
       :status: open
       :type_ext: Functional
       :reasoning: Users often need static images for documentation.
       :test: Diagram renders correctly in PNG format.
       :acceptance: Exported image must match visible diagram state.
       :satisfy: ftr_demo_00001

       The system must allow users to export the currently viewed diagram as a PNG image.


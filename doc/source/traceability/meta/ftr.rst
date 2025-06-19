ftr
###

The ``ftr`` directive is used to define high-level software features. Each feature should describe a distinct capability or service expected from the system. Features can be refined by other features to indicate hierarchical decomposition.

.. code-block:: rst

   .. ftr:: TITLE
      :id: ftr_demo_00001
      :status: open
      :refinement: ftr_demo_00002, ftr_demo_00003

      CONTENT_BODY

**Field Descriptions:**

- ``:id:``  
  A unique identifier for the feature.  
  Must follow the pattern: ``ftr_demo_[0-9]{5,5}``.

- ``:status:``  
  Current status of the feature (e.g., ``open``, ``in progress``, ``closed``).

- ``:refinement:``  
  (Optional) A comma-separated list of other ``ftr`` IDs that refine this feature.  
  Use a single line for multiple values.

- ``CONTENT_BODY``  
  The content block should provide a clear and complete description of the feature's purpose, scope, and role within the system.

**Example:**

.. code-block:: rst

   .. ftr:: Diagram rendering support
      :id: ftr_demo_00001
      :status: open
      :refinement: ftr_demo_00002

      Enables generation of UML diagrams from textual descriptions via a service endpoint.

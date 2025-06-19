usc
####

The ``usc`` directive defines a user interaction scenario that elaborates features into actionable requirements. It describes how the system behaves to achieve a specific user goal and helps bridge the gap between high-level features and detailed requirements.

.. code-block:: rst

    .. uc:: TITLE
       :id: usc_demo_00001
       :status: open
       :refinement: usc_demo_00002, usc_demo_00003
       :realization: ftr_demo_00001, ftr_demo_00002
       :elaboration: req_demo_00001

       CONTENT_BODY

**Field Descriptions:**

- ``:id:``  
  A unique identifier for the use case.  
  Must follow the pattern: ``usc_demo_[0-9]{5,5}``.

- ``:status:``  
  Current status of the use case (e.g., ``open``, ``in progress``, ``closed``).

- ``:refinement:``  
  (Optional) A comma-separated list of other ``usc`` IDs that refine this use case.

- ``:realization:``  
  A comma-separated list of ``ftr`` IDs that this use case realizes.

- ``:elaboration:``  
  A ``req`` ID that this use case elaborates.

- ``CONTENT_BODY``  
  should follow this structure, ensuring all headings and directive content are correctly indented and separated by blank lines:  
  
  * **Main Flow:** (Numbered steps)
  * **Alternative Flows:** (Optional, numbered steps)
  * **Exceptional Flows:** (Optional, numbered steps)
  * **Preconditions:** (Bullet points)
  * **Postconditions:** (Bullet points)
  * **Use Case Diagram:** (This should be followed by a **blank line**, then the `.. uml::` directive.  
    The `.. uml::` directive itself must be followed by **another blank line**, and then the PlantUML code, 
    which should be indented by **exactly 3 spaces** relative to the `.. uml::` directive.  
    The PlantUML code must also include `left to right direction` at its beginning.)

**Example:**

.. code-block:: rst

  .. usc:: Clear Cache
    :id: usc_demo_00005
    :status: open
    :realization: ftr_demo_00003
    :elaboration: req_demo_00006

    Main Flow:
      1.  User triggers a cache clear operation (e.g., via a management interface or restart).
      2.  Proxy server empties its internal cache.

    Preconditions:
      * Proxy server is running.

    Postconditions:
      * Cache is empty.

    Use Case Diagram:

    .. uml::

        left to right direction
        Actor "User" as user
        Rectangle "PlantUML Proxy Server" {
          (Clear Cache) as usc_05
        }
        user --> usc_05


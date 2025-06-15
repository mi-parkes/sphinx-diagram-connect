C4-PlantUML
###########

The C4-PlantUML examples are configured for SVG interactive mode.
This is achieved by including the following pragma within the PlantUML 
definition:

.. code-block::

   @startuml
   ' ...
   !pragma svginteractive true
   ' ...
   @enduml

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   system_context
   container_diagram
   component_diagram

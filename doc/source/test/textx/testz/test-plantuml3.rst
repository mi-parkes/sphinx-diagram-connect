Test PlantUML 2
###############

Heading 3 1
===========

Some Text here

:ref:`PlantUML Label1`

Heading 3 2
===========

Some other text here

.. py:function:: lumache.get_Random_Ingredients(kind=None)

   Return a list of random ingredients as strings.

   :param kind: Optional "kind" of ingredients.
   :type kind: list[str] or None
   :raise lumache.InvalidKindError: If the kind is invalid.
   :return: The ingredients list.
   :rtype: list[str]

Some more text here   

.. uml::
    :caption: PlantUML Caption with **bold** and *italic*
    :name: PlantUML Label2

    @startmindmap mindmap2
    scale 0.3
    skinparam defaultFontSize 56
    skinparam backgroundColor transparent
    *[#Orange] Clickable references
    **[#lightgreen] [[ ":ref:`plantuml label1`" Internal Page Arbitrary Reference ]]
    **[#lightyellow] [[ ":py:func:`lumache.get_Random_Ingredients`" Internal Page Arbitrary Reference to Python]]
    **[#lightblue] [[ ":ref:`spc_demo_00001`" sphinx-needs Reference ]]
    **[#Tomato] [[ ":ref:`N_00003`" Internal Page Arbitrary Invalid Reference ]]

    @endmindmap



Cross References
================

Here some tests to anchors in other document:


See :ref:`Explicit-CPP-Anchor`

Or the reference to the role: :cpp:func:`myMethod`


See :ref:`Explicit-Python-Anchor`

Or the reference to the role: :py:func:`Timer.repeat`


.. uml::
   :caption: PlantUML Caption with **bold** and *italic*
   :name: PlantUML Cross Ref

   @startuml
   A -> B: Request [[":ref:`Explicit-CPP-Anchor`" Exp Cpp]]
   B --> A: Response [[":ref:`Explicit-Python-Anchor`" Exp Python]]

   A -> B: another Request [[":cpp:func:`myMethod`" Cpp role]]
   A <-- B: another Response [[":py:func:`Timer.repeat`" Python role]]
   @enduml

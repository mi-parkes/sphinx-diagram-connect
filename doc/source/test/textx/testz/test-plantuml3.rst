Test PlantUML 2
###############

Heading 3 1
============

Some Text here

:ref:`PlantUML Label1`

Heading 3 2
===========

Some other text here

.. py:function:: lumache.get_random_ingredients(kind=None)

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
    **[#lightyellow] [[ ":py:func:`lumache.get_random_ingredients`" Internal Page Arbitrary Reference to Python]]
    **[#lightblue] [[ ":ref:`spc_demo_00001`" sphinx-needs Reference ]]
    **[#Tomato] [[ ":ref:`N_00003`" Internal Page Arbitrary Invalid Reference ]]

    @endmindmap

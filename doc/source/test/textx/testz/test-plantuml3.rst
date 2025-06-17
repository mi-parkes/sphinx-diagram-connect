Test PlantUML 3
###############

Heading 3 1
============

Some Text here

:ref:`PlantUML Label1`

Heading 3 2
===========

Some other text here

.. uml::
    :caption: PlantUML Caption with **bold** and *italic*
    :name: PlantUML Label2

    @startmindmap mindmap2
    scale 0.3
    skinparam defaultFontSize 56

    *[#Orange] Example of clickable references
    **[#lightgreen] [[ ":ref:`plantuml label1`" Internal Page Arbitrary Reference ]]
    **[#lightblue] [[ ":ref:`N_00001`" sphinx-needs Reference ]]
    **[#Tomato] [[ ":ref:`N_00003`" Internal Page Arbitrary Invalid Reference ]]

    @endmindmap

.. need:: Some Other Need
    :id: N_00002
    :status: open

    Some Other Need description

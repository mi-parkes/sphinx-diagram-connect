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

    *[#Orange] Example of clickable references
    **[#lightgreen] [[ ":ref:`plantuml label1`" Internal Page Reference1 ]]
    **[#lightblue] [[ ":ref:`N_00001`" Internal Page Reference2 on sphinx-need ]]
    **[#red] [[ ":ref:`N_00003`" Invalid Refrence ]]

    @endmindmap

.. need:: Some Other Need
    :id: N_00002
    :status: open

    Some Other Need description

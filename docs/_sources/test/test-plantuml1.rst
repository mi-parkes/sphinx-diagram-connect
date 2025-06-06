Test PlantUML 1
###############

:ref:`Heading 1`

.. uml::
    :caption: PlantUML Caption with **bold** and *italic*
    :name: PlantUML Label1

    @startmindmap mindmap1

    *[#Orange] Example of clickable references
    **[#lightgreen] [[ https://www.sphinx-doc.org/en/master/ External Page Reference ]]
    **[#lightgreen] [[ ":ref:`Heading 2`" Internal Page Arbitrary Reference1 ]]
    **[#lightblue] [[ ":ref:`N_00002`" Internal Page Arbitrary Reference2 on sphinx-needs ]]
    **[#lightgrey] [[ ":doc:`Test PlantUML 3`" Internal Page Reference3 ]]

    @endmindmap

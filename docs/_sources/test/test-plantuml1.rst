Test PlantUML 1
###############

.. uml::
    :caption: PlantUML Caption with **bold** and *italic*
    :name: PlantUML Label1

    @startmindmap mindmap1
    scale 0.3
    skinparam defaultFontSize 56
    *[#Orange] Clickable references
    **[#yellow] [[ https://www.sphinx-doc.org/en/master/ External Page Reference ]]
    **[#lightgreen] [[ ":ref:`Extension Architecture`" Internal Page Arbitrary Reference ]]
    **[#lightblue] [[ ":ref:`spc_demo_00001`" sphinx-needs Reference ]]
    **[#lightgrey] [[ ":doc:`Meta Model`" Internal Page Reference ]]

    @endmindmap

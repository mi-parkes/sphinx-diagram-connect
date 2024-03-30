# Enhanced integration between Sphinx documentation and PlantUML diagrams

`sphinx_ref_in_plantuml_hyperlinks` is a [Sphinx](https://www.sphinx-doc.org/en/master/index.html) extension that automatically resolves references (links) created using the `std:ref:` syntax within [PlantUML](https://plantuml.com) diagrams. This allows you to link elements in your PlantUML diagrams to corresponding sections or elements in your Sphinx documentation, enhancing navigation and information flow.

![](https://mi-parkes.github.io/sphinx-ref-in-plantuml-hyperlinks/_images/refInPlantuml.png)

    .. uml::
        :caption: PlantUML Caption with **bold** and *italic*
        :name: PlantUML Label2
    
        @startmindmap mindmap2
    
        *[#Orange] Example of clickable references
        **[#lightgreen] [[ ":ref:`plantuml label1`" Internal Page Reference1 ]]
        **[#lightblue] [[ ":ref:`N_00001`" Internal Page Reference2 on Sphinx-Needs ]]

        @endmindmap

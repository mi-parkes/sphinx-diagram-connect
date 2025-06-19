Test PlantUML 4 (Graphviz)
##########################

:ref:`Heading 1`

.. uml::
    :caption: Graphviz Example
    :name: PlantUML Label4

    @startuml digraph
    digraph G {
        rankdir = RL;
        labelloc = "t";
        fontsize = "28pt";
        nodesep=1.0
        node [
            fontsize = "22"
            fixedsize=true 
            width=2.6 
            height=1.3 
            shape="box"
            shape="oval"
            style="filled"
            target="_top"
        ];
        edge [ fontname=Helvetica, fontsize=25, minlen=2 ];

        node1 [ label="Node1" tooltip="Node tooltip" URL=":ref:`Heading 2`"]
        node2 [ label="Node2" tooltip="Node tooltip" URL=":ref:`spc_demo_00001`"]

        node1 -> node2 [ label="test" ]
    }
    @enduml

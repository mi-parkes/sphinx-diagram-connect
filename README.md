# Enhance Your Sphinx Documentation with Dynamic Diagram Links

See the **[complete documentation rendered with Sphinx](https://mi-parkes.github.io/sphinx-diagram-connect/)** 📚.

## Unlock Seamless Navigation Between Diagrams and Documentation

`sphinx_diagram_connect` is a powerful [Sphinx](https://www.sphinx-doc.org/en/master/index.html) extension designed to create intelligent, clickable links within your [PlantUML](https://plantuml.com) or [DrawIO](https://pypi.org/project/sphinxcontrib-drawio/) diagrams.

* By automatically resolving `std:doc` or `std:ref` syntax, this extension allows you to effortlessly connect elements in your diagrams directly to relevant sections or components within your Sphinx documentation.

* Also references to other domain like `py:func` will be resolved.

* **Optionally**, references to *sphinx-needs* items will also be resolved. Precondition is that you have the corresponding package available in your pyhton environment and the extension *sphinx-needs* is configured in your documentation setup.

The **sphinx_diagram_connect** extension works on the generated *svg* files of your graphical tools. This means also other diagram types are supported automatically.

> This means enhanced navigation, improved information flow, and a more interactive experience for your readers!

### See It in Action: Dynamic References in PlantUML

Imagine clicking on a diagram element and being taken directly to its detailed explanation in your documentation. This is precisely what `sphinx_diagram_connect` enables.

![](https://mi-parkes.github.io/sphinx-diagram-connect/_images/refInPlantuml.png)

This example demonstrates how references of the standard domain `std` with `:doc:` and `:ref:` syntax within your PlantUML code becomes a live hyperlink in your rendered documentation:

```rst
.. uml::
    :caption: PlantUML Caption with **bold** and *italic*
    :name: PlantUML Label2

    @startmindmap mindmap2

    *[#Orange] Example of clickable references
    **[#lightgreen] [[ ":ref:`Heading 2`" Internal Page Arbitrary Reference1 ]]
    **[#lightblue] [[ ":ref:`N_00002`" Internal Page Arbitrary Reference2 on sphinx-needs ]]
    **[#lightgrey] [[ ":doc:`Test PlantUML 3`" Internal Page Reference3 ]]

    @endmindmap
```
## Installation

You can easily install [sphinx-diagram-connect](https://pypi.org/project/sphinx-diagram-connect/) using pip:

```bash
pip install sphinx-diagram-connect
```

Alternatively (for Linux users with Poetry):

```bash
git clone https://github.com/mi-parkes/sphinx-diagram-connect.git
cd sphinx-diagram-connect

poetry install
poetry build

poetry add -G sphinx dist/sphinx_diagram_connect-*-py3-none-any.whl
```

## Activation

Once installed, simply add `sphinx_diagram_connect` to your extensions list in your conf.py file:

```python
extensions = [
    ...,
    'sphinx_diagram_connect'
]
```

## Listing Available Labels:

To see all referenceable labels in your project, use:

```bash
poetry run task labels
```

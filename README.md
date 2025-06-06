# Enhance Your Sphinx Documentation with Dynamic Diagram Links

---

## Unlock Seamless Navigation Between Diagrams and Documentation

`sphinx_ref_in_plantuml_hyperlinks` is a powerful [Sphinx](https://www.sphinx-doc.org/en/master/index.html) extension designed to create intelligent, clickable links within your [PlantUML](https://plantuml.com) and [DrawIO](https://pypi.org/project/sphinxcontrib-drawio/) diagrams. By automatically resolving `std:doc:` and `std:ref:` syntax, this extension allows you to effortlessly connect elements in your diagrams directly to relevant sections or components within your Sphinx documentation. This means enhanced navigation, improved information flow, and a more interactive experience for your readers.

---

### See It in Action: Dynamic References in PlantUML

Imagine clicking on a diagram element and being taken directly to its detailed explanation in your documentation. This is precisely what `sphinx_ref_in_plantuml_hyperlinks` enables.

![](https://mi-parkes.github.io/sphinx-ref-in-plantuml-hyperlinks/_images/refInPlantuml.png)

This example demonstrates how `std:doc:` and `std:ref:` syntax within your PlantUML code becomes a live hyperlink in your rendered documentation:

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

You can easily install [sphinx-ref-in-plantuml-hyperlinks](https://pypi.org/project/sphinx-ref-in-plantuml-hyperlinks/) using pip:

```bash
pip install sphinx-ref-in-plantuml-hyperlinks
```

Alternatively (for Linux users with Poetry):

```bash
git clone https://github.com/mi-parkes/sphinx-ref-in-plantuml-hyperlinks.git
cd sphinx-ref-in-plantuml-hyperlinks

poetry install
poetry build

poetry add -G sphinx dist/sphinx_ref_in_plantuml_hyperlinks-*-py3-none-any.whl
```

## Activation

Once installed, simply add `sphinx_ref_in_plantuml_hyperlinks` to your extensions list in your conf.py file:

```python
extensions = [
    ...,
    'sphinx_ref_in_plantuml_hyperlinks'
]
```

## Listing Available Labels:

To see all referenceable labels in your project, use:

```bash
poetry run task labels
```

# Enhanced integration between Sphinx documentation, PlantUML, and DrawIO diagrams

`sphinx_ref_in_plantuml_hyperlinks` is a [Sphinx](https://www.sphinx-doc.org/en/master/index.html) extension that automatically resolves references (links) created using the `std:ref:` syntax within [PlantUML](https://plantuml.com) and [DrawIO](https://pypi.org/project/sphinxcontrib-drawio/) diagrams. This allows you to link elements in your  diagrams to corresponding sections or elements in your Sphinx documentation, enhancing navigation and information flow.

![](https://mi-parkes.github.io/sphinx-ref-in-plantuml-hyperlinks/_images/refInPlantuml.png)

## Example of Use

```rst
.. uml::
    :caption: PlantUML Caption with **bold** and *italic*
    :name: PlantUML Label2

    @startmindmap mindmap2

    *[#Orange] Example of clickable references
    **[#lightgreen] [[ ":ref:`plantuml label1`" Internal Page Reference1 ]]
    **[#lightblue] [[ ":ref:`N_00001`" Internal Page Reference2 on Sphinx-Needs ]]

    @endmindmap
```
## Installation

You can install [sphinx-ref-in-plantuml-hyperlinks](https://pypi.org/project/sphinx-ref-in-plantuml-hyperlinks/) with pip

```bash
pip install sphinx-ref-in-plantuml-hyperlinks
```

Alternatively (Linux)

```bash
git clone https://github.com/mi-parkes/sphinx-ref-in-plantuml-hyperlinks.git
cd sphinx-ref-in-plantuml-hyperlinks

poetry install
poetry build

poetry add -G sphinx dist/sphinx_ref_in_plantuml_hyperlinks-*-py3-none-any.whl
```

## Activation

In your conf.py configuration file, add `sphinx_ref_in_plantuml_hyperlinks` to your extensions list:

```python
extensions = [
    ...
    'sphinx_ref_in_plantuml_hyperlinks'
    ...
]
```

## List Labels:

```bash
poetry run task labels
```


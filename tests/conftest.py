import pytest
from unittest.mock import MagicMock, Mock, patch
import os

from sphinx_diagram_connect import DiagramConnect, setup, __version__

@pytest.fixture
def mock_sphinx_app(): # Renamed from mock_app to mock_sphinx_app
    """
    Provides a mock Sphinx application object for testing.
    """
    app = MagicMock()
    app.config = MagicMock()
    app.config.sphinx_diagram_connect_verbose = False
    app.config.needs_build_json = False  # Default to False
    app.builder = MagicMock()
    app.builder.format = "html"
    app.builder.outdir = "/mock/outdir"
    app.builder.imagedir = "html/_images"
    app.env = MagicMock()
    # Mock the 'std' domain for resolving references
    app.env.domains = {"std": MagicMock()}

    # Define a named function for the side_effect to ensure clear scoping
    def _resolve_xref_side_effect(env, refdoc, builder, typ, target_val, node, content):
        if target_val == "my-ref":
            return MagicMock(attributes={"refuri": "/_static/resolved_my-ref.html"})
        elif target_val == "another-doc":
            return MagicMock(attributes={"refuri": "/_static/resolved_another-doc.html"})
        return None

    app.env.domains["std"].resolve_xref = MagicMock(side_effect=_resolve_xref_side_effect)
    return app

@pytest.fixture
def temp_sphinx_project(tmp_path):
    """
    Creates a temporary Sphinx project structure for integration tests.
    Returns the path to the project root.
    """
    project_root = tmp_path / "test_project"
    (project_root / "_static").mkdir(parents=True)
    (project_root / "_build" / "html" / "_images").mkdir(parents=True)

    # Create a dummy SVG file
    dummy_svg_content = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
      <a xlink:href=":ref:`my_reference`">
        <rect x="10" y="10" width="100" height="50" fill="blue"/>
      </a>
      <a xlink:href=":doc:`my_document`">
        <circle cx="150" cy="150" r="40" fill="red"/>
      </a>
      <a xlink:href="https://example.com/external">
        <text x="50" y="180">External Link</text>
      </a>
    </svg>
    """
    (project_root / "_build" / "html" / "_images" / "diagram.svg").write_text(dummy_svg_content)

    # Create a dummy needs.json file (if testing needs integration)
    needs_json_content = """
    {
        "versions": {
            "0.1": {
                "needs": {
                    "my_need": {
                        "docname": "my_needs_doc"
                    }
                }
            }
        }
    }
    """
    (project_root / "_build" / "html" / "needs.json").write_text(needs_json_content)

    return project_root

# Fixture for an instance of DiagramConnect
@pytest.fixture
def diagram_connect_instance(mock_sphinx_app):
    """
    Provides an initialized DiagramConnect instance for tests.
    """
    return DiagramConnect(mock_sphinx_app)


# Fixture for a mock logger
@pytest.fixture
def mock_logger():
    """
    Mocks the Sphinx logger to capture log messages.
    """
    with patch("sphinx_diagram_connect.logger") as mock:
        yield mock


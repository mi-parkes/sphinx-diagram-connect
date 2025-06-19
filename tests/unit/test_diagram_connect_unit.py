# tests/unit/test_diagram_connect_unit.py

"""
Unit tests for the `DiagramConnect` class, focusing on isolated method behaviors.

These tests verify the initialization logic of `DiagramConnect` and the
behavior of internal methods like `_init_needs` and `_resolve_ref`,
using mocks to avoid external dependencies like file system interactions or
actual Sphinx domain resolutions.
"""

import pytest
from unittest.mock import MagicMock, patch

from sphinx_diagram_connect import DiagramConnect


class TestDiagramConnectUnit:
    """
    Unit tests for the DiagramConnect class's internal methods and initialization.
    """

    def test_init(self, mock_sphinx_app: MagicMock):
        """
        Tests the initialization of the `DiagramConnect` class.

        Ensures that `app`, `verbose` setting, and `needs_build_json` setting
        are correctly stored.

        Parameters
        ----------
        mock_sphinx_app : MagicMock
            A mock Sphinx application object.
        """
        instance = DiagramConnect(mock_sphinx_app)
        assert instance.app == mock_sphinx_app
        assert (
            instance.sphinx_diagram_connect_verbose
            == mock_sphinx_app.config.sphinx_diagram_connect_verbose
        )
        assert instance.needs_build_json == mock_sphinx_app.config.needs_build_json
        assert instance.needs_list is None

        # Test with verbose and needs_build_json set to True
        mock_sphinx_app.config.sphinx_diagram_connect_verbose = True
        mock_sphinx_app.config.needs_build_json = True
        instance = DiagramConnect(mock_sphinx_app)
        assert instance.sphinx_diagram_connect_verbose is True
        assert instance.needs_build_json is True

    @patch("sphinx_diagram_connect.NeedsList")
    @patch("os.path.join", return_value="/mock/outdir/needs.json")
    def test_init_needs_success(
        self,
        mock_join: MagicMock,
        mock_needs_list: MagicMock,
        diagram_connect_instance: DiagramConnect,
    ):
        """
        Tests `_init_needs` when `needs.json` is valid and contains data.

        Parameters
        ----------
        mock_join : MagicMock
            Mock for `os.path.join`.
        mock_needs_list : MagicMock
            Mock for the `NeedsList` class.
        diagram_connect_instance : DiagramConnect
            An initialized `DiagramConnect` instance.
        """
        mock_needs_list_instance = mock_needs_list.return_value
        mock_needs_list_instance.needs_list = {
            "versions": {
                "1.0": {
                    "needs": {
                        "REQ_001": {
                            "docname": "requirements",
                            "title": "Requirement 1",
                        },
                        "REQ_002": {
                            "docname": "requirements",
                            "title": "Requirement 2",
                        },
                    }
                }
            }
        }

        needs = diagram_connect_instance._init_needs()
        assert needs == {
            "REQ_001": {"docname": "requirements", "title": "Requirement 1"},
            "REQ_002": {"docname": "requirements", "title": "Requirement 2"},
        }
        mock_needs_list_instance.load_json.assert_called_once_with(
            "/mock/outdir/needs.json"
        )

    @patch("sphinx_diagram_connect.NeedsList")
    @patch("os.path.join", return_value="/mock/outdir/needs.json")
    def test_init_needs_no_needs_json(
        self,
        mock_join: MagicMock,
        mock_needs_list: MagicMock,
        diagram_connect_instance: DiagramConnect,
    ):
        """
        Tests `_init_needs` when `needs.json` is empty or invalid.

        Parameters
        ----------
        mock_join : MagicMock
            Mock for `os.path.join`.
        mock_needs_list : MagicMock
            Mock for the `NeedsList` class.
        diagram_connect_instance : DiagramConnect
            An initialized `DiagramConnect` instance.
        """
        mock_needs_list_instance = mock_needs_list.return_value
        mock_needs_list_instance.needs_list = {}

        needs = diagram_connect_instance._init_needs()
        assert needs is None
        mock_needs_list_instance.load_json.assert_called_once_with(
            "/mock/outdir/needs.json"
        )

    def test_resolve_ref_success(self, diagram_connect_instance: DiagramConnect):
        """
        Tests `_resolve_ref` with a target that Sphinx can resolve.

        Parameters
        ----------
        diagram_connect_instance : DiagramConnect
            An initialized `DiagramConnect` instance.
        """
        resolved_uri = diagram_connect_instance._resolve_ref("my-ref")
        assert resolved_uri == "/_static/resolved_my-ref.html"
        diagram_connect_instance.app.env.domains[
            "std"
        ].resolve_xref.assert_called_once()

    def test_resolve_ref_failure(self, diagram_connect_instance: DiagramConnect):
        """
        Tests `_resolve_ref` with a target that Sphinx cannot resolve.

        Parameters
        ----------
        diagram_connect_instance : DiagramConnect
            An initialized `DiagramConnect` instance.
        """
        resolved_uri = diagram_connect_instance._resolve_ref("non-existent-ref")
        assert resolved_uri is None
        diagram_connect_instance.app.env.domains[
            "std"
        ].resolve_xref.assert_called_once()

# tests/unit/test_setup_function_unit.py

"""
Unit tests for the `setup` function of the `sphinx_diagram_connect` extension.

These tests ensure that the `setup` function correctly registers the extension,
connects to the 'build-finished' event, and adds necessary configuration values
to the Sphinx application, using mocks for isolation.
"""

import pytest
from unittest.mock import MagicMock

# Import the setup function and version from your package
from sphinx_diagram_connect import setup, __version__


class TestSetupFunction:
    """
    Unit tests for the `setup` function.
    """

    def test_setup_registers_extension(self, mock_sphinx_app: MagicMock):
        """
        Tests that the setup function correctly registers the extension,
        connects the build-finished event, and adds the config value.

        Parameters
        ----------
        mock_sphinx_app : MagicMock
            A mock Sphinx application object provided by the `mock_sphinx_app` fixture.
        """
        mock_sphinx_app.connect = MagicMock()
        mock_sphinx_app.add_config_value = MagicMock()

        result = setup(mock_sphinx_app)

        mock_sphinx_app.connect.assert_called_once()
        args, kwargs = mock_sphinx_app.connect.call_args
        assert args[0] == "build-finished"
        assert args[1].__qualname__.startswith("DiagramConnect.resolve_references")

        mock_sphinx_app.add_config_value.assert_called_once_with(
            "sphinx_diagram_connect_verbose", False, "html"
        )

        assert result == {
            "parallel_read_safe": True,
            "parallel_write_safe": True,
            "version": __version__,
        }

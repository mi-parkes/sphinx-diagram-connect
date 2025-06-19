# tests/integration/test_diagram_connect_integration.py

"""
Integration tests for the `DiagramConnect` class, focusing on its interaction
with the file system and Sphinx-related processes.

These tests verify the end-to-end behavior of `resolve_references`, including
reading and writing SVG files and integrating with mocked Sphinx environments
and Sphinx-Needs data.
"""

import os
import pytest
from unittest.mock import MagicMock, patch, mock_open
from lxml import etree

from sphinx_diagram_connect import DiagramConnect


class TestDiagramConnectIntegration:
    """
    Integration tests for the DiagramConnect class, focusing on file I/O and
    interaction with mocked external systems (like Sphinx's file system structure).
    """

    @patch("sphinx_diagram_connect.glob.glob")
    @patch("builtins.open", new_callable=mock_open)
    @patch("lxml.etree.fromstring")
    @patch("lxml.etree.tostring")
    @patch("lxml.etree.XMLParser")
    @patch("os.getcwd", return_value="/mock/outdir")
    def test_resolve_references_html_format_success(
        self,
        mock_getcwd: MagicMock,
        mock_xml_parser: MagicMock,
        mock_tostring: MagicMock,
        mock_fromstring: MagicMock,
        mock_open_file: MagicMock,
        mock_glob: MagicMock,
        diagram_connect_instance: DiagramConnect,
        mock_logger: MagicMock,
    ):
        """
        Tests `resolve_references` with a mock SVG containing a resolvable Sphinx reference.

        Parameters
        ----------
        mock_getcwd : MagicMock
            Mock for `os.getcwd`.
        mock_xml_parser : MagicMock
            Mock for `lxml.etree.XMLParser`.
        mock_tostring : MagicMock
            Mock for `lxml.etree.tostring`.
        mock_fromstring : MagicMock
            Mock for `lxml.etree.fromstring`.
        mock_open_file : MagicMock
            Mock for `builtins.open`.
        mock_glob : MagicMock
            Mock for `glob.glob`.
        diagram_connect_instance : DiagramConnect
            An initialized `DiagramConnect` instance.
        mock_logger : MagicMock
            Mock for the Sphinx logger.
        """
        mock_glob.return_value = ["/mock/outdir/html/_images/diagram.svg"]
        mock_svg_content = b'<svg><a xlink:href=":ref:`my-ref`">Link</a></svg>'
        mock_open_file.return_value.read.return_value = mock_svg_content

        mock_root = MagicMock()
        mock_element = MagicMock()

        _attributes_dict = {"{http://www.w3.org/1999/xlink}href": ":ref:`my-ref`"}
        mock_element.attrib = MagicMock()
        mock_element.attrib.__getitem__.side_effect = _attributes_dict.__getitem__
        mock_element.attrib.__setitem__.side_effect = _attributes_dict.__setitem__
        mock_element.attrib.keys.return_value = list(_attributes_dict.keys())

        mock_root.iter.return_value = [mock_element]
        mock_fromstring.return_value = mock_root
        mock_tostring.return_value = (
            b'<svg><a xlink:href="/_static/resolved_my-ref.html">Link</a></svg>'
        )

        diagram_connect_instance.resolve_references(diagram_connect_instance.app, None)

        mock_open_file.assert_any_call("/mock/outdir/html/_images/diagram.svg", "rb")
        mock_xml_parser.assert_called_once_with(ns_clean=True)
        mock_fromstring.assert_called_once_with(
            mock_svg_content, mock_xml_parser.return_value
        )

        assert (
            mock_element.attrib["{http://www.w3.org/1999/xlink}href"]
            == "/_static/resolved_my-ref.html"
        )
        mock_tostring.assert_called_once_with(
            mock_root, pretty_print=True, xml_declaration=True, encoding="UTF-8"
        )
        mock_open_file.assert_any_call("/mock/outdir/html/_images/diagram.svg", "wb")
        mock_logger.info.assert_any_call(
            "Updating SVG file with resolved references:'html/_images/diagram.svg'",
            color="darkblue",
        )

    @patch("sphinx_diagram_connect.glob.glob")
    @patch("builtins.open", new_callable=mock_open)
    @patch("lxml.etree.fromstring")
    @patch("lxml.etree.tostring")
    @patch("lxml.etree.XMLParser")
    @patch("os.getcwd", return_value="/mock/outdir")
    def test_resolve_references_html_format_unresolved(
        self,
        mock_getcwd: MagicMock,
        mock_xml_parser: MagicMock,
        mock_tostring: MagicMock,
        mock_fromstring: MagicMock,
        mock_open_file: MagicMock,
        mock_glob: MagicMock,
        diagram_connect_instance: DiagramConnect,
        mock_logger: MagicMock,
    ):
        """
        Tests `resolve_references` with a mock SVG containing an unresolvable Sphinx reference.

        Parameters
        ----------
        mock_getcwd : MagicMock
            Mock for `os.getcwd`.
        mock_xml_parser : MagicMock
            Mock for `lxml.etree.XMLParser`.
        mock_tostring : MagicMock
            Mock for `lxml.etree.tostring`.
        mock_fromstring : MagicMock
            Mock for `lxml.etree.fromstring`.
        mock_open_file : MagicMock
            Mock for `builtins.open`.
        mock_glob : MagicMock
            Mock for `glob.glob`.
        diagram_connect_instance : DiagramConnect
            An initialized `DiagramConnect` instance.
        mock_logger : MagicMock
            Mock for the Sphinx logger.
        """
        mock_glob.return_value = ["/mock/outdir/html/_images/diagram.svg"]
        mock_svg_content = (
            b'<svg><a xlink:href=":ref:`non-existent-ref`">Link</a></svg>'
        )
        mock_open_file.return_value.read.return_value = mock_svg_content

        mock_root = MagicMock()
        mock_element = MagicMock()

        _attributes_dict = {
            "{http://www.w3.org/1999/xlink}href": ":ref:`non-existent-ref`"
        }
        mock_element.attrib = MagicMock()
        mock_element.attrib.__getitem__.side_effect = _attributes_dict.__getitem__
        mock_element.attrib.__setitem__.side_effect = _attributes_dict.__setitem__
        mock_element.attrib.keys.return_value = list(_attributes_dict.keys())

        mock_root.iter.return_value = [mock_element]
        mock_fromstring.return_value = mock_root
        mock_tostring.return_value = mock_svg_content

        diagram_connect_instance.resolve_references(diagram_connect_instance.app, None)

        mock_open_file.assert_any_call("/mock/outdir/html/_images/diagram.svg", "rb")
        mock_xml_parser.assert_called_once_with(ns_clean=True)
        mock_fromstring.assert_called_once_with(
            mock_svg_content, mock_xml_parser.return_value
        )

        assert (
            mock_element.attrib["{http://www.w3.org/1999/xlink}href"]
            == ":ref:`non-existent-ref`"
        )
        mock_tostring.assert_not_called()
        mock_logger.warning.assert_called_once_with(
            "Failed to resolve reference:'%s' in file:'%s'"
            % ("non-existent-ref", "html/_images/diagram.svg"),
            color="darkred",
            type="sphinx-diagram-connect-missing-reference",
        )
        mock_logger.info.assert_not_called()

    @patch("sphinx_diagram_connect.glob.glob")
    @patch("builtins.open", new_callable=mock_open)
    @patch("lxml.etree.fromstring")
    @patch("lxml.etree.tostring")
    @patch("sphinx_diagram_connect.NeedsList")
    @patch("os.path.join", return_value="/mock/outdir/needs.json")
    @patch("lxml.etree.XMLParser")
    @patch("os.getcwd", return_value="/mock/outdir")
    def test_resolve_references_with_needs_json_success(
        self,
        mock_getcwd: MagicMock,
        mock_xml_parser: MagicMock,
        mock_join: MagicMock,
        mock_needs_list: MagicMock,
        mock_tostring: MagicMock,
        mock_fromstring: MagicMock,
        mock_open_file: MagicMock,
        mock_glob: MagicMock,
        mock_sphinx_app: MagicMock,
        mock_logger: MagicMock,
    ):
        """
        Tests `resolve_references` with a mock SVG and `needs_build_json` enabled,
        resolving a needs reference.

        Parameters
        ----------
        mock_getcwd : MagicMock
            Mock for `os.getcwd`.
        mock_xml_parser : MagicMock
            Mock for `lxml.etree.XMLParser`.
        mock_join : MagicMock
            Mock for `os.path.join`.
        mock_needs_list : MagicMock
            Mock for the `NeedsList` class.
        mock_tostring : MagicMock
            Mock for `lxml.etree.tostring`.
        mock_fromstring : MagicMock
            Mock for `lxml.etree.fromstring`.
        mock_open_file : MagicMock
            Mock for `builtins.open`.
        mock_glob : MagicMock
            Mock for `glob.glob`.
        mock_sphinx_app : MagicMock
            A mock Sphinx application object.
        mock_logger : MagicMock
            Mock for the Sphinx logger.
        """
        mock_sphinx_app.config.needs_build_json = True
        diagram_connect_instance = DiagramConnect(mock_sphinx_app)

        mock_needs_list_instance = mock_needs_list.return_value
        mock_needs_list_instance.needs_list = {
            "versions": {
                "1.0": {
                    "needs": {
                        "MY_NEED_001": {
                            "docname": "specifications",
                            "title": "My Test Need",
                        },
                    }
                }
            }
        }

        mock_glob.return_value = ["/mock/outdir/html/_images/diagram.svg"]
        mock_svg_content = b'<svg><a xlink:href=":ref:`MY_NEED_001`">Link</a></svg>'
        mock_open_file.return_value.read.return_value = mock_svg_content

        mock_root = MagicMock()
        mock_element = MagicMock()

        _attributes_dict = {"{http://www.w3.org/1999/xlink}href": ":ref:`MY_NEED_001`"}
        mock_element.attrib = MagicMock()
        mock_element.attrib.__getitem__.side_effect = _attributes_dict.__getitem__
        mock_element.attrib.__setitem__.side_effect = _attributes_dict.__setitem__
        mock_element.attrib.keys.return_value = list(_attributes_dict.keys())

        mock_root.iter.return_value = [mock_element]
        mock_fromstring.return_value = mock_root
        mock_tostring.return_value = (
            b'<svg><a xlink:href="../specifications.html#MY_NEED_001">Link</a></svg>'
        )

        diagram_connect_instance.resolve_references(mock_sphinx_app, None)

        mock_needs_list.assert_called_once()
        mock_xml_parser.assert_called_once_with(ns_clean=True)
        mock_fromstring.assert_called_once_with(
            mock_svg_content, mock_xml_parser.return_value
        )

        assert (
            mock_element.attrib["{http://www.w3.org/1999/xlink}href"]
            == "../specifications.html#MY_NEED_001"
        )
        mock_tostring.assert_called_once()
        mock_logger.info.assert_any_call(
            "Updating SVG file with resolved references:'html/_images/diagram.svg'",
            color="darkblue",
        )

    @patch("sphinx_diagram_connect.glob.glob")
    @patch("builtins.open", new_callable=mock_open)
    @patch("lxml.etree.fromstring")
    @patch("lxml.etree.tostring")
    @patch("lxml.etree.XMLParser")
    @patch("os.getcwd", return_value="/mock/outdir")
    def test_resolve_references_verbose_logging(
        self,
        mock_getcwd: MagicMock,
        mock_xml_parser: MagicMock,
        mock_tostring: MagicMock,
        mock_fromstring: MagicMock,
        mock_open_file: MagicMock,
        mock_glob: MagicMock,
        mock_sphinx_app: MagicMock,
        mock_logger: MagicMock,
    ):
        """
        Tests that verbose logging is enabled when `sphinx_diagram_connect_verbose` is True.

        Parameters
        ----------
        mock_getcwd : MagicMock
            Mock for `os.getcwd`.
        mock_xml_parser : MagicMock
            Mock for `lxml.etree.XMLParser`.
        mock_tostring : MagicMock
            Mock for `lxml.etree.tostring`.
        mock_fromstring : MagicMock
            Mock for `lxml.etree.fromstring`.
        mock_open_file : MagicMock
            Mock for `builtins.open`.
        mock_glob : MagicMock
            Mock for `glob.glob`.
        mock_sphinx_app : MagicMock
            A mock Sphinx application object.
        mock_logger : MagicMock
            Mock for the Sphinx logger.
        """
        mock_sphinx_app.config.sphinx_diagram_connect_verbose = True
        diagram_connect_instance = DiagramConnect(mock_sphinx_app)

        mock_glob.return_value = ["/mock/outdir/html/_images/diagram.svg"]
        mock_svg_content = b'<svg><a xlink:href=":ref:`my-ref`">Link</a></svg>'
        mock_open_file.return_value.read.return_value = mock_svg_content

        mock_root = MagicMock()
        mock_element = MagicMock()

        _attributes_dict = {"{http://www.w3.org/1999/xlink}href": ":ref:`my-ref`"}
        mock_element.attrib = MagicMock()
        mock_element.attrib.__getitem__.side_effect = _attributes_dict.__getitem__
        mock_element.attrib.__setitem__.side_effect = _attributes_dict.__setitem__
        mock_element.attrib.keys.return_value = list(_attributes_dict.keys())

        mock_root.iter.return_value = [mock_element]
        mock_fromstring.return_value = mock_root
        mock_tostring.return_value = (
            b'<svg><a xlink:href="/_static/resolved_my-ref.html">Link</a></svg>'
        )

        diagram_connect_instance.resolve_references(mock_sphinx_app, None)

        mock_logger.info.assert_any_call(
            "href resolution: '%s' -> '%s'"
            % ("my-ref", "/_static/resolved_my-ref.html"),
            color="purple",
        )
        mock_logger.info.assert_any_call(
            "Updating SVG file with resolved references:'html/_images/diagram.svg'",
            color="darkblue",
        )

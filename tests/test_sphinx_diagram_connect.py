import os
import pytest
import re
from unittest.mock import MagicMock, patch, mock_open
from lxml import etree
import types # Import types for checking method types if needed, though removed for now

# Import the DiagramConnect class and setup function from your package
# Assuming the file is named __init__.py inside a package directory
# For testing, we might need to adjust the import path if running tests
# from a different directory. For simplicity, we'll assume it's in the
# same directory or correctly installed for import.
from sphinx_diagram_connect import DiagramConnect, setup, __version__

class TestSetupFunction:
    """
    Tests for the setup function.
    """

    def test_setup_registers_extension(self, mock_sphinx_app):
        """
        Tests that the setup function correctly registers the extension,
        connects the build-finished event, and adds the config value.
        """
        mock_sphinx_app.connect = MagicMock()
        mock_sphinx_app.add_config_value = MagicMock()

        result = setup(mock_sphinx_app)

        # Check if the event is connected
        mock_sphinx_app.connect.assert_called_once()
        # Get the actual arguments passed to connect
        args, kwargs = mock_sphinx_app.connect.call_args
        assert args[0] == "build-finished"
        # The second argument should be the bound method 'resolve_references'
        # Check if it's callable and its qualified name
        assert callable(args[1])
        assert args[1].__qualname__.startswith("DiagramConnect.resolve_references")

        # Check if the config value is added
        mock_sphinx_app.add_config_value.assert_called_once_with(
            "sphinx_diagram_connect_verbose", False, "html"
        )

        # Check the returned metadata
        assert result == {
            "parallel_read_safe": True,
            "parallel_write_safe": True,
            "version": __version__,
        }

class TestDiagramConnect:
    """
    Tests for the DiagramConnect class.
    """

    def test_init(self, mock_sphinx_app):
        """
        Tests the initialization of the DiagramConnect class.
        Ensures that app, verbose setting, and needs_build_json setting are correctly stored.
        """
        instance = DiagramConnect(mock_sphinx_app)
        assert instance.app == mock_sphinx_app
        assert instance.sphinx_diagram_connect_verbose == mock_sphinx_app.config.sphinx_diagram_connect_verbose
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
    def test_init_needs_success(self, mock_join, mock_needs_list, diagram_connect_instance):
        """
        Tests _init_needs when needs.json is valid and contains data.
        """
        # Configure mock_needs_list to return valid data
        mock_needs_list_instance = mock_needs_list.return_value
        mock_needs_list_instance.needs_list = {
            "versions": {
                "1.0": {
                    "needs": {
                        "REQ_001": {"docname": "requirements", "title": "Requirement 1"},
                        "REQ_002": {"docname": "requirements", "title": "Requirement 2"},
                    }
                }
            }
        }

        needs = diagram_connect_instance._init_needs()
        assert needs == {
            "REQ_001": {"docname": "requirements", "title": "Requirement 1"},
            "REQ_002": {"docname": "requirements", "title": "Requirement 2"},
        }
        mock_needs_list_instance.load_json.assert_called_once_with("/mock/outdir/needs.json")
    @patch("sphinx_diagram_connect.NeedsList")
    @patch("os.path.join", return_value="/mock/outdir/needs.json")

    def test_init_needs_no_needs_json(self, mock_join, mock_needs_list, diagram_connect_instance):
        """
        Tests _init_needs when needs.json is empty or invalid.
        """
        mock_needs_list_instance = mock_needs_list.return_value
        mock_needs_list_instance.needs_list = {}  # Simulate empty or invalid needs_list

        needs = diagram_connect_instance._init_needs()
        assert needs is None
        mock_needs_list_instance.load_json.assert_called_once_with("/mock/outdir/needs.json")

    # @pytest.mark.skip("This test is broken")
    def test_resolve_ref_success(self, diagram_connect_instance):
        """
        Tests _resolve_ref with a target that Sphinx can resolve.
        """
        resolved_uri = diagram_connect_instance._resolve_ref("my-ref")
        # Updated: Assert against the new mock path format
        assert resolved_uri == "/_static/resolved_my-ref.html"
        diagram_connect_instance.app.env.domains["std"].resolve_xref.assert_called_once()

    def test_resolve_ref_failure(self, diagram_connect_instance):
        """
        Tests _resolve_ref with a target that Sphinx cannot resolve.
        """
        resolved_uri = diagram_connect_instance._resolve_ref("non-existent-ref")
        assert resolved_uri is None
        diagram_connect_instance.app.env.domains["std"].resolve_xref.assert_called_once()

    @patch("sphinx_diagram_connect.glob.glob")
    @patch("builtins.open", new_callable=mock_open)
    @patch("lxml.etree.fromstring")
    @patch("lxml.etree.tostring")
    @patch("lxml.etree.XMLParser") # Patch XMLParser
    @patch("os.getcwd", return_value="/mock/outdir") # Added patch for os.getcwd()
    def test_resolve_references_html_format_success(self, mock_getcwd, mock_xml_parser, mock_tostring, mock_fromstring, mock_open_file, mock_glob, diagram_connect_instance, mock_logger):
        """
        Tests resolve_references with a mock SVG containing a resolvable Sphinx reference.
        """
        mock_glob.return_value = ["/mock/outdir/html/_images/diagram.svg"]
        mock_svg_content = b'<svg><a xlink:href=":ref:`my-ref`">Link</a></svg>'
        mock_open_file.return_value.read.return_value = mock_svg_content

        # Mock the parsed XML tree and its modification
        mock_root = MagicMock()
        mock_element = MagicMock()
        
        # Create a real dictionary to hold the attributes' state
        _attributes_dict = {"{http://www.w3.org/1999/xlink}href": ":ref:`my-ref`"}

        # Assign a MagicMock to mock_element.attrib
        mock_element.attrib = MagicMock()

        # Configure the MagicMock to simulate dictionary access
        mock_element.attrib.__getitem__.side_effect = _attributes_dict.__getitem__
        mock_element.attrib.__setitem__.side_effect = _attributes_dict.__setitem__
        mock_element.attrib.keys.return_value = list(_attributes_dict.keys()) # For the initial call to .keys()

        mock_root.iter.return_value = [mock_element]
        mock_fromstring.return_value = mock_root
        mock_tostring.return_value = b'<svg><a xlink:href="/_static/resolved_my-ref.html">Link</a></svg>'

        diagram_connect_instance.resolve_references(diagram_connect_instance.app, None)

        mock_open_file.assert_any_call("/mock/outdir/html/_images/diagram.svg", "rb")
        # Assert that XMLParser was called correctly
        mock_xml_parser.assert_called_once_with(ns_clean=True)
        # Assert that fromstring was called with the mock parser
        mock_fromstring.assert_called_once_with(mock_svg_content, mock_xml_parser.return_value)
        
        # Now check the value via dictionary-like access
        assert mock_element.attrib["{http://www.w3.org/1999/xlink}href"] == "/_static/resolved_my-ref.html"
        mock_tostring.assert_called_once_with(mock_root, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        mock_open_file.assert_any_call("/mock/outdir/html/_images/diagram.svg", "wb")
        mock_logger.info.assert_any_call(
            "Updating SVG file with resolved references:'html/_images/diagram.svg'",
            color="darkblue",
        )
        # Removed the assertion for 'href resolution' as it's only called when verbose is True
        # mock_logger.info.assert_any_call(
        #     "href resolution: '%s' -> '%s'" % ("my-ref", "/_static/resolved_my-ref.html"), color="purple"
        # ) # This would be called if verbose is True, need to test that
    
    @patch("sphinx_diagram_connect.glob.glob")
    @patch("builtins.open", new_callable=mock_open)
    @patch("lxml.etree.fromstring")
    @patch("lxml.etree.tostring")
    @patch("lxml.etree.XMLParser") # Patch XMLParser
    @patch("os.getcwd", return_value="/mock/outdir") # Added patch for os.getcwd()
    def test_resolve_references_html_format_unresolved(self, mock_getcwd, mock_xml_parser, mock_tostring, mock_fromstring, mock_open_file, mock_glob, diagram_connect_instance, mock_logger):
        """
        Tests resolve_references with a mock SVG containing an unresolvable Sphinx reference.
        """
        mock_glob.return_value = ["/mock/outdir/html/_images/diagram.svg"]
        mock_svg_content = b'<svg><a xlink:href=":ref:`non-existent-ref`">Link</a></svg>'
        mock_open_file.return_value.read.return_value = mock_svg_content

        mock_root = MagicMock()
        mock_element = MagicMock()

        _attributes_dict = {"{http://www.w3.org/1999/xlink}href": ":ref:`non-existent-ref`"}
        mock_element.attrib = MagicMock()
        mock_element.attrib.__getitem__.side_effect = _attributes_dict.__getitem__
        mock_element.attrib.__setitem__.side_effect = _attributes_dict.__setitem__
        mock_element.attrib.keys.return_value = list(_attributes_dict.keys())
        
        mock_root.iter.return_value = [mock_element]
        mock_fromstring.return_value = mock_root
        mock_tostring.return_value = mock_svg_content # No change, as it's unresolved

        diagram_connect_instance.resolve_references(diagram_connect_instance.app, None)

        mock_open_file.assert_any_call("/mock/outdir/html/_images/diagram.svg", "rb")
        # Assert that XMLParser was called correctly
        mock_xml_parser.assert_called_once_with(ns_clean=True)
        # Assert that fromstring was called with the mock parser
        mock_fromstring.assert_called_once_with(mock_svg_content, mock_xml_parser.return_value)
        
        # The href should remain unchanged since it couldn't be resolved by _resolve_ref or needs
        assert mock_element.attrib["{http://www.w3.org/1999/xlink}href"] == ":ref:`non-existent-ref`"
        mock_tostring.assert_not_called() # Should not write if not modified
        mock_logger.warning.assert_called_once_with(
            "Failed to resolve reference:'%s' in file:'%s'" % ("non-existent-ref", "html/_images/diagram.svg"),
            color="darkred",
            type="sphinx-diagram-connect-missing-reference",
        )
        mock_logger.info.assert_not_called() # No update info if nothing changed

    @patch("sphinx_diagram_connect.glob.glob")
    @patch("builtins.open", new_callable=mock_open)
    @patch("lxml.etree.fromstring")
    @patch("lxml.etree.tostring")
    @patch("sphinx_diagram_connect.NeedsList")
    @patch("os.path.join", return_value="/mock/outdir/needs.json")
    @patch("lxml.etree.XMLParser") # Patch XMLParser
    @patch("os.getcwd", return_value="/mock/outdir") # Added patch for os.getcwd()
    def test_resolve_references_with_needs_json_success(self, mock_getcwd, mock_xml_parser, mock_join, mock_needs_list, mock_tostring, mock_fromstring, mock_open_file, mock_glob, mock_sphinx_app, mock_logger): # Using mock_sphinx_app
        """
        Tests resolve_references with a mock SVG and needs_build_json enabled,
        resolving a needs reference.
        """
        mock_sphinx_app.config.needs_build_json = True # Using mock_sphinx_app
        diagram_connect_instance = DiagramConnect(mock_sphinx_app) # Re-init with updated config

        # Mock needs_list data
        mock_needs_list_instance = mock_needs_list.return_value
        mock_needs_list_instance.needs_list = {
            "versions": {
                "1.0": {
                    "needs": {
                        "MY_NEED_001": {"docname": "specifications", "title": "My Test Need"},
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
        mock_tostring.return_value = b'<svg><a xlink:href="../specifications.html#MY_NEED_001">Link</a></svg>'


        diagram_connect_instance.resolve_references(mock_sphinx_app, None) # Using mock_sphinx_app

        mock_needs_list.assert_called_once() # _init_needs should be called
        # Assert that XMLParser was called correctly
        mock_xml_parser.assert_called_once_with(ns_clean=True)
        # Assert that fromstring was called with the mock parser
        mock_fromstring.assert_called_once_with(mock_svg_content, mock_xml_parser.return_value)

        assert mock_element.attrib["{http://www.w3.org/1999/xlink}href"] == "../specifications.html#MY_NEED_001"
        mock_tostring.assert_called_once()
        mock_logger.info.assert_any_call(
            "Updating SVG file with resolved references:'html/_images/diagram.svg'",
            color="darkblue",
        )
        # Removed the assertion for 'href resolution' as it's only called when verbose is True
        # mock_logger.info.assert_any_call(
        #     "href resolution: '%s' -> '%s'" % ("MY_NEED_001", "../specifications.html#MY_NEED_001"), color="purple"
        # ) # This would be called if verbose is True, need to test that

    @patch("sphinx_diagram_connect.glob.glob")
    @patch("builtins.open", new_callable=mock_open)
    @patch("lxml.etree.fromstring")
    @patch("lxml.etree.tostring")
    @patch("lxml.etree.XMLParser") # Patch XMLParser
    @patch("os.getcwd", return_value="/mock/outdir") # Added patch for os.getcwd()
    def test_resolve_references_verbose_logging(self, mock_getcwd, mock_xml_parser, mock_tostring, mock_fromstring, mock_open_file, mock_glob, mock_sphinx_app, mock_logger): # Using mock_sphinx_app
        """
        Tests that verbose logging is enabled when sphinx_diagram_connect_verbose is True.
        """
        mock_sphinx_app.config.sphinx_diagram_connect_verbose = True # Using mock_sphinx_app
        diagram_connect_instance = DiagramConnect(mock_sphinx_app) # Re-init with updated config

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
        mock_tostring.return_value = b'<svg><a xlink:href="/_static/resolved_my-ref.html">Link</a></svg>'

        diagram_connect_instance.resolve_references(mock_sphinx_app, None) # Using mock_sphinx_app

        mock_logger.info.assert_any_call(
            "href resolution: '%s' -> '%s'" % ("my-ref", "/_static/resolved_my-ref.html"), color="purple"
        )
        mock_logger.info.assert_any_call(
            "Updating SVG file with resolved references:'html/_images/diagram.svg'",
            color="darkblue",
        )

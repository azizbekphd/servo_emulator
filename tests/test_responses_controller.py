import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
import os
import sys

from controllers.responses import ResponsesController, ResponsesControllerState
from config import Config
from utils.conversion import Conversion


class TestResponsesControllerState:
    """Tests for ResponsesControllerState."""

    def test_create_with_defaults(self):
        """Test creating state with default values."""
        state = ResponsesControllerState(config={})
        assert state.workbook is None
        assert state.request_response_pairs == {}
        assert state.sniffer_stack == []
        assert state.config == {}

    def test_create_with_custom_values(self):
        """Test creating state with custom values."""
        config = {"key": "value"}
        pairs = {"req1": "res1"}
        stack = ["item1"]
        
        state = ResponsesControllerState(
            config=config,
            request_response_pairs=pairs,
            sniffer_stack=stack
        )
        
        assert state.config == config
        assert state.request_response_pairs == pairs
        assert state.sniffer_stack == stack

    def test_state_attributes_are_mutable(self):
        """Test that state attributes can be modified."""
        state = ResponsesControllerState(config={})
        state.request_response_pairs["new_key"] = "new_value"
        assert state.request_response_pairs["new_key"] == "new_value"


class TestResponsesController:
    """Tests for ResponsesController class."""

    def test_controller_initialization(self):
        """Test initializing ResponsesController."""
        state = ResponsesControllerState(config={})
        controller = ResponsesController(state)
        assert controller.state == state

    def test_run_calls_load_pairs(self):
        """Test that run() calls load_pairs."""
        state = ResponsesControllerState(config=Config.REQUEST_RESPONSE_PAIRS)
        controller = ResponsesController(state)
        
        with patch.object(controller, 'load_pairs', return_value=True) as mock_load:
            result = controller.run()
            mock_load.assert_called_once()
            assert result is True

    def test_set_pair_converts_to_hex_strings(self):
        """Test that set_pair converts bytes to hex strings."""
        state = ResponsesControllerState(config={})
        controller = ResponsesController(state)
        
        req = bytes([0x0D, 0x0A])
        res = bytes([0x06])
        
        controller.set_pair(req, res)
        
        req_string = Conversion.bytes_to_hex_string(req)
        res_string = Conversion.bytes_to_hex_string(res)
        
        assert state.request_response_pairs[req_string] == res_string

    def test_set_pair_returns_true(self):
        """Test that set_pair returns True."""
        state = ResponsesControllerState(config={})
        controller = ResponsesController(state)
        
        result = controller.set_pair(b"req", b"res")
        assert result is True

    def test_get_response_existing_pair(self):
        """Test getting response for existing request."""
        state = ResponsesControllerState(config={})
        controller = ResponsesController(state)
        
        req = bytes([0x0D])
        res = bytes([0x06])
        controller.set_pair(req, res)
        
        result = controller.get_response(req)
        assert result == res

    def test_get_response_non_existing_returns_ack(self):
        """Test that getting response for non-existing request returns ACK."""
        state = ResponsesControllerState(config={})
        controller = ResponsesController(state)
        
        req = bytes([0xFF])
        result = controller.get_response(req)
        assert result == Config.ACK

    def test_get_response_with_populated_pairs(self):
        """Test getting response with multiple pairs in store."""
        state = ResponsesControllerState(config={})
        controller = ResponsesController(state)
        
        req1 = bytes([0x0D, 0x0A])
        res1 = bytes([0x06])
        req2 = bytes([0xFF])
        res2 = bytes([0x01, 0x02])
        
        controller.set_pair(req1, res1)
        controller.set_pair(req2, res2)
        
        assert controller.get_response(req1) == res1
        assert controller.get_response(req2) == res2

    @patch('controllers.responses.Workbook')
    def test_save_pairs_creates_workbook(self, mock_workbook_class):
        """Test that save_pairs creates a new workbook."""
        mock_workbook = MagicMock()
        mock_workbook_class.return_value = mock_workbook
        
        state = ResponsesControllerState(config=Config.REQUEST_RESPONSE_PAIRS)
        controller = ResponsesController(state)
        
        # Add some pairs
        controller.state.request_response_pairs = {
            "0D 0A": "06",
            "FF": "01 02"
        }
        
        controller.save_pairs()
        
        mock_workbook_class.assert_called_once()

    @patch('controllers.responses.Workbook')
    def test_save_pairs_sets_titles(self, mock_workbook_class):
        """Test that save_pairs sets proper column titles."""
        mock_workbook = MagicMock()
        mock_sheet = MagicMock()
        mock_workbook.active = mock_sheet
        mock_workbook_class.return_value = mock_workbook
        
        state = ResponsesControllerState(config=Config.REQUEST_RESPONSE_PAIRS)
        controller = ResponsesController(state)
        controller.state.request_response_pairs = {"0D": "06"}
        
        controller.save_pairs()
        
        # Check that titles were set
        assert mock_sheet.__setitem__.called

    def test_load_pairs_with_empty_dict(self):
        """Test load_pairs behavior with no file."""
        state = ResponsesControllerState(config=Config.REQUEST_RESPONSE_PAIRS)
        controller = ResponsesController(state)
        
        with patch('controllers.responses.os.path.isfile', return_value=False):
            result = controller.load_pairs()
        
        assert result is True

    def test_multiple_pairs_independence(self):
        """Test that setting multiple pairs doesn't interfere."""
        state = ResponsesControllerState(config={})
        state.request_response_pairs = {}  # Reset to empty dict
        controller = ResponsesController(state)
        
        for i in range(5):
            req = bytes([i])
            res = bytes([i + 10])
            controller.set_pair(req, res)
        
        assert len(state.request_response_pairs) == 5

    def test_pair_storage_format(self):
        """Test that pairs are stored in correct format."""
        state = ResponsesControllerState(config={})
        controller = ResponsesController(state)
        
        req = bytes([0x12, 0x34])
        res = bytes([0x56, 0x78])
        controller.set_pair(req, res)
        
        # Pairs should be stored as hex strings
        pairs = state.request_response_pairs
        assert "12 34" in pairs
        assert pairs["12 34"] == "56 78"

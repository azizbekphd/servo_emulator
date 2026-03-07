import pytest
import sys
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from models.request_response_pair import RequestResponsePair


class TestRequestResponsePair:
    """Tests for RequestResponsePair model."""

    def test_create_with_defaults(self):
        """Test creating RequestResponsePair with default values."""
        pair = RequestResponsePair()
        assert pair.request is None
        assert pair.response is None

    def test_create_with_request_only(self):
        """Test creating RequestResponsePair with request only."""
        pair = RequestResponsePair(request=b"test_request")
        assert pair.request == b"test_request"
        assert pair.response is None

    def test_create_with_response_only(self):
        """Test creating RequestResponsePair with response only."""
        pair = RequestResponsePair(response=b"test_response")
        assert pair.request is None
        assert pair.response == b"test_response"

    def test_create_with_both(self):
        """Test creating RequestResponsePair with both request and response."""
        pair = RequestResponsePair(request=b"req", response=b"res")
        assert pair.request == b"req"
        assert pair.response == b"res"

    def test_request_attribute_modification(self):
        """Test modifying request attribute after creation."""
        pair = RequestResponsePair()
        pair.request = b"modified_request"
        assert pair.request == b"modified_request"

    def test_response_attribute_modification(self):
        """Test modifying response attribute after creation."""
        pair = RequestResponsePair()
        pair.response = b"modified_response"
        assert pair.response == b"modified_response"

    def test_string_requests_and_responses(self):
        """Test that string requests and responses are supported."""
        pair = RequestResponsePair(request="string_request", response="string_response")
        assert pair.request == "string_request"
        assert pair.response == "string_response"

    def test_multiple_instances_independence(self):
        """Test that multiple instances don't share state."""
        pair1 = RequestResponsePair(request=b"req1")
        pair2 = RequestResponsePair(request=b"req2")
        
        assert pair1.request == b"req1"
        assert pair2.request == b"req2"
        assert pair1.request != pair2.request

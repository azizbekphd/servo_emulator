import pytest
from models.serial_signal import SerialSignal


class TestSerialSignal:
    """Tests for SerialSignal model."""

    def test_create_with_bytes_content(self):
        """Test creating SerialSignal with bytes content."""
        signal = SerialSignal(b"test_content")
        assert signal.content == b"test_content"

    def test_create_with_string_content(self):
        """Test creating SerialSignal with string content."""
        signal = SerialSignal("test_content")
        assert signal.content == "test_content"

    def test_create_with_none_content(self):
        """Test creating SerialSignal with None content."""
        signal = SerialSignal(None)
        assert signal.content is None

    def test_create_with_empty_bytes(self):
        """Test creating SerialSignal with empty bytes."""
        signal = SerialSignal(b"")
        assert signal.content == b""

    def test_create_with_empty_string(self):
        """Test creating SerialSignal with empty string."""
        signal = SerialSignal("")
        assert signal.content == ""

    def test_content_modification(self):
        """Test modifying signal content after creation."""
        signal = SerialSignal(b"original")
        signal.content = b"modified"
        assert signal.content == b"modified"

    def test_multiple_instances_independence(self):
        """Test that multiple instances don't share state."""
        signal1 = SerialSignal(b"content1")
        signal2 = SerialSignal(b"content2")
        
        assert signal1.content == b"content1"
        assert signal2.content == b"content2"
        assert signal1.content != signal2.content

    def test_large_content(self):
        """Test creating SerialSignal with large content."""
        large_content = b"x" * 10000
        signal = SerialSignal(large_content)
        assert len(signal.content) == 10000

    def test_special_bytes(self):
        """Test creating SerialSignal with special bytes."""
        special = bytes([0x00, 0xFF, 0x0D, 0x0A])
        signal = SerialSignal(special)
        assert signal.content == special

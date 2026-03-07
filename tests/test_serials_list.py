import pytest
from unittest.mock import Mock
from utils.serials_list import SerialsList


class TestSerialsList:
    """Tests for SerialsList utility class."""

    def test_find_serial_by_port_found(self):
        """Test finding a serial by port when it exists."""
        serial1 = Mock(port="COM1")
        serial2 = Mock(port="COM2")
        serials_list = [serial1, serial2]
        
        result = SerialsList.find_serial_by_port(serials_list, "COM2")
        
        assert result == serial2

    def test_find_serial_by_port_not_found(self):
        """Test finding a serial by port when it doesn't exist."""
        serial1 = Mock(port="COM1")
        serial2 = Mock(port="COM2")
        serials_list = [serial1, serial2]
        
        result = SerialsList.find_serial_by_port(serials_list, "COM99")
        
        assert result is False

    def test_find_serial_by_port_empty_list(self):
        """Test finding a serial in empty list."""
        result = SerialsList.find_serial_by_port([], "COM1")
        assert result is False

    def test_find_serial_by_port_first_serial(self):
        """Test finding the first serial in list."""
        serial1 = Mock(port="COM1")
        serial2 = Mock(port="COM2")
        serials_list = [serial1, serial2]
        
        result = SerialsList.find_serial_by_port(serials_list, "COM1")
        
        assert result == serial1

    def test_find_serial_by_port_last_serial(self):
        """Test finding the last serial in list."""
        serial1 = Mock(port="COM1")
        serial2 = Mock(port="COM2")
        serial3 = Mock(port="COM3")
        serials_list = [serial1, serial2, serial3]
        
        result = SerialsList.find_serial_by_port(serials_list, "COM3")
        
        assert result == serial3

    def test_find_serial_by_port_multiple_serials(self):
        """Test finding correct serial among many."""
        serials_list = [Mock(port=f"COM{i}") for i in range(1, 6)]
        
        result = SerialsList.find_serial_by_port(serials_list, "COM3")
        
        assert result.port == "COM3"

    def test_find_serial_by_port_with_device_path(self):
        """Test finding serial with Linux-style device path."""
        serial1 = Mock(port="/dev/ttyUSB0")
        serial2 = Mock(port="/dev/ttyUSB1")
        serials_list = [serial1, serial2]
        
        result = SerialsList.find_serial_by_port(serials_list, "/dev/ttyUSB1")
        
        assert result == serial2

    def test_find_serial_by_port_case_sensitivity(self):
        """Test that port finding is case-sensitive."""
        serial1 = Mock(port="COM1")
        serials_list = [serial1]
        
        result = SerialsList.find_serial_by_port(serials_list, "com1")
        
        assert result is False

    def test_find_serial_by_port_returns_false_not_none(self):
        """Test that function returns False (not None) when not found."""
        result = SerialsList.find_serial_by_port([], "COM1")
        assert result is False
        assert result is not None

    def test_find_serial_by_port_preserves_serial_object(self):
        """Test that returned serial object is the exact same object."""
        serial1 = Mock(port="COM1")
        serials_list = [serial1]
        
        result = SerialsList.find_serial_by_port(serials_list, "COM1")
        
        assert result is serial1  # Same object, not a copy

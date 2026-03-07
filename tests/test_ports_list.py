import pytest
from unittest.mock import Mock, MagicMock, patch
from utils.ports_list import PortsList


class TestPortsList:
    """Tests for PortsList utility class."""

    @patch('utils.ports_list.comports')
    def test_load_ports_returns_list(self, mock_comports):
        """Test that load_ports returns result from comports."""
        mock_ports = [Mock(name="COM1"), Mock(name="COM2")]
        mock_comports.return_value = mock_ports
        
        result = PortsList.load_ports()
        
        assert result == mock_ports
        mock_comports.assert_called_once_with(include_links=True)

    @patch('utils.ports_list.comports')
    def test_load_ports_with_include_links(self, mock_comports):
        """Test that load_ports calls comports with include_links=True."""
        mock_comports.return_value = []
        
        PortsList.load_ports()
        
        mock_comports.assert_called_once_with(include_links=True)

    def test_find_port_by_name_found(self):
        """Test finding a port by name when it exists."""
        port1 = Mock()
        port1.name = "COM1"
        port2 = Mock()
        port2.name = "COM2"
        ports_list = [port1, port2]
        
        result = PortsList.find_port_by_name(ports_list, "COM2")
        
        assert result == port2

    def test_find_port_by_name_not_found(self):
        """Test finding a port by name when it doesn't exist."""
        port1 = Mock(name="COM1")
        port2 = Mock(name="COM2")
        ports_list = [port1, port2]
        
        result = PortsList.find_port_by_name(ports_list, "COM99")
        
        assert result is False

    def test_find_port_by_name_empty_list(self):
        """Test finding a port in empty list."""
        result = PortsList.find_port_by_name([], "COM1")
        assert result is False

    def test_find_port_by_name_first_port(self):
        """Test finding the first port in list."""
        port1 = Mock()
        port1.name = "COM1"
        port2 = Mock()
        port2.name = "COM2"
        ports_list = [port1, port2]
        
        result = PortsList.find_port_by_name(ports_list, "COM1")
        
        assert result == port1

    def test_find_port_by_address_found(self):
        """Test finding a port by address when it exists."""
        port1 = Mock(device="/dev/ttyUSB0")
        port2 = Mock(device="/dev/ttyUSB1")
        ports_list = [port1, port2]
        
        result = PortsList.find_port_by_address(ports_list, "/dev/ttyUSB1")
        
        assert result == port2

    def test_find_port_by_address_not_found(self):
        """Test finding a port by address when it doesn't exist."""
        port1 = Mock(device="/dev/ttyUSB0")
        port2 = Mock(device="/dev/ttyUSB1")
        ports_list = [port1, port2]
        
        result = PortsList.find_port_by_address(ports_list, "/dev/ttyUSB99")
        
        assert result is False

    def test_find_port_by_address_empty_list(self):
        """Test finding a port by address in empty list."""
        result = PortsList.find_port_by_address([], "/dev/ttyUSB0")
        assert result is False

    def test_find_port_by_address_windows_com(self):
        """Test finding Windows COM port by address."""
        port1 = Mock(device="COM1")
        port2 = Mock(device="COM2")
        ports_list = [port1, port2]
        
        result = PortsList.find_port_by_address(ports_list, "COM1")
        
        assert result == port1

    def test_find_port_by_name_with_special_characters(self):
        """Test finding port with special characters in name."""
        port1 = Mock()
        port1.name = "COM1-USB"
        port2 = Mock()
        port2.name = "COM2-TTL"
        ports_list = [port1, port2]
        
        result = PortsList.find_port_by_name(ports_list, "COM2-TTL")
        
        assert result == port2

    def test_find_port_case_sensitivity(self):
        """Test that port finding is case-sensitive."""
        port1 = Mock(name="COM1")
        ports_list = [port1]
        
        result = PortsList.find_port_by_name(ports_list, "com1")
        
        assert result is False

import pytest
from unittest.mock import Mock, patch, MagicMock
from models.serial_port import SerialPort
import serial


class TestSerialPort:
    """Tests for SerialPort model."""

    def test_create_with_port_only(self):
        """Test creating SerialPort with port name only."""
        port = SerialPort(port="COM1")
        assert port.port == "COM1"
        assert port.baudrate == 9600

    def test_create_with_custom_baudrate(self):
        """Test creating SerialPort with custom baudrate."""
        port = SerialPort(port="COM1", baudrate=115200)
        assert port.port == "COM1"
        assert port.baudrate == 115200

    def test_default_bytesize(self):
        """Test that default bytesize is EIGHTBITS."""
        port = SerialPort()
        assert port.bytesize == serial.EIGHTBITS

    def test_default_parity(self):
        """Test that default parity is NONE."""
        port = SerialPort()
        assert port.parity == serial.PARITY_NONE

    def test_default_stopbits(self):
        """Test that default stopbits is ONE."""
        port = SerialPort()
        assert port.stopbits == serial.STOPBITS_ONE

    def test_default_timeout_is_none(self):
        """Test that default timeout is None."""
        port = SerialPort()
        assert port.timeout is None

    def test_custom_timeout(self):
        """Test creating SerialPort with custom timeout."""
        port = SerialPort(timeout=1.0)
        assert port.timeout == 1.0

    def test_xonxoff_default(self):
        """Test that xonxoff defaults to False."""
        port = SerialPort()
        assert port.xonxoff is False

    def test_xonxoff_enabled(self):
        """Test enabling xonxoff."""
        port = SerialPort(xonxoff=True)
        assert port.xonxoff is True

    def test_rtscts_default(self):
        """Test that rtscts defaults to False."""
        port = SerialPort()
        assert port.rtscts is False

    def test_rtscts_enabled(self):
        """Test enabling rtscts."""
        port = SerialPort(rtscts=True)
        assert port.rtscts is True

    def test_write_timeout(self):
        """Test write_timeout attribute."""
        port = SerialPort(write_timeout=2.0)
        assert port.write_timeout == 2.0

    def test_dsrdtr_default(self):
        """Test that dsrdtr defaults to False."""
        port = SerialPort()
        assert port.dsrdtr is False

    def test_dsrdtr_enabled(self):
        """Test enabling dsrdtr parameter."""
        port = SerialPort(dsrdtr=True)
        assert port.dsrdtr is True

    def test_inter_byte_timeout(self):
        """Test inter_byte_timeout attribute."""
        port = SerialPort(inter_byte_timeout=0.1)
        assert port.inter_byte_timeout == 0.1

    def test_exclusive(self):
        """Test exclusive attribute."""
        port = SerialPort(exclusive=True)
        assert port.exclusive is True

    def test_all_parameters(self):
        """Test creating SerialPort with all parameters."""
        port = SerialPort(
            port="COM3",
            baudrate=57600,
            bytesize=serial.SEVENBITS,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_TWO,
            timeout=2.0,
            xonxoff=True,
            rtscts=True,
            write_timeout=1.0,
            dsrdtr=True,
            inter_byte_timeout=0.05,
            exclusive=True
        )
        assert port.port == "COM3"
        assert port.baudrate == 57600
        assert port.bytesize == serial.SEVENBITS
        assert port.parity == serial.PARITY_EVEN
        assert port.stopbits == serial.STOPBITS_TWO
        assert port.timeout == 2.0
        assert port.xonxoff is True
        assert port.rtscts is True
        assert port.write_timeout == 1.0
        assert port.dsrdtr is True
        assert port.inter_byte_timeout == 0.05
        assert port.exclusive is True

    def test_none_port(self):
        """Test creating SerialPort with None port."""
        port = SerialPort(port=None)
        assert port.port is None

    def test_standard_configurations(self):
        """Test common serial port configurations."""
        # Standard 9600 8N1 configuration
        port = SerialPort(
            port="COM1",
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
        assert port.baudrate == 9600
        assert port.bytesize == serial.EIGHTBITS
        assert port.parity == serial.PARITY_NONE
        assert port.stopbits == serial.STOPBITS_ONE

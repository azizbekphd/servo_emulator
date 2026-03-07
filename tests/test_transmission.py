import pytest
from datetime import datetime
from models.transmission import Transmission, TransmissionType


class TestTransmissionType:
    """Tests for the TransmissionType enum."""

    def test_read_enum_value(self):
        """Test that READ enum has correct value."""
        assert TransmissionType.READ.value == "R"

    def test_write_enum_value(self):
        """Test that WRITE enum has correct value."""
        assert TransmissionType.WRITE.value == "W"

    def test_enum_members_count(self):
        """Test that enum has exactly two members."""
        assert len(list(TransmissionType)) == 2


class TestTransmission:
    """Tests for the Transmission class."""

    def test_create_transmission_with_all_params(self):
        """Test creating transmission with all parameters."""
        t = Transmission(
            ttype=TransmissionType.READ,
            port="COM1",
            data_string="0D 0A FF",
            date="2026-03-08",
            time="12:30:45.123456"
        )
        assert t.ttype == TransmissionType.READ
        assert t.port == "COM1"
        assert t.data_string == "0D 0A FF"
        assert t.date == "2026-03-08"
        assert t.time == "12:30:45.123456"

    def test_create_transmission_with_none_params(self):
        """Test creating transmission with None parameters."""
        t = Transmission()
        assert t.ttype is None
        assert t.port is None
        assert t.data_string is None
        assert t.date is None
        assert t.time is None

    def test_transmission_new_factory_read(self):
        """Test creating transmission via new factory method for READ."""
        data = bytes([0x0D, 0x0A])
        t = Transmission.new(TransmissionType.READ, "COM1", data)
        
        assert t.ttype == TransmissionType.READ
        assert t.port == "COM1"
        assert t.data_string == "0D 0A"
        assert t.date is not None
        assert t.time is not None

    def test_transmission_new_factory_write(self):
        """Test creating transmission via new factory method for WRITE."""
        data = bytes([0xFF, 0xEE])
        t = Transmission.new(TransmissionType.WRITE, "COM2", data)
        
        assert t.ttype == TransmissionType.WRITE
        assert t.port == "COM2"
        assert t.data_string == "FF EE"

    def test_transmission_new_factory_empty_data(self):
        """Test creating transmission with empty data."""
        data = bytes([])
        t = Transmission.new(TransmissionType.READ, "COM1", data)
        
        assert t.data_string == ""

    def test_transmission_new_sets_current_datetime(self):
        """Test that new factory sets current date and time."""
        data = bytes([0x01])
        before = datetime.now()
        t = Transmission.new(TransmissionType.READ, "COM1", data)
        after = datetime.now()
        
        # Parse the date and time from transmission
        trans_datetime_str = f"{t.date} {t.time}"
        trans_datetime = datetime.fromisoformat(trans_datetime_str)
        
        # Check that transmission datetime is within before and after
        assert before <= trans_datetime <= after

    def test_transmission_str_read_symbol(self):
        """Test string representation uses correct symbol for READ."""
        t = Transmission(
            ttype=TransmissionType.READ,
            port="COM1",
            data_string="0D 0A",
            date="2026-03-08",
            time="12:30:45.123456"
        )
        result = str(t)
        assert '<' in result  # READ uses '<'

    def test_transmission_str_write_symbol(self):
        """Test string representation uses correct symbol for WRITE."""
        t = Transmission(
            ttype=TransmissionType.WRITE,
            port="COM1",
            data_string="0D 0A",
            date="2026-03-08",
            time="12:30:45.123456"
        )
        result = str(t)
        assert '>' in result  # WRITE uses '>'

    def test_transmission_str_format(self):
        """Test complete string representation format."""
        t = Transmission(
            ttype=TransmissionType.READ,
            port="COM1",
            data_string="0D 0A",
            date="2026-03-08",
            time="12:30:45.123456"
        )
        result = str(t)
        assert "[2026-03-08 12:30:45.123456]" in result
        assert "COM1" in result
        assert "0D 0A" in result

    def test_transmission_str_contains_all_info(self):
        """Test that string representation contains all transmission info."""
        t = Transmission(
            ttype=TransmissionType.WRITE,
            port="COM99",
            data_string="FF EE DD",
            date="2026-01-01",
            time="10:20:30.000000"
        )
        result = str(t)
        assert "2026-01-01" in result
        assert "10:20:30" in result
        assert "COM99" in result
        assert "FF EE DD" in result
        assert ">" in result

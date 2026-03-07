import pytest
from utils.conversion import Conversion


class TestConversion:
    """Tests for the Conversion utility class."""

    def test_bytes_to_hex_string_list_single_byte(self):
        """Test converting single byte to hex string list."""
        b = bytes([0x0D])
        result = Conversion.bytes_to_hex_string_list(b)
        assert result == ['0D']

    def test_bytes_to_hex_string_list_multiple_bytes(self):
        """Test converting multiple bytes to hex string list."""
        b = bytes([0x0D, 0x0A, 0xFF])
        result = Conversion.bytes_to_hex_string_list(b)
        assert result == ['0D', '0A', 'FF']

    def test_bytes_to_hex_string_list_empty(self):
        """Test converting empty bytes to hex string list."""
        b = bytes([])
        result = Conversion.bytes_to_hex_string_list(b)
        assert result == []

    def test_bytes_to_hex_string_list_zero_bytes(self):
        """Test converting zero bytes to hex string list."""
        b = bytes([0x00, 0x00])
        result = Conversion.bytes_to_hex_string_list(b)
        assert result == ['00', '00']

    def test_bytes_to_hex_string_default_separator(self):
        """Test converting bytes to hex string with default space separator."""
        b = bytes([0x0D, 0x0A, 0xFF])
        result = Conversion.bytes_to_hex_string(b)
        assert result == '0D 0A FF'

    def test_bytes_to_hex_string_custom_separator(self):
        """Test converting bytes to hex string with custom separator."""
        b = bytes([0x0D, 0x0A, 0xFF])
        result = Conversion.bytes_to_hex_string(b, separator='-')
        assert result == '0D-0A-FF'

    def test_bytes_to_hex_string_no_separator(self):
        """Test converting bytes to hex string with no separator."""
        b = bytes([0x0D, 0x0A, 0xFF])
        result = Conversion.bytes_to_hex_string(b, separator='')
        assert result == '0D0AFF'

    def test_bytes_to_hex_string_empty(self):
        """Test converting empty bytes to hex string."""
        b = bytes([])
        result = Conversion.bytes_to_hex_string(b)
        assert result == ''

    def test_hex_string_to_bytes_single(self):
        """Test converting single hex string to bytes."""
        s = '0D'
        result = Conversion.hex_string_to_bytes(s)
        assert result == bytes([0x0D])

    def test_hex_string_to_bytes_multiple(self):
        """Test converting multiple hex values to bytes."""
        s = '0D0AFF'
        result = Conversion.hex_string_to_bytes(s)
        assert result == bytes([0x0D, 0x0A, 0xFF])

    def test_hex_string_to_bytes_with_spaces(self):
        """Test converting hex string with spaces to bytes."""
        s = '0D 0A FF'
        result = Conversion.hex_string_to_bytes(s)
        assert result == bytes([0x0D, 0x0A, 0xFF])

    def test_hex_string_to_bytes_lowercase(self):
        """Test converting lowercase hex string to bytes."""
        s = '0d0aff'
        result = Conversion.hex_string_to_bytes(s)
        assert result == bytes([0x0D, 0x0A, 0xFF])

    def test_roundtrip_conversion(self):
        """Test roundtrip conversion: bytes -> hex string -> bytes."""
        original = bytes([0x0D, 0x0A, 0xFF, 0x01])
        hex_string = Conversion.bytes_to_hex_string(original)
        restored = Conversion.hex_string_to_bytes(hex_string)
        assert restored == original

    def test_roundtrip_conversion_with_custom_separator(self):
        """Test roundtrip conversion requires cleaning custom separator."""
        original = bytes([0x0D, 0x0A, 0xFF])
        hex_string = Conversion.bytes_to_hex_string(original, separator='-')
        # Note: hex_string_to_bytes uses bytes.fromhex() which handles spaces but not other separators
        # So we need to remove the separator before converting back
        cleaned = hex_string.replace('-', '')
        restored = Conversion.hex_string_to_bytes(cleaned)
        assert restored == original

    def test_bytes_to_hex_string_uppercase(self):
        """Test that hex output is uppercase."""
        b = bytes([0xab, 0xcd, 0xef])
        result = Conversion.bytes_to_hex_string(b)
        assert result == 'AB CD EF'

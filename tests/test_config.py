import pytest
from config import Config
from models.program_mode import ProgramModes


class TestConfigConstants:
    """Tests for Config class constants."""

    def test_timeout_value(self):
        """Test that TIMEOUT is set correctly."""
        assert Config.TIMEOUT == 1

    def test_cr_value(self):
        """Test that CR (carriage return) has correct bytes."""
        assert Config.CR == bytes([0x0D])

    def test_ack_value(self):
        """Test that ACK has correct bytes."""
        assert Config.ACK == bytes([0x06])

    def test_input_size(self):
        """Test that INPUT_SIZE is set correctly."""
        assert Config.INPUT_SIZE == 12

    def test_test_output(self):
        """Test that TEST_OUTPUT is set correctly."""
        assert Config.TEST_OUTPUT == b'a'

    def test_program_modes_list(self):
        """Test that PROGRAM_MODES list is initialized."""
        assert isinstance(Config.PROGRAM_MODES, list)
        assert len(Config.PROGRAM_MODES) > 0

    def test_program_modes_contains_sniffer(self):
        """Test that PROGRAM_MODES contains sniffer mode."""
        modes = Config.PROGRAM_MODES
        names = [mode.name for mode in modes]
        assert "Sniffer" in names

    def test_program_modes_contains_emulator(self):
        """Test that PROGRAM_MODES contains emulator mode."""
        modes = Config.PROGRAM_MODES
        names = [mode.name for mode in modes]
        assert "Emulator" in names

    def test_program_modes_sniffer_value(self):
        """Test that sniffer mode has correct enum value."""
        sniffer = next((m for m in Config.PROGRAM_MODES if m.name == "Sniffer"), None)
        assert sniffer is not None
        assert sniffer.value == ProgramModes.SNIFFER

    def test_program_modes_emulator_value(self):
        """Test that emulator mode has correct enum value."""
        emulator = next((m for m in Config.PROGRAM_MODES if m.name == "Emulator"), None)
        assert emulator is not None
        assert emulator.value == ProgramModes.EMULATOR


class TestRequestResponsePairsConfig:
    """Tests for REQUEST_RESPONSE_PAIRS configuration."""

    def test_rrp_config_exists(self):
        """Test that REQUEST_RESPONSE_PAIRS config exists."""
        assert hasattr(Config, 'REQUEST_RESPONSE_PAIRS')
        assert isinstance(Config.REQUEST_RESPONSE_PAIRS, dict)

    def test_rrp_filename(self):
        """Test REQUEST_RESPONSE_PAIRS filename."""
        assert Config.REQUEST_RESPONSE_PAIRS["FILENAME"] == "request_response_pairs.xlsx"

    def test_rrp_worksheet_title(self):
        """Test REQUEST_RESPONSE_PAIRS worksheet title."""
        assert Config.REQUEST_RESPONSE_PAIRS["WORKSHEET_TITLE"] == "Sheet"

    def test_rrp_start_row(self):
        """Test REQUEST_RESPONSE_PAIRS start row."""
        assert Config.REQUEST_RESPONSE_PAIRS["START_ROW"] == 3

    def test_rrp_requests_config(self):
        """Test REQUEST_RESPONSE_PAIRS requests configuration."""
        requests = Config.REQUEST_RESPONSE_PAIRS["REQUESTS"]
        assert requests["TITLE"] == "Request"
        assert requests["COLUMN"] == "A"

    def test_rrp_responses_config(self):
        """Test REQUEST_RESPONSE_PAIRS responses configuration."""
        responses = Config.REQUEST_RESPONSE_PAIRS["RESPONSES"]
        assert responses["TITLE"] == "Response"
        assert responses["COLUMN"] == "B"

    def test_rrp_all_required_keys(self):
        """Test that all required keys exist in REQUEST_RESPONSE_PAIRS."""
        required_keys = ["FILENAME", "WORKSHEET_TITLE", "START_ROW", "REQUESTS", "RESPONSES"]
        for key in required_keys:
            assert key in Config.REQUEST_RESPONSE_PAIRS

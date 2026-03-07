import pytest
from models.program_mode import ProgramMode, ProgramModes


class TestProgramModes:
    """Tests for the ProgramModes enum."""

    def test_sniffer_enum_value(self):
        """Test that SNIFFER enum has correct value."""
        assert ProgramModes.SNIFFER.value == 0

    def test_emulator_enum_value(self):
        """Test that EMULATOR enum has correct value."""
        assert ProgramModes.EMULATOR.value == 1

    def test_enum_members_count(self):
        """Test that enum has exactly two members."""
        assert len(list(ProgramModes)) == 2


class TestProgramMode:
    """Tests for the ProgramMode class."""

    def test_create_sniffer_mode(self):
        """Test creating a sniffer program mode."""
        mode = ProgramMode("Sniffer", ProgramModes.SNIFFER)
        assert mode.name == "Sniffer"
        assert mode.value == ProgramModes.SNIFFER

    def test_create_emulator_mode(self):
        """Test creating an emulator program mode."""
        mode = ProgramMode("Emulator", ProgramModes.EMULATOR)
        assert mode.name == "Emulator"
        assert mode.value == ProgramModes.EMULATOR

    def test_program_mode_name_attribute(self):
        """Test that ProgramMode stores name correctly."""
        mode = ProgramMode("TestMode", ProgramModes.SNIFFER)
        assert mode.name == "TestMode"

    def test_program_mode_value_attribute(self):
        """Test that ProgramMode stores enum value correctly."""
        mode = ProgramMode("TestMode", ProgramModes.EMULATOR)
        assert mode.value == ProgramModes.EMULATOR

    def test_program_mode_with_different_names(self):
        """Test creating modes with different names."""
        sniffer = ProgramMode("Sniff", ProgramModes.SNIFFER)
        emulator = ProgramMode("Emulate", ProgramModes.EMULATOR)
        
        assert sniffer.name == "Sniff"
        assert emulator.name == "Emulate"
        assert sniffer.value != emulator.value

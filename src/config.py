from abc import ABC
from models.program_mode import ProgramMode, ProgramModes


class Config(ABC):

    TIMEOUT = 1
    CR = bytes([0x0D])
    ACK = bytes([0x06])
    INPUT_SIZE = 12
    TEST_OUTPUT = b'a'
    PROGRAM_MODES = [
        ProgramMode(
            "Sniffer", ProgramModes.SNIFFER),
        ProgramMode(
            "Emulator", ProgramModes.EMULATOR),
    ]
    REQUEST_RESPONSE_PAIRS = {
        "FILENAME": "request_response_pairs.xlsx",
        "WORKSHEET_TITLE": "Sheet",
        "START_ROW": 3,
        "REQUESTS": {
            "TITLE": "Request",
            "COLUMN": "A",
        },
        "RESPONSES": {
            "TITLE": "Response",
            "COLUMN": "B",
        }
    }

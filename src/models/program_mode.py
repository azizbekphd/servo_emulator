from enum import Enum

class ProgramModes(Enum):
    SNIFFER = 0
    EMULATOR = 1

class ProgramMode:

    def __init__(self, name, value):
        self.name = name
        self.value = value


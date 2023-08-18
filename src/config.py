from abc import ABC

class Config(ABC):

    TIMEOUT = 1
    CR = bytes([0x0D])
    ACK = bytes([0x06])
    INPUT_SIZE = 12
    TEST_OUTPUT = b'a'


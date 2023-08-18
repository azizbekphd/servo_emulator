from enum import Enum
import datetime

from utils.conversion import Conversion

class TransmissionType(Enum):
    READ = "R"
    WRITE = "W"

class Transmission:

    def __init__(self, ttype=None, port=None, data_string=None,
                 date=None, time=None):
        self.ttype = ttype
        self.port = port
        self.data_string = data_string
        self.date = date
        self.time = time

    @staticmethod
    def new(ttype, port, data):
        now = datetime.datetime.now()
        data_string = ' '.join(Conversion.bytes_to_hex_string_list(data))
        return Transmission(ttype, port, data_string,
                             str(now.date()), str(now.time()))

    def __str__(self):
        direction = '<' if self.ttype == TransmissionType.READ else '>'
        return (f'[{self.date} {self.time}] {self.port} ' +
                f'{direction} {self.data_string}')


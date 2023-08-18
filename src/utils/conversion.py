from abc import ABC, abstractmethod

class Conversion(ABC):

    @abstractmethod
    def bytes_to_hex_string_list(b):
        bh = b.hex()
        return [bh[i:i+2].upper() for i in range(0, len(bh), 2)]


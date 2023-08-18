from abc import ABC, abstractmethod

class SerialsList(ABC):

    @abstractmethod
    def find_serial_by_port(serials_list, port):
        for ser in serials_list:
            if ser.port == port:
                return ser
        return False


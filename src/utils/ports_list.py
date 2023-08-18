from serial.tools.list_ports import comports 
from abc import ABC, abstractmethod

class PortsList(ABC):

    @abstractmethod
    def load_ports():
        return comports(include_links=True)

    @abstractmethod
    def find_port_by_name(ports_list, name):
        for port in ports_list:
            if port.name == name:
                return port
        return False

    @abstractmethod
    def find_port_by_address(ports_list, address):
        for port in ports_list:
            if port.device == address:
                return port
        return False


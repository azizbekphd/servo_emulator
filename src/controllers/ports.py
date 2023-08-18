from utils.ports_list import PortsList
from utils.serials_list import SerialsList
from models.transmission import Transmission, TransmissionType
from config import Config

from kivy.storage.dictstore import DictStore
from kivy.clock import Clock
from kivy.logger import Logger
from serial import Serial
from enum import Enum
from threading import Thread

class PortsControllerState:

    def __init__(self, input_port=None, output_port=None,
                    input_serial=None, output_serial=None,
                    serials=[], ports=[], transmissions=[]):
        self.input_port = input_port
        self.output_port = output_port
        self.input_serial = input_serial
        self.output_serial = output_serial
        self.serials = serials
        self.ports = ports
        self.transmissions = transmissions

class PortsStoreKeys(Enum):
    INPUT_PORT = "input_port"
    OUTPUT_PORT = "output_port"

class PortsController:

    def __init__(self):
        self.state = PortsControllerState()
        self.store = DictStore('ports.py')
        self.listen = True

    def run(self):
        self.load_ports()
        self.refresh_serials()
        self.start_listener()

    def refresh(self):
        self.refresh_serials()
        self.start_listener()

    def ports_available(self):
        return len(self.state.ports) > 0

    def select_input_port(self, port):
        self.store.put(PortsStoreKeys.INPUT_PORT, port=port.device)
        self.state.input_port = port
        self.refresh()

    def select_output_port(self, port):
        self.store.put(PortsStoreKeys.OUTPUT_PORT, port=port.device)
        self.state.output_port = port
        self.refresh()

    def load_ports(self):
        self.state.ports = PortsList.load_ports()
        if (len(self.state.ports) == 0):
            return False

        self.state.serials = [Serial(port.device, timeout=Config.TIMEOUT)
                              for port in self.state.ports]

        if (self.store.exists(PortsStoreKeys.INPUT_PORT)):
            self.state.input_port = PortsList.find_port_by_address(
                    self.state.ports,
                    self.store.get(PortsStoreKeys.INPUT_PORT)['port'])
        if (self.store.exists(PortsStoreKeys.OUTPUT_PORT)):
            self.state.output_port = PortsList.find_port_by_address(
                    self.state.ports,
                    self.store.get(PortsStoreKeys.OUTPUT_PORT)['port'])
        return True

    def refresh_serials(self):
        if (self.state.input_port):
            self.state.input_serial = SerialsList.find_serial_by_port(
                    self.state.serials,
                    self.state.input_port.device)
            if (not (self.state.input_serial
                     and self.state.input_serial.is_open)):
                self.state.input_serial.open()
        if (self.state.output_port):
            self.state.output_serial = SerialsList.find_serial_by_port(
                    self.state.serials,
                    self.state.output_port.device)
            if (not (self.state.output_serial
                     and self.state.output_serial.is_open)):
                self.state.output_serial.open()
        return True

    def start_listener(self):
        if (not (self.state.input_serial and self.state.output_serial)):
            return False
        self.listen = False

        thread = Thread(target=self.listener, daemon=True)
        thread.start()

        Clock.schedule_once(lambda _: setattr(self, 'listen', True),
                            Config.TIMEOUT)
        return True

    def listener(self):
        thread = Thread(target=self.listener_callback)
        thread.start()
        thread.join()

    def listener_callback(self):
        rdata = self.state.input_serial.read_until(
                expected=Config.CR, size=Config.INPUT_SIZE)
        if (not rdata):
            if (self.listen):
                self.listener()
            return
        self.add_transmission(TransmissionType.READ,
                              self.state.input_port.device, rdata)

        wdata = Config.ACK
        self.state.output_serial.write(wdata)
        self.add_transmission(TransmissionType.WRITE,
                              self.state.output_port.device, wdata)
        self.listener()
        return True

    def add_transmission(self, ttype, port, data):
        t = Transmission.new(ttype, port, data)
        self.state.transmissions.append(t)

    def get_queued_transmission(self):
        if (len(self.state.transmissions) == 0):
            return False
        return self.state.transmissions.pop(0)


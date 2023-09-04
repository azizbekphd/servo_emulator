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
                 serials=[], ports=[], transmissions=[],
                 program_modes=[], program_mode=None):
        self.input_port = input_port
        self.output_port = output_port
        self.input_serial = input_serial
        self.output_serial = output_serial
        self.serials = serials
        self.ports = ports
        self.transmissions = transmissions
        self.program_modes = program_modes
        self.program_mode = program_mode


class PortsStoreKeys(Enum):
    PROGRAM_MODE = "program_mode"
    INPUT_PORT = "input_port"
    OUTPUT_PORT = "output_port"


class PortsController:

    def __init__(self):
        self.state = PortsControllerState()
        self.store = DictStore('settings')
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

    def select_program_mode(self, program_mode):
        self.store.put(PortsStoreKeys.PROGRAM_MODE, value=program_mode.value)
        self.state.program_mode = program_mode
        self.refresh()

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
        self.state.program_modes = Config.PROGRAM_MODES
        if (len(self.state.ports) == 0):
            return False

        self.state.serials = [Serial(port.device, timeout=Config.TIMEOUT)
                              for port in self.state.ports]

        if (self.store.exists(PortsStoreKeys.PROGRAM_MODE)):
            self.state.program_mode = next(
                    (mode for mode in self.state.program_modes if mode.value ==
                     self.store.get(PortsStoreKeys.PROGRAM_MODE)['value']),
                    [None])
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
        if (not (self.state.program_mode and
                 self.state.input_serial and
                 self.state.output_serial)):
            return False

        thread = Thread(target=self.listener, daemon=True)
        thread.start()

        Clock.schedule_once(lambda _: setattr(self, 'listen', True),
                            Config.TIMEOUT)
        return True

    def listener(self):
        while (self.listen):
            self.listener_callback()

    def listener_callback(self):
        rdata = self.state.input_serial.read_until(
                expected=Config.CR, size=Config.INPUT_SIZE)
        if (rdata):
            self.add_transmission(TransmissionType.READ,
                                  self.state.input_port.device, rdata)
        return

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
        t = self.state.transmissions[:]
        del self.state.transmissions[:]
        return t

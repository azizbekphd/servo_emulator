from utils.ports_list import PortsList
from utils.serials_list import SerialsList
from models.transmission import Transmission, TransmissionType
from models.program_mode import ProgramModes
from config import Config

from kivy.storage.dictstore import DictStore
from kivy.clock import Clock
from serial import Serial
from enum import Enum
from threading import Thread


class PortsControllerState:

    def __init__(self, input_port=None, output_port=None,
                 input_serial=None, output_serial=None,
                 serials=[], ports=[], transmissions=[],
                 program_modes=[], program_mode=None,
                 baud_rate=Config.BAUD_RATE):
        self.input_port = input_port
        self.output_port = output_port
        self.input_serial = input_serial
        self.output_serial = output_serial
        self.serials = serials
        self.ports = ports
        self.transmissions = transmissions
        self.program_modes = program_modes
        self.program_mode = program_mode
        self.baud_rate = baud_rate


class PortsStoreKeys(Enum):
    PROGRAM_MODE = "program_mode"
    INPUT_PORT = "input_port"
    OUTPUT_PORT = "output_port"
    BAUD_RATE = "baud_rate"


class PortsController:

    def __init__(self, responses_controller):
        self.responses = responses_controller
        self.state = PortsControllerState()
        self.store = DictStore('settings')
        self.listen = True

    def run(self):
        self.load_ports()
        self.refresh()

    def refresh(self):
        self.refresh_serials()
        self.start_listener()

    def ports_available(self):
        return len(self.state.ports) > 0

    def select_program_mode(self, program_mode):
        self.store.put(PortsStoreKeys.PROGRAM_MODE.value, value=program_mode.value)
        self.state.program_mode = program_mode
        Clock.schedule_once(lambda _: self.refresh(), Config.TIMEOUT)

    def select_baud_rate(self, baud_rate):
        self.store.put(PortsStoreKeys.BAUD_RATE.value, value=baud_rate)
        self.state.baud_rate = baud_rate
        self.refresh()

    def select_input_port(self, port):
        self.store.put(PortsStoreKeys.INPUT_PORT.value, port=port.device)
        self.state.input_port = port
        self.refresh()

    def select_output_port(self, port):
        self.store.put(PortsStoreKeys.OUTPUT_PORT.value, port=port.device)
        self.state.output_port = port
        self.refresh()

    def load_ports(self):
        self.state.ports = PortsList.load_ports()
        self.state.program_modes = Config.PROGRAM_MODES
        if (len(self.state.ports) == 0):
            return False

        if (self.store.exists(PortsStoreKeys.BAUD_RATE.value)):
            self.state.baud_rate = self.store.get(
                PortsStoreKeys.BAUD_RATE.value)['value']

        if (self.store.exists(PortsStoreKeys.PROGRAM_MODE.value)):
            self.state.program_mode = next(
                (mode for mode in self.state.program_modes if mode.value ==
                 self.store.get(PortsStoreKeys.PROGRAM_MODE.value)['value']),
                [None])

        if (self.store.exists(PortsStoreKeys.INPUT_PORT.value)):
            self.state.input_port = PortsList.find_port_by_address(
                self.state.ports,
                self.store.get(PortsStoreKeys.INPUT_PORT.value)['port'])

        if (self.store.exists(PortsStoreKeys.OUTPUT_PORT.value)):
            self.state.output_port = PortsList.find_port_by_address(
                self.state.ports,
                self.store.get(PortsStoreKeys.OUTPUT_PORT.value)['port'])
        return True

    def refresh_serials(self):
        try:
            if (self.state.input_serial):
                self.state.input_serial.close()
            if (self.state.output_serial):
                self.state.output_serial.close()

            if (self.state.input_port):
                self.state.input_serial = Serial(
                    self.state.input_port.device,
                    baudrate=self.state.baud_rate,
                    timeout=Config.TIMEOUT)
            
            if (self.state.output_port):
                self.state.output_serial = Serial(
                    self.state.output_port.device,
                    baudrate=self.state.baud_rate,
                    timeout=Config.TIMEOUT)
        except Exception as e:
            print(f"Error opening serial ports: {e}")
            return False
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
        try:
            if (self.state.program_mode.value == ProgramModes.EMULATOR):
                self.emulator_callback()
            elif (self.state.program_mode.value == ProgramModes.SNIFFER):
                self.sniffer_callback()
        except Exception as e:
            print(f"Listener error: {e}")

    def emulator_callback(self):
        while (self.listen and
               self.state.program_mode.value == ProgramModes.EMULATOR):
            try:
                rdata = self.state.input_serial.read_until(
                    expected=Config.CR, size=Config.INPUT_SIZE)
                if (not rdata):
                    continue
                self.add_transmission(TransmissionType.READ,
                                      self.state.input_port.device, rdata)
                wdata = self.responses.get_response(rdata)
                self.state.output_serial.write(wdata)
                self.add_transmission(TransmissionType.WRITE,
                                      self.state.output_port.device, wdata)
            except Exception as e:
                print(f"Emulator error: {e}")
                break

    def sniffer_callback(self):
        controller_port_thread = Thread(
            target=self.sniffer_controller_listener, daemon=True)
        slave_port_thread = Thread(
            target=self.sniffer_slave_listener, daemon=True)
        controller_port_thread.start()
        slave_port_thread.start()

    def sniffer_controller_listener(self):
        while (self.listen and
               self.state.program_mode.value == ProgramModes.SNIFFER):
            try:
                rdata = self.state.input_serial.read_until(
                    expected=Config.CR, size=Config.INPUT_SIZE)
                if (not rdata):
                    continue
                self.add_transmission(TransmissionType.READ,
                                      self.state.input_port.device, rdata)

                wdata = rdata
                self.state.output_serial.write(wdata)
                self.add_transmission(TransmissionType.WRITE,
                                      self.state.output_port.device, wdata)

                self.responses.state.sniffer_stack.append(rdata)
            except Exception as e:
                print(f"Controller listener error: {e}")
                break

    def sniffer_slave_listener(self):
        while (self.listen and
               self.state.program_mode.value == ProgramModes.SNIFFER):
            try:
                # Use read_until(Config.CR) instead of read(1) to get full responses
                rdata = self.state.output_serial.read_until(
                    expected=Config.CR, size=Config.INPUT_SIZE)
                if (not rdata):
                    continue
                self.add_transmission(TransmissionType.READ,
                                      self.state.output_port.device, rdata)

                wdata = rdata
                self.state.input_serial.write(wdata)
                self.add_transmission(TransmissionType.WRITE,
                                      self.state.input_port.device, wdata)

                if (not self.responses.state.sniffer_stack):
                    continue
                self.responses.set_pair(
                    self.responses.state.sniffer_stack.pop(0), rdata)
            except Exception as e:
                print(f"Slave listener error: {e}")
                break

    def add_transmission(self, ttype, port, data):
        t = Transmission.new(ttype, port, data)
        self.state.transmissions.append(t)

    def get_queued_transmission(self):
        if (len(self.state.transmissions) == 0):
            return False
        t = self.state.transmissions[:]
        del self.state.transmissions[:]
        return t

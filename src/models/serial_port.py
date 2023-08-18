import serial

class SerialPort:

    def __init__(self, port=None, baudrate=9600, bytesize=serial.EIGHTBITS,
                 parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                 timeout=None, xonxoff=False, rtscts=False,
                 write_timeout=None, dsrdtr=False,
                 inter_byte_timeout=None, exclusive=None):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self.write_timeout = write_timeout
        self.dsrstr = dsrdtr
        self.inter_byte_timeout = inter_byte_timeout
        self.exclusive = exclusive


class Locale:
    def __init__(
            self,
            please_choose=None,
            no_com_ports_found=None,
            program_mode=None,
            baud_rate=None,
            input_com_port=None,
            output_com_port=None
            ):
        self.please_choose = please_choose
        self.no_com_ports_found = no_com_ports_found
        self.program_mode = program_mode
        self.baud_rate = baud_rate
        self.input_com_port = input_com_port
        self.output_com_port = output_com_port

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.logger import Logger

from controllers.ports import PortsController
from utils.ports_list import PortsList
from i18n.i18n import I18n

Builder.load_string('''
<LogsWidget>:
    viewclass: 'LogRow'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')

class LogsWidget(RecycleView):
    def __init__(self, **kwargs):
        super(LogsWidget, self).__init__(**kwargs)
        self.data = []

class LogRow(Label):
    def __init__(self, **kwargs):
        super(LogRow, self).__init__(**kwargs)
        self.halign = 'left'

class MainScreen:

    ports = PortsController()
    layout = GridLayout(padding=10)

    def __input_serial_menu_on_release(self, port):
        self.__input_serial_menu_button.text = port.name if port else "Please, choose..."
        self.ports.select_input_port(port)
        return True

    def __output_serial_menu_on_release(self, port):
        self.__output_serial_menu_button.text = port.name if port else "Please, choose..."
        self.ports.select_output_port(port)
        return True

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.layout.rows = 2
        self.layout.padding = 15

        ports_control_grid = GridLayout()
        ports_control_grid.cols = 2
        ports_control_grid.spacing = [0, 8]
        ports_control_grid.size_hint_max_y = 94

        self.ports.run()
        ports_available = self.ports.ports_available()
        ports_list = self.ports.state.ports if (ports_available) else []

        # Input port
        button_text = self.ports.state.input_port.name if (
                self.ports.state.input_serial) else "Please, choose..."
        self.__input_serial_menu_button = Button(
                text=button_text, size_hint_max_y=35)
        self.__input_serial_menu = DropDown()

        # Output port
        button_text = self.ports.state.output_port.name if (
                self.ports.state.output_serial) else "Please, choose..."
        self.__output_serial_menu_button = Button(
                text=button_text, size_hint_max_y=35)
        self.__output_serial_menu = DropDown()

        if (ports_available):
            for port in ports_list:

                # Input port
                input_menu_button = Button(text=port.name,
                                size_hint_y=None, height=30)
                input_menu_button.bind(on_release=lambda btn:
                                 self.__input_serial_menu.select(
                                    PortsList.find_port_by_name(
                                        ports_list, btn.text)))
                self.__input_serial_menu.add_widget(input_menu_button)

                # Output port
                output_menu_button = Button(text=port.name,
                                     size_hint_y=None, height=30)
                output_menu_button.bind(on_release=lambda btn:
                                 self.__output_serial_menu.select(
                                    PortsList.find_port_by_name(
                                        ports_list, btn.text)))
                self.__output_serial_menu.add_widget(output_menu_button)

        # Input port
        ports_control_grid.add_widget(Label(text="Input COM Port:"))
        self.__input_serial_menu_button.bind(on_release=
                                             self.__input_serial_menu.open)
        self.__input_serial_menu.bind(on_select=lambda _, port:
                             self.__input_serial_menu_on_release(port))
        ports_control_grid.add_widget(self.__input_serial_menu_button)

        # Output port
        ports_control_grid.add_widget(Label(text="Output COM Port:"))
        self.__output_serial_menu_button.bind(on_release=
                                             self.__output_serial_menu.open)
        self.__output_serial_menu.bind(on_select=lambda _, port:
                             self.__output_serial_menu_on_release(port))
        ports_control_grid.add_widget(self.__output_serial_menu_button)

        self.layout.add_widget(ports_control_grid)
        self.logs_widget = LogsWidget()
        self.layout.add_widget(self.logs_widget)
        Clock.schedule_interval(lambda dt: self.update_logs(), 0.05)

    def update_logs(self):
        t = self.ports.get_queued_transmission()
        if (not t):
            return
        if (len(self.logs_widget.data) >= 99):
            self.logs_widget.data.pop(0)
        self.logs_widget.data.append({'text': str(t)})
        self.logs_widget.scroll_y = 0
        return True


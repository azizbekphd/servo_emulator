import os
import kivy
from kivy.base import EventLoop
from kivy.config import Config as KivyConfig

from kivy.core.window import Window
from kivy.app import App
from ui.windows.main import MainScreen


class ServoEmulatorApp(App):

    def on_request_close(self, *args):
        self.responses_controller.save_pairs()
        self.stop()
        return True

    def build(self):

        main_screen = MainScreen()
        self.responses_controller = main_screen.responses
        Window.bind(on_request_close=self.on_request_close)
        return main_screen.layout


if __name__ == '__main__':
    os.environ['KIVY_GL_BACKEND'] = 'gl'
    kivy.require('2.1.0')
    EventLoop.ensure_window()
    KivyConfig.set('kivy', 'exit_on_escape', '0')
    ServoEmulatorApp().run()


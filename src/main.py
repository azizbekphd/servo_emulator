import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
import kivy
kivy.require('2.1.0')
from kivy.base import EventLoop
EventLoop.ensure_window()

from kivy.app import App
from ui.windows.main import MainScreen

class ServoEmulatorApp(App):

    def build(self):
        return MainScreen().layout

if __name__ == '__main__':
    ServoEmulatorApp().run()


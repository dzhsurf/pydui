# application.py
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class PyDuiApplication:
    @staticmethod
    def main_run():
        Gtk.main()

    @staticmethod
    def main_quit():
        Gtk.main_quit()

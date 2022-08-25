""" PyDuiApplication module

Example::

    PyDuiApplication.main_run()


"""
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class PyDuiApplication:

    """Application global function"""

    @staticmethod
    def main_run():
        """Start main run-loop"""
        Gtk.main()

    @staticmethod
    def main_quit():
        """Quit main run-loop"""
        Gtk.main_quit()

# -*- coding: utf-8 -*-
""" PyDuiApplication module

Example::

    PyDuiApplication.main_run()


"""
from pydui.common.import_gtk import *


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

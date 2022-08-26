import random

import gi

from pydui.core.layout import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk


class PyDuiHLayout(PyDuiLayout):
    """Horizontal layout"""

    def __init__(self):
        super().__init__()
        self.set_gtk_widget(Gtk.HBox())

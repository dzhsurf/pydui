import gi

from pydui.core.layout import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk


class PyDuiVLayout(PyDuiLayout):

    """Vertical layout"""

    def __init__(self):
        super().__init__()
        self.set_gtk_widget(Gtk.VBox())

"""FixedLayout unit
"""

import gi

from pydui.core.base import *
from pydui.core.layout import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk


class PyDuiFixedLayout(PyDuiLayout):
    """FixedLayout implement"""

    def __init__(self, parent: PyDuiWidget):
        # custom_gtk_widget = Gtk.Fixed.new()
        super().__init__(parent, custom_gtk_widget)

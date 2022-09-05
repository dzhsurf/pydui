"""FixedLayout unit
"""

from pydui.core.base import *
from pydui.core.import_gtk import *
from pydui.core.layout import *


class PyDuiFixedLayout(PyDuiLayout):
    """FixedLayout implement"""

    def __init__(self, parent: PyDuiWidget):
        # custom_gtk_widget = Gtk.Fixed.new()
        super().__init__(parent, custom_gtk_widget)

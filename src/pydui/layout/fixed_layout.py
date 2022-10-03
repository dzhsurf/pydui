# -*- coding: utf-8 -*-
"""FixedLayout unit
"""

from pydui.common.base import *
from pydui.common.import_gtk import *
from pydui.core.layout import *


class PyDuiFixedLayout(PyDuiLayout):
    """FixedLayout implement"""

    @staticmethod
    def build_name() -> str:
        return "FixedLayout"

    def __init__(self, parent: PyDuiWidget):
        # custom_gtk_widget = Gtk.Fixed.new()
        super().__init__(parent, None)

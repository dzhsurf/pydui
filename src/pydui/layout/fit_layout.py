# -*- coding: utf-8 -*-
"""FitLayout unit
"""

from pydui.core.layout import *
from pydui.core.widget import *


class PyDuiFitLayout(PyDuiLayout):
    """FitLayout implement"""

    @staticmethod
    def build_name() -> str:
        return "FitLayout"

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)

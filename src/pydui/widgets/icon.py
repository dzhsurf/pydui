# -*- coding: utf-8 -*-
from pydui.core.widget import PyDuiWidget
from pydui.widgets.label import PyDuiLabel


class PyDuiIcon(PyDuiLabel):
    @staticmethod
    def build_name() -> str:
        return "Icon"

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)

    def parse_attrib(self, k: str, v: str):
        if k == "icon":
            self.bkimage = v
        return super().parse_attrib(k, v)

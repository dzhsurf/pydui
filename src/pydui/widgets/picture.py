# -*- coding: utf-8 -*-
from pydui.core.widget import PyDuiWidget
from pydui.widgets.label import PyDuiLabel


class PyDuiPicture(PyDuiLabel):
    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)

    def parse_attrib(self, k: str, v: str):
        if k == "image":
            self.bkimage = v
        return super().parse_attrib(k, v)

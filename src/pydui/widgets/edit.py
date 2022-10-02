# -*- coding: utf-8 -*-
from pydui.core.widget import PyDuiWidget
from pydui.widgets.pgview import PyDuiPGView


class PyDuiEdit(PyDuiPGView):
    @staticmethod
    def build_name() -> str:
        return "Edit"

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)

    def parse_attrib(self, k: str, v: str):
        return super().parse_attrib(k, v)

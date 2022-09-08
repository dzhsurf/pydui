# -*- coding: utf-8 -*-
from pydui.core.widget import PyDuiWidget


class PyDuiEdit(PyDuiWidget):
    @staticmethod
    def build_name() -> str:
        return "Edit"

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)

    def parse_attrib(self, k: str, v: str):
        return super().parse_attrib(k, v)

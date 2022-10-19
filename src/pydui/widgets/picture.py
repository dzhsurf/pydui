# -*- coding: utf-8 -*-
from pydui.widgets.label import PyDuiLabel


class PyDuiPicture(PyDuiLabel):
    @staticmethod
    def build_name() -> str:
        return "Picture"

    def __init__(self):
        super().__init__()

    def parse_attrib(self, k: str, v: str):
        if k == "image":
            self.bkimage = v
        return super().parse_attrib(k, v)

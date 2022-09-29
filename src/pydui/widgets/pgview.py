# -*- coding: utf-8 -*-
from typing import Iterable, Tuple

from poga import *

from pydui import utils
from pydui.core.base import PyDuiLayoutConstraint
from pydui.core.widget import PyDuiWidget
from pydui.utils.poga_utils import *

class PyDuiPGView(PyDuiWidget, PogaView):
    """PyDuiPGView
    """

    # PyDuiWidget interface
    @staticmethod
    def build_name() -> str:
        return "PGView"

    # PyDuiWidget interface
    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)
        self.__layout = PogaLayout(self)

    def parse_attrib(self, k: str, v: str):
        if not apply_poga_attributes(self.__layout, k, v):
            super().parse_attrib(k, v)

    # PogaView interface
    # PogaView interface
    def size_that_fits(self, width: float, height: float) -> Tuple[float, float]:
        # only leaf node will call this function
        # override by subclass
        return (0, 0)

    def frame_origin(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def set_frame_origin(self, x: float, y: float):
        super().layout(x, y, self.width, self.height, constraint=PyDuiLayoutConstraint())

    def set_frame_size(self, width: float, height: float):
        super().layout(self.x, self.y, width, height, constraint=PyDuiLayoutConstraint())

    def bounds_size(self) -> Tuple[float, float]:
        return (self.width, self.height)

    def subviews_count(self) -> int:
        return 0

    def subviews(self) -> Iterable[PogaView]:
        # PGView is leaf, without any subview
        return list()

    def poga_layout(self) -> PogaLayout:
        return self.__layout

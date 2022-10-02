# -*- coding: utf-8 -*-
from typing import Iterable, Tuple

from poga import *

from pydui import utils
from pydui.core.base import PyDuiLayoutConstraint
from pydui.core.import_gtk import *
from pydui.core.widget import PyDuiWidget
from pydui.utils.poga_utils import *


class PyDuiPGView(PyDuiWidget, PogaView):
    """PyDuiPGView"""

    # PyDuiWidget interface
    @staticmethod
    def build_name() -> str:
        return "Control"

    # PyDuiWidget interface
    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)
        self.__layout = PogaLayout(self)

    def parse_attrib(self, k: str, v: str):
        super().parse_attrib(k, v)
        # not a pglayout item
        if k.lower() in ["width", "height", "margin", "align_self"]:
            apply_poga_attributes(self.__layout, k, v)

    def draw(self, ctx: cairo.Context, x: float, y: float, width: float, height: float):
        super().draw(ctx, x, y, width, height)

    # PogaView interface
    # PogaView interface
    def size_that_fits(self, width: float, height: float) -> Tuple[float, float]:
        # only leaf node will call this function
        # override by subclass
        constraint = PyDuiLayoutConstraint()
        if not YGFloatIsUndefined(width):
            constraint.width = width
        if not YGFloatIsUndefined(height):
            constraint.height = height
        size = self.estimate_size(width, height, constraint=constraint)
        if size[0] == 0:
            size = (width, size[1])
        if size[1] == 0:
            size = (size[0], height)
        # print(self, "size_that_fits", "w", width, "h", height, "size", size)
        return size

    def frame_origin(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def set_frame_origin(self, x: float, y: float):
        # print(self, "set_frame_origin", "x", x, "y", y)
        layout_x, layout_y = x, y
        if self.parent is not None:
            layout_x += self.parent.x
            layout_y += self.parent.y
        super().layout(layout_x, layout_y, self.width, self.height, constraint=PyDuiLayoutConstraint())

    def set_frame_size(self, width: float, height: float):
        # print(self, "set_frame_size", "w", width, "h", height)
        super().layout(self.x, self.y, width, height, constraint=PyDuiLayoutConstraint())

    def bounds_size(self) -> Tuple[float, float]:
        return (self.width, self.height)

    def subviews_count(self) -> int:
        return 0

    def subviews(self) -> Iterable[PogaView]:
        # PGView is leaf, without any subview
        return list()

    def is_container(self) -> bool:
        return False

    def poga_layout(self) -> PogaLayout:
        return self.__layout

# -*- coding: utf-8 -*-
from typing import List, Tuple

from poga import *  # type: ignore

from pydui.common.base import PyDuiLayoutConstraint, PyDuiRect
from pydui.common.import_gtk import *
from pydui.core.widget import PyDuiWidget
from pydui.utils.poga_utils import *


class PyDuiPGView(PyDuiWidget, PogaView):
    """PyDuiPGView"""

    # PyDuiWidget interface
    @staticmethod
    def build_name() -> str:
        return "Control"

    # PyDuiWidget interface
    def __init__(self):
        super().__init__()
        self.__layout = PogaLayout(self)

    def parse_attrib(self, k: str, v: str):
        super().parse_attrib(k, v)
        # not a pglayout item
        if k in ["width", "height", "margin", "align_self"]:
            apply_poga_attributes(self.__layout, k, v)

    def draw(self, ctx: cairo.Context, dirty_rect: PyDuiRect, clip_rect: PyDuiRect):
        super().draw(ctx, dirty_rect, clip_rect)

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

    def set_frame_position_and_size(self, x: float, y: float, width: float, height: float):
        # print(self, "set_frame_position_and_size", "x", x, "y", y, "w", width, "h", height)
        layout_x, layout_y = x, y

        constraint = PyDuiLayoutConstraint()
        if YGFloatIsUndefined(width):
            width = 0
        else:
            constraint.width = width
        if YGFloatIsUndefined(height):
            height = 0
        else:
            constraint.height = height
        self.layout(layout_x, layout_y, width, height, constraint=constraint)

    def bounds_size(self) -> Tuple[float, float]:
        return (self.width, self.height)

    def subviews_count(self) -> int:
        return 0

    def subviews(self) -> List[PogaView]:
        # PGView is leaf, without any subview
        return []

    def is_container(self) -> bool:
        return False

    def poga_layout(self) -> PogaLayout:
        return self.__layout

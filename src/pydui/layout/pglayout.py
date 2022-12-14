# -*- coding: utf-8 -*-
from typing import List, Tuple

from poga import *  # type: ignore

from pydui.common.base import PyDuiLayoutConstraint, PyDuiRect
from pydui.common.import_gtk import *
from pydui.core.layout import PyDuiLayout
from pydui.core.screen import PyDuiScreen
from pydui.utils.poga_utils import *


class PyDuiLayoutWithPogaSupport(PyDuiLayout, PogaView):
    """PyDuiLayoutWithPogaSupport

    PyDui-GTK internal layout engine, with poga layout support.
    """

    def __init__(self):
        super().__init__()
        self.__layout = PogaLayout(self)

    def parse_attrib(self, k: str, v: str):
        super().parse_attrib(k, v)
        # not a pglayout item
        if k in ["width", "height", "margin", "align_self"]:
            apply_poga_attributes(self.__layout, k, v)

    # PogaView interface
    def size_that_fits(self, width: float, height: float) -> Tuple[float, float]:
        # only leaf node will call this function
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
        if self.parent is not None:
            layout_x += self.parent.x
            layout_y += self.parent.y

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
        return len(self.subviews())

    def subviews(self) -> List[PogaView]:
        return []

    def is_container(self) -> bool:
        return False

    def poga_layout(self) -> PogaLayout:
        return self.__layout


class PyDuiPGLayout(PyDuiLayout, PogaView):
    """PyDuiPGLayout

    YogaLayout on PyDui-GTK

    """

    global __global_init
    __global_init = False

    # PyDuiWidget interface
    @staticmethod
    def build_name() -> str:
        """PyDuiPGLayout build name: PGLayout"""
        return "PGLayout"

    def __init__(self):
        super().__init__()
        self.__global_init_poga_layout__()
        self.__layout: PogaLayout = PogaLayout(self)

    def __global_init_poga_layout__(self):
        global __global_init
        if __global_init:
            return
        __global_init = True
        scale = PyDuiScreen.get_system_dpi_scale()
        PogaLayout.config_set_point_scale_factor(scale)

    def parse_attrib(self, k: str, v: str):
        if not apply_poga_attributes(self.__layout, k, v):
            super().parse_attrib(k, v)

    def estimate_size(
        self, parent_width: float, parent_height: float, constraint: PyDuiLayoutConstraint
    ) -> Tuple[float, float]:
        return self.__layout.calculate_layout_with_size((parent_width, parent_height))

    def layout(self, x: float, y: float, width: float, height: float, constraint: PyDuiLayoutConstraint):
        super().layout(x, y, width, height, constraint)
        self.__layout.apply_layout()

    def draw(self, ctx: cairo.Context, dirty_rect: PyDuiRect, clip_rect: PyDuiRect):
        super().draw(ctx, dirty_rect, clip_rect)

    # PogaView interface
    def size_that_fits(self, width: float, height: float) -> Tuple[float, float]:
        # only leaf node will call this function
        constraint = PyDuiLayoutConstraint()
        if not YGFloatIsUndefined(width):
            constraint.width = width
        if not YGFloatIsUndefined(height):
            constraint.height = height
        return self.estimate_size(width, height, constraint=constraint)

    def frame_origin(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def set_frame_position_and_size(self, x: float, y: float, width: float, height: float):
        # print(self, "set_frame_origin", "x", x, "y", y)
        layout_x, layout_y = x, y
        super().layout(layout_x, layout_y, width, height, constraint=PyDuiLayoutConstraint())

    def bounds_size(self) -> Tuple[float, float]:
        return (self.width, self.height)

    def subviews_count(self) -> int:
        return len(self.subviews())

    def subviews(self) -> List[PogaView]:
        # TODO: performance issue
        subviews = list[PogaView]()
        for i in range(self.child_count):
            child = self.get_child_at(i)
            if isinstance(child, PogaView):
                subviews.append(child)
        return subviews

    def is_container(self) -> bool:
        return True

    def poga_layout(self) -> PogaLayout:
        return self.__layout

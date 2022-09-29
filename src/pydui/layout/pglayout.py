# -*- coding: utf-8 -*-
from typing import Iterable, Tuple

from poga import *

from pydui import utils
from pydui.core.base import PyDuiLayoutConstraint
from pydui.core.import_gtk import *
from pydui.core.layout import PyDuiLayout
from pydui.core.widget import PyDuiWidget
from pydui.utils.poga_utils import *


class PyDuiPGLayout(PyDuiLayout, PogaView):
    """PyDuiPGLayout

    YogaLayout on PyDui-GTK

    """

    __layout: PogaLayout = None

    # PyDuiWidget interface
    @staticmethod
    def build_name() -> str:
        """PyDuiPGLayout build name: PGLayout"""
        return "PGLayout"

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)
        self.__layout = PogaLayout(self)

    def parse_attrib(self, k: str, v: str):
        if not apply_poga_attributes(self.__layout, k.lower(), v):
            super().parse_attrib(k, v)

    # def add_child(self, child: PyDuiWidget):
    #     super().add_child(child)

    # def remove_child(self, widget_id: str):
    #     super().remove_child(widget_id)

    def estimate_size(
        self, parent_width: float, parent_height: float, constraint: PyDuiLayoutConstraint
    ) -> tuple[float, float]:
        return self.__layout.calculate_layout_with_size((parent_width, parent_height))

    def layout(self, x: float, y: float, width: float, height: float, constraint: PyDuiLayoutConstraint):
        super().layout(x, y, width, height, constraint)
        self.__layout.apply_layout()

    def draw(self, ctx: cairo.Context, x: float, y: float, width: float, height: float):
        super().draw(ctx, x, y, width, height)

        for i in range(self.child_count):
            child = self.get_child_at(i)
            child.draw(ctx, child.x, child.y, child.width, child.height)

    # PogaView interface
    def size_that_fits(self, width: float, height: float) -> Tuple[float, float]:
        # only leaf node will call this function
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
        return len(self.subviews())

    def subviews(self) -> Iterable[PogaView]:
        # TODO: performance issue
        subviews = list[PogaView]()
        for i in range(self.child_count):
            child = self.get_child_at(i)
            if isinstance(child, PogaView):
                subviews.append(child)
        return subviews

    def poga_layout(self) -> PogaLayout:
        return self.__layout

from faulthandler import is_enabled
from math import isnan
from typing import Iterable, Tuple

from poga import *

from pydui import utils
from pydui.core.base import PyDuiLayoutConstraint
from pydui.core.import_gtk import *
from pydui.core.layout import PyDuiLayout
from pydui.core.widget import PyDuiWidget


def Str2YGPostionType(text: str) -> YGPositionType:
    text = text.lower()
    pos_types = {
        "relative": YGPositionType.Relative,
        "absolute": YGPositionType.Absolute,
    }
    if text in pos_types:
        return pos_types[text]
    # default is relative
    return YGPositionType.Relative


def Str2YGAlign(text: str) -> YGAlign:
    text = text.lower()
    align_types = {
        "felx_start": YGAlign.FlexStart,
        "flex_end": YGAlign.FlexEnd,
        "stretch": YGAlign.Stretch,
        "center": YGAlign.Center,
        "space_between": YGAlign.SpaceBetween,
        "space_around": YGAlign.SpaceAround,
        "baseline": YGAlign.Baseline,
        "auto": YGAlign.Auto,
    }
    if text in align_types:
        return align_types[text]
    return YGAlign.FlexStart


def Str2YGWrap(text: str) -> YGWrap:
    text = text.lower()
    wrap_types = {
        "nowrap": YGWrap.NoWrap,
        "wrap": YGWrap.Wrap,
        "wrap_reverse": YGWrap.WrapReverse,
    }
    if text in wrap_types:
        return wrap_types[text]
    return YGWrap.NoWrap


def Str2Justify(text: str) -> YGJustify:
    text = text.lower()
    justify_types = {
        "flex_start": YGJustify.FlexStart,
        "flex_end": YGJustify.FlexEnd,
        "center": YGJustify.Center,
        "space_between": YGJustify.SpaceBetween,
        "space_around": YGJustify.SpaceAround,
        "space_evenly": YGJustify.SpaceEvenly,
    }
    if text in justify_types:
        return justify_types[text]
    return YGJustify.FlexStart


def Str2YGDirection(text: str) -> YGDirection:
    text = text.lower()
    direction_types = {
        "ltr": YGDirection.LTR,
        "rtl": YGDirection.RTL,
    }
    if text in direction_types:
        return direction_types[text]
    return YGDirection.LTR


def Str2YGFlexDirection(text: str) -> YGFlexDirection:
    text = text.lower()
    flex_direction_types = {
        "row": YGFlexDirection.Row,
        "column": YGFlexDirection.Column,
        "row_reverse": YGFlexDirection.RowReverse,
        "column_reverse": YGFlexDirection.ColumnReverse,
    }
    if text in flex_direction_types:
        return flex_direction_types[text]
    return YGFlexDirection.Row


class PyDuiPGLayout(PyDuiLayout, PogaView):
    """PyDuiPGView

    YogaLayout on pydui

    """

    __layout: PogaLayout = None

    # PyDuiWidget interface
    @staticmethod
    def build_name() -> str:
        return "PGLayout"

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)
        self.__layout = PogaLayout(self)
        self.__layout.flex_direction = YGFlexDirection.Row

    def parse_attrib(self, k: str, v: str):
        lower_k = k.lower()
        if lower_k == "poga_layout":
            self.__layout.is_enabled = v.lower() == "true"
        elif lower_k == "position_type":
            self.__layout.position = Str2YGPostionType(v)
        elif lower_k == "align_content":
            self.__layout.align_content = Str2YGAlign(v)
        elif lower_k == "align_items":
            self.__layout.align_items = Str2YGAlign(v)
        elif lower_k == "align_self":
            self.__layout.align_self = Str2YGAlign(v)
        elif lower_k == "aspect_ratio":
            self.__layout.aspect_ratio = float(v)
        elif lower_k == "flex_wrap":
            self.__layout.flex_wrap = Str2YGWrap(v)
        elif lower_k == "flex_grow":
            self.__layout.flex_grow = float(v)
        elif lower_k == "flex_shrink":
            self.__layout.flex_shrink = float(v)
        elif lower_k == "flex_basis":
            # TODO:
            pass
        elif lower_k == "justify_content":
            self.__layout.justify_content = Str2Justify(v)
        elif lower_k == "layout_direction":
            self.__layout.direction = Str2YGDirection(v)
        elif lower_k == "margin":
            # TODO:
            pass
        elif lower_k == "padding":
            # TODO:
            pass
        elif lower_k == "border":
            # TODO:
            pass
        elif lower_k == "min_width":
            pass
        elif lower_k == "min_height":
            pass
        elif lower_k == "max_width":
            pass
        elif lower_k == "max_height":
            pass
        elif lower_k == "flex_direction":
            self.__layout.flex_direction = Str2YGFlexDirection(v)
        elif lower_k == "width":
            if v.lower() == "auto":
                self.__layout.width = YGValue(0.0, YGUnit.Auto)
            else:
                self.__layout.width = YGValue(float(v), YGUnit.Point)
        elif lower_k == "width_percent":
            self.__layout.width = YGValue(float(v), YGUnit.Percent)
        elif lower_k == "height":
            if v.lower() == "auto":
                self.__layout.height = YGValue(0.0, YGUnit.Auto)
            else:
                self.__layout.height = YGValue(float(v), YGUnit.Point)
        elif lower_k == "height_percent":
            self.__layout.height = YGValue(float(v), YGUnit.Percent)
        else:
            super().parse_attrib(k, v)

    def add_child(self, child: PyDuiWidget):
        super().add_child(child)

    def remove_child(self, widget_id: str):
        super().remove_child(widget_id)

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
    def size_that_fits(self) -> Tuple[float, float]:
        print("size_that_fits")
        # only leaf node will call this function
        return (0, 0)

    def frame_origin(self) -> Tuple[float, float]:
        print("frame_origin", self.x, self.y)
        return (self.x, self.y)

    def set_frame_origin(self, x: float, y: float):
        print("set_origin: x,", x, "y,", y)
        super().layout(x, y, self.width, self.height, constraint=PyDuiLayoutConstraint())

    def set_frame_size(self, width: float, height: float):
        print("set_frame_size", width, height)
        super().layout(self.x, self.y, width, height, constraint=PyDuiLayoutConstraint())

    def bounds_size(self) -> Tuple[float, float]:
        print("bounds_size", (self.width, self.height))
        return (self.width, self.height)

    def subviews_count(self) -> int:
        return self.child_count

    def subviews(self) -> Iterable[PogaView]:
        subviews = list[PogaView]()
        for i in range(self.child_count):
            child = self.get_child_at(i)
            subviews.append(child)
        return subviews

    def poga_layout(self) -> PogaLayout:
        return self.__layout

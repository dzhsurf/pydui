# -*- coding: utf-8 -*-
import logging
from typing import Optional, Tuple

from poga import *  # type: ignore

from pydui import utils
from pydui.common.base import PyDuiLayoutConstraint, PyDuiRect
from pydui.common.import_gtk import *
from pydui.core.event import ScrollDirection, ScrollEvent
from pydui.core.layout import PyDuiLayout
from pydui.core.widget import PyDuiWidget
from pydui.layout.pglayout import PyDuiLayoutWithPogaSupport
from pydui.utils.poga_utils import *
from pydui.widgets.scrollbar import PyDuiScrollbar, PyDuiScrollbarType


class PyDuiFitLayout(PyDuiLayoutWithPogaSupport):
    """PyDuiFitLayout"""

    @staticmethod
    def build_name() -> str:
        return "FitLayout"

    def __init__(self):
        super().__init__()

    def draw(self, ctx: cairo.Context, dirty_rect: PyDuiRect, clip_rect: PyDuiRect):
        super().draw(ctx, dirty_rect, clip_rect)

    def estimate_size(
        self, parent_width: float, parent_height: float, constraint: PyDuiLayoutConstraint
    ) -> Tuple[float, float]:
        result = (0, 0)
        for i in range(self.child_count):
            child = self.get_child_at(i)
            if child is None:
                continue
            size = child.estimate_size(parent_width, parent_height, constraint=PyDuiLayoutConstraint())
            if size[0] == 0:
                size = (parent_width, size[1])
            if size[1] == 0:
                size = (size[0], parent_height)
            result = (max(result[0], size[0]), max(result[1], size[1]))
            return result
        return (parent_width, parent_height)

    def layout(self, x: float, y: float, width: float, height: float, constraint: PyDuiLayoutConstraint):
        super(PyDuiLayout, self).layout(x, y, width, height, constraint)
        for i in range(self.child_count):
            child = self.get_child_at(i)
            if child is None:
                continue
            child.layout(0, 0, width, height, constraint)


class PyDuiScrolledLayout(PyDuiLayoutWithPogaSupport):
    """PyDuiScrolledLayout"""

    @staticmethod
    def build_name() -> str:
        return "ScrolledLayout"

    def __init__(self):
        super().__init__()

        self.__enable_vscroll: bool = False
        self.__enable_hscroll: bool = False
        self.__vscrollbar: Optional[PyDuiScrollbar] = None
        self.__hscrollbar: Optional[PyDuiScrollbar] = None
        self.__mouse_enter: bool = False

        self.enable_mouse_wheel_event = True
        self.__body: PyDuiFitLayout = PyDuiFitLayout()
        super().add_child(self.__body)

    def parse_attrib(self, k: str, v: str):
        if k == "vscroll":
            self.enable_vscroll(utils.Str2Bool(v))
        elif k == "hscroll":
            self.enable_hscroll(utils.Str2Bool(v))
        return super().parse_attrib(k, v)

    def estimate_size(
        self, parent_width: float, parent_height: float, constraint: PyDuiLayoutConstraint
    ) -> Tuple[float, float]:
        return super().estimate_size(parent_width, parent_height, constraint)

    def add_child(self, child: PyDuiWidget):
        if self.__body.child_count >= 1:
            raise ValueError("ScrolledLayout only support one child.")
        return self.__body.add_child(child)

    def add_child_at(self, child: PyDuiWidget, index: int):
        logging.warn("ScrolledLayout not support add_chat_at, index will be ignored.")
        return self.add_child(child)

    def remove_child(self, child: PyDuiWidget):
        self.__body.remove_child(child)

    def remove_child_by_id(self, widget_id: str):
        self.__body.remove_child_by_id(widget_id)

    def remove_child_at(self, index: int):
        self.__body.remove_child_at(index)

    def draw(self, ctx: cairo.Context, dirty_rect: PyDuiRect, clip_rect: PyDuiRect):
        super().draw(ctx, dirty_rect, clip_rect)

    def layout(self, x: float, y: float, width: float, height: float, constraint: PyDuiLayoutConstraint):
        super(PyDuiLayout, self).layout(x, y, width, height, constraint)

        body_size = self.__body.estimate_size(width, height, constraint=PyDuiLayoutConstraint())
        self.__body.layout(
            self.__body.fixed_x, self.__body.fixed_y, body_size[0], body_size[1], constraint=PyDuiLayoutConstraint()
        )
        self.__update_scrollbar__()
        # layout scrollbar
        self.__layout_scrollbar__()

    def enable_vscroll(self, enabled: bool):
        self.__enable_vscroll = enabled

    def enable_hscroll(self, enabled: bool):
        self.__enable_hscroll = enabled

    def scroll_to(self, dx: float, dy: float):
        if self.__vscrollbar is not None and dy != 0:
            self.__vscrollbar.__scroll_to__(0, round(dy * 15))

    # event
    def on_mouse_enter(self) -> None:
        return super().on_mouse_enter()

    def on_mouse_leave(self, next_widget: Optional[PyDuiWidget]) -> None:
        return super().on_mouse_leave(next_widget)

    def on_scroll_event(self, event: ScrollEvent) -> bool:
        if event.direction == ScrollDirection.UP:
            self.scroll_to(0, -event.delta_y)
        elif event.direction == ScrollDirection.DOWN:
            self.scroll_to(0, event.delta_y)
        return False

    # private
    def __update_scrollbar__(self):
        min_scroller_size = 16

        has_hscrollbar = self.__body.width > self.width
        if has_hscrollbar and self.__enable_hscroll and self.width > 0:
            # create scrollbar
            if self.__hscrollbar is None:
                self.__hscrollbar = PyDuiScrollbar()
                self.__hscrollbar.set_scrollbar_type(PyDuiScrollbarType.HScrollbar)
                self.__hscrollbar.bind_event("vscroll-changed", self.__on_vscroll_changed__)
                super().add_child(self.__hscrollbar)
            # update scrollbar position
            scroller_width = max(min_scroller_size, round(self.width / self.__body.width * self.width))
            self.__hscrollbar.update_scroller(scroller_width)

        has_vscrollbar = self.__body.height > self.height
        if has_vscrollbar and self.__enable_vscroll and self.height > 0:
            # create scrollbar
            if self.__vscrollbar is None:
                self.__vscrollbar = PyDuiScrollbar()
                self.__vscrollbar.set_scrollbar_type(PyDuiScrollbarType.VScrollbar)
                self.__vscrollbar.bind_event("vscroll-changed", self.__on_vscroll_changed__)
                super().add_child(self.__vscrollbar)
            # update scrollbar position
            scroller_height = max(min_scroller_size, round(self.height / self.__body.height * self.height))
            self.__vscrollbar.update_scroller(scroller_height)
        else:
            if self.__vscrollbar is not None:
                super().remove_child(self.__vscrollbar)
                self.__vscrollbar = None

    def __layout_scrollbar__(self):
        if self.__hscrollbar is not None:
            self.__hscrollbar.fixed_x = 0
            self.__hscrollbar.fixed_y = self.height - self.__hscrollbar.fixed_height
            self.__hscrollbar.fixed_width = self.width
            if self.__vscrollbar is not None:
                self.__hscrollbar.fixed_width = self.width - self.__hscrollbar.fixed_height
            self.__hscrollbar.layout(
                self.__hscrollbar.fixed_x,
                self.__hscrollbar.fixed_y,
                self.__hscrollbar.fixed_width,
                self.__hscrollbar.fixed_height,
                constraint=PyDuiLayoutConstraint(),
            )

        if self.__vscrollbar is not None:
            self.__vscrollbar.fixed_x = self.width - self.__vscrollbar.fixed_width
            self.__vscrollbar.fixed_y = 0
            self.__vscrollbar.fixed_height = self.height
            if self.__hscrollbar is not None:
                self.__vscrollbar.fixed_height = self.height - self.__vscrollbar.fixed_width
            self.__vscrollbar.layout(
                self.__vscrollbar.fixed_x,
                self.__vscrollbar.fixed_y,
                self.__vscrollbar.fixed_width,
                self.__vscrollbar.fixed_height,
                constraint=PyDuiLayoutConstraint(),
            )

    def __on_vscroll_changed__(self, pos: float) -> bool:
        if self.__body is None:
            return False
        factor = self.__body.height / self.height
        self.__body.fixed_y = -round(pos * factor)
        return False

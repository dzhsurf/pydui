# -*- coding: utf-8 -*-
from enum import Enum
from typing import List

from pydui.common.base import PyDuiEdge, PyDuiLayoutConstraint, PyDuiRect
from pydui.common.import_gtk import *
from pydui.core.layout import PyDuiLayout
from pydui.core.widget import PyDuiWidget
from pydui.widgets.button import PyDuiButton


class PyDuiScrollbarType(Enum):
    VScrollbar = 0
    HScrollbar = 1


class PyDuiScrollbar(PyDuiLayout):
    """PyDuiScrollbar"""

    @staticmethod
    def build_name() -> str:
        return "Scrollbar"

    def __init__(self):
        super().__init__()
        self.__scroller: PyDuiButton = PyDuiButton()
        self.add_child(self.__scroller)
        self.__scroller.bind_event("lbutton-press", self.__on_lbutton_press__)
        self.__scroller.bind_event("lbutton-release", self.__on_lbutton_release__)

        self.__press_x: float = 0
        self.__press_y: float = 0
        self.__scroller_x: float = 0
        self.__scroller_y: float = 0
        self.__type: PyDuiScrollbarType = PyDuiScrollbarType.VScrollbar

    def set_scrollbar_type(self, type: PyDuiScrollbarType):
        self.__type = type
        self.__update_scrollbar_style__()

    def on_post_init(self):
        super().on_post_init()

    def parse_attrib(self, k: str, v: str):
        return super().parse_attrib(k, v)

    def update_scroller(self, size: float):
        self.__scroller.fixed_x = self.__scroller_x + 2
        self.__scroller.fixed_y = self.__scroller_y + 2
        if self.__type == PyDuiScrollbarType.VScrollbar:
            self.__scroller.fixed_height = size
        else:
            self.__scroller.fixed_width = size

    def draw(self, ctx: cairo.Context, dirty_rect: PyDuiRect, clip_rect: PyDuiRect):
        super().draw(ctx, dirty_rect, clip_rect)

    def layout(self, x: float, y: float, width: float, height: float, constraint: PyDuiLayoutConstraint):
        super(PyDuiLayout, self).layout(x, y, width, height, constraint)
        self.__scroller.layout(
            self.__scroller.fixed_x,
            self.__scroller.fixed_y,
            self.__scroller.fixed_width,
            self.__scroller.fixed_height,
            constraint=PyDuiLayoutConstraint(),
        )

    # properties
    @property
    def scroll_position(self) -> float:
        return self.__scroller_y

    # events
    def get_signals(self) -> List[str]:
        signals = super().get_signals()
        signals.extend(["vscroll-changed", "hscroll-changed"])
        return signals

    # private
    def __update_scrollbar_style__(self):
        scroller_size = 7
        scroller_corner = PyDuiEdge.from_value(3)
        edge = PyDuiEdge.from_value(2)
        if self.__type == PyDuiScrollbarType.VScrollbar:
            self.__scroller.bkimage = "res/images/vscroller.png"
            self.__scroller.bkimage_hover = "res/images/vscroller_hover.png"
            self.__scroller.bkimage_press = "res/images/vscroller_press.png"
            self.__scroller.corner = scroller_corner
            self.__scroller.fixed_width = scroller_size
            self.fixed_width = self.__scroller.fixed_width + edge.width
        else:
            self.__scroller.bkimage = "res/images/hscroller.png"
            self.__scroller.bkimage_hover = "res/images/hscroller_hover.png"
            self.__scroller.bkimage_press = "res/images/hscroller_press.png"
            self.__scroller.corner = scroller_corner
            self.__scroller.fixed_height = scroller_size
            self.fixed_height = self.__scroller.fixed_height + edge.height

    def __on_lbutton_press__(self, widget: PyDuiWidget, x: float, y: float) -> bool:
        self.__press_x = x
        self.__press_y = y
        self.get_window_client().add_event_observer("mouse-move", self.__on_mouse_move__)
        return False

    def __on_lbutton_release__(self, widget: PyDuiWidget, x: float, y: float) -> bool:
        self.__press_x = 0
        self.__press_y = 0
        self.get_window_client().remove_event_observer("mouse-move", self.__on_mouse_move__)
        return False

    def __on_mouse_move__(self, x: float, y: float):
        dx, dy = x - self.__press_x, y - self.__press_y
        self.__scroll_to__(dx, dy)
        self.__press_x = x
        self.__press_y = y

    def __scroll_to__(self, dx: float, dy: float):
        self.__scroller_y += dy
        self.__scroller_y = max(0, self.__scroller_y)
        self.__scroller_y = min(self.height - self.__scroller.fixed_height, self.__scroller_y)
        self.__scroller.fixed_y = self.__scroller_y + 2
        self.do_bind_event("vscroll-changed", self.scroll_position)
        # self.emit("vscroll-changed", self.scroll_position)
        # TODO, set needupdate, invalidrect
        self.get_window_client().notify_redraw()

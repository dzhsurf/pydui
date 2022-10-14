# -*- coding: utf-8 -*-
import logging
from typing import Tuple

from poga import *

from pydui import utils
from pydui.common.base import PyDuiLayoutConstraint
from pydui.common.import_gtk import *
from pydui.core.layout import PyDuiLayout
from pydui.core.widget import PyDuiWidget
from pydui.layout.pglayout import PyDuiLayoutWithPogaSupport
from pydui.utils.poga_utils import *
from pydui.widgets.scrollbar import PyDuiScrollbar


class PyDuiFitLayout(PyDuiLayoutWithPogaSupport):
    """PyDuiFitLayout"""

    @staticmethod
    def build_name() -> str:
        return "FitLayout"

    def __init__(self):
        super().__init__()

    def draw(self, ctx: cairo.Context, x: float, y: float, width: float, height: float):
        super().draw(ctx, x, y, width, height)

    def estimate_size(
        self, parent_width: float, parent_height: float, constraint: PyDuiLayoutConstraint
    ) -> Tuple[float, float]:
        result = (0, 0)
        for i in range(self.child_count):
            child = self.get_child_at(i)
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
            child.layout(0, 0, width, height, constraint)


class PyDuiScrolledLayout(PyDuiLayoutWithPogaSupport):
    """PyDuiScrolledLayout"""

    __body: PyDuiFitLayout = None
    __vscroll: bool = False
    __hscroll: bool = False
    __vscrollbar: PyDuiScrollbar = None
    __hscrollbar: PyDuiScrollbar = None

    @staticmethod
    def build_name() -> str:
        return "ScrolledLayout"

    def __init__(self):
        super().__init__()
        self.__body = PyDuiFitLayout()
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

    def draw(self, ctx: cairo.Context, x: float, y: float, width: float, height: float):
        super().draw(ctx, x, y, width, height)

    def layout(self, x: float, y: float, width: float, height: float, constraint: PyDuiLayoutConstraint):
        super(PyDuiLayout, self).layout(x, y, width, height, constraint)

        body_size = self.__body.estimate_size(width, height, constraint=PyDuiLayoutConstraint())
        self.__body.layout(
            self.__body.fixed_x, self.__body.fixed_y, body_size[0], body_size[1], constraint=PyDuiLayoutConstraint()
        )
        print('estimate size', body_size)
        self.__init_scrollbar_if_needed__()
        self.__update_scrollbar__()
        if self.__vscrollbar is not None:
            self.__vscrollbar.fixed_x = width - self.__vscrollbar.fixed_width
            self.__vscrollbar.fixed_y = 0
            self.__vscrollbar.fixed_height = height
            self.__vscrollbar.layout(
                self.__vscrollbar.fixed_x,
                self.__vscrollbar.fixed_y,
                self.__vscrollbar.fixed_width,
                self.__vscrollbar.fixed_height,
                constraint=PyDuiLayoutConstraint(),
            )

    def enable_vscroll(self, enabled: bool):
        self.__vscroll = enabled

    def enable_hscroll(self, enabled: bool):
        self.__hscroll = enabled

    # private
    def __init_scrollbar_if_needed__(self):
        has_hscrollbar = self.__body.width > self.width
        if has_hscrollbar:
            pass

        has_vscrollbar = self.__body.height > self.height
        if has_vscrollbar:
            if self.__vscrollbar is None:
                self.__vscrollbar = PyDuiScrollbar()
                self.__vscrollbar.bind_event("vscroll-changed", self.__on_vscroll_changed__)
                super().add_child(self.__vscrollbar)

    def __update_scrollbar__(self):
        has_vscrollbar = self.__body.height > self.height
        if has_vscrollbar:
            if self.__vscrollbar is None:
                return
            scroller_height = max(32, round(self.height / self.__body.height * self.height))
            self.__vscrollbar.update_scroller(0, scroller_height)
            print('scrollbar height', self.height, 'body height', self.__body.height, ' scroller', scroller_height)
        else:
            if self.__vscrollbar is not None:
                super().remove_child(self.__vscrollbar)
                self.__vscrollbar = None

    def __on_vscroll_changed__(self, pos: float):
        if self.__body is None:
            return
        factor = self.__body.height / self.height
        self.__body.fixed_y = -(pos * factor)

# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from typing import Any

from pydui import utils
from pydui.core.base import *
from pydui.core.import_gtk import *
from pydui.core.render import PyDuiRender
from pydui.core.render_base import PyDuiRenderManagerBase


@dataclass(frozen=True)
class PyDuiConstraint:

    """Constraint dataclass"""

    min_width: float = 0
    max_width: float = sys.maxsize
    min_height: float = 0
    max_height: float = sys.maxsize


class PyDuiWidget(object):

    """Widget base class"""

    __render_manager: PyDuiRenderManagerBase = None

    __id: str = ""
    __parent: PyDuiWidget
    __x: float = 0
    __y: float = 0
    __width: float = 0
    __height: float = 0
    __fixed_x: float = 0
    __fixed_y: float = 0
    __fixed_width: float = 0
    __fixed_height: float = 0
    # attrib
    __bkcolor: Gdk.RGBA = None
    __margin: tuple[float, float, float, float] = (0, 0, 0, 0)
    __corner: tuple[float, float, float, float] = (0, 0, 0, 0)
    __bkimage: str = ""
    # event
    __signals: dict[str, list[callable]] = None
    __enable_mouse_event: bool = False

    @staticmethod
    def find_widget_default_filter(widget: PyDuiWidget) -> bool:
        return widget is not None

    @staticmethod
    def find_widget_mouse_event_filter(widget: PyDuiWidget) -> bool:
        if widget is None:
            return False
        return widget.enable_mouse_event

    def __init__(self, parent: PyDuiWidget):
        super().__init__()
        self.__parent = parent
        self.__signals = dict[str, list[callable]]()

    def set_render_manager(self, render_manager: PyDuiRenderManagerBase):
        """Set the render mananger

        Do not call this function yourself if you do not know what it is for!
        """
        self.__render_manager = render_manager

    def get_render_manager(self):
        """Get the widget render manager

        If widget is a child and not contain render manager, it will find the parent until reach to top.
        It's not a good design as it will cause problems by incorrect maintain the widget render manager.
        It will reimplment later.
        """
        render_manager = self.__render_manager
        widget = self
        while render_manager is None and widget is not None:
            widget = widget.parent
            render_manager = widget.__render_manager

        return render_manager

    def get_id(self) -> str:
        """Return widget id

        Returns:
            str: widget id
        """
        return self.__id

    def draw(
        self,
        ctx: cairo.Context,
        x: float,
        y: float,
        width: float,
        height: float,
    ):
        self.draw_bkcolor(ctx, x, y, width, height)
        self.draw_bkimage(ctx, x, y, width, height)

    def draw_bkcolor(
        self,
        ctx: cairo.Context,
        x: float,
        y: float,
        width: float,
        height: float,
    ):
        if self.bkcolor is None:
            return

        PyDuiRender.Rectangle(ctx, self.bkcolor, x, y, width, height)

    def draw_bkimage(
        self,
        ctx: cairo.Context,
        x: float,
        y: float,
        width: float,
        height: float,
    ):
        if self.bkimage == "":
            return

        PyDuiRender.DrawImage(
            ctx,
            loader=self.get_render_manager().get_resource_loader(),
            path=self.bkimage,
            xy=(x, y),
            wh=(width, height),
            corner=self.corner,
        )

    def layout(self, x: float, y: float, width: float, height: float):
        self.__x, self.__y = x, y
        self.__width, self.__height = width, height
        logging.debug(f"{self} => ({x}, {y}, {width}, {height})")

    def estimate_size(self, parent_width: float, parent_height: float) -> tuple[float, float]:
        return (self.__fixed_width, self.__fixed_height)

    def parse_attributes(self, attrib: dict[str, str]):
        """Parse all attributes

        Args:
            attrib (dict[str, str]): attributes dict key=value ...
        """
        for k, v in attrib.items():
            self.parse_attrib(k, v)
        pass

    def parse_attrib(self, k: str, v: str):
        """Parse single attribute

        Args:
            attrib (dict[str, str]): attributes dict key=value ...
        """
        logging.debug(f"{self} parse {k} = {v}")
        if k == "id":
            self.__id = v
        elif k == "width":
            self.fixed_width = float(v)
        elif k == "height":
            self.fixed_height = float(v)
        elif k == "size":
            size_arr = v.split(",")
            self.fixed_size(tuple(float(n) for n in size_arr))
        elif k == "x":
            self.fixed_x = float(v)
        elif k == "y":
            self.fixed_y = float(v)
        elif k == "xy":
            self.fixed_xy = tuple(float(a) for a in v.split(","))
        elif k == "margin":
            self.margin = utils.Str2Rect(v)
        elif k == "bkcolor":
            self.bkcolor = utils.Str2Color(v)
        elif k == "bkimage":
            self.bkimage = v
        elif k == "corner":
            self.corner = utils.Str2Rect(v)

    # event
    @property
    def enable_mouse_event(self) -> bool:
        return self.__enable_mouse_event

    @enable_mouse_event.setter
    def enable_mouse_event(self, enable: bool):
        self.__enable_mouse_event = enable

    def on_mouse_enter(self):
        pass

    def on_mouse_leave(self, next_widget: PyDuiWidget):
        pass

    def on_mouse_move(self, x: float, y: float):
        pass

    def on_lbutton_press(self, x: float, y: float):
        return False

    def on_lbutton_release(self, x: float, y: float):
        pass

    def on_rbutton_press(self, x: float, y: float):
        return False

    def on_rbutton_release(self, x: float, y: float):
        pass

    def on_lbutton_click(self, x: float, y: float):
        self.emit("lclick", self, x, y)

    def on_rbutton_click(self, x: float, y: float):
        self.emit("rclick", self, x, y)

    def on_l2button_click(self, x: float, y: float):
        self.emit("l2click", self, x, y)

    def on_r2button_click(self, x: float, y: float):
        self.emit("r2click", self, x, y)

    def on_l3button_click(self, x: float, y: float):
        self.emit("l3click", self, x, y)

    def on_r3button_click(self, x: float, y: float):
        self.emit("r3click", self, x, y)

    # method
    def connect(self, signal_name: str, callback: callable):
        if signal_name in self.__signals:
            self.__signals[signal_name].append(callback)
        else:
            self.__signals[signal_name] = list([callback])

    def disconnect(self, signal_name: str, callback: callable):
        def remove_fn(item: callable):
            if item == callback:
                return True
            return False

        if signal_name in self.__signals:
            self.__signals[signal_name] = list(filter(remove_fn, self.__signals[signal_name]))

    def disconnect_signal(self, signal_name: str):
        if signal_name in self.__signals:
            self.__signals.pop(signal_name)

    def emit(self, signal_name: str, *args: Any, **kwargs: Any):
        if signal_name in self.__signals:
            fn_list = self.__signals[signal_name].copy()

            def run_all_fn(*args: Any, **kwargs: Any):
                for fn in fn_list:
                    if fn(*args, **kwargs):
                        break

            self.get_render_manager().post_task(run_all_fn, *args, **kwargs)

    def set_focus(self):
        pass

    def contain_pos(self, x: float, y: float) -> bool:
        if x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height:
            return True
        return False

    # properties
    # position & size

    @property
    def parent(self) -> PyDuiWidget:
        return self.__parent

    @property
    def size(self) -> tuple[float, float]:
        return (self.width, self.height)

    @property
    def width(self) -> float:
        return self.__width

    @property
    def height(self) -> float:
        return self.__height

    @property
    def layout_rect(self) -> tuple[float, float, float, float]:
        return (
            self.x,
            self.y,
            self.x + self.width + utils.RectW(self.margin),
            self.y + self.height + utils.RectH(self.margin),
        )

    @property
    def fixed_size(self) -> tuple[float, float]:
        return (self.fixed_width, self.fixed_height)

    @fixed_size.setter
    def fixed_size(self, size: tuple[float, float]):
        self.fixed_width = size[0]
        self.fixed_height = size[1]

    @property
    def fixed_width(self) -> float:
        return self.__fixed_width

    @fixed_width.setter
    def fixed_width(self, w: float):
        self.__fixed_width = w

    @property
    def fixed_height(self) -> float:
        return self.__fixed_height

    @fixed_height.setter
    def fixed_height(self, h: float):
        self.__fixed_height = h

    @property
    def xy(self) -> tuple[float, float]:
        return (self.x, self.y)

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def is_float(self) -> bool:
        pass

    @property
    def fixed_x(self) -> float:
        return self.__fixed_x

    @fixed_x.setter
    def fixed_x(self, x: float):
        self.__fixed_x = x

    @property
    def fixed_y(self) -> float:
        return self.__fixed_y

    @fixed_y.setter
    def fixed_y(self, y: float):
        self.__fixed_y = y

    @property
    def fixed_xy(self) -> tuple[float, float]:
        return (self.__fixed_x, self.__fixed_y)

    @fixed_xy.setter
    def fixed_xy(self, xy: tuple[float, float]):
        self.fixed_x = xy[0]
        self.fixed_y = xy[1]

    @is_float.setter
    def is_float(self, is_float: bool):
        pass

    @property
    def margin(self) -> tuple[float, float, float, float]:
        """Return widget margin

        The value in tuple means [left, top, right, bottom]

        Returns:
            tuple[float, float, float, float]: return margin.
        """
        return self.__margin

    @margin.setter
    def margin(self, margin: tuple[float, float, float, float]):
        """Set the widget margin

        Args:
            margin (tuple[float, float, float, float]): widget margin

        """
        self.__margin = margin

    # constraint
    @property
    def constraint(self) -> PyDuiConstraint:
        pass

    @constraint.setter
    def constraint(self, v: PyDuiConstraint):
        pass

    # state
    @property
    def visible(self) -> bool:
        pass

    @visible.setter
    def visible(self, visible: bool):
        pass

    @property
    def enabled(self) -> bool:
        pass

    @enabled.setter
    def enabled(self, enabled: bool):
        pass

    @property
    def is_focused(self) -> bool:
        pass

    # appearance
    @property
    def bkcolor(self) -> Gdk.RGBA:
        return self.__bkcolor

    @bkcolor.setter
    def bkcolor(self, color: Gdk.RGBA):
        self.__bkcolor = color

    @property
    def bkimage(self) -> str:
        return self.__bkimage

    @bkimage.setter
    def bkimage(self, image: str):
        self.__bkimage = image

    @property
    def corner(self) -> tuple[float, float, float, float]:
        return self.__corner

    @corner.setter
    def corner(self, corner: tuple[float, float, float, float]):
        self.__corner = corner

    # private function

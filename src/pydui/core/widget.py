from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Optional

import cairo
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk

from pydui.core import utils
from pydui.core.base import *
from pydui.core.render import PyDuiRender


@dataclass(frozen=True)
class PyDuiConstraint:

    """Constraint dataclass"""

    min_width: float = 0
    max_width: float = sys.maxsize
    min_height: float = 0
    max_height: float = sys.maxsize


class PyDuiWidget(object):

    """Widget base class"""

    __render_manager: PyDuiRenderManager = None

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
    __layout_class: PyDuiLayoutEnum
    # attrib
    __bkcolor: Gdk.RGBA = None
    __margin: tuple[float, float, float, float] = (0, 0, 0, 0)

    def __init__(self, parent: PyDuiWidget, layout_class: PyDuiLayoutEnum = PyDuiLayoutEnum.NotLayout):
        self.__parent = parent
        self.__layout_class = layout_class

    def set_render_manager(self, render_manager: PyDuiRenderManager):
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
        canvas_width: float,
        canvas_height: float,
    ):
        ctx.save()
        ctx.scale(canvas_width, canvas_height)
        self.__draw_bkcolor__(ctx, x, y, width, height, canvas_width, canvas_height)
        ctx.restore()

    def layout(self, x: float, y: float, width: float, height: float):
        self.__x, self.__y = x, y
        self.__width, self.__height = width, height
        print(f"{self} => ({x}, {y}, {width}, {height})")

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
        print(f"{self} parser {k} = {v}")
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

    # method
    def connect(self, signal_name: str, callback: callable):
        pass

    def set_focus(self):
        pass

    # properties
    # position & size
    @property
    def layout_class(self) -> PyDuiLayoutEnum:
        return self.__layout_class

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
        if self.parent is None or self.parent.__layout_class is None:
            return
        if self.parent.layout_class != PyDuiLayoutEnum.HLayout:
            return
        self.__fixed_width = w

    @property
    def fixed_height(self) -> float:
        return self.__fixed_height

    @fixed_height.setter
    def fixed_height(self, h: float):
        if self.parent is None or self.parent.__layout_class is None:
            return
        if self.parent.layout_class != PyDuiLayoutEnum.VLayout:
            return
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
        pass

    @bkimage.setter
    def bkimage(self, image: str):
        pass

    # private function

    def __draw_bkcolor__(
        self,
        ctx: cairo.Context,
        x: float,
        y: float,
        width: float,
        height: float,
        canvas_width: float,
        canvas_height: float,
    ):
        if self.bkcolor is None:
            return

        PyDuiRender.Rectangle(ctx, self.bkcolor, x, y, width, height, canvas_width, canvas_height)

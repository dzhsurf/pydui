# widget.py
# all ui element is PyDuiWidget
from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Optional

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk

from pydui.core import utils
from pydui.core.base import *


@dataclass(frozen=True)
class PyDuiConstraint:

    """Constraint dataclass"""

    min_width: int = 0
    max_width: int = sys.maxsize
    min_height: int = 0
    max_height: int = sys.maxsize


class PyDuiWidget(object):

    """Widget base class"""

    __widget: Gtk.Widget
    __id: str
    __parent: PyDuiWidget
    __x: int
    __y: int
    __width: int
    __height: int
    __fixed_x: int
    __fixed_y: int
    __fixed_width: int
    __fixed_height: int
    __layout_class: PyDuiLayoutEnum

    def __init__(self, parent: PyDuiWidget, layout_class: PyDuiLayoutEnum = PyDuiLayoutEnum.NotLayout):
        self.__widget = None
        self.__widget_layout = None
        self.__id = ""
        self.__parent = parent
        self.__x, self.__y = 0, 0
        self.__width, self.__height = 0, 0
        self.__fixed_x, self.__fixed_y = 0, 0
        self.__fixed_width, self.__fixed_height = 0, 0
        self.__layout_class = layout_class

    def get_id(self) -> str:
        """Return widget id

        Returns:
            str: widget id
        """
        return self.__id

    def set_id(self, id: str):
        """Set widget id

        Args:
            id (str): widget id
        """
        self.__id = id

    def set_gtk_widget(self, gtk_widget: Gtk.Widget):
        """Set gtk widget

        Args:
            gtk_widget (Gtk.Widget): Gtk widget object
        """
        if gtk_widget is None:
            return
        self.__widget = gtk_widget
        if self.__layout_class == PyDuiLayoutEnum.NotLayout:
            self.__widget_layout = Gtk.Layout.new(None, None)
            self.__widget_layout.put(self.__widget, 0, 0)

    def get_gtk_widget(self) -> Gtk.Widget:
        """Return gtk widget object

        Returns:
            Gtk.Widget: Gtk widget object
        """
        return self.__widget

    def get_gtk_widget_layout(self) -> Gtk.Layout:
        """Return gtk widget layout object

        Returns:
            Gtk.Layout: Gtk widget layout object
        """
        return self.__widget_layout

    def layout(self, width: int, height: int):
        if self.__widget is None:
            return
        self.__width, self.__height = width, height
        # if self.__widget_layout is not None:
        #     self.__widget_layout.set_size_request(width, height)
        # else:
        #     self.__widget.set_size_request(width, height)
        print(f"{self.get_id()} layouted: {self.width} {self.height}")

    def estimate_size(self, parent_width: int, parent_height: int) -> tuple[int, int]:
        return (self.__fixed_width, self.__fixed_height)

    def parse_attrib(self, attrib: dict[str, str]):
        """Parse attrib

        Args:
            attrib (dict[str, str]): attributes dict key=value ...
        """
        for k, v in attrib.items():
            print(f"parser {k} = {v}")
            if k == "id":
                self.set_id(v)
            elif k == "bkcolor":
                self.__widget.override_background_color(Gtk.StateType.NORMAL, utils.Str2Color(v))
            elif k == "width":
                self.__apply_layout_size__(int(v), -1)
            elif k == "height":
                self.__apply_layout_size__(-1, int(v))
            elif k == "size":
                size_arr = v.split(",")
                self.__apply_layout_size__(int(size_arr[0]), int(size_arr[1]))
            elif k == "x":
                pass
            elif k == "y":
                pass
            elif k == "xy":
                pass

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
    def size(self) -> tuple[int, int]:
        return (self.width, self.height)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def fixed_size(self) -> tuple[int, int]:
        return (self.fixed_width, self.fixed_height)

    @fixed_size.setter
    def fixed_size(self, size: tuple[int, int]):
        self.fixed_width = size[0]
        self.fixed_height = size[1]

    @property
    def fixed_width(self) -> int:
        return self.__fixed_width

    @fixed_width.setter
    def fixed_width(self, w: int):
        self.__fixed_width = w

    @property
    def fixed_height(self) -> int:
        return self.__fixed_height

    @fixed_height.setter
    def fixed_height(self, h: int):
        self.__fixed_height = h

    @property
    def xy(self) -> tuple[int, int]:
        return (self.x, self.y)

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def is_float(self) -> bool:
        pass

    @property
    def fixed_x(self) -> int:
        return self.__fixed_x

    @fixed_x.setter
    def fixed_x(self, x: int):
        self.__fixed_x = x

    @property
    def fixed_y(self) -> int:
        return self.__fixed_y

    @fixed_y.setter
    def fixed_y(self, y: int):
        self.__fixed_y = y

    @property
    def fixed_xy(self) -> tuple[int, int]:
        return (self.__fixed_x, self.__fixed_y)

    @fixed_xy.setter
    def fixed_xy(self, xy: tuple[int, int]):
        self.fixed_x = xy[0]
        self.fixed_y = xy[1]

    @is_float.setter
    def is_float(self, is_float: bool):
        pass

    @property
    def padding(self) -> tuple[int, int, int, int]:
        pass

    @padding.setter
    def padding(self, padding: tuple[int, int, int, int]):
        pass

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
    def bkcolor(self) -> str:
        pass

    @bkcolor.setter
    def bkcolor(self, color: str):
        pass

    @property
    def bkimage(self) -> str:
        pass

    @bkimage.setter
    def bkimage(self, image: str):
        pass

    # private function

    def __apply_layout_size__(self, width: int, height: int):
        # self.__widget.width_request = width
        # self.__widget.height_request = height
        parent = self.parent
        if parent is None or parent.__layout_class is None:
            print(f"No parent, ignore layout. {self}")
            return
        print(f"Parent layout type: {parent.layout_class}")
        if parent.layout_class == PyDuiLayoutEnum.VLayout:
            print(f"is VLayout: {width} {height}")
            self.fixed_height = height
            # self.__widget.set_size_request(width, height)
        elif parent.layout_class == PyDuiLayoutEnum.HLayout:
            print(f"is HLayout {width} {height}")
            self.fixed_width = width
            # self.__widget.set_size_request(width, height)
        else:
            print("Unknow layout type")

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

    def __init__(self):
        self.__widget = None
        self.__id = ""

    def get_id(self) -> str:
        return self.__id

    def set_gtk_widget(self, gtk_widget: Gtk.Widget):
        self.__widget = gtk_widget

    def get_gtk_widget(self) -> Gtk.Widget:
        return self.__widget

    def parse_attrib(self, attrib: dict[str, str]):
        if "bkcolor" in attrib:
            color = utils.Str2Color(attrib["bkcolor"])
            self.__widget.override_background_color(Gtk.StateType.NORMAL, color)

    # method
    def connect(self, signal_name: str, callback: callable):
        pass

    def set_focus(self):
        pass

    # properties
    # position & size
    @property
    def parent(self) -> Optional[PyDuiWidget]:
        pass

    @property
    def size(self) -> tuple[int, int]:
        pass

    @property
    def width(self) -> int:
        pass

    @property
    def height(self) -> int:
        pass

    @property
    def request_size(self) -> tuple[int, int]:
        pass

    @property
    def request_width(self) -> int:
        pass

    @request_width.setter
    def request_width(self, w: int):
        pass

    @property
    def request_height(self) -> int:
        pass

    @request_height.setter
    def request_height(self, w: int):
        pass

    @property
    def xy(self) -> tuple[int, int]:
        pass

    @property
    def x(self) -> int:
        pass

    @property
    def y(self) -> int:
        pass

    @property
    def is_float(self) -> bool:
        pass

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

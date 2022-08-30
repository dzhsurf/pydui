# layout.py
import math
from dataclasses import dataclass, field
from enum import Enum

import cairo
import gi

from pydui.core import utils
from pydui.core.base import *
from pydui.core.widget import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk


@dataclass(frozen=True)
class PyDuiLayoutEstimateResult:
    """Estimate layout result"""

    auto_layout_count: int = 0
    auto_layout_value: int = 0
    estimate_items: list[int] = field(default_factory=list)


class PyDuiLayout(PyDuiWidget):

    """Layout base class, all layouts inherit from PyDuiLayout"""

    __children: list[PyDuiWidget]
    __children_id_dict: dict[str, PyDuiWidget]
    __padding: tuple[float, float, float, float] = (0, 0, 0, 0)

    def __init__(self, parent: PyDuiWidget, layout_class: PyDuiLayoutEnum, custom_gtk_widget: Gtk.Widget = None):
        super().__init__(parent, layout_class)
        self.__children = []
        self.__children_id_dict = {}

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
        super().draw(ctx, x, y, width, height, canvas_width, canvas_height)

    def layout(self, x: float, y: float, width: float, height: float):
        super().layout(x, y, width, height)

    def get_children_range_fixed_width(self, start, stop) -> float:
        w = 0
        for i in range(start, stop):
            child = self.get_child_at(i)
            margin = child.margin
            w = w + child.fixed_width + utils.RectW(margin)
        return w

    def get_children_range_fixed_height(self, start, stop) -> float:
        h = 0
        for i in range(start, stop):
            child = self.get_child_at(i)
            margin = child.margin
            h = h + child.fixed_height + utils.RectH(margin)
        return h

    def get_child(self, widget_id: str) -> Optional[PyDuiWidget]:
        """Get child widget by widget_id

        Args:
            widget_id (str): widget id

        Returns:
            PyDuiWidget: return widget object.
        """
        if widget_id in self.__children_id_dict:
            return self.__children_id_dict[widget_id]
        return None

    def get_child_at(self, index: int) -> Optional[PyDuiWidget]:
        """Get child widget at index

        if the index overbound, it will return None.

        Args:
            index (int): child index

        Returns:
            PyDuiWidget: return widget object.
        """
        if index < 0 or index >= len(self.__children):
            return None
        return self.__children[index]

    def add_child(self, child: PyDuiWidget):
        """Add child widget.

        if child has been added, ignore.

        Args:
            child (PyDuiWidget): child widget

        """
        if (child is None) or (self.get_child(child.get_id()) is not None):
            return

        self.__children.append(child)
        widget_id = child.get_id()
        if len(widget_id) > 0 and (widget_id not in self.__children_id_dict):
            self.__children_id_dict[widget_id] = child

    def add_child_at(self, child: PyDuiWidget, index: int):
        """Add child widget at index

        if the index overbound, it will add widget to last position.

        Args:
            child (PyDuiWidget): child widget
            index (int): target index

        Returns:
            PyDuiWidget: return widget object.
        """
        pass

    def remove_child(self, widget_id: str):
        """Remove child widget by widget_id

        Args:
            widget_id (str): widget id

        """
        pass

    def remove_child_at(self, index: int):
        """Remove child widget at index

        if the index overbound, do nothing.

        Args:
            index (int): widget index

        """
        pass

    @property
    def child_count(self) -> int:
        """Return child count

        Returns:
            int: return child widget count.
        """
        return len(self.__children)

    @property
    def padding(self) -> tuple[float, float, float, float]:
        """Return widget padding

        The value in tuple means [left, top, right, bottom]

        Returns:
            tuple[float, float, float, float]: return padding.
        """
        return self.__padding

    @padding.setter
    def padding(self, padding: tuple[float, float, float, float]):
        """Set the widget padding

        Args:
            padding (tuple[float, float, float, float]): widget padding

        """
        self.__padding = padding

    # private function
    def __do_layout__(self):
        pass

    # private functions
    def __process_resize_or_move__(self, gtk_widget, gtk_event):
        print(f"resize, {object}")

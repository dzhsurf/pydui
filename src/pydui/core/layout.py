# -*- coding: utf-8 -*-
import math
from dataclasses import dataclass, field
from enum import Enum

from pydui.core.base import *
from pydui.core.import_gtk import *
from pydui.core.widget import *


@dataclass(frozen=True)
class PyDuiLayoutEstimateResult:
    """Estimate layout result"""

    auto_layout_count: int = 0
    auto_layout_value: int = 0
    estimate_items: list[int] = field(default_factory=list)


class PyDuiLayout(PyDuiWidget):

    """Layout base class, all layouts inherit from PyDuiLayout"""

    __children: list[PyDuiWidget] = None
    __padding: tuple[float, float, float, float] = (0, 0, 0, 0)
    __childHVAlign: tuple[PyDuiAlign, PyDuiAlign] = (PyDuiAlign.START, PyDuiAlign.START)

    def __init__(self, parent: PyDuiWidget, custom_gtk_widget: Gtk.Widget = None):
        super().__init__(parent)
        self.__children = list()

    def parse_attrib(self, k: str, v: str):
        if k == "halign":
            self.__childHVAlign = (Text2PyDuiAlign(v), self.valign)
        elif k == "valign":
            self.__childHVAlign = (self.halign, Text2PyDuiAlign(v))
        else:
            super().parse_attrib(k, v)

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

    def get_child(self, widget_id: str) -> PyDuiWidget:
        """Get child widget by widget_id

        Args:
            widget_id (str): widget id

        Returns:
            PyDuiWidget: return widget object.
        """
        for i in range(self.child_count):
            child = self.get_child_at(i)
            if child.get_id() == widget_id:
                return child
            if issubclass(type(child), PyDuiLayout):
                target = child.get_child(widget_id)
                if target is not None:
                    return target

        return None

    def get_child_by_pos(self, x: float, y: float) -> PyDuiWidget:
        """Get child by position"""
        for i in range(self.child_count):
            child = self.get_child_at(i)
            if not child.contain_pos(x, y):
                continue

            if issubclass(type(child), PyDuiLayout):
                target = child.get_child_by_pos(x, y)
                return target if target is not None else child
            else:
                return child
        return None

    def get_child_at(self, index: int) -> PyDuiWidget:
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
        if child is None:
            return
        self.__children.append(child)

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

    @property
    def halign(self) -> PyDuiAlign:
        return self.__childHVAlign[0]

    @property
    def valign(self) -> PyDuiAlign:
        return self.__childHVAlign[1]

    # private function
    def __do_layout__(self):
        pass

    # private functions
    def __process_resize_or_move__(self, gtk_widget, gtk_event):
        logging.debug(f"resize, {object}")

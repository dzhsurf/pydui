# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

from pydui import utils
from pydui.core.base import *
from pydui.core.import_gtk import *
from pydui.core.widget import *


class PyDuiLayout(PyDuiWidget):

    """Layout base class, all layouts inherit from PyDuiLayout"""

    __children: list[PyDuiWidget] = None
    __padding: tuple[float, float, float, float] = (0, 0, 0, 0)
    __childHVAlign: tuple[PyDuiAlign, PyDuiAlign] = (PyDuiAlign.START, PyDuiAlign.START)
    __fitrule: list[str] = None

    def __init__(self, parent: PyDuiWidget, custom_gtk_widget: Gtk.Widget = None):
        super().__init__(parent)
        self.__children = list[PyDuiWidget]()
        self.__fitrule = list[str]()

    def parse_attrib(self, k: str, v: str):
        if k == "padding":
            self.padding = utils.Str2Rect(v)
        elif k == "halign":
            self.__childHVAlign = (Text2PyDuiAlign(v), self.valign)
        elif k == "valign":
            self.__childHVAlign = (self.halign, Text2PyDuiAlign(v))
        elif k == "fitrule":
            self.__fitrule = v.split(",")

        super().parse_attrib(k, v)

    def draw(
        self,
        ctx: cairo.Context,
        x: float,
        y: float,
        width: float,
        height: float,
    ):
        super().draw(ctx, x, y, width, height)

    def layout(self, x: float, y: float, width: float, height: float, constraint: PyDuiLayoutConstraint):
        super().layout(x, y, width, height, constraint)

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

    def find_widget_by_pos(
        self, x: float, y: float, *, filter: Callable[[PyDuiWidget], bool] = PyDuiWidget.find_widget_default_filter
    ) -> PyDuiWidget:
        """Get child by position"""
        for i in range(self.child_count):
            child = self.get_child_at(i)
            if not child.contain_pos(x, y):
                continue

            if issubclass(type(child), PyDuiLayout):
                target = child.find_widget_by_pos(x, y, filter=filter)
                if target is not None and filter(target):
                    return target

            if filter(child):
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
        if self.get_render_manager() is not None:
            child.__do_post_init__(self.get_render_manager())

    def add_child_at(self, child: PyDuiWidget, index: int):
        """Add child widget at index

        if the index overbound, it will add widget to last position.

        Args:
            child (PyDuiWidget): child widget
            index (int): target index

        Returns:
            PyDuiWidget: return widget object.
        """
        if child is None:
            return
        self.__children.insert(index, child)
        if self.get_render_manager() is not None:
            child.__do_post_init__(self.get_render_manager())

    def remove_child(self, widget_id: str):
        """Remove child widget by widget_id

        Args:
            widget_id (str): widget id

        """
        child = self.get_child(widget_id)
        if child is None:
            return
        self.__children.remove(child)

    def remove_child_at(self, index: int):
        """Remove child widget at index

        if the index overbound, do nothing.

        Args:
            index (int): widget index

        """
        child = self.get_child_at(index)
        if child is None:
            return
        self.__children.pop(index)

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

    @property
    def fitrule(self) -> list[str]:
        return self.__fitrule

    # private function
    def __do_layout__(self):
        pass

    def __do_post_init__(self, render_manager: PyDuiRenderManagerBase):
        super().__do_post_init__(render_manager)
        for i in range(self.child_count):
            child = self.get_child_at(i)
            child.__do_post_init__(render_manager)

    # private functions
    def __process_resize_or_move__(self, gtk_widget, gtk_event):
        pass
        # logging.debug(f"resize, {object}")

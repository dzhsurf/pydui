# -*- coding: utf-8 -*-
from typing import Callable

from pydui import utils
from pydui.common.base import *
from pydui.common.import_gtk import *
from pydui.core.widget import *


class PyDuiLayout(PyDuiWidget):

    """Layout base class, all layouts inherit from PyDuiLayout"""

    __children: List[PyDuiWidget] = None
    __padding: PyDuiEdge = None
    __childHVAlign: Tuple[PyDuiAlign, PyDuiAlign] = (PyDuiAlign.START, PyDuiAlign.START)
    __fitrule: List[str] = None

    def __init__(self):
        super().__init__()
        self.__padding = PyDuiEdge()
        self.__children = []
        self.__fitrule = []

    def parse_attrib(self, k: str, v: str):
        if k == "padding":
            self.padding = utils.Str2Edge(v)
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
        """draw

        Draw layout and children widgets.

        Args:
            ctx (cairo.Context): draw context, replace cairo.Context to DrawContext later.
            x (float): dirty rect, x offset relative to parent view
            y (float): dirty rect, y offset relative to parent view
            width (float): dirty rect, rect width
            height (float): dirty rect, rect height
            # dirty_rect (PyDuiRect): dirty rect
            # clip_rect (PyDuiRect): clip rect
        """
        # TODO, detect draw region is contain widget or not.
        # then you can use this draw region to draw the dirty region only.
        super().draw(ctx, x, y, width, height)
        rc1 = PyDuiRect.from_size((0, 0), (self.width, self.height))
        for i in range(self.child_count):
            child = self.get_child_at(i)
            ctx.save()
            # clip region
            rc2 = PyDuiRect.from_size((child.x, child.y), (child.width, child.height))
            draw_rc = utils.intersect_rect(rc1, rc2)
            ctx.rectangle(draw_rc.left, draw_rc.top, draw_rc.width, draw_rc.height)
            ctx.clip()
            ctx.translate(child.x, child.y)
            child.draw(ctx, 0, 0, draw_rc.width, draw_rc.height)
            ctx.restore()

    def layout(self, x: float, y: float, width: float, height: float, constraint: PyDuiLayoutConstraint):
        """layout

        Args:
            x (float): x offset relative to parent
            y (float): y offset relative to parent
            width (float): widget width
            height (float): widget height
            constraint (PyDuiLayoutConstraint): layout constraint
        """
        super().layout(x, y, width, height, constraint)

    def get_children_range_fixed_width(self, start, stop) -> float:
        w = 0
        for i in range(start, stop):
            child = self.get_child_at(i)
            margin = child.margin
            w = w + child.fixed_width + margin.width
        return w

    def get_children_range_fixed_height(self, start, stop) -> float:
        h = 0
        for i in range(start, stop):
            child = self.get_child_at(i)
            margin = child.margin
            h = h + child.fixed_height + margin.height
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
        child.set_parent(self)
        self.__children.append(child)
        if self.get_window_client() is not None:
            child.__do_post_init__(self.get_window_client())

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
        child.set_parent(self)
        self.__children.insert(index, child)
        if self.get_window_client() is not None:
            child.__do_post_init__(self.get_window_client())

    def remove_child(self, child: PyDuiWidget):
        """Remove child widget.

        Args:
            widget (PyDuiWidget): widget object
        """
        self.__children.remove(child)

    def remove_child_by_id(self, widget_id: str):
        """Remove child widget by widget_id

        Args:
            widget_id (str): widget id

        """
        child = self.get_child(widget_id)
        if child is None:
            return
        self.remove_child(child)

    def remove_child_at(self, index: int):
        """Remove child widget at index

        if the index overbound, do nothing.

        Args:
            index (int): widget index

        """
        child = self.get_child_at(index)
        if child is None:
            return
        self.remove_child(child)

    @property
    def child_count(self) -> int:
        return len(self.__children)

    @property
    def padding(self) -> PyDuiEdge:
        return self.__padding

    @padding.setter
    def padding(self, padding: PyDuiEdge):
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

    def __do_post_init__(self, window_client: PyDuiWindowClientInterface):
        super().__do_post_init__(window_client)
        for i in range(self.child_count):
            child = self.get_child_at(i)
            child.__do_post_init__(window_client)

    # private functions
    def __process_resize_or_move__(self, gtk_widget, gtk_event):
        pass
        # logging.debug(f"resize, {object}")

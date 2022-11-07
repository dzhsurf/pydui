# -*- coding: utf-8 -*-
from typing import Callable, Optional, cast

from pydui import utils
from pydui.common.base import *
from pydui.common.import_gtk import *
from pydui.core.widget import *


class PyDuiLayout(PyDuiWidget):
    """Layout base class, all layouts inherit from PyDuiLayout"""

    def __init__(self) -> None:
        super().__init__()
        self.__padding = PyDuiEdge()
        self.__children: List[PyDuiWidget] = []
        self.__fitrule: List[str] = []
        self.__childHVAlign: Tuple[PyDuiAlign, PyDuiAlign] = (PyDuiAlign.START, PyDuiAlign.START)

    def parse_attrib(self, k: str, v: str) -> None:
        if k == "padding":
            self.padding = utils.Str2Edge(v)
        elif k == "halign":
            self.__childHVAlign = (Text2PyDuiAlign(v), self.valign)
        elif k == "valign":
            self.__childHVAlign = (self.halign, Text2PyDuiAlign(v))
        elif k == "fitrule":
            self.__fitrule = v.split(",")

        super().parse_attrib(k, v)

    def draw(self, ctx: cairo.Context, dirty_rect: PyDuiRect, clip_rect: PyDuiRect):
        """draw

        Draw layout and children widgets.

        Args:
            ctx (cairo.Context): draw context, replace cairo.Context to DrawContext later.
            dirty_rect (PyDuiRect): dirty rect, relative to root
            clip_rect (PyDuiRect): clip rect, relative to root
        """
        # TODO, detect draw region is contain widget or not.
        # then you can use this draw region to draw the dirty region only.
        if clip_rect.width == 0 or clip_rect.height == 0:
            return

        super().draw(ctx, dirty_rect, clip_rect)
        rc1 = PyDuiRect.from_size((0, 0), (self.width, self.height))

        def internal_draw_child(child: PyDuiWidget):
            ctx.save()
            # clip region
            rc2 = PyDuiRect.from_size((child.x, child.y), (child.width, child.height))
            draw_rc = utils.intersect_rect(rc1, rc2)
            ctx.rectangle(draw_rc.left, draw_rc.top, draw_rc.width, draw_rc.height)
            ctx.clip()
            # translate child coordinate
            ctx.translate(child.x, child.y)
            child_rc = PyDuiRect.from_size((child.root_x, child.root_y), (child.width, child.height))
            child_clip_rect = utils.intersect_rect(child_rc, clip_rect)
            child.draw(ctx, dirty_rect, child_clip_rect)
            ctx.restore()

        float_widgets: Dict[int, List[PyDuiWidget]] = {}

        for i in range(self.child_count):
            child = self.get_child_at(i)
            if child is None:
                continue
            if child.is_float:
                if child.zindex in float_widgets:
                    float_widgets[child.zindex].append(child)
                else:
                    float_widgets[child.zindex] = [child]
                continue
            internal_draw_child(child)

        for key in sorted(float_widgets.keys()):
            for child in float_widgets[key]:
                internal_draw_child(child)

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

    def get_children_range_fixed_width(self, start: int, stop: int) -> float:
        w: float = 0
        for i in range(start, stop):
            child = self.get_child_at(i)
            if child is None:
                continue
            margin = child.margin
            w = w + child.fixed_width + margin.width
        return w

    def get_children_range_fixed_height(self, start: int, stop: int) -> float:
        h: float = 0
        for i in range(start, stop):
            child = self.get_child_at(i)
            if child is None:
                continue
            margin = child.margin
            h = h + child.fixed_height + margin.height
        return h

    def get_child(self, widget_id: str) -> Optional[PyDuiWidget]:
        """Get child widget by widget_id

        Args:
            widget_id (str): widget id

        Returns:
            PyDuiWidget: return widget object.
        """
        for i in range(self.child_count):
            child = self.get_child_at(i)
            if child is None:
                continue
            if child.get_id() == widget_id:
                return child
            if issubclass(type(child), PyDuiLayout):
                target = cast(PyDuiLayout, child).get_child(widget_id)
                if target is None:
                    continue
                if target is not None:
                    return target

        return None

    def find_widget_by_pos(
        self, x: float, y: float, *, filter: Callable[[PyDuiWidget], bool] = PyDuiWidget.find_widget_default_filter
    ) -> Optional[PyDuiWidget]:
        """Get child by position"""
        for i in range(self.child_count):
            child = self.get_child_at(i)
            if child is None:
                continue
            if not child.contain_pos(x, y):
                continue

            if issubclass(type(child), PyDuiLayout):
                target = cast(PyDuiLayout, child).find_widget_by_pos(x, y, filter=filter)
                if target is not None and filter(target):
                    return target

            if filter(child):
                return child
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
        if child is None:
            return
        child.set_parent(self)
        self.__children.append(child)
        if self.has_window_client():
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

    def set_need_update(self):
        super().set_need_update()

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
    def fitrule(self) -> List[str]:
        return self.__fitrule

    # private function
    def __do_layout__(self):
        pass

    def __do_post_init__(self, window_client: PyDuiWindowClientInterface):
        super().__do_post_init__(window_client)
        for i in range(self.child_count):
            child = self.get_child_at(i)
            if child is None:
                continue
            child.__do_post_init__(window_client)

    # private functions
    def __process_resize_or_move__(self, gtk_widget: Gtk.Widget, gtk_event: Gdk.Event):
        pass
        # logging.debug(f"resize, {object}")

# -*- coding: utf-8 -*-
"""PyDui window provider implement with GTK-3"""
from dataclasses import dataclass
from typing import Dict, Tuple

from pydui.common.base import PyDuiRect
from pydui.common.import_gtk import *
from pydui.component.embedded_widget import PyDuiEmbeddedWidgetHost, PyDuiEmbeddedWidgetProvider
from pydui.component.text_view.text_view_gtk3 import PyDuiEmbeddedTextViewGTK3
from pydui.provider.embedded_widget_host_gtk3 import PyDuiEmbeddedWidgetHostGTK3


@dataclass
class __PyDuiEmbeddedWidgetLayoutItem__:
    layer: Gtk.Overlay
    fixed: Gtk.Fixed
    x: float
    y: float
    last_clip_rect: PyDuiRect


class PyDuiEmbeddedWidgetProviderGTK3(PyDuiEmbeddedWidgetProvider):
    """PyDuiEmbeddedWidgetProviderGTK3"""

    __parent_layer: Gtk.Fixed = None
    __gtk_widget_dict: Dict[Gtk.Widget, __PyDuiEmbeddedWidgetLayoutItem__] = None

    def __init__(self, parent_layer: Gtk.Fixed) -> None:
        super().__init__()
        self.__gtk_widget_dict = {}
        self.__parent_layer = parent_layer

    def create_embedded_widget(self, widget_typename: str) -> PyDuiEmbeddedWidgetHost:
        if widget_typename == "TextView":
            return PyDuiEmbeddedTextViewGTK3()
        return None

    def add_embedded_widget(self, widget: PyDuiEmbeddedWidgetHostGTK3):
        gtk_widget = widget.get_gtk_widget()
        if gtk_widget is None:
            return

        item = __PyDuiEmbeddedWidgetLayoutItem__(
            layer=Gtk.Overlay(),
            fixed=Gtk.Fixed(),
            x=0,
            y=0,
            last_clip_rect=PyDuiRect(),
        )
        item.fixed.add(gtk_widget)
        item.layer.add_overlay(item.fixed)

        self.__gtk_widget_dict[gtk_widget] = item
        self.__parent_layer.add(item.layer)

    def remove_embedded_widget(self, widget: PyDuiEmbeddedWidgetHostGTK3):
        gtk_widget = widget.get_gtk_widget()
        if gtk_widget in self.__gtk_widget_dict:
            item = self.__gtk_widget_dict.pop(gtk_widget)
            self.__parent_layer.remove(item.layer)

    def update_embedded_widget_position(self, widget: PyDuiEmbeddedWidgetHostGTK3, x: float, y: float):
        item = self.__get_layout_item__(widget)
        if item is None:
            return
        item.x = x
        item.y = y
        item.last_clip_rect = PyDuiRect()
        self.__parent_layer.move(item.layer, x, y)

    def update_embedded_widget_viewport(self, widget: PyDuiEmbeddedWidgetHostGTK3, rect: PyDuiRect):
        item = self.__get_layout_item__(widget)
        gtk_widget = widget.get_gtk_widget()
        if item is None or gtk_widget is None:
            return

        if rect.is_same(item.last_clip_rect):
            return
        item.last_clip_rect = rect

        if rect.width < 0 or rect.height < 0:
            item.layer.set_visible(False)
        else:
            item.layer.set_visible(True)
            item.fixed.move(gtk_widget, 0, item.y - rect.top)
            item.layer.set_size_request(max(0, rect.width), max(0, rect.height))
            self.__parent_layer.move(item.layer, item.x, rect.top)

    # private
    def __get_layout_item__(self, widget: PyDuiEmbeddedWidgetHostGTK3) -> __PyDuiEmbeddedWidgetLayoutItem__:
        gtk_widget = widget.get_gtk_widget()
        if gtk_widget is None:
            return None
        if gtk_widget in self.__gtk_widget_dict:
            return self.__gtk_widget_dict[gtk_widget]
        return None

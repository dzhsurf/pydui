# -*- coding: utf-8 -*-
"""PyDui window provider implement with GTK-3"""
from dataclasses import dataclass
from typing import Dict, Optional

from pydui.common.base import PyDuiRect
from pydui.common.import_gtk import *
from pydui.component.embedded_widget import (
    PyDuiEmbeddedWidgetHost,
    PyDuiEmbeddedWidgetProtocol,
    PyDuiEmbeddedWidgetProvider,
)
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

    def __init__(self, parent_layer: Gtk.Fixed) -> None:
        super().__init__()
        self.__gtk_widget_dict: Dict[Gtk.Widget, __PyDuiEmbeddedWidgetLayoutItem__] = {}
        self.__parent_layer: Gtk.Fixed = parent_layer

    def create_embedded_widget(self, widget_typename: str) -> PyDuiEmbeddedWidgetHost[PyDuiEmbeddedWidgetProtocol]:
        if widget_typename == "TextView":
            return PyDuiEmbeddedTextViewGTK3()

        raise ValueError(f"widget typename not support. {widget_typename}")

    def add_embedded_widget(self, widget: PyDuiEmbeddedWidgetHost[PyDuiEmbeddedWidgetProtocol]) -> None:
        if not isinstance(widget, PyDuiEmbeddedWidgetHostGTK3):
            return

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

    def remove_embedded_widget(self, widget: PyDuiEmbeddedWidgetHost[PyDuiEmbeddedWidgetProtocol]):
        if not isinstance(widget, PyDuiEmbeddedWidgetHostGTK3):
            return

        gtk_widget = widget.get_gtk_widget()
        if gtk_widget in self.__gtk_widget_dict:
            item = self.__gtk_widget_dict.pop(gtk_widget)
            self.__parent_layer.remove(item.layer)

    def update_embedded_widget_position(
        self, widget: PyDuiEmbeddedWidgetHost[PyDuiEmbeddedWidgetProtocol], x: float, y: float
    ):
        if not isinstance(widget, PyDuiEmbeddedWidgetHostGTK3):
            return

        item = self.__get_layout_item__(widget)
        if item is None:
            return
        item.x = x
        item.y = y
        item.last_clip_rect = PyDuiRect()
        self.__parent_layer.move(item.layer, x, y)  # type: ignore

    def update_embedded_widget_viewport(
        self, widget: PyDuiEmbeddedWidgetHost[PyDuiEmbeddedWidgetProtocol], rect: PyDuiRect
    ):
        if not isinstance(widget, PyDuiEmbeddedWidgetHostGTK3):
            return

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
            item.fixed.move(gtk_widget, 0, item.y - rect.top)  # type: ignore
            item.layer.set_size_request(max(0, rect.width), max(0, rect.height))  # type: ignore
            self.__parent_layer.move(item.layer, item.x, rect.top)  # type: ignore

    # private
    def __get_layout_item__(
        self, widget: PyDuiEmbeddedWidgetHostGTK3[PyDuiEmbeddedWidgetProtocol]
    ) -> Optional[__PyDuiEmbeddedWidgetLayoutItem__]:
        gtk_widget = widget.get_gtk_widget()
        if gtk_widget is None:
            return None
        if gtk_widget in self.__gtk_widget_dict:
            return self.__gtk_widget_dict[gtk_widget]
        return None

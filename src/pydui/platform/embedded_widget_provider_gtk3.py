# -*- coding: utf-8 -*-
"""PyDui window provider implement with GTK-3"""
from pydui.common.import_gtk import *
from pydui.component.embedded_widget import PyDuiEmbeddedWidgetHost, PyDuiEmbeddedWidgetProvider
from pydui.component.text_view.text_view_gtk3 import PyDuiEmbeddedTextViewGTK3
from pydui.platform.embedded_widget_host_gtk3 import PyDuiEmbeddedWidgetHostGTK3


class PyDuiEmbeddedWidgetProviderGTK3(PyDuiEmbeddedWidgetProvider):
    """PyDuiEmbeddedWidgetProviderGTK3"""

    __parent_layer: Gtk.Fixed

    def __init__(self, parent_layer: Gtk.Fixed) -> None:
        super().__init__()
        self.__parent_layer = parent_layer

    def create_embedded_widget(self, widget_typename: str) -> PyDuiEmbeddedWidgetHost:
        if widget_typename == "TextView":
            return PyDuiEmbeddedTextViewGTK3()
        return None

    def add_embedded_widget(self, widget: PyDuiEmbeddedWidgetHostGTK3):
        self.__parent_layer.add(widget.get_gtk_widget())

    def remove_embedded_widget(self, widget: PyDuiEmbeddedWidgetHostGTK3):
        self.__parent_layer.remove(widget.get_gtk_widget())

    def update_embedded_widget_position(self, widget: PyDuiEmbeddedWidgetHostGTK3, x: float, y: float):
        self.__parent_layer.move(widget.get_gtk_widget(), x, y)

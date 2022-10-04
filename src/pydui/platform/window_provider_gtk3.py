# -*- coding: utf-8 -*-
"""PyDui window provider implement with GTK-3"""
from typing import Any, Callable, Protocol, TypeVar

from pydui.common.import_gtk import *
from pydui.component.embedded_widget import PyDuiEmbeddedWidgetProvider
from pydui.core.render_canvas import PyDuiRenderCanvas
from pydui.core.window_base import PyDuiWindowProvider
from pydui.core.window_config import PyDuiWindowConfig
from pydui.platform.embedded_widget_provider_gtk3 import PyDuiEmbeddedWidgetProviderGTK3


class PyDuiWindowProviderGTK3(PyDuiWindowProvider):
    """PyDuiWindowProviderGTK3"""

    __gtk_window: Gtk.Window = None
    __layer: Gtk.Fixed = None
    __ctx: cairo.Context = None
    __embedded_widget_provider: PyDuiEmbeddedWidgetProvider = None

    def __init__(self) -> None:
        super().__init__()

        print("init")

        # Init Gtk Window
        self.__gtk_window = Gtk.Window()
        # TODO: custom window style
        # self.__gtk_window.set_decorated(False)

    def init_window(self, config: PyDuiWindowConfig, ondraw: Callable[[Any, float, float], None]):
        super().init_window(config, ondraw)
        self.__canvas = PyDuiRenderCanvas(ondraw)

        # create window
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)

        self.__layer = Gtk.Fixed()
        self.__layer.set_has_window(True)
        self.__layer.put(self.__canvas, 0, 0)
        scrolled_window.add(self.__layer)

        self.__gtk_window.add(scrolled_window)

        # init window attributes
        self.__gtk_window.set_title(config.title)
        self.__gtk_window.set_default_size(*config.size)
        self.__gtk_window.set_size_request(*config.min_size)
        self.__gtk_window.set_position(config.position)

    def set_render_context(self, context: Any):
        self.__ctx = context

    def get_render_context(self) -> Any:
        return self.__ctx

    def notify_redraw(self):
        self.__canvas.redraw()
        self.__canvas.queue_draw_area(0, 0, self.__canvas.get_width(), self.__canvas.get_height())

    def show(self):
        self.__gtk_window.show_all()

    def set_window_size(self, width: float, height: float):
        self.__canvas.set_size_request(width, height)

    def get_embedded_widget_provider(self) -> PyDuiEmbeddedWidgetProvider:
        if self.__embedded_widget_provider is None:
            self.__embedded_widget_provider = PyDuiEmbeddedWidgetProviderGTK3(self.__layer)
        return self.__embedded_widget_provider

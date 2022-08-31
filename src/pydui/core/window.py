from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Type

import cairo
import gi

from pydui.core.layout import *
from pydui.core.render import *
from pydui.core.widget import *
from pydui.core.window_handler import PyDuiWindowHandler

gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, GdkPixbuf, Gtk


@dataclass(frozen=True)
class PyDuiWindowConfig:

    """Window config dataclass

    Attributes:
        title (str): window title
        size (tuple[int, int]): window size, default is (400, 300)
        min_size (tuple[int, int]): window min size, default is (0, 0)
        max_size (tuple[int, int]): window max size, default is (0, 0), when set to zero, means no limit.
        positon (Gtk.WindowPosition): window initial position

    """

    title: str
    size: tuple[int, int]
    min_size: tuple[int, int]
    max_size: tuple[int, int]
    position: Gtk.WindowPosition = Gtk.WindowPosition.CENTER


class PyDuiWindow(object):

    """Window object"""

    __gtk_window: Gtk.Window = None
    __manager: PyDuiRenderManager = None
    __handler: PyDuiWindowHandler = None

    __xy: tuple[float, float] = (0.0, 0.0)
    __wh: tuple[float, float] = (0.0, 0.0)

    def __init__(
        self,
        loader: Type[PyDuiResourceLoader],
        config: PyDuiWindowConfig,
        rootview: PyDuiWidget,
        handler: Type[PyDuiWindowHandler] = None,
    ):
        # Init Gtk Window
        self.__gtk_window = Gtk.Window()
        # self.__gtk_window.set_decorated(False)

        # Init render manger
        self.__manager = PyDuiRenderManager(window=self, loader=loader)
        self.__manager.set_rootview(rootview)

        # Init handler
        self.__handler = PyDuiWindowHandler()
        if handler is not None:
            self.__handler = handler()

        # config window
        self.__config_window__(self.__gtk_window, config)
        self.__initial_events__()

        self.__init_window_finish__()

    def __config_window__(
        self,
        gtk_window: Gtk.Window,
        config: PyDuiWindowConfig,
    ):
        gtk_window.set_title(config.title)
        gtk_window.set_default_size(*config.size)
        gtk_window.set_size_request(*config.min_size)
        gtk_window.set_position(config.position)

    def __initial_events__(self):
        self.__gtk_window.add_events(Gdk.EventMask.SUBSTRUCTURE_MASK)
        self.__gtk_window.connect("configure-event", self.__on_config_event__)
        self.__gtk_window.connect("destroy", self.__on_window_destroy__)
        self.__gtk_window.connect("window-state-event", self.__on_window_state_event__)
        self.__gtk_window.connect("show", self.__on_window_show__)
        self.__gtk_window.connect("hide", self.__on_window_hide__)

    def __init_window_finish__(self):
        self.__handler.on_window_init(self)

    def __on_window_show__(self, gtk_object: Gtk.Widget):
        logging.debug(f"__on_window_show__: {gtk_object}")
        self.__handler.on_window_visible_changed(True)

    def __on_window_hide__(self, gtk_object: Gtk.Widget):
        logging.debug(f"__on_window_hide__: {gtk_object}")
        self.__handler.on_window_visible_changed(False)

    def __on_window_destroy__(self, gtk_object: Gtk.Widget):
        logging.debug(f"__on_window_destroy__: {self}, {gtk_object}")
        self.__handler.on_window_destroy()

    def __on_window_state_event__(self, gtk_object: Gtk.Widget, event_window_state: Gdk.EventWindowState):
        pass

    def __on_config_event__(self, gtk_object: Gtk.Widget, gtk_event: Gdk.EventConfigure):
        x, y = gtk_event.x, gtk_event.y
        w, h = gtk_event.width, gtk_event.height
        if x != self.__xy[0] or y != self.__xy[1]:
            self.__xy = (x, y)
            self.__handler.on_window_position_changed(x, y)
        if w != self.__wh[0] or y != self.__wh[1]:
            self.__wh = (w, h)
            self.__handler.on_window_size_changed(w, h)

    def get_gtk_window(self):
        return self.__gtk_window

    def show(self):
        self.__gtk_window.show_all()

    def get_widget(self, widget_id: str) -> PyDuiWidget:
        return self.__manager.get_widget(widget_id=widget_id)

    @property
    def handler(self) -> PyDuiWindowHandler:
        return self.__handler

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Type

import cairo
import gi

from pydui.core.event_dispatcher import PyDuiEventDispatcher
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
    __event_dispatcher: PyDuiEventDispatcher = None

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

        # Init manger
        self.__manager = PyDuiRenderManager(window=self, loader=loader)
        self.__manager.set_rootview(rootview)
        self.__event_dispatcher = PyDuiEventDispatcher(manager=self.__manager, handler=handler)

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
        self.__gtk_window.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.__gtk_window.connect("configure-event", self.__event_dispatcher.on_configure_event)
        self.__gtk_window.connect("destroy", self.__event_dispatcher.on_window_destroy)
        self.__gtk_window.connect("window-state-event", self.__event_dispatcher.on_window_state_event)
        self.__gtk_window.connect("show", self.__event_dispatcher.on_window_show)
        self.__gtk_window.connect("hide", self.__event_dispatcher.on_window_hide)
        self.__gtk_window.connect("motion-notify-event", self.__event_dispatcher.on_motion_notify)

    def __init_window_finish__(self):
        self.__event_dispatcher.on_window_init(self)

    def get_gtk_window(self):
        return self.__gtk_window

    def show(self):
        self.__gtk_window.show_all()

    def get_widget(self, widget_id: str) -> PyDuiWidget:
        return self.__manager.get_widget(widget_id=widget_id)

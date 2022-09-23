# -*- coding: utf-8 -*-
from __future__ import annotations

import imp
import logging
from dataclasses import dataclass
from typing import Type

from pydui.core.event_dispatcher import PyDuiEventDispatcher
from pydui.core.import_gtk import *
from pydui.core.layout import *
from pydui.core.render_manager import PyDuiRenderManager
from pydui.core.resource_loader import PyDuiResourceLoader
from pydui.core.widget import *
from pydui.core.window_base import PyDuiWindowBase
from pydui.core.window_handler import PyDuiWindowHandler


@dataclass(frozen=True)
class PyDuiWindowConfig:

    """Window config dataclass

    Attributes:
        title (str): window title
        size (tuple[int, int]): window size, default is (400, 300)
        min_size (tuple[int, int]): window min size, default is (0, 0)
        max_size (tuple[int, int]): window max size, default is (0, 0), when set to zero, means no limit.
        positon (Gtk.WindowPosition): window initial position
        default_font (str): window default font
        default_fontsize (int): window default font size
        default_fontbold (bool): window default font is bold or not
    """

    title: str
    size: tuple[int, int]
    min_size: tuple[int, int]
    max_size: tuple[int, int]
    position: Gtk.WindowPosition = Gtk.WindowPosition.CENTER
    default_font: str = "Arial"
    default_fontsize: int = 16
    default_fontbold: bool = False


class PyDuiWindow(PyDuiWindowBase):

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
        # TODO: custom window style
        # self.__gtk_window.set_decorated(False)

        # Init manger
        self.__manager = PyDuiRenderManager(window=self, loader=loader)
        self.__manager.set_rootview(rootview)
        self.__event_dispatcher = PyDuiEventDispatcher(
            window=self.get_gtk_window(),
            manager=self.__manager,
            handler=handler,
            on_init=self.__on_window_init__,
        )

        # config window
        self.__config_window__(self.__gtk_window, config)

        # init events
        self.__event_dispatcher.init_events()

    def __config_window__(
        self,
        gtk_window: Gtk.Window,
        config: PyDuiWindowConfig,
    ):
        gtk_window.set_title(config.title)
        gtk_window.set_default_size(*config.size)
        gtk_window.set_size_request(*config.min_size)
        gtk_window.set_position(config.position)

        self.__manager.default_fontfamily = config.default_font
        if config.default_fontbold:
            self.__manager.default_fontfamily = self.__manager.default_fontfamily + " bold"
        self.__manager.default_fontsize = config.default_fontsize

    def __on_window_init__(self):
        self.__event_dispatcher.handler.on_window_init(self)

    def get_gtk_window(self):
        return self.__gtk_window

    def show(self):
        self.__gtk_window.show_all()

    def get_widget(self, widget_id: str) -> PyDuiWidget:
        return self.__manager.get_widget(widget_id=widget_id)

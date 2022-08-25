# window.py
import logging
from dataclasses import dataclass
from typing import Optional, Type

import gi

from pydui.core.widget import *
from pydui.core.window import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class PyDuiWindow(object):
    pass


class PyDuiWindowHandler(object):
    pass


class PyDuiRenderManager(object):

    """Render manager"""

    # manager all widget
    def __init__(self):
        pass

    def get_widget(self, widget_id: str) -> Optional[PyDuiWidget]:
        return PyDuiWidget()


@dataclass(frozen=True)
class PyDuiWindowConfig:

    """Window config dataclass

    Attributes:
        title (str): window title
        size (tuple[int, int]): window size
        positon (Gtk.WindowPosition): window initial position

    """

    title: str
    size: tuple[int, int]
    position: Gtk.WindowPosition = Gtk.WindowPosition.CENTER


class PyDuiWindow(object):

    """Window object"""

    __gtk_window: Gtk.Window
    __manager: PyDuiRenderManager
    __handler: PyDuiWindowHandler

    def __init__(
        self,
        config: PyDuiWindowConfig,
        handler: Type[PyDuiWindowHandler] = None,
    ):
        # Init Gtk Window
        self.__gtk_window = Gtk.Window()
        # Init render manger
        self.__manager = PyDuiRenderManager()
        # Init handler
        self.__handler = PyDuiWindowHandler(window=self)
        if handler is not None:
            self.__handler = handler(window=self)
        # config window
        self.__config_window__(self.__gtk_window, config)
        self.__initial_events__()

    def __config_window__(
        self,
        gtk_window: Gtk.Window,
        config: PyDuiWindowConfig,
    ):
        gtk_window.title = config.title
        gtk_window.set_size_request(*config.size)
        gtk_window.set_position(config.position)

    def __initial_events__(self):
        self.__gtk_window.connect("show", self.__on_window_show__)
        self.__gtk_window.connect("destroy", self.__on_window_destroy__)

    def __on_window_show__(self, gtk_object: Gtk.Widget):
        logging.debug(f"__on_window_show__: {self}, {gtk_object}")
        self.__handler.on_window_show()

    def __on_window_destroy__(self, gtk_object: Gtk.Widget):
        logging.debug(f"__on_window_destroy__: {self}, {gtk_object}")
        self.__handler.on_window_destroy()

    def show(self):
        self.__gtk_window.show()

    def get_widget(self, widget_id: str) -> Optional[PyDuiWidget]:
        return self.__manager.get_widget(widget_id=widget_id)


class PyDuiWindowHandler(object):
    __window: PyDuiWindow

    def __init__(self, window: PyDuiWindow):
        self.__window = window

    def window(self) -> PyDuiWindow:
        return self.__window

    def on_window_show(self):
        pass

    def on_window_destroy(self):
        pass

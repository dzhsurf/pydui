from __future__ import annotations

import logging
from typing import Type

import gi

from pydui.core.render import PyDuiRenderManager
from pydui.core.widget import PyDuiWidget
from pydui.core.window_handler import PyDuiWindowHandler

gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk


class PyDuiEventDispatcher(object):
    """Event Dispatcher"""

    __manager: PyDuiRenderManager = None
    __handler: PyDuiWindowHandler = None
    # window position
    __xy: tuple[float, float] = (0, 0)
    __wh: tuple[float, float] = (0, 0)

    # mouse state
    __mouse_x: int = 0
    __mouse_y: int = 0
    __last_hover_widget: PyDuiWidget = None

    def __init__(
        self,
        manager: PyDuiRenderManager,
        handler: PyDuiWindowHandler,
    ):
        self.__manager = manager
        self.__handler = PyDuiWindowHandler()
        if handler is not None:
            self.__handler = handler()

    def on_window_init(self, window: PyDuiWindow):
        logging.debug(f"on_window_init: {window}")
        self.__handler.on_window_init(window)

    def on_window_destroy(self, object: Gtk.Widget):
        logging.debug(f"on_window_destroy: {object}")
        self.__handler.on_window_destroy()

    def on_window_show(self, object: Gtk.Widget):
        logging.debug(f"on_window_show: {object}")
        self.__handler.on_window_visible_changed(True)

    def on_window_hide(self, object: Gtk.Widget):
        logging.debug(f"on_window_hide: {object}")
        self.__handler.on_window_visible_changed(False)

    def on_configure_event(self, object: Gtk.Widget, event: Gdk.EventConfigure):
        if event.type == Gdk.EventType.NOTHING:
            self.__manager.notify_redraw()
            return

        x, y = event.x, event.y
        w, h = event.width, event.height
        if x != self.__xy[0] or y != self.__xy[1]:
            self.__xy = (x, y)
            self.__handler.on_window_position_changed(x, y)
        if w != self.__wh[0] or y != self.__wh[1]:
            self.__wh = (w, h)
            self.__handler.on_window_size_changed(w, h)

    def on_window_state_event(self, object: Gtk.Widget, event: Gdk.EventWindowState):
        pass

    def on_motion_notify(self, object: Gtk.Widget, event: Gtk.MotionEvent):
        x, y, x_root, y_root = int(event.x), int(event.y), event.x_root, event.y_root

        if x != self.__mouse_x or y != self.__mouse_y:
            self.__dispatch_mouse_move(x, y)

    def __dispatch_mouse_move(self, x: int, y: int):
        self.__mouse_x, self.__mouse_y = x, y

        widget = self.__manager.get_widget_by_pos(x, y)
        hover_change = widget != self.__last_hover_widget
        old_widget = self.__last_hover_widget
        self.__last_hover_widget = widget

        if hover_change:
            if old_widget is not None:
                old_widget.on_mouse_leave(widget)
            if widget is not None:
                widget.on_mouse_enter()
        else:
            if widget is not None:
                widget.on_mouse_move(x, y)

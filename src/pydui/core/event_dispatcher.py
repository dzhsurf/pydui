from __future__ import annotations

import logging
from typing import Any, Type

from pynoticenter import PyNotiCenter, PyNotiTaskQueue

from pydui.core.import_gtk import *
from pydui.core.render_manager import PyDuiRenderManager
from pydui.core.widget import PyDuiWidget
from pydui.core.window_handler import PyDuiWindowHandler


class PyDuiEventDispatcher(object):
    """Event Dispatcher"""

    __window: Gtk.Window = None
    __manager: PyDuiRenderManager = None
    __handler: PyDuiWindowHandler = None
    __on_init: callable = None
    __task_queue: PyNotiTaskQueue = None

    # window position
    __xy: tuple[float, float] = (0, 0)
    __wh: tuple[float, float] = (0, 0)

    # mouse state
    __mouse_x: int = 0
    __mouse_y: int = 0
    __last_hover_widget: PyDuiWidget = None
    __last_mouse_press_time: int = 0
    __last_mouse_release_time: int = 0

    def __init__(
        self,
        window: Gtk.Window,
        manager: PyDuiRenderManager,
        handler: PyDuiWindowHandler,
        on_init: callable,
    ):
        self.__task_queue = PyNotiCenter.default().create_task_queue("pydui_event")
        self.__task_queue.set_preprocessor(self.__switch_to_gtk_thread__)
        self.__window = window
        self.__manager = manager
        self.__handler = PyDuiWindowHandler()
        self.__on_init = on_init
        if handler is not None:
            self.__handler = handler()

    def init_events(self):
        self.__window.add_events(Gdk.EventMask.SUBSTRUCTURE_MASK)
        self.__window.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.__window.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.__window.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.__window.connect("configure-event", self.on_configure_event)
        self.__window.connect("destroy", self.on_window_destroy)
        self.__window.connect("window-state-event", self.on_window_state_event)
        self.__window.connect("show", self.on_window_show)
        self.__window.connect("hide", self.on_window_hide)
        self.__window.connect("motion-notify-event", self.on_motion_notify)
        self.__window.connect("button-press-event", self.on_button_press)
        self.__window.connect("button-release-event", self.on_button_release)

        if self.__on_init is not None:
            self.__on_init()

    @property
    def handler(self) -> PyDuiWindowHandler:
        return self.__handler

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

    def on_button_press(self, object: Gtk.Widget, event: Gdk.EventButton) -> bool:
        x, y = event.x, event.y
        button = event.button
        # event.time
        # event.state : Gdk.ModifierType
        widget = self.__manager.get_widget_by_pos(x, y)

        if event.type == Gdk.EventType.BUTTON_PRESS:
            self.__dispatch_button_press(widget, button, x, y)
        elif event.type == Gdk.EventType._2BUTTON_PRESS:
            self.__dispatch_2button_press(widget, button, x, y)
        elif event.type == Gdk.EventType._3BUTTON_PRESS:
            self.__dispatch_3button_press(widget, button, x, y)
        return True

    def on_button_release(self, object: Gtk.Widget, event: Gdk.EventButton) -> bool:
        if event.type != Gdk.EventType.BUTTON_RELEASE:
            return
        x, y = event.x, event.y
        button = event.button
        widget = self.__manager.get_widget_by_pos(x, y)
        self.__dispatch_button_release(widget, button, x, y)
        return True

    def __switch_to_gtk_thread__(self, fn: callable, *args: Any, **kwargs: Any) -> None:
        GLib.idle_add(fn, *args, **kwargs)

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

    def __dispatch_button_press(self, widget: PyDuiWidget, button: int, x: float, y: float):
        if widget is None:
            return

    def __dispatch_2button_press(self, widget: PyDuiWidget, button: int, x: float, y: float):
        pass

    def __dispatch_3button_press(self, widget: PyDuiWidget, button: int, x: float, y: float):
        pass

    def __dispatch_button_release(self, widget: PyDuiWidget, button: int, x: float, y: float):
        pass

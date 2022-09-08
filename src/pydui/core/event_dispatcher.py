# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
import queue
from typing import Any, Callable, Tuple, Type

from pydui.core.base import PyDuiClickType
from pydui.core.import_gtk import *
from pydui.core.render_manager import PyDuiRenderManager
from pydui.core.widget import PyDuiWidget
from pydui.core.window_handler import PyDuiWindowHandler


class PyDuiEventDispatcher(object):
    """Event Dispatcher"""

    __window: Gtk.Window = None
    __manager: PyDuiRenderManager = None
    __handler: PyDuiWindowHandler = None
    __on_init: Callable[[None], None] = None

    # window position
    __xy: tuple[float, float] = (0, 0)
    __wh: tuple[float, float] = (0, 0)

    # mouse state
    __mouse_x: int = 0
    __mouse_y: int = 0
    __last_hover_widget: PyDuiWidget = None
    __last_click_task: str = ""
    __last_press_widget: PyDuiWidget = None
    __last_press_button: int = 0
    __last_press_time: int = 0
    __last_click_type: PyDuiClickType = PyDuiClickType.NONE

    def __init__(
        self,
        window: Gtk.Window,
        manager: PyDuiRenderManager,
        handler: PyDuiWindowHandler,
        on_init: Callable[[None], None],
    ):
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
        self.__manager.release()

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
            self.__dispatch_mouse_move__(x, y)

    def on_button_press(self, object: Gtk.Widget, event: Gdk.EventButton) -> bool:
        x, y = event.x, event.y
        widget = self.__manager.get_widget_by_pos(x, y, filter=PyDuiWidget.find_widget_mouse_event_filter)
        if widget is None:
            return True
        if not widget.enabled:
            return True

        if event.type == Gdk.EventType.BUTTON_PRESS:
            self.__dispatch_button_press__(widget, event)
        elif event.type == Gdk.EventType._2BUTTON_PRESS:
            self.__dispatch_2button_press__(widget, event)
        elif event.type == Gdk.EventType._3BUTTON_PRESS:
            self.__dispatch_3button_press__(widget, event)
        return True

    def on_button_release(self, object: Gtk.Widget, event: Gdk.EventButton) -> bool:
        if event.type != Gdk.EventType.BUTTON_RELEASE:
            return
        x, y = event.x, event.y
        widget = self.__manager.get_widget_by_pos(x, y, filter=PyDuiWidget.find_widget_mouse_event_filter)
        if widget is None:
            return True

        self.__dispatch_button_release__(widget, event)
        return True

    def __switch_to_gtk_thread__(
        self, fn: Callable[[Tuple[Any], dict[str, Any]], None], *args: Any, **kwargs: Any
    ) -> bool:
        GLib.idle_add(fn, *args, **kwargs)
        return True

    def __dispatch_mouse_move__(self, x: int, y: int):
        self.__mouse_x, self.__mouse_y = x, y

        widget = self.__manager.get_widget_by_pos(x, y, filter=PyDuiWidget.find_widget_mouse_event_filter)

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

    def __dispatch_button_press__(self, widget: PyDuiWidget, event: Gdk.EventButton):
        if widget is None:
            return
        if widget.on_lbutton_press(event.x, event.y):
            return
        # event.state : Gdk.ModifierType
        button, time = event.button, event.time
        self.__last_press_widget = widget
        self.__last_press_button = button
        self.__last_press_time = time

    def __dispatch_button_release__(self, widget: PyDuiWidget, event: Gdk.EventButton):
        if widget is None:
            return True
        if not widget.enabled:
            return True

        click = True
        if widget != self.__last_press_widget or event.button != self.__last_press_button:
            click = False
        if not widget.contain_pos(event.x, event.y):
            click = False

        if click:
            if self.__last_click_type == PyDuiClickType.CLICK:
                self.__last_click_type = PyDuiClickType.DBCLICK
                self.__manager.cancel_task(self.__last_click_task)
                self.__last_click_task = self.__manager.post_task(self.__dispatch_button_dbclick__, widget, event)
            else:
                interval = 0.2  # TODO, get dbclick interval from setting
                self.__last_click_type = PyDuiClickType.CLICK
                self.__last_click_task = self.__manager.post_task_with_delay(
                    interval, self.__dispatch_button_click__, widget, event
                )
        else:
            if self.__last_click_task != "":
                self.__manager.cancel_task(self.__last_click_task)
            self.__reset_button_click_state__()

    def __reset_button_click_state__(self):
        self.__last_click_type = PyDuiClickType.NONE
        self.__last_click_task = ""
        self.__last_press_widget = None
        self.__last_press_button = 0
        self.__last_press_time = 0

    def __dispatch_button_click__(self, widget: PyDuiWidget, event: Gdk.EventButton):
        last_press_widget = self.__last_press_widget
        last_press_button = self.__last_press_button
        last_press_time = self.__last_press_time
        last_click_type = self.__last_click_type
        self.__reset_button_click_state__()
        if (
            widget is None
            or last_press_widget != widget
            or last_press_button != event.button
            or last_click_type != PyDuiClickType.CLICK
        ):
            return
        if last_press_time == 0:
            return
        if event.button == 3:
            widget.on_rbutton_click(event.x, event.y)
        else:
            widget.on_lbutton_click(event.x, event.y)

    def __dispatch_button_dbclick__(self, widget: PyDuiWidget, event: Gdk.EventButton):
        last_press_widget = self.__last_press_widget
        last_press_button = self.__last_press_button
        last_press_time = self.__last_press_time
        last_click_type = self.__last_click_type
        self.__reset_button_click_state__()
        if (
            widget is None
            or last_press_widget != widget
            or last_press_button != event.button
            or last_click_type != PyDuiClickType.DBCLICK
        ):
            return
        if last_press_time == 0:
            return
        if event.button == 3:
            widget.on_r2button_click(event.x, event.y)
        else:
            widget.on_l2button_click(event.x, event.y)

    def __dispatch_2button_press__(self, widget: PyDuiWidget, event: Gdk.EventButton):
        # This event is difficult to manage and should be avoided. Use press to simulate.
        pass

    def __dispatch_3button_press__(self, widget: PyDuiWidget, event: Gdk.EventButton):
        # This event is difficult to manage and should be avoided. Use press to simulate.
        pass

# -*- coding: utf-8 -*-
import logging
import weakref
from typing import Any, Callable, Tuple, Type
from weakref import ReferenceType

from pydui.common.base import PyDuiClickType
from pydui.core.event import ButtonEvent, ButtonEventType, ButtonType
from pydui.core.widget import PyDuiWidget
from pydui.core.window_client import PyDuiWindowClientInterface
from pydui.core.window_handler import PyDuiWindowHandler
from pydui.core.window_interface import PyDuiWindowInterface


class PyDuiWindowEventDispatcher:
    """Window Event Dispatcher"""

    __window: ReferenceType[PyDuiWindowInterface] = None
    __client: ReferenceType[PyDuiWindowClientInterface] = None
    __handler: PyDuiWindowHandler = None
    __on_init: Callable[[None], None] = None

    # window position
    __xy: Tuple[float, float] = (0, 0)
    __wh: Tuple[float, float] = (0, 0)

    # focus widget
    __focused_widget: PyDuiWidget = None

    # mouse state
    __mouse_x: int = 0
    __mouse_y: int = 0
    __last_hover_widget: PyDuiWidget = None
    __last_click_task: str = ""
    __last_press_widget: PyDuiWidget = None
    __last_press_button: ButtonType = ButtonType.UNDEFINED
    __last_press_time: int = 0
    __last_click_type: PyDuiClickType = PyDuiClickType.NONE

    def __init__(
        self,
        window: PyDuiWindowInterface,
        client: PyDuiWindowClientInterface,
        handler: PyDuiWindowHandler,
        on_init: Callable[[None], None],
    ):
        self.__window = weakref.ref(window)
        self.__client = weakref.ref(client)
        self.__handler = PyDuiWindowHandler()
        self.__on_init = on_init
        if handler is not None:
            self.__handler = handler()

    def init_events(self):
        window = self.__window()
        if window is None:
            return

        provider = window.get_window_provider()
        provider.connect("configure-event", self.on_configure_event)
        provider.connect("destroy", self.on_window_destroy)
        provider.connect("window-state-event", self.on_window_state_event)
        provider.connect("show", self.on_window_show)
        provider.connect("hide", self.on_window_hide)
        provider.connect("motion-notify-event", self.on_motion_notify)
        provider.connect("button-press-event", self.on_button_press)
        provider.connect("button-release-event", self.on_button_release)

        # init finish, callback
        if self.__on_init is not None:
            self.__on_init()

    @property
    def handler(self) -> PyDuiWindowHandler:
        return self.__handler

    def on_window_destroy(self):
        logging.debug("on_window_destroy")
        self.__handler.on_window_destroy()
        self.__client().release()

    def on_window_show(self):
        logging.debug("on_window_show")
        self.__handler.on_window_visible_changed(True)

    def on_window_hide(self):
        logging.debug("on_window_hide")
        self.__handler.on_window_visible_changed(False)

    def on_configure_event(self, x: float, y: float, w: float, h: float) -> bool:

        if x != self.__xy[0] or y != self.__xy[1]:
            self.__xy = (x, y)
            self.__handler.on_window_position_changed(x, y)
        if w != self.__wh[0] or y != self.__wh[1]:
            self.__client().set_window_size(w, h)
            self.__wh = (w, h)
            self.__handler.on_window_size_changed(w, h)

        return False

    def on_window_state_event(self):
        pass

    def on_motion_notify(self, x: int, y: int, x_root: int, y_root: int) -> bool:
        if x != self.__mouse_x or y != self.__mouse_y:
            self.__dispatch_mouse_move__(x, y)
        return False

    def on_button_press(self, event: ButtonEvent) -> bool:
        x, y = event.x, event.y
        widget = self.__client().get_widget_by_pos(x, y, filter=PyDuiWidget.find_widget_mouse_event_filter)
        if widget is None:
            return False
        if not widget.enabled:
            return False

        if event.event == ButtonEventType.PRESS:
            self.__dispatch_button_press__(widget, event)
        elif event.event == ButtonEventType.DBPRESS:
            self.__dispatch_2button_press__(widget, event)
        elif event.event == ButtonEventType.TRIPRESS:
            self.__dispatch_3button_press__(widget, event)

        return True

    def on_button_release(self, event: ButtonEvent) -> bool:
        if event.event != ButtonEventType.RELEASE:
            return False

        x, y = event.x, event.y
        widget = self.__client().get_widget_by_pos(x, y, filter=PyDuiWidget.find_widget_mouse_event_filter)
        if widget is None:
            return False

        self.__dispatch_button_release__(widget, event)
        return True

    def __dispatch_mouse_move__(self, x: int, y: int):
        self.__mouse_x, self.__mouse_y = x, y

        widget = self.__client().get_widget_by_pos(x, y, filter=PyDuiWidget.find_widget_mouse_event_filter)

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

    def __dispatch_button_press__(self, widget: PyDuiWidget, event: ButtonEvent):
        if widget is None:
            return
        if widget.on_lbutton_press(event.x, event.y):
            return
        button, time = event.button, event.time
        self.__last_press_widget = widget
        self.__last_press_button = button
        self.__last_press_time = time

    def __dispatch_button_release__(self, widget: PyDuiWidget, event: ButtonEvent):
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
                self.__client().cancel_task(self.__last_click_task)
                self.__last_click_task = self.__client().post_task(self.__dispatch_button_dbclick__, widget, event)
            else:
                interval = 0.2  # TODO, get dbclick interval from setting
                self.__last_click_type = PyDuiClickType.CLICK
                self.__last_click_task = self.__client().post_task_with_delay(
                    interval, self.__dispatch_button_click__, widget, event
                )
        else:
            if self.__last_click_task != "":
                self.__client().cancel_task(self.__last_click_task)
            self.__reset_button_click_state__()

    def __reset_button_click_state__(self):
        self.__last_click_type = PyDuiClickType.NONE
        self.__last_click_task = ""
        self.__last_press_widget = None
        self.__last_press_button = ButtonType.UNDEFINED
        self.__last_press_time = 0

    def __dispatch_button_click__(self, widget: PyDuiWidget, event: ButtonEvent):
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
        if event.button == ButtonType.BUTTON_RIGHT:
            widget.on_rbutton_click(event.x, event.y)
        else:
            widget.on_lbutton_click(event.x, event.y)

    def __dispatch_button_dbclick__(self, widget: PyDuiWidget, event: ButtonEvent):
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
        if event.button == ButtonType.BUTTON_RIGHT:
            widget.on_r2button_click(event.x, event.y)
        else:
            widget.on_l2button_click(event.x, event.y)

    def __dispatch_2button_press__(self, widget: PyDuiWidget, event: ButtonEvent):
        # This event is difficult to manage and should be avoided. Use press to simulate.
        pass

    def __dispatch_3button_press__(self, widget: PyDuiWidget, event: ButtonEvent):
        # This event is difficult to manage and should be avoided. Use press to simulate.
        pass
# -*- coding: utf-8 -*-
import logging
import weakref
from typing import Any, Callable, Dict, List, Optional, Tuple, Type
from weakref import ReferenceType

from pydui.common.base import PyDuiClickType, PyDuiRect
from pydui.core.event import ButtonEvent, ButtonEventType, ButtonType, NCAreaType, ScrollEvent
from pydui.core.widget import PyDuiWidget
from pydui.core.window_client_interface import PyDuiWindowClientInterface
from pydui.core.window_handler import PyDuiWindowHandler
from pydui.core.window_interface import PyDuiWindowInterface


class PyDuiWindowEventDispatcher:
    """Window Event Dispatcher"""

    def __init__(
        self,
        window: PyDuiWindowInterface,
        client: PyDuiWindowClientInterface,
        handler: Optional[Type[PyDuiWindowHandler]],
        on_init: Callable[[], None],
    ) -> None:
        self.__xy: Tuple[float, float] = (0, 0)
        self.__wh: Tuple[float, float] = (0, 0)
        self.__focused_widget: Optional[PyDuiWidget] = None
        self.__mouse_x: int = 0
        self.__mouse_y: int = 0
        self.__last_hover_widget: Optional[PyDuiWidget] = None
        self.__last_click_task: str = ""
        self.__last_press_widget: Optional[PyDuiWidget] = None
        self.__last_press_button: ButtonType = ButtonType.UNDEFINED
        self.__last_press_time: int = 0
        self.__last_click_type: PyDuiClickType = PyDuiClickType.NONE

        self.__window: ReferenceType[PyDuiWindowInterface] = weakref.ref(window)
        self.__client: ReferenceType[PyDuiWindowClientInterface] = weakref.ref(client)
        self.__handler: PyDuiWindowHandler = PyDuiWindowHandler()
        self.__on_init: Callable[[], None] = on_init
        self.__event_observers: Dict[str, List[Callable[..., Any]]] = {"mouse-move": []}
        if handler is not None:
            self.__handler = handler()

    def init_events(self) -> None:
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
        provider.connect("scroll-event", self.on_scroll_event)

        # init finish, callback
        if self.__on_init is not None:
            self.__on_init()

    def add_event_observer(self, key: str, fn: Callable[..., Any]) -> None:
        if key not in self.__event_observers:
            return
        self.__event_observers[key].append(fn)

    def remove_event_observer(self, key: str, fn: Callable[..., Any]) -> None:
        if key not in self.__event_observers:
            return
        fn_list = list(filter(lambda x: x != fn, self.__event_observers[key]))
        self.__event_observers[key] = fn_list

    @property
    def handler(self) -> PyDuiWindowHandler:
        return self.__handler

    def on_window_destroy(self) -> None:
        logging.debug("on_window_destroy")
        self.__handler.on_window_destroy()
        client = self.__client()
        if client:
            client.release()

    def on_window_show(self) -> None:
        logging.debug("on_window_show")
        self.__handler.on_window_visible_changed(True)

    def on_window_hide(self) -> None:
        logging.debug("on_window_hide")
        self.__handler.on_window_visible_changed(False)

    def on_configure_event(self, x: float, y: float, w: float, h: float) -> bool:

        if x != self.__xy[0] or y != self.__xy[1]:
            self.__xy = (x, y)
            self.__handler.on_window_position_changed(x, y)
        if w != self.__wh[0] or y != self.__wh[1]:
            client = self.__client()
            if client is None:
                return False
            client.set_window_size(w, h)
            self.__wh = (w, h)
            self.__handler.on_window_size_changed(w, h)

        return False

    def on_window_state_event(self):
        pass

    def on_motion_notify(self, x: int, y: int, x_root: int, y_root: int) -> bool:
        if x_root != self.__mouse_x or y_root != self.__mouse_y:
            self.__dispatch_mouse_move__(x_root, y_root)
        return False

    def on_button_press(self, event: ButtonEvent) -> bool:
        x, y = event.x, event.y

        if self.__handler is not None:
            area_type = self.__handler.on_nchittest(x, y)
            if area_type == NCAreaType.UNDEFINED:
                area_type = self.__default_on_nchittest__(x, y)

            if area_type != NCAreaType.UNDEFINED and area_type != NCAreaType.CLIENT:
                self.__handle_ncpress__(area_type, x, y)
                return False

        client = self.__client()
        if client is None:
            return False

        widget = client.get_widget_by_pos(x, y, filter=PyDuiWidget.find_widget_mouse_event_filter)
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

        if self.__last_press_widget is not None:
            self.__dispatch_button_release__(self.__last_press_widget, event)
            return True

        client = self.__client()
        if client is None:
            return False

        widget = client.get_widget_by_pos(x, y, filter=PyDuiWidget.find_widget_mouse_event_filter)
        if widget is None:
            return False

        self.__dispatch_button_release__(widget, event)
        return True

    def on_scroll_event(self, event: ScrollEvent) -> bool:
        x, y = event.x, event.y

        client = self.__client()
        if client is None:
            return False

        widget = client.get_widget_by_pos(x, y, filter=PyDuiWidget.find_widget_mouse_wheel_event_filter)
        if widget is None:
            return False

        return widget.on_scroll_event(event)

    def __dispatch_mouse_move__(self, x: int, y: int):
        self.__mouse_x, self.__mouse_y = x, y

        fn_list = self.__event_observers["mouse-move"].copy()
        for fn in fn_list:
            fn(x, y)

        if self.__last_press_widget is not None:
            self.__last_press_widget.on_mouse_move(x, y)
            return

        client = self.__client()
        if client is None:
            return

        widget = client.get_widget_by_pos(x, y, filter=PyDuiWidget.find_widget_mouse_event_filter)
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
        if time != self.__last_press_time:
            # it is another click press event, reset click task.
            self.__last_click_task = ""
        self.__last_press_widget = widget
        self.__last_press_button = button
        self.__last_press_time = time

    def __dispatch_button_release__(self, widget: Optional[PyDuiWidget], event: ButtonEvent) -> None:
        if widget is None:
            return
        client = self.__client()
        if client is None:
            return

        if widget.enabled:
            if widget.on_lbutton_release(event.x, event.y):
                return
        else:
            widget = None

        click = True
        if widget != self.__last_press_widget or event.button != self.__last_press_button:
            click = False
        if widget and not widget.contain_pos(event.x, event.y):
            click = False

        if click:
            if self.__last_click_type == PyDuiClickType.CLICK:
                self.__last_click_type = PyDuiClickType.DBCLICK
                client.cancel_task(self.__last_click_task)
                self.__last_click_task = client.post_task(self.__dispatch_button_dbclick__, widget, event)
            else:
                interval = 0.2  # TODO, get dbclick interval from setting
                self.__last_click_type = PyDuiClickType.CLICK
                self.__last_click_task = client.post_task_with_delay(
                    interval, self.__dispatch_button_click__, widget, event
                )
        else:
            if self.__last_click_task != "":
                client.cancel_task(self.__last_click_task)
            self.__reset_button_click_state__()
            self.__dispatch_mouse_move__(event.x, event.y)

    def __reset_button_click_state__(self) -> None:
        self.__last_click_type = PyDuiClickType.NONE
        self.__last_click_task = ""
        self.__last_press_widget = None
        self.__last_press_button = ButtonType.UNDEFINED
        self.__last_press_time = 0

    def __dispatch_button_click__(self, task_id: str, widget: PyDuiWidget, event: ButtonEvent) -> None:
        if task_id != self.__last_click_task:
            return

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

    def __dispatch_button_dbclick__(self, task_id: str, widget: PyDuiWidget, event: ButtonEvent) -> None:
        if task_id != self.__last_click_task:
            return

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
            widget.on_rbutton_dbclick(event.x, event.y)
        else:
            widget.on_lbutton_dbclick(event.x, event.y)

    def __dispatch_2button_press__(self, widget: PyDuiWidget, event: ButtonEvent) -> None:
        # This event is difficult to manage and should be avoided. Use press to simulate.
        pass

    def __dispatch_3button_press__(self, widget: PyDuiWidget, event: ButtonEvent) -> None:
        # This event is difficult to manage and should be avoided. Use press to simulate.
        pass

    def __default_on_nchittest__(self, x: float, y: float) -> NCAreaType:
        client = self.__client()
        if client is None:
            return NCAreaType.UNDEFINED

        if client.get_customize_titlebar():

            w, h = client.get_window_size()
            box_size = client.get_box_size()

            if PyDuiRect.from_ltrb(0, 0, box_size.left, box_size.top).contain_point((x, y)):
                return NCAreaType.LEFT_TOP
            if PyDuiRect.from_ltrb(box_size.left, 0, w - box_size.right, box_size.top).contain_point((x, y)):
                return NCAreaType.TOP
            if PyDuiRect.from_ltrb(w - box_size.right, 0, w, box_size.top).contain_point((x, y)):
                return NCAreaType.RIGHT_TOP

            if PyDuiRect.from_ltrb(0, box_size.top, box_size.left, h - box_size.bottom).contain_point((x, y)):
                return NCAreaType.LEFT
            if PyDuiRect.from_ltrb(w - box_size.right, box_size.top, w, h - box_size.bottom).contain_point((x, y)):
                return NCAreaType.RIGHT

            if PyDuiRect.from_ltrb(0, h - box_size.bottom, box_size.left, h).contain_point((x, y)):
                return NCAreaType.LEFT_BOTTOM
            if PyDuiRect.from_ltrb(box_size.left, h - box_size.bottom, w - box_size.right, h).contain_point((x, y)):
                return NCAreaType.BOTTOM
            if PyDuiRect.from_ltrb(w - box_size.right, h - box_size.bottom, w, h).contain_point((x, y)):
                return NCAreaType.RIGHT_BOTTOM

            caption_area = client.get_caption_area()
            if caption_area.contain_point((x, y)):
                return NCAreaType.CAPTION

            return NCAreaType.CLIENT

        return NCAreaType.UNDEFINED

    def __handle_ncpress__(self, area_type: NCAreaType, x: float, y: float) -> None:
        if area_type == NCAreaType.CAPTION:
            self.__process_begin_move_drag__(x, y)
        else:
            self.__process_begin_resize_drag__(area_type, x, y)

    def __process_begin_move_drag__(self, x: float, y: float) -> None:
        client = self.__client()
        if client is None:
            return
        client.get_window_provider().begin_move_drag(x, y)

    def __process_begin_resize_drag__(self, area_type: NCAreaType, x: float, y: float) -> None:
        client = self.__client()
        if client is None:
            return
        client.get_window_provider().begin_resize_drag(area_type, x, y)

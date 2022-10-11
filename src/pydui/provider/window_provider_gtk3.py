# -*- coding: utf-8 -*-
"""PyDui window provider implement with GTK-3"""
from distutils.util import convert_path
from time import time
from typing import Any, Callable, Dict, List, Tuple

from pydui.common.import_gtk import *
from pydui.component.embedded_widget import PyDuiEmbeddedWidgetProvider
from pydui.core.event import ButtonEvent, ButtonEventType, ButtonType, NCAreaType
from pydui.core.render_canvas import PyDuiRenderCanvas
from pydui.core.window_config import PyDuiWindowConfig
from pydui.core.window_interface import PyDuiWindowProvider
from pydui.provider.embedded_widget_provider_gtk3 import PyDuiEmbeddedWidgetProviderGTK3


def __to_button_type__(button: int) -> ButtonType:
    if button == 3:
        return ButtonType.BUTTON_RIGHT
    return ButtonType.BUTTON_LEFT


def __to_event_type__(type: Gdk.EventType) -> ButtonEventType:
    if type == Gdk.EventType.BUTTON_PRESS:
        return ButtonEventType.PRESS
    elif type == Gdk.EventType._2BUTTON_PRESS:
        return ButtonEventType.DBPRESS
    elif type == Gdk.EventType._3BUTTON_PRESS:
        return ButtonEventType.TRIPRESS
    elif type == Gdk.EventType.BUTTON_RELEASE:
        return ButtonEventType.RELEASE
    return ButtonEventType.UNDEFINED


def __to_button_event__(event: Gdk.EventButton) -> ButtonEvent:
    screen_x, screen_y = event.window.get_root_coords(event.x, event.y)
    base_x, base_y = event.window.get_root_coords(0, 0)
    return ButtonEvent(
        x=int(screen_x - base_x),
        y=int(screen_y - base_y),
        button=__to_button_type__(event.button),
        event=__to_event_type__(event.type),
        time=int(event.time),
    )


class PyDuiWindowProviderGTK3(PyDuiWindowProvider):
    """PyDuiWindowProviderGTK3"""

    __gtk_window: Gtk.Window = None
    __layer: Gtk.Fixed = None
    __ctx: cairo.Context = None
    __embedded_widget_provider: PyDuiEmbeddedWidgetProvider = None
    __signals_fn_dict: Dict[str, List[Callable]] = None

    def __init__(self) -> None:
        super().__init__()
        self.__signals_fn_dict = dict()

        # Init Gtk Window
        self.__gtk_window = Gtk.Window()
        self.__gtk_window.set_border_width(0)

    def init_window(self, config: PyDuiWindowConfig, ondraw: Callable[[Any, float, float], None]):
        super().init_window(config, ondraw)
        self.__canvas = PyDuiRenderCanvas(ondraw)

        # create window
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_border_width(0)
        scrolled_window.set_shadow_type(Gtk.ShadowType.NONE)
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.__layer = Gtk.Fixed()
        self.__layer.set_has_window(True)

        viewport = Gtk.Viewport()
        viewport.set_shadow_type(Gtk.ShadowType.NONE)
        viewport.add(self.__layer)

        self.__layer.put(self.__canvas, 0, 0)
        scrolled_window.add(viewport)

        gtk_window = self.__gtk_window
        gtk_window.add(scrolled_window)

        # init window attributes
        gtk_window.set_title(config.title)
        gtk_window.set_default_size(*config.size)
        gtk_window.set_size_request(*config.min_size)
        gtk_window.set_position(config.position)
        if config.customize_titlebar:
            self.__gtk_window.set_decorated(False)

        # init window events
        gtk_window.add_events(Gdk.EventMask.SUBSTRUCTURE_MASK)
        gtk_window.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        gtk_window.add_events(Gdk.EventMask.POINTER_MOTION_HINT_MASK)
        self.__layer.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.__layer.add_events(Gdk.EventMask.POINTER_MOTION_HINT_MASK)
        self.__layer.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.__layer.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        gtk_window.connect("configure-event", self.on_configure_event)
        gtk_window.connect("destroy", self.on_window_destroy)
        gtk_window.connect("window-state-event", self.on_window_state_event)
        gtk_window.connect("show", self.on_window_show)
        gtk_window.connect("hide", self.on_window_hide)
        gtk_window.connect("motion-notify-event", self.on_motion_notify)
        gtk_window.connect("drag-begin", self.on_drag_begin)
        gtk_window.connect("drag-end", self.on_drag_end)
        # scrolled_window.connect("button-press-event", self.on_button_press)
        # scrolled_window.connect("button-release-event", self.on_button_release)
        self.__layer.connect("button-press-event", self.on_button_press)
        self.__layer.connect("button-release-event", self.on_button_release)

    def set_render_context(self, context: Any):
        self.__ctx = context

    def get_render_context(self) -> Any:
        return self.__ctx

    def notify_redraw(self):
        self.__canvas.redraw()
        self.__canvas.queue_draw_area(0, 0, self.__canvas.get_width(), self.__canvas.get_height())

    def show(self):
        self.__gtk_window.show_all()

    def get_window_size(self) -> Tuple[float, float]:
        w = self.__gtk_window.get_allocated_width()
        h = self.__gtk_window.get_allocated_height()
        return (float(w), float(h))

    def set_window_size(self, width: float, height: float):
        self.__canvas.set_size_request(width, height)

    def get_embedded_widget_provider(self) -> PyDuiEmbeddedWidgetProvider:
        if self.__embedded_widget_provider is None:
            self.__embedded_widget_provider = PyDuiEmbeddedWidgetProviderGTK3(self.__layer)
        return self.__embedded_widget_provider

    def connect(self, signal: str, fn: Callable):
        if signal in self.__signals_fn_dict:
            self.__signals_fn_dict[signal].append(fn)
        else:
            self.__signals_fn_dict[signal] = [fn]

    def disconnect(self, signal: str, fn: Callable):
        if signal not in self.__signals_fn_dict:
            return
        self.__signals_fn_dict[signal] = list(filter(lambda x: x != fn, self.__signals_fn_dict[signal]))
        if len(self.__signals_fn_dict[signal]) == 0:
            self.__signals_fn_dict.pop(signal)

    def disaconnect_all(self, signal: str):
        if signal not in self.__signals_fn_dict:
            return
        self.__signals_fn_dict.pop(signal)

    # private
    def on_configure_event(self, object: Gtk.Widget, event: Gdk.EventConfigure) -> bool:
        if event.type == Gdk.EventType.NOTHING:
            self.notify_redraw()
            return True

        x, y = event.x, event.y
        w, h = event.width, event.height
        self.__notify_signals__("configure-event", x, y, w, h)

        return False

    def on_window_state_event(self, object: Gtk.Widget, event: Gdk.EventWindowState):
        self.__notify_signals__("window-state-event")

    def on_window_destroy(self, object: Gtk.Widget):
        self.__notify_signals__("destroy")

    def on_window_show(self, object: Gtk.Widget):
        self.__notify_signals__("show")

    def on_window_hide(self, object: Gtk.Widget):
        return self.__notify_signals__("hide")

    def on_motion_notify(self, object: Gtk.Widget, event: Gdk.EventMotion) -> bool:
        x, y, x_root, y_root = int(event.x), int(event.y), int(event.x_root), int(event.y_root)

        return self.__notify_signals__("motion-notify-event", x, y, x_root, y_root)

    def on_drag_begin(self, object: Gtk.Widget, context: Gdk.DragContext):
        pass

    def on_drag_end(self, object: Gtk.Widget, context: Gdk.DragContext):
        pass

    def on_button_press(self, object: Gtk.Widget, event: Gdk.EventButton) -> bool:
        return self.__notify_signals__("button-press-event", __to_button_event__(event))

    def on_button_release(self, object: Gtk.Widget, event: Gdk.EventButton) -> bool:
        return self.__notify_signals__("button-release-event", __to_button_event__(event))

    def begin_move_drag(self, x: float, y: float):
        timestamp = int(time())
        self.__gtk_window.begin_move_drag(1, int(x), int(y), timestamp)

    def begin_resize_drag(self, area_type: NCAreaType, x: float, y: float):
        convert_table = {
            NCAreaType.LEFT: Gdk.WindowEdge.WEST,
            NCAreaType.TOP: Gdk.WindowEdge.NORTH,
            NCAreaType.RIGHT: Gdk.WindowEdge.EAST,
            NCAreaType.BOTTOM: Gdk.WindowEdge.SOUTH,
            NCAreaType.LEFT_TOP: Gdk.WindowEdge.NORTH_WEST,
            NCAreaType.LEFT_BOTTOM: Gdk.WindowEdge.SOUTH_WEST,
            NCAreaType.RIGHT_TOP: Gdk.WindowEdge.NORTH_EAST,
            NCAreaType.RIGHT_BOTTOM: Gdk.WindowEdge.SOUTH_EAST,
        }
        edge = convert_table[area_type]
        timestamp = int(time())
        self.__gtk_window.begin_resize_drag(edge, 1, int(x), int(y), timestamp)

    def __notify_signals__(self, signal: str, *args: Any) -> bool:
        if signal not in self.__signals_fn_dict:
            return False

        for fn in self.__signals_fn_dict[signal]:
            result = fn(*args)
            if result:
                return True

        return False

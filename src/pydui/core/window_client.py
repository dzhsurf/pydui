# -*- coding: utf-8 -*-
import weakref
from typing import Any, Callable, Optional, Tuple, Type
from weakref import ReferenceType

from pynoticenter import PyNotiCenter, PyNotiOptions  # type: ignore

from pydui.common.base import PyDuiEdge, PyDuiLayoutConstraint, PyDuiRect
from pydui.common.import_gtk import *
from pydui.component.embedded_widget import PyDuiEmbeddedWidgetHost
from pydui.core.appearance_manager import PyDuiAppearanceManager
from pydui.core.layout import PyDuiLayout
from pydui.core.resource_loader import PyDuiResourceLoader
from pydui.core.widget import PyDuiWidget
from pydui.core.window_client_interface import PyDuiWindowClientInterface
from pydui.core.window_config import PyDuiWindowConfig
from pydui.core.window_event_dispatcher import PyDuiWindowEventDispatcher
from pydui.core.window_handler import PyDuiWindowHandler
from pydui.core.window_interface import PyDuiWindowInterface, PyDuiWindowProvider


class PyDuiWindowClient(PyDuiWindowClientInterface):
    """Window client"""

    def __init__(
        self,
        window: PyDuiWindowInterface,
        config: PyDuiWindowConfig,
        loader: PyDuiResourceLoader,
        rootview: PyDuiLayout,
        handler: Optional[Type[PyDuiWindowHandler]],
    ):
        # init component
        self.__window: ReferenceType[PyDuiWindowInterface] = weakref.ref(window)  # weakref
        self.__appearance_manager = PyDuiAppearanceManager()
        self.__loader = loader
        self.__task_queue = PyNotiCenter.default().create_task_queue(
            options=PyNotiOptions(queue="pydui-client-queue", fn_with_task_id=True)
        )
        self.__task_queue.set_preprocessor(self.__post_task_to_gtk_thread__)
        self.__rootview = rootview
        self.__event_dispatcher = PyDuiWindowEventDispatcher(
            window=window,  # weakref
            client=self,  # weakref
            handler=handler,
            on_init=self.__on_window_init__,
        )

        # start build window
        window.get_window_provider().init_window(config, ondraw=self.__on_draw__)
        self.__config_window__(config)

    def release(self):
        self.__task_queue.terminate(False)

    def init_window(self, config: PyDuiWindowConfig, ondraw: Callable[[Any, float, float], None]):
        self.get_window_provider().init_window(config, ondraw)

    def get_window_size(self) -> Tuple[float, float]:
        return self.get_window_provider().get_window_size()

    def set_window_size(self, width: float, height: float):
        self.get_window_provider().set_window_size(width, height)

    def get_customize_titlebar(self) -> bool:
        return self.__appearance_manager.customize_titlebar

    def get_caption_area(self) -> PyDuiRect:
        caption_height = self.__appearance_manager.caption_height
        w, _ = self.get_window_size()
        return PyDuiRect.from_ltrb(0, 0, w, caption_height)

    def get_box_size(self) -> PyDuiEdge:
        return self.__appearance_manager.box_size

    def get_render_context(self) -> cairo.Context:
        return self.get_window_provider().get_render_context()

    def add_event_observer(self, key: str, fn: Callable[..., Any]) -> None:
        self.__event_dispatcher.add_event_observer(key, fn)

    def remove_event_observer(self, key: str, fn: Callable[..., Any]) -> None:
        self.__event_dispatcher.remove_event_observer(key, fn)

    def cancel_task(self, task_id: str) -> None:
        self.__task_queue.cancel_task(task_id)

    def post_task(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> str:
        return self.post_task_with_delay(0.0, fn, *args, **kwargs)

    def post_task_with_delay(self, delay: float, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> str:
        if self.__task_queue.is_terminated:
            return ""
        if fn is None:
            return ""
        return self.__task_queue.post_task_with_delay(delay, fn, *args, **kwargs)

    def get_resource_loader(self):
        return self.__loader

    def get_window_interface(self) -> PyDuiWindowInterface:
        window = self.__window()
        if window is None:
            raise ValueError("window interface is None")
        return window

    def get_window_provider(self) -> PyDuiWindowProvider:
        window = self.__window()
        if window is None:
            raise ValueError("window provider is None")
        return window.get_window_provider()

    def create_embedded_widget(self, widget_typename: str) -> PyDuiEmbeddedWidgetHost[Any]:
        return self.get_window_provider().get_embedded_widget_provider().create_embedded_widget(widget_typename)

    def add_embedded_widget(self, widget: PyDuiEmbeddedWidgetHost[Any]):
        self.get_window_provider().get_embedded_widget_provider().add_embedded_widget(widget)

    def remove_embedded_widget(self, widget: PyDuiEmbeddedWidgetHost[Any]):
        self.get_window_provider().get_embedded_widget_provider().remove_embedded_widget(widget)

    def update_embedded_widget_position(self, widget: PyDuiEmbeddedWidgetHost[Any], x: float, y: float):
        self.get_window_provider().get_embedded_widget_provider().update_embedded_widget_position(widget, x, y)

    def update_embedded_widget_viewport(self, widget: PyDuiEmbeddedWidgetHost[Any], rect: PyDuiRect):
        self.get_window_provider().get_embedded_widget_provider().update_embedded_widget_viewport(widget, rect)

    def get_appearance(self) -> PyDuiAppearanceManager:
        return self.__appearance_manager

    def get_rootview(self) -> PyDuiLayout:
        """Return root view widget.

        Returns:
            PyDuiLayout: root view.
        """
        return self.__rootview

    def get_widget(self, widget_id: str) -> Optional[PyDuiWidget]:
        """Get widget by widget id

        Args:
            widget_id (str): widget id
        """
        return self.__rootview.get_child(widget_id)

    def get_widget_by_pos(
        self,
        x: float,
        y: float,
        *,
        filter: Callable[[PyDuiWidget], bool] = PyDuiWidget.find_widget_default_filter,
    ) -> Optional[PyDuiWidget]:
        if self.__rootview is None:
            return None

        return self.__rootview.find_widget_by_pos(x, y, filter=filter)

    def mark_dirty(self, widget: PyDuiWidget):
        p = widget.parent
        if p is None or p.is_need_update:
            # no parent or is setted, return directly.
            return

        # mark parent need update
        p.set_need_update()
        if not isinstance(p, PyDuiLayout):
            return
        if not p.autofit:
            return
        # mark sibling dirty
        find: bool = False
        for i in range(p.child_count):
            child = p.get_child_at(i)
            if child is None or not child.visible:
                continue
            if find:
                child.set_need_update()
            elif child is widget:
                find = True

    # private

    def __config_window__(
        self,
        config: PyDuiWindowConfig,
    ):
        self.__appearance_manager.default_fontfamily = config.default_font
        if config.default_fontbold:
            self.__appearance_manager.default_fontfamily = self.__appearance_manager.default_fontfamily + " bold"
        self.__appearance_manager.default_fontsize = config.default_fontsize
        self.__appearance_manager.customize_titlebar = config.customize_titlebar
        self.__appearance_manager.box_size = config.box_size
        self.__appearance_manager.caption_height = config.caption_height
        self.set_window_size(config.size[0], config.size[1])
        self.__event_dispatcher.init_events()

    def __on_window_init__(self):
        self.__rootview.__do_post_init__(self)
        window = self.__window()
        if window is None:
            raise ValueError("window is None")

        self.__event_dispatcher.handler.on_window_init(window)

    def __on_draw__(self, ctx: cairo.Context, width: float, height: float):
        if self.__rootview is None:
            return
        self.get_window_provider().set_render_context(ctx)
        constraint = PyDuiLayoutConstraint(width, height)
        self.__rootview.layout(0, 0, width, height, constraint)
        dirty_rect = PyDuiRect.from_ltrb(0, 0, width, height)
        clip_rect = dirty_rect.copy()
        self.__rootview.draw(ctx, dirty_rect, clip_rect)

    def __post_task_to_gtk_thread__(self, fn: Callable[..., None], task_id: str, *args: Any, **kwargs: Any) -> bool:
        if self.__task_queue.is_terminated:
            return True
        GLib.idle_add(fn, task_id, *args, **kwargs)
        return True

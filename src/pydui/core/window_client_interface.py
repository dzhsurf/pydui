# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Tuple

from pydui.common.base import PyDuiEdge, PyDuiRect
from pydui.common.import_gtk import *
from pydui.component.embedded_widget import PyDuiEmbeddedWidgetHost
from pydui.core.appearance_manager import PyDuiAppearanceManager
from pydui.core.resource_loader import PyDuiResourceLoader
from pydui.core.window_config import PyDuiWindowConfig
from pydui.core.window_provider import PyDuiWindowProvider


class PyDuiWindowClientInterface(ABC):
    @abstractmethod
    def get_resource_loader(self) -> PyDuiResourceLoader:
        pass

    @abstractmethod
    def get_window_provider(self) -> PyDuiWindowProvider:
        pass

    @abstractmethod
    def get_appearance(self) -> PyDuiAppearanceManager:
        pass

    @abstractmethod
    def create_embedded_widget(self, widget_typename: str) -> PyDuiEmbeddedWidgetHost[Any]:
        pass

    @abstractmethod
    def add_embedded_widget(self, widget: PyDuiEmbeddedWidgetHost[Any]) -> None:
        pass

    @abstractmethod
    def remove_embedded_widget(self, widget: PyDuiEmbeddedWidgetHost[Any]) -> None:
        pass

    @abstractmethod
    def update_embedded_widget_position(self, widget: PyDuiEmbeddedWidgetHost[Any], x: float, y: float) -> None:
        pass

    @abstractmethod
    def update_embedded_widget_viewport(self, widget: PyDuiEmbeddedWidgetHost[Any], rect: PyDuiRect) -> None:
        pass

    @abstractmethod
    def init_window(self, config: PyDuiWindowConfig, ondraw: Callable[[Any, float, float], None]) -> None:
        pass

    @abstractmethod
    def release(self):
        pass

    @abstractmethod
    def get_window_size(self) -> Tuple[float, float]:
        pass

    @abstractmethod
    def set_window_size(self, width: float, height: float) -> None:
        pass

    @abstractmethod
    def get_customize_titlebar(self) -> bool:
        pass

    @abstractmethod
    def get_caption_area(self) -> PyDuiRect:
        pass

    @abstractmethod
    def get_box_size(self) -> PyDuiEdge:
        pass

    # render

    @abstractmethod
    def get_render_context(self) -> cairo.Context:
        pass

    @abstractmethod
    def get_widget(self, widget_id: str) -> Optional[Any]:
        pass

    @abstractmethod
    def get_widget_by_pos(
        self,
        x: float,
        y: float,
        *,
        filter: Callable[[Any], bool],
    ) -> Optional[Any]:
        pass

    @abstractmethod
    def mark_dirty(self, widget: Any):
        pass

    # event

    @abstractmethod
    def add_event_observer(self, key: str, fn: Callable[..., Any]) -> None:
        pass

    @abstractmethod
    def remove_event_observer(self, key: str, fn: Callable[..., Any]) -> None:
        pass

    @abstractmethod
    def cancel_task(self, task_id: str) -> None:
        pass

    @abstractmethod
    def post_task(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> str:
        pass

    @abstractmethod
    def post_task_with_delay(self, delay: float, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> str:
        pass

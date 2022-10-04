# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any, Callable

from pydui.common.import_gtk import *
from pydui.component.embedded_widget import PyDuiEmbeddedWidgetHost
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
    def create_embedded_widget(self, widget_typename: str) -> PyDuiEmbeddedWidgetHost:
        pass

    @abstractmethod
    def add_embedded_widget(self, widget: PyDuiEmbeddedWidgetHost):
        pass

    @abstractmethod
    def remove_embedded_widget(self, widget: PyDuiEmbeddedWidgetHost):
        pass

    @abstractmethod
    def update_embedded_widget_position(self, widget: PyDuiEmbeddedWidgetHost, x: float, y: float):
        pass

    @abstractmethod
    def init_window(self, config: PyDuiWindowConfig, ondraw: Callable[[Any, float, float], None]):
        pass

    @abstractmethod
    def set_window_size(self, width: float, height: float):
        pass

    @abstractmethod
    def notify_redraw(self):
        pass

    @abstractmethod
    def get_render_context(self) -> cairo.Context:
        pass

    @abstractmethod
    def cancel_task(self, task_id: str):
        pass

    @abstractmethod
    def post_task(self, fn: callable, *args: Any, **kwargs: Any):
        pass

    @abstractmethod
    def post_task_with_delay(self, delay: float, fn: callable, *args: Any, **kwargs: Any):
        pass

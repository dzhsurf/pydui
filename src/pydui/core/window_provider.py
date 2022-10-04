# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Any, Callable, Protocol

from pydui.component.embedded_widget import PyDuiEmbeddedWidgetProvider
from pydui.core.window_config import PyDuiWindowConfig


class PyDuiWindowProvider(Protocol):
    @abstractmethod
    def set_render_context(self, context: Any):
        pass

    @abstractmethod
    def get_render_context(self) -> Any:
        pass

    @abstractmethod
    def init_window(self, config: PyDuiWindowConfig, ondraw: Callable[[Any, float, float], None]):
        pass

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def notify_redraw(self):
        pass

    @abstractmethod
    def set_window_size(self, width: float, height: float):
        pass

    @abstractmethod
    def get_embedded_widget_provider(self) -> PyDuiEmbeddedWidgetProvider:
        pass

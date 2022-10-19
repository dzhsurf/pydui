# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Any, Callable, Protocol, Tuple

from pydui.component.embedded_widget import PyDuiEmbeddedWidgetProvider
from pydui.core.event import NCAreaType
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
    def get_window_size(self) -> Tuple[float, float]:
        pass

    @abstractmethod
    def set_window_size(self, width: float, height: float):
        pass

    @abstractmethod
    def get_embedded_widget_provider(self) -> PyDuiEmbeddedWidgetProvider:
        pass

    @abstractmethod
    def connect(self, signal: str, fn: Callable[..., Any]):
        pass

    @abstractmethod
    def disconnect(self, signal: str, fn: Callable[..., Any]):
        pass

    @abstractmethod
    def disaconnect_all(self, signal: str):
        pass

    @abstractmethod
    def begin_move_drag(self, x: float, y: float):
        pass

    @abstractmethod
    def begin_resize_drag(self, area_type: NCAreaType, x: float, y: float):
        pass

# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any, Callable, Protocol

from pydui.common.import_gtk import *
from pydui.component.embedded_widget import PyDuiEmbeddedWidgetHost
from pydui.core.widget import PyDuiWidget
from pydui.core.window_provider import PyDuiWindowProvider


class PyDuiWindowBase(ABC):
    @abstractmethod
    def get_widget(self, widget_id: str) -> PyDuiWidget:
        pass

    @abstractmethod
    def execute_platform_code(self, cb: Callable[[Any], None]):
        pass

    @abstractmethod
    def create_embedded_widget(self, widget_typename: str) -> PyDuiEmbeddedWidgetHost:
        pass

    @abstractmethod
    def get_window_provider(self) -> PyDuiWindowProvider:
        pass

    @abstractmethod
    def show(self):
        pass

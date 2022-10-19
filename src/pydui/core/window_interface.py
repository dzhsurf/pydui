# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any, Optional

from pydui.common.import_gtk import *
from pydui.component.embedded_widget import PyDuiEmbeddedWidgetHost
from pydui.core.widget import PyDuiWidget
from pydui.core.window_provider import PyDuiWindowProvider


class PyDuiWindowInterface(ABC):
    @abstractmethod
    def get_widget(self, widget_id: str) -> Optional[PyDuiWidget]:
        pass

    @abstractmethod
    def create_embedded_widget(self, widget_typename: str) -> PyDuiEmbeddedWidgetHost[Any]:
        pass

    @abstractmethod
    def get_window_provider(self) -> PyDuiWindowProvider:
        pass

    @abstractmethod
    def show(self):
        pass

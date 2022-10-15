# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Generic, Protocol, TypeVar

from pydui.common.base import PyDuiRect
from pydui.common.import_gtk import *

T = TypeVar("T")


class PyDuiEmbeddedWidgetHost(Generic[T]):
    """PyDuiEmbeddedWidgetHost"""

    def __init__(self) -> None:
        super().__init__()

    @property
    def api(self) -> T:
        return self

    def show(self):
        pass


class PyDuiEmbeddedWidgetProvider(Protocol[T]):
    """PyDuiEmbeddedWidgetProvider"""

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
    def update_embedded_widget_viewport(self, widget: PyDuiEmbeddedWidgetHost, rect: PyDuiRect):
        pass

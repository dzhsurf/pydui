# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import Protocol, TypeVar, cast

from pydui.common.base import PyDuiRect
from pydui.common.import_gtk import *

P = TypeVar("P", covariant=True)


class PyDuiEmbeddedWidgetProtocol(Protocol):
    pass


class PyDuiEmbeddedWidgetHost(Protocol[P]):
    """PyDuiEmbeddedWidgetHost"""

    def __init__(self) -> None:
        super().__init__()

    @property
    def api(self) -> P:
        return cast(P, self)

    def show(self):
        pass


class PyDuiEmbeddedWidgetProvider:
    """PyDuiEmbeddedWidgetProvider"""

    @abstractmethod
    def create_embedded_widget(self, widget_typename: str) -> PyDuiEmbeddedWidgetHost[PyDuiEmbeddedWidgetProtocol]:
        pass

    @abstractmethod
    def add_embedded_widget(self, widget: PyDuiEmbeddedWidgetHost[PyDuiEmbeddedWidgetProtocol]):
        pass

    @abstractmethod
    def remove_embedded_widget(self, widget: PyDuiEmbeddedWidgetHost[PyDuiEmbeddedWidgetProtocol]):
        pass

    @abstractmethod
    def update_embedded_widget_position(
        self, widget: PyDuiEmbeddedWidgetHost[PyDuiEmbeddedWidgetProtocol], x: float, y: float
    ):
        pass

    @abstractmethod
    def update_embedded_widget_viewport(
        self, widget: PyDuiEmbeddedWidgetHost[PyDuiEmbeddedWidgetProtocol], rect: PyDuiRect
    ):
        pass

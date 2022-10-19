# -*- coding: utf-8 -*-
"""PyDuiTextViewProtocol"""
from abc import abstractmethod

from pydui.component.embedded_widget import PyDuiEmbeddedWidgetProtocol


class PyDuiTextViewProtocol(PyDuiEmbeddedWidgetProtocol):
    @abstractmethod
    def set_text(self, text: str):
        pass

    @abstractmethod
    def get_text(self) -> str:
        pass

    @abstractmethod
    def set_font(self, font: str, fontsize: int):
        pass

    @abstractmethod
    def set_editable(self, editable: bool):
        pass

    @abstractmethod
    def get_editable(self) -> bool:
        pass

    @abstractmethod
    def set_size_request(self, width: float, height: float):
        pass

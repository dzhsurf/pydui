# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import TypeVar

from pydui.common.import_gtk import *
from pydui.component.embedded_widget import PyDuiEmbeddedWidgetHost

T = TypeVar("T")


class PyDuiEmbeddedWidgetHostGTK3(PyDuiEmbeddedWidgetHost[T]):
    """PyDuiEmbeddedWidgetHostGTK3"""

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_gtk_widget(self) -> Gtk.Widget:
        pass

    def show(self):
        widget = self.get_gtk_widget()
        if widget is None:
            return
        widget.show_all()

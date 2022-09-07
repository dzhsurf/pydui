# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from pydui.core.import_gtk import *
from pydui.core.widget import PyDuiWidget


class PyDuiWindowBase(ABC):
    @abstractmethod
    def get_gtk_window(self) -> Gtk.Window:
        pass

    @abstractmethod
    def get_widget(self, widget_id: str) -> PyDuiWidget:
        pass

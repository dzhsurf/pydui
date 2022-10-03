# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from pydui.common.import_gtk import *


class PyDuiGtkWidgetInterface(ABC):
    @abstractmethod
    def get_gtk_widget(self) -> Gtk.Widget:
        pass

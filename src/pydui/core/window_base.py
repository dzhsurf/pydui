from abc import ABC, abstractmethod

from pydui.core.import_gtk import *


class PyDuiWindowBase(ABC):
    @abstractmethod
    def get_gtk_window(self) -> Gtk.Window:
        pass

# widget.py
# all ui element is PyDuiWidget
from typing import Optional

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class PyDuiWidget(object):
    pass


class PyDuiWidget(object):
    __widget: Gtk.Widget

    def __init__(self):
        pass

    def get_child(self, widget_id: str) -> Optional[PyDuiWidget]:
        pass

    def get_parent(self) -> Optional[PyDuiWidget]:
        pass

    def connect(self, signal_name: str, callback: callable):
        pass

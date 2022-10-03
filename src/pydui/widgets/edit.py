# -*- coding: utf-8 -*-
from pydui.core.base import PyDuiLayoutConstraint
from pydui.core.gtk_widget_interface import PyDuiGtkWidgetInterface
from pydui.core.import_gtk import *
from pydui.core.widget import PyDuiWidget
from pydui.widgets.pgview import PyDuiPGView


class PyDuiEdit(PyDuiPGView, PyDuiGtkWidgetInterface):

    __gtk_text_view: Gtk.TextView = None
    __gtk_scrolled_window: Gtk.ScrolledWindow = None

    @staticmethod
    def build_name() -> str:
        return "Edit"

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)

    def on_post_init(self):
        self.__init_gtk_text_view_if_needed__()

    def parse_attrib(self, k: str, v: str):
        return super().parse_attrib(k, v)

    def layout(self, x: float, y: float, width: float, height: float, constraint: PyDuiLayoutConstraint):
        super().layout(x, y, width, height, constraint)
        self.get_render_manager().move_gtk_widget(self, x, y)
        self.__gtk_scrolled_window.set_size_request(width, height)

    # PyDuiGtkWidgetInterface
    def get_gtk_widget(self) -> Gtk.Widget:
        return self.__gtk_scrolled_window

    # private
    def __init_gtk_text_view_if_needed__(self):
        if self.__gtk_text_view is not None:
            return
        self.__gtk_scrolled_window = Gtk.ScrolledWindow()
        self.__gtk_scrolled_window.set_hexpand(True)
        self.__gtk_scrolled_window.set_vexpand(True)

        self.__gtk_text_view = Gtk.TextView()
        self.__gtk_scrolled_window.add(self.__gtk_text_view)
        self.get_render_manager().put_gtk_widget(self)

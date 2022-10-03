# -*- coding: utf-8 -*-
from pydui.core.base import PyDuiLayoutConstraint
from pydui.core.gtk_widget_interface import PyDuiGtkWidgetInterface
from pydui.core.import_gtk import *
from pydui.core.widget import PyDuiWidget
from pydui.widgets.pgview import PyDuiPGView


class PyDuiEdit(PyDuiPGView, PyDuiGtkWidgetInterface):

    __gtk_text_view: Gtk.TextView = None
    __gtk_scrolled_window: Gtk.ScrolledWindow = None
    __text: str = ""
    __editable: bool = True  # Default is can edit
    __font: str = ""
    __fontsize: int = 0

    @staticmethod
    def build_name() -> str:
        return "Edit"

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)

    def on_post_init(self):
        self.__init_gtk_text_view_if_needed__()

    def parse_attrib(self, k: str, v: str):
        if k == "text":
            self.text = v
        elif k == "editable":
            self.editable = v == "true"
        elif k == "font":
            self.font = v
        elif k == "fontsize":
            self.fontsize = int(v)
        super().parse_attrib(k, v)

    def layout(self, x: float, y: float, width: float, height: float, constraint: PyDuiLayoutConstraint):
        super().layout(x, y, width, height, constraint)
        if self.__gtk_scrolled_window is None:
            return
        self.get_render_manager().move_gtk_widget(self, x, y)
        self.__gtk_scrolled_window.set_size_request(width, height)

    # PyDuiGtkWidgetInterface
    def get_gtk_widget(self) -> Gtk.Widget:
        return self.__gtk_scrolled_window

    @property
    def text(self) -> str:
        if self.__gtk_text_view is None:
            return self.__text
        return self.__gtk_text_view.get_buffer().text()

    @text.setter
    def text(self, txt: str):
        self.__text = txt
        if self.__gtk_text_view is None:
            return
        self.__gtk_text_view.get_buffer().set_text(txt)

    @property
    def editable(self) -> bool:
        if self.__gtk_text_view is None:
            return self.__editable
        return self.__gtk_text_view.get_editable()

    @editable.setter
    def editable(self, editable: bool):
        self.__editable = editable
        if self.__gtk_text_view is None:
            return
        self.__gtk_text_view.set_editable(self.__editable)

    @property
    def font(self) -> str:
        if self.__font == "":
            return self.get_render_manager().default_fontfamily
        return self.__font

    @font.setter
    def font(self, font: str):
        self.__font = font
        if self.__gtk_text_view is None:
            return
        desc = f"{self.font} {self.fontsize}"
        self.__gtk_text_view.override_font(Pango.font_description_from_string(desc))

    @property
    def fontsize(self) -> int:
        if self.__fontsize == 0:
            return self.get_render_manager().default_fontsize
        return self.__fontsize

    @fontsize.setter
    def fontsize(self, fontsize: int):
        self.__fontsize = fontsize
        if self.__gtk_text_view is None:
            return
        desc = f"{self.font} {self.fontsize}"
        self.__gtk_text_view.override_font(Pango.font_description_from_string(desc))

    # private
    def __init_gtk_text_view_if_needed__(self):
        if self.__gtk_scrolled_window is not None:
            return
        self.__gtk_scrolled_window = Gtk.ScrolledWindow()
        self.__gtk_scrolled_window.set_hexpand(True)
        self.__gtk_scrolled_window.set_vexpand(True)

        self.__gtk_text_view = Gtk.TextView()
        self.__gtk_text_view.override_font(Pango.font_description_from_string(f"{self.font} {self.fontsize}"))
        self.__gtk_text_view.set_editable(self.__editable)
        self.__gtk_text_view.get_buffer().set_text(self.__text)
        self.__gtk_scrolled_window.add(self.__gtk_text_view)
        self.get_render_manager().put_gtk_widget(self)

# -*- coding: utf-8 -*-
from typing import Tuple

from pydui import utils
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
    __text_padding: Tuple[float, float, float, float] = (0, 0, 0, 0)

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
            self.set_font(v)
        elif k == "fontsize":
            self.set_fontsize(int(v))
        elif k == "text_padding":
            self.set_textpadding(utils.Str2Rect(v))
        super().parse_attrib(k, v)

    def layout(self, x: float, y: float, width: float, height: float, constraint: PyDuiLayoutConstraint):
        super().layout(x, y, width, height, constraint)
        if self.__gtk_scrolled_window is None:
            return
        self.get_render_manager().move_gtk_widget(self, x + self.__text_padding[0], y + self.__text_padding[1])
        text_padding_w = utils.RectW(self.__text_padding)
        text_padding_h = utils.RectH(self.__text_padding)
        self.__gtk_scrolled_window.set_size_request(max(0, width - text_padding_w), max(0, height - text_padding_h))

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

    def get_font(self) -> str:
        if self.__font == "":
            return self.get_render_manager().default_fontfamily
        return self.__font

    def set_font(self, font: str):
        self.__font = font
        if self.__gtk_text_view is None:
            return
        desc = f"{self.font} {self.fontsize}"
        self.__gtk_text_view.override_font(Pango.font_description_from_string(desc))

    def get_fontsize(self) -> int:
        if self.__fontsize == 0:
            return self.get_render_manager().default_fontsize
        return self.__fontsize

    def set_fontsize(self, fontsize: int):
        self.__fontsize = fontsize
        if self.__gtk_text_view is None:
            return
        desc = f"{self.get_font()} {self.get_fontsize()}"
        self.__gtk_text_view.override_font(Pango.font_description_from_string(desc))

    def set_textpadding(self, text_padding: Tuple[float, float, float, float]):
        self.__text_padding = text_padding
        if self.__gtk_text_view is None:
            return
        self.get_render_manager().notify_redraw()

    def get_textpadding(self) -> Tuple[float, float, float, float]:
        return self.__text_padding

    # private
    def __init_gtk_text_view_if_needed__(self):
        if self.__gtk_scrolled_window is not None:
            return
        self.__gtk_scrolled_window = Gtk.ScrolledWindow()
        self.__gtk_scrolled_window.set_hexpand(True)
        self.__gtk_scrolled_window.set_vexpand(True)

        self.__gtk_text_view = Gtk.TextView()
        desc = f"{self.get_font()} {self.get_fontsize()}"
        self.__gtk_text_view.override_font(Pango.font_description_from_string(desc))
        self.__gtk_text_view.set_editable(self.__editable)
        self.__gtk_text_view.get_buffer().set_text(self.__text)
        self.__gtk_scrolled_window.add(self.__gtk_text_view)
        self.get_render_manager().put_gtk_widget(self)

# -*- coding: utf-8 -*-
from curses import textpad
from signal import signal
from typing import List, Tuple

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
        self.can_focus = True

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
        self.get_window_client().move_gtk_widget(self, x + self.__text_padding[0], y + self.__text_padding[1])
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
            return self.get_window_client().get_appearance().default_fontfamily
        return self.__font

    def set_font(self, font: str):
        self.__font = font
        if self.__gtk_text_view is None:
            return
        desc = f"{self.font} {self.fontsize}"
        self.__gtk_text_view.override_font(Pango.font_description_from_string(desc))

    def get_fontsize(self) -> int:
        if self.__fontsize == 0:
            return self.get_window_client().get_appearance().default_fontsize
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
        self.get_window_client().notify_redraw()

    def get_textpadding(self) -> Tuple[float, float, float, float]:
        return self.__text_padding

    def get_signals(self) -> List[str]:
        signals = super().get_signals()
        signals.extend(
            [
                "changed",
                "insert-text",
                "paste-done",
            ]
        )
        return signals

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
        self.__gtk_text_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.__gtk_text_view.get_buffer().set_text(self.__text)
        self.__gtk_scrolled_window.add(self.__gtk_text_view)
        self.get_window_client().put_gtk_widget(self)

        # register event
        text_buffer = self.__gtk_text_view.get_buffer()
        text_buffer.connect("changed", self.__on_changed__)
        text_buffer.connect("insert-text", self.__on_insert_text__)
        text_buffer.connect("paste-done", self.__on_paste_done__)

    def __on_changed__(self, text_buffer: Gtk.TextBuffer):
        start = text_buffer.get_iter_at_offset(0)
        end = text_buffer.get_iter_at_offset(-1)
        self.__text = text_buffer.get_text(start, end, False)
        self.emit("changed", self.__text)

    def __on_insert_text__(self, text_buffer: Gtk.TextBuffer, location: Gtk.TextIter, text: str, len: int):
        self.emit("insert-text", location.get_offset(), text)

    def __on_paste_done__(self, text_buffer: Gtk.TextBuffer, clipboard: Gtk.Clipboard):
        # print("paste done", clipboard.wait_for_text())
        self.emit("paste-done", clipboard)

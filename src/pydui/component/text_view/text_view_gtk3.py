# -*- coding: utf-8 -*-
"""PyDuiEmbbeddedTextViewGTK3"""
from pydui.common.import_gtk import *
from pydui.component.text_view.text_view_protocol import PyDuiTextViewProtocol
from pydui.provider.embedded_widget_host_gtk3 import PyDuiEmbeddedWidgetHostGTK3


class PyDuiEmbeddedTextViewGTK3(PyDuiEmbeddedWidgetHostGTK3[PyDuiTextViewProtocol], PyDuiTextViewProtocol):
    """PyDuiEmbeddedTextViewGTK3"""

    __gtk_text_view: Gtk.TextView = None
    __gtk_scrolled_window: Gtk.ScrolledWindow = None
    __text_buffer: Gtk.TextBuffer = None

    def __init__(self) -> None:
        super().__init__()

        self.__gtk_scrolled_window = Gtk.ScrolledWindow()
        self.__gtk_scrolled_window.set_hexpand(True)
        self.__gtk_scrolled_window.set_vexpand(True)

        self.__gtk_text_view = Gtk.TextView()
        self.__gtk_text_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.__gtk_scrolled_window.add(self.__gtk_text_view)

        # register event
        self.__text_buffer = self.__gtk_text_view.get_buffer()
        self.__text_buffer.connect("changed", self.__on_changed__)
        self.__text_buffer.connect("insert-text", self.__on_insert_text__)
        self.__text_buffer.connect("paste-done", self.__on_paste_done__)

    # PyDuiEmbeddedWidgetHostGTK3 interface
    def get_gtk_widget(self) -> Gtk.Widget:
        return self.__gtk_scrolled_window

    # PyDuiTextViewProtocol implement
    def set_text(self, text: str):
        self.__text_buffer.set_text(text)

    def get_text(self) -> str:
        start = self.__text_buffer.get_iter_at_offset(0)
        end = self.__text_buffer.get_iter_at_offset(-1)
        return self.__text_buffer.get_text(start, end, False)

    def set_font(self, font: str, fontsize: int):
        desc = f"{font} {fontsize}"
        self.__gtk_text_view.override_font(Pango.font_description_from_string(desc))

    def set_editable(self, editable: bool):
        self.__gtk_text_view.set_editable(editable)

    def get_editable(self) -> bool:
        return self.__gtk_text_view.get_editable()

    def set_size_request(self, width: float, height: float):
        self.__gtk_scrolled_window.set_size_request(width, height)

    def __on_changed__(self, text_buffer: Gtk.TextBuffer):
        start = text_buffer.get_iter_at_offset(0)
        end = text_buffer.get_iter_at_offset(-1)
        # self.__text = text_buffer.get_text(start, end, False)
        # self.emit("changed", self.__text)

    def __on_insert_text__(self, text_buffer: Gtk.TextBuffer, location: Gtk.TextIter, text: str, len: int):
        # self.emit("insert-text", location.get_offset(), text)
        pass

    def __on_paste_done__(self, text_buffer: Gtk.TextBuffer, clipboard: Gtk.Clipboard):
        # print("paste done", clipboard.wait_for_text())
        # self.emit("paste-done", clipboard)
        pass

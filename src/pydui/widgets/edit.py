# -*- coding: utf-8 -*-
from typing import List, Optional

from pydui import utils
from pydui.common.base import PyDuiEdge, PyDuiLayoutConstraint, PyDuiRect
from pydui.common.import_gtk import *
from pydui.component.embedded_widget import PyDuiEmbeddedWidgetHost
from pydui.component.text_view.text_view_protocol import PyDuiTextViewProtocol
from pydui.widgets.pgview import PyDuiPGView


class PyDuiEdit(PyDuiPGView):
    @staticmethod
    def build_name() -> str:
        return "Edit"

    def __init__(self):
        super().__init__()
        self.can_focus = True
        self.__text_padding = PyDuiEdge()

        self.__text_view: Optional[PyDuiEmbeddedWidgetHost[PyDuiTextViewProtocol]] = None
        self.__text: str = ""
        self.__editable: bool = True  # Default is can edit
        self.__font: str = ""
        self.__fontsize: int = 0

    def on_post_init(self):
        pass

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
            self.set_textpadding(utils.Str2Edge(v))
        super().parse_attrib(k, v)

    def draw(self, ctx: cairo.Context, dirty_rect: PyDuiRect, clip_rect: PyDuiRect):
        if self.__text_view is not None:
            viewport = PyDuiRect.from_ltrb(
                clip_rect.left + self.__text_padding.left,
                clip_rect.top + self.__text_padding.top,
                clip_rect.right - self.__text_padding.right,
                clip_rect.bottom - self.__text_padding.bottom,
            )
            self.get_window_client().update_embedded_widget_viewport(self.__text_view, viewport)
        return super().draw(ctx, dirty_rect, clip_rect)

    def layout(self, x: float, y: float, width: float, height: float, constraint: PyDuiLayoutConstraint):
        super().layout(x, y, width, height, constraint)
        if self.__text_view is None:
            self.get_window_client().post_task(self.__init_text_view_if_needed__)
            return
        self.__update_text_view_position_and_size__()

    @property
    def text(self) -> str:
        if self.__text_view is None:
            return self.__text
        return self.__text_view.api.get_text()

    @text.setter
    def text(self, text: str):
        self.__text = text
        if self.__text_view is None:
            return
        self.__text_view.api.set_text(text)

    @property
    def editable(self) -> bool:
        if self.__text_view is None:
            return self.__editable
        return self.__text_view.api.get_editable()

    @editable.setter
    def editable(self, editable: bool):
        self.__editable = editable
        if self.__text_view is None:
            return
        self.__text_view.api.set_editable(self.__editable)

    def get_font(self) -> str:
        if self.__font == "":
            return self.get_window_client().get_appearance().default_fontfamily
        return self.__font

    def set_font(self, font: str):
        self.__font = font
        if self.__text_view is None:
            return
        self.__text_view.api.set_font(self.get_font(), self.get_fontsize())

    def get_fontsize(self) -> int:
        if self.__fontsize == 0:
            return self.get_window_client().get_appearance().default_fontsize
        return self.__fontsize

    def set_fontsize(self, fontsize: int):
        self.__fontsize = fontsize
        if self.__text_view is None:
            return
        self.__text_view.api.set_font(self.get_font(), self.get_fontsize())

    def set_textpadding(self, text_padding: PyDuiEdge):
        self.__text_padding = text_padding
        if self.__text_view is None:
            return
        self.poga_layout().mark_dirty()
        self.get_window_client().notify_redraw()

    def get_textpadding(self) -> PyDuiEdge:
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
    def __init_text_view_if_needed__(self, task_id: str):
        client = self.get_window_client()
        if client is None:
            return
        if self.__text_view is not None:
            return

        self.__text_view = client.create_embedded_widget("TextView")
        client.add_embedded_widget(self.__text_view)
        # init attributes
        self.__text_view.api.set_text(self.__text)
        self.__text_view.api.set_editable(self.__editable)
        self.__text_view.api.set_font(self.get_font(), self.get_fontsize())
        client.get_window_provider().show()
        self.__update_text_view_position_and_size__()

    def __update_text_view_position_and_size__(self):
        if self.__text_view is None:
            return

        text_padding_w = self.__text_padding.width
        text_padding_h = self.__text_padding.height
        self.get_window_client().update_embedded_widget_position(
            self.__text_view, self.root_x + self.__text_padding.left, self.root_y + self.__text_padding.top
        )
        self.__text_view.api.set_size_request(max(0, self.width - text_padding_w), max(0, self.height - text_padding_h))

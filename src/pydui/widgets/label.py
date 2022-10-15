# -*- coding: utf-8 -*-
from typing import Tuple

from pydui import utils
from pydui.common.base import *
from pydui.common.import_gtk import *
from pydui.core.layout import *
from pydui.core.render import PyDuiRender
from pydui.core.widget import *
from pydui.widgets.pgview import PyDuiPGView


class PyDuiLabel(PyDuiPGView):

    """Label widget

    Attributes:
        font (str): font family name
        fontsize (int): fontsize in pt unit
        fontcolor (Gdk.RGBA): font color
        ellipsis (str): ellipsis mode, [NONE, START, MIDDLE, END], default is END
        wrap (str): wrap mode, [NONE, WORD, CHAR, WORD_CHAR], default is WORD
        halign (str): horizontal TextAlign, [CENTER, STAET, END], default is CENTER
        valign (str): vertical TextAlign, [CENTER, STAET, END], default is CENTER
        line_spacing (float): line spacing
        autofit (bool): text is autofit or not
        autofit_padding (Rect): when autofit is set, autofit area padding
        text_padding (Rect): text padding
    """

    __text: str = ""
    __font: str = ""
    __fontsize: int = None
    __fontcolor: Gdk.RGBA = None

    __ellipsize_mode: str = "END"
    __wrap_mode: str = "WORD_CHAR"
    __halign: str = "CENTER"
    __valign: str = "CENTER"
    __line_spacing: float = 1.25
    __autofit_padding: PyDuiEdge = None
    __text_padding: PyDuiEdge = None

    @staticmethod
    def build_name() -> str:
        return "Label"

    def __init__(self):
        super().__init__()
        self.__autofit_padding = PyDuiEdge()
        self.__text_padding = PyDuiEdge()

    def parse_attrib(self, k: str, v: str):
        if k == "text":
            self.__text = v
        elif k == "fontcolor":
            self.__fontcolor = utils.Str2Color(v)
        elif k == "fontsize":
            self.__fontsize = int(v)
        elif k == "font":
            self.__font = v
        elif k == "wrap":
            self.__wrap_mode = v
        elif k == "ellipsis":
            self.__ellipsize_mode = v
        elif k == "halign":
            self.__halign = v
        elif k == "valign":
            self.__valign = v
        elif k == "line_spacing":
            self.__line_spacing = float(v)
        elif k == "autofit_padding":
            self.__autofit_padding = utils.Str2Edge(v)
        elif k == "text_padding":
            self.__text_padding = utils.Str2Edge(v)

        super().parse_attrib(k, v)

    def estimate_size(
        self, parent_width: float, parent_height: float, constraint: PyDuiLayoutConstraint
    ) -> Tuple[float, float]:
        if self.autofit:
            size = (0, 0)
            pw, ph = parent_width, parent_height
            pw = max(0, pw - self.__autofit_padding.width)
            ph = max(0, ph - self.__autofit_padding.height)
            if len(self.text) > 0:
                pw = max(0, pw - self.__text_padding.width)
                ph = max(0, ph - self.__text_padding.height)
                if constraint.width == -1:
                    pw = -1
                if constraint.height == -1:
                    ph = -1
                size = self.__estimate_text_size__(pw, ph)
                size = (size[0] + self.__text_padding.width, size[1] + self.__text_padding.height)
            elif len(self.bkimage) > 0:
                if constraint.width == -1:
                    pw = -1
                if constraint.height == -1:
                    ph = -1
                size = self.__estimate_image_size__(pw, ph)
            if size[0] > 0 and size[1] > 0:
                size = (
                    size[0] + self.__autofit_padding.width,
                    size[1] + self.__autofit_padding.height,
                )
                return size
            return super().estimate_size(parent_width, parent_height, constraint)
        return super().estimate_size(parent_width, parent_height, constraint)

    def draw_text(self, ctx: cairo.Context, dirty_rect: PyDuiRect, clip_rect: PyDuiRect):
        draw_x = 0
        draw_y = 0
        draw_width = self.width
        draw_height = self.height

        fontfamily, fontsize, fontcolor = self.__get_font_info__()

        draw_xy = (draw_x + self.__text_padding.left, draw_y + self.__text_padding.top)
        draw_wh = (draw_width - self.__text_padding.width, draw_height - self.__text_padding.height)
        if self.autofit:
            draw_xy = (draw_x + self.__autofit_padding.left, draw_y + self.__autofit_padding.top)
            draw_wh = (draw_width - self.__autofit_padding.width, draw_height - self.__autofit_padding.height)
        draw_wh = (max(0, draw_wh[0]), max(0, draw_wh[1]))
        if draw_wh[0] == 0 or draw_wh[1] == 0:
            return

        # draw text
        PyDuiRender.DrawText(
            ctx,
            text=self.text,
            font=fontfamily,
            font_size=fontsize,
            color=fontcolor,
            xy=draw_xy,
            wh=draw_wh,
            hvalign=(Text2PyDuiAlign(self.__halign), Text2PyDuiAlign(self.__valign)),
            ellipsis_mode=Text2EllipsizeMode(self.__ellipsize_mode),
            wrap_mode=Text2WrapMode(self.__wrap_mode),
            line_spacing=self.__line_spacing,
        )

    def draw(self, ctx: cairo.Context, dirty_rect: PyDuiRect, clip_rect: PyDuiRect):
        # draw bkcolor
        super().draw(ctx, dirty_rect, clip_rect)
        # families = PangoCairo.font_map_get_default().list_families()
        # for f in families:
        #     print(f.get_name())

        # draw text
        self.draw_text(ctx, dirty_rect, clip_rect)

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text

    def __get_font_info__(self) -> Tuple[str, int, str]:
        window_client = self.get_window_client()
        fontfamily = self.__font
        if fontfamily is None or fontfamily == "":
            fontfamily = window_client.get_appearance().default_fontfamily

        fontsize = self.__fontsize
        if fontsize is None:
            fontsize = window_client.get_appearance().default_fontsize

        fontcolor = self.__fontcolor
        if fontcolor is None:
            fontcolor = window_client.get_appearance().default_fontcolor
        return (fontfamily, fontsize, fontcolor)

    def __estimate_text_size__(self, limit_width: float, limit_height: float) -> Tuple[float, float]:
        fontfamily, fontsize, fontcolor = self.__get_font_info__()
        ctx = self.get_window_client().get_render_context()
        return PyDuiRender.EstimateTextSize(
            ctx,
            text=self.text,
            font=fontfamily,
            fontsize=fontsize,
            limit_wh=(limit_width, limit_height),
            hvalign=(Text2PyDuiAlign(self.__halign), Text2PyDuiAlign(self.__valign)),
            ellipsis_mode=Text2EllipsizeMode(self.__ellipsize_mode),
            wrap_mode=Text2WrapMode(self.__wrap_mode),
            line_spacing=self.__line_spacing,
        )

    def __estimate_image_size__(self, limit_width: float, limit_height: float) -> Tuple[float, float]:
        loader = self.get_window_client().get_resource_loader()

        return PyDuiRender.EstimateImageSize(loader, self.bkimage, limit_width, limit_height)

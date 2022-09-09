# -*- coding: utf-8 -*-
from typing import Tuple

from pydui import utils
from pydui.core.base import *
from pydui.core.import_gtk import *
from pydui.core.layout import *
from pydui.core.render import PyDuiRender
from pydui.core.widget import *


class PyDuiLabel(PyDuiWidget):

    """Label widget

    Attributes:
        text (str): text content
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
    __wrap_mode: str = "WORD"
    __halign: str = "CENTER"
    __valign: str = "CENTER"
    __line_spacing: float = 1.25
    __autofit_padding: Tuple[float, float, float, float] = (0, 0, 0, 0)
    __text_padding: Tuple[float, float, float, float] = (0, 0, 0, 0)

    @staticmethod
    def build_name() -> str:
        return "Label"

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)

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
            self.__autofit_padding = utils.Str2Rect(v)
        elif k == "text_padding":
            self.__text_padding = utils.Str2Rect(v)

        super().parse_attrib(k, v)

    def estimate_size(
        self, parent_width: float, parent_height: float, constraint: PyDuiLayoutConstraint
    ) -> tuple[float, float]:
        if self.autofit:
            size = (0, 0)
            pw, ph = parent_width, parent_height
            pw = max(0, pw - utils.RectW(self.__autofit_padding))
            ph = max(0, ph - utils.RectH(self.__autofit_padding))
            if len(self.text) > 0:
                pw = max(0, pw - utils.RectW(self.__text_padding))
                ph = max(0, ph - utils.RectH(self.__text_padding))
                if constraint.width == -1:
                    pw = -1
                if constraint.height == -1:
                    ph = -1
                size = self.__estimate_text_size__(pw, ph)
                size = (size[0] + utils.RectW(self.__text_padding), size[1] + utils.RectH(self.__text_padding))
            elif len(self.bkimage) > 0:
                if constraint.width == -1:
                    pw = -1
                if constraint.height == -1:
                    ph = -1
                size = self.__estimate_image_size__(pw, ph)
            if size[0] > 0 and size[1] > 0:
                size = (
                    size[0] + utils.RectW(self.__autofit_padding),  # + utils.RectW(self.margin),
                    size[1] + utils.RectH(self.__autofit_padding),  # + utils.RectH(self.margin),
                )
                return size
            return super().estimate_size(parent_width, parent_height, constraint)
        return super().estimate_size(parent_width, parent_height, constraint)

    def draw_text(
        self,
        ctx: cairo.Context,
        x: float,
        y: float,
        width: float,
        height: float,
    ):
        fontfamily, fontsize, fontcolor = self.__get_font_info__()

        draw_xy = (x + self.__text_padding[0], y + self.__text_padding[1])
        draw_wh = (width - utils.RectW(self.__text_padding), height - utils.RectH(self.__text_padding))
        if self.autofit:
            draw_xy = (x + self.__autofit_padding[0], y + self.__autofit_padding[1])
            draw_wh = (width - utils.RectW(self.__autofit_padding), height - utils.RectH(self.__autofit_padding))
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

    def draw(
        self,
        ctx: cairo.Context,
        x: float,
        y: float,
        width: float,
        height: float,
    ):
        # draw bkcolor
        super().draw(ctx, x, y, width, height)
        # families = PangoCairo.font_map_get_default().list_families()
        # for f in families:
        #     print(f.get_name())

        # draw text
        self.draw_text(ctx, x, y, width, height)

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text

    def __get_font_info__(self) -> Tuple[str, int, str]:
        render_manager = self.get_render_manager()
        fontfamily = self.__font
        if fontfamily is None or fontfamily == "":
            fontfamily = render_manager.default_fontfamily

        fontsize = self.__fontsize
        if fontsize is None:
            fontsize = render_manager.default_fontsize

        fontcolor = self.__fontcolor
        if fontcolor is None:
            fontcolor = render_manager.default_fontcolor
        return (fontfamily, fontsize, fontcolor)

    def __estimate_text_size__(self, parent_width: float, parent_height: float) -> tuple[float, float]:
        fontfamily, fontsize, fontcolor = self.__get_font_info__()
        ctx = self.get_render_manager().get_render_context()
        return PyDuiRender.EstimateTextSize(
            ctx,
            text=self.text,
            font=fontfamily,
            fontsize=fontsize,
            limit_wh=(parent_width, parent_height),
            hvalign=(Text2PyDuiAlign(self.__halign), Text2PyDuiAlign(self.__valign)),
            ellipsis_mode=Text2EllipsizeMode(self.__ellipsize_mode),
            wrap_mode=Text2WrapMode(self.__wrap_mode),
            line_spacing=self.__line_spacing,
        )

    def __estimate_image_size__(self, parent_width: float, parent_height: float) -> tuple[float, float]:
        loader = self.get_render_manager().get_resource_loader()

        return PyDuiRender.EstimateImageSize(loader, self.bkimage, parent_width, parent_height)

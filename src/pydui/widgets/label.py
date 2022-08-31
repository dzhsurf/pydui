from dataclasses import dataclass
from typing import Type

import cairo
import gi

gi.require_version("Gdk", "3.0")

from gi.repository import Gdk

from pydui.core import utils
from pydui.core.base import *
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

    __bkimage: str = ""

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)

    def parse_attrib(self, k: str, v: str):
        handled = True
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
        elif k == "bkimage":
            self.__bkimage = v
        else:
            super().parse_attrib(k, v)
            handled = False
        if handled:
            print(f"{self} parse {k} {v}")

    def draw_bkimage(
        self,
        ctx: cairo.Context,
        x: float,
        y: float,
        width: float,
        height: float,
        canvas_width: float,
        canvas_height: float,
    ):
        PyDuiRender.DrawImage(
            ctx,
            image=self.__bkimage,
            xy=(x, y),
            wh=(width, height),
        )

    def draw_text(
        self,
        ctx: cairo.Context,
        x: float,
        y: float,
        width: float,
        height: float,
        canvas_width: float,
        canvas_height: float,
    ):
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

        # draw text
        PyDuiRender.DrawText(
            ctx,
            text=self.__text,
            font=fontfamily,
            font_size=fontsize,
            color=fontcolor,
            xy=(x, y),
            wh=(width, height),
            hvalign=(Text2TextAlign(self.__halign), Text2TextAlign(self.__valign)),
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
        canvas_width: float,
        canvas_height: float,
    ):
        # draw bkcolor
        super().draw(ctx, x, y, width, height, canvas_width, canvas_height)

        # draw bkimage
        self.draw_bkimage(ctx, x, y, width, height, canvas_width, canvas_height)

        # families = PangoCairo.font_map_get_default().list_families()
        # for f in families:
        #     print(f.get_name())

        # draw text
        self.draw_text(ctx, x, y, width, height, canvas_width, canvas_height)

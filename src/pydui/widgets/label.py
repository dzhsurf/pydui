from dataclasses import dataclass
from typing import Optional, Type

import cairo
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")

from gi.repository import Gdk, GdkPixbuf, Gtk, Pango, PangoCairo

from pydui.core import utils
from pydui.core.layout import *
from pydui.core.render import PyDuiRender
from pydui.core.widget import *


class PyDuiLabel(PyDuiWidget):

    """Label widget"""

    __text: str = ""

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)

    def parse_attrib(self, k: str, v: str):
        print(f"{self} parse {k} {v}")
        if k == "text":
            self.__text = v
        else:
            super().parse_attrib(k, v)

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
        super().draw(ctx, x, y, width, height, canvas_width, canvas_height)

        # families = PangoCairo.font_map_get_default().list_families()
        # for f in families:
        #     print(f.get_name())

        PyDuiRender.DrawText(
            ctx,
            text=self.__text,
            font="Helvetica",
            font_size=13,
            color=utils.Str2Color("#FF000000"),
            x=x,
            y=y,
            w=width,
            h=height,
        )

# window.py
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional, Type

import cairo
import gi

from pydui.core.layout import *
from pydui.core.render_canvas import *
from pydui.core.widget import *

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Gdk, GdkPixbuf, Gtk, Pango, PangoCairo


class PyDuiRender:
    """Render static function"""

    @staticmethod
    def Rectangle(
        ctx: cairo.Context,
        color: Gdk.RBGA,
        x: float,
        y: float,
        w: float,
        h: float,
        canvas_width: float,
        canvas_height: float,
    ):
        ctx.save()
        ctx.rectangle(x / canvas_width, y / canvas_height, w / canvas_width, h / canvas_height)
        ctx.set_source_rgba(*color)
        ctx.fill()
        ctx.restore()

    @staticmethod
    def DrawText(
        ctx: cairo.Context,
        text: str,
        font: str,
        font_size: int,
        color: Gdk.RBGA,
        x: float,
        y: float,
        w: float,
        h: float,
    ):
        # save ctx
        ctx.save()
        # draw text
        ctx.move_to(x, y)
        ctx.set_source_rgba(*color)
        # ctx.set_operator(cairo.OPERATOR_OVER)
        # ctx.set_antialias(cairo.Antialias.SUBPIXEL)
        # status, attrs, plain_text, _ = Pango.parse_markup(text, len(text), '\0')
        layout = PangoCairo.create_layout(ctx)
        layout.set_text(text, -1)
        fo = cairo.FontOptions()
        fo.set_antialias(cairo.ANTIALIAS_GRAY)  # ANTIALIAS_SUBPIXEL ANTIALIAS_GRAY
        fo.set_hint_style(cairo.HINT_STYLE_FULL)
        # PangoCairo.context_set_resolution(layout.get_context(), 200)
        PangoCairo.context_set_font_options(layout.get_context(), fo)
        # ctx.set_font_options(fo)
        # ctx.get_source().set_filter(cairo.FILTER_GOOD)
        # ctx.scale(0.5, 0.5)
        # print(dir(PangoCairo))

        font_desc = Pango.font_description_from_string(f"{font} {round(font_size / 1.3333343412075)}")
        layout.set_font_description(font_desc)
        # layout.set_spacing(5)
        # layout.set_attributes(attrs)
        PangoCairo.update_layout(ctx, layout)
        PangoCairo.show_layout(ctx, layout)

        # fo = cairo.FontOptions()
        # fo.set_antialias(cairo.ANTIALIAS_SUBPIXEL) # ANTIALIAS_SUBPIXEL
        # ctx.set_font_options(fo)
        # ctx.set_source_rgb(0.1, 0.1, 0.1)
        # ctx.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        # ctx.set_font_size(13)
        # ctx.move_to(20, 30)
        # ctx.show_text("Most relationships seem so transitory")

        # restore ctx
        ctx.restore()

    @staticmethod
    def EstimateText(
        ctx: cairo.Context,
        text: str,
        font_desc: str,
        limit_width: float = None,
        limit_height: float = None,
    ) -> tuple[float, float]:
        """Estimate text size"""
        ctx.save()
        layout = PangoCairo.create_layout(ctx)
        font_desc = Pango.font_description_from_string(font_desc)
        layout.set_font_description(font_desc)
        layout.set_text(text, -1)
        PangoCairo.update_layout(ctx, layout)
        w, h = layout.get_size()
        ctx.restore()
        return (w.Pango.SCALE, h / Pango.SCALE)


class PyDuiRenderManager(object):

    """Render manager"""

    __canvas: PyDuiRenderCanvas
    __rootview: PyDuiLayout
    __default_font_family: str = "Arial"
    __default_font_size: int = 16
    __default_font_color: Gdk.RGBA = Gdk.RGBA(0.0, 0.0, 0.0, 1.0)

    # manager all widget
    def __init__(self, window: PyDuiWindow):
        self.__window = window
        self.__canvas = PyDuiRenderCanvas(self.__on_draw__)
        self.__rootview = None

        gtk_window = self.__window.get_gtk_window()
        gtk_window.add(self.__canvas)

    @property
    def default_font_color(self) -> Gdk.RGBA:
        """return default font color, default is Gdk.RGBA(0.0, 0.0, 0.0, 1.0)

        Returns:
            Gdk.RGBA: return default font color
        """
        return self.__default_font_color

    @default_font_color.setter
    def default_font_color(self, font_color: Gdk.RGBA):
        """set default font color

        Args:
            font_color (Gdk.RGBA): font color
        """
        self.__default_font_color = font_color

    @property
    def default_font_desc(self) -> str:
        """return font desc in format f"{font_family} {font_size}"

        Returns:
            str: font desc
        """
        return f"{self.default_font_family} {self.default_font_size}"

    @property
    def default_font_family(self) -> str:
        """return default font family, default is Arial

        Returns:
            str: font family
        """
        return self.__default_font_family

    @default_font_family.setter
    def default_font_family(self, font_family: str):
        """set fefault font family

        Args:
            font_family (str): font family
        """
        self.__default_font_family = font_family

    @property
    def default_font_size(self) -> int:
        """return default font size, default is 16

        Returns:
            int: font size
        """
        return self.__default_font_size

    @default_font_size.setter
    def default_font_size(self, font_size: int):
        """set fefault font size

        Args:
            font_size (int): font size
        """
        self.__default_font_size = font_size

    def set_rootview(self, rootview: PyDuiLayout):
        """set window root view

        Args:
            rootview (PyDuiWidget): widnow root view
        """
        self.__rootview = rootview

    def get_widget(self, widget_id: str) -> Optional[PyDuiWidget]:
        """Get widget by widget id

        Args:
            widget_id (str): widget id
        """
        return self.__rootview.get_child(widget_id)

    def __on_draw__(self, ctx: cairo.Context, width: float, height: float):
        if self.__rootview is None:
            return
        self.__rootview.layout(0, 0, width, height)
        self.__rootview.draw(ctx, 0, 0, width, height, width, height)

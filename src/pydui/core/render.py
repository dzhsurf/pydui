# window.py
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional, Type

import cairo
import gi

from pydui.core.base import *
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
        xy: tuple[float, float],
        wh: tuple[float, float],
        hvalign: tuple[PyDuiTextAlign, PyDuiTextAlign] = (PyDuiTextAlign.CENTER, PyDuiTextAlign.CENTER),
        ellipsis_mode: Pango.EllipsizeMode = Pango.EllipsizeMode.END,
        wrap_mode: Pango.WrapMode = Pango.WrapMode.WORD,
        line_spacing: float = 0.0,
    ):
        x, y = xy
        w, h = wh
        # save ctx
        ctx.save()
        # draw text
        ctx.set_source_rgba(*color)
        # ctx.set_operator(cairo.OPERATOR_OVER)
        # ctx.set_antialias(cairo.Antialias.SUBPIXEL)
        # status, attrs, plain_text, _ = Pango.parse_markup(text, len(text), '\0')
        layout = PangoCairo.create_layout(ctx)
        layout.set_text(text, -1)
        fo = cairo.FontOptions()
        fo.set_antialias(cairo.ANTIALIAS_GRAY)  # ANTIALIAS_SUBPIXEL ANTIALIAS_GRAY
        fo.set_hint_style(cairo.HINT_STYLE_FULL)  # HINT_STYLE_SLIGHT HINT_STYLE_FULL
        fo.set_hint_metrics(cairo.HINT_METRICS_DEFAULT)  # HINT_METRICS_ON
        # PangoCairo.context_set_resolution(layout.get_context(), 96 * 2)
        PangoCairo.context_set_font_options(layout.get_context(), fo)

        font_desc = Pango.font_description_from_string(f"{font} {round(font_size / 1.3333343412075)}")
        layout.set_font_description(font_desc)
        layout.set_line_spacing(line_spacing)

        layout.set_ellipsize(ellipsis_mode)
        if ellipsis_mode != Pango.EllipsizeMode.NONE:
            layout.set_height(int(h * Pango.SCALE))
        else:
            layout.set_height(-1)

        layout.set_width(int(w * Pango.SCALE))
        if wrap_mode is None:
            if ellipsis_mode == Pango.EllipsizeMode.NONE:
                layout.set_width(-1)
            else:
                # set layout height to single line text height
                layout.set_height(font_desc.get_size())
        else:
            layout.set_wrap(wrap_mode)

        # layout.set_spacing(5 * Pango.SCALE)
        # layout.set_attributes(attrs)
        PangoCairo.update_layout(ctx, layout)

        # calulate text align
        layout_w, layout_h = layout.get_size()
        layout_w, layout_h = layout_w / Pango.SCALE, layout_h / Pango.SCALE
        if hvalign[0] == PyDuiTextAlign.CENTER:
            x = x + round((w - layout_w) / 2)
        elif hvalign[0] == PyDuiTextAlign.END:
            x = x + round(w - layout_w)
        if hvalign[1] == PyDuiTextAlign.CENTER:
            y = y + round((h - layout_h) / 2)
        elif hvalign[1] == PyDuiTextAlign.END:
            y = y + round(h - layout_h)
        ctx.move_to(x, y)
        PangoCairo.show_layout(ctx, layout)

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
    __default_fontfamily: str = "Arial"
    __default_fontsize: int = 16
    __default_fontcolor: Gdk.RGBA = Gdk.RGBA(0.0, 0.0, 0.0, 1.0)

    # manager all widget
    def __init__(self, window: PyDuiWindow):
        self.__window = window
        self.__canvas = PyDuiRenderCanvas(self.__on_draw__)
        self.__rootview = None

        gtk_window = self.__window.get_gtk_window()
        gtk_window.add(self.__canvas)

    @property
    def default_fontcolor(self) -> Gdk.RGBA:
        """return default font color, default is Gdk.RGBA(0.0, 0.0, 0.0, 1.0)

        Returns:
            Gdk.RGBA: return default font color
        """
        return self.__default_fontcolor

    @default_fontcolor.setter
    def default_fontcolor(self, fontcolor: Gdk.RGBA):
        """set default font color

        Args:
            font_color (Gdk.RGBA): font color
        """
        self.__default_fontcolor = fontcolor

    @property
    def default_font_desc(self) -> str:
        """return font desc in format f"{font_family} {font_size}"

        Returns:
            str: font desc
        """
        return f"{self.default_fontfamily} {self.default_fontsize}"

    @property
    def default_fontfamily(self) -> str:
        """return default font family, default is Arial

        Returns:
            str: font family
        """
        return self.__default_fontfamily

    @default_fontfamily.setter
    def default_fontfamily(self, font_family: str):
        """set fefault font family

        Args:
            font_family (str): font family
        """
        self.__default_fontfamily = font_family

    @property
    def default_fontsize(self) -> int:
        """return default font size, default is 16

        Returns:
            int: font size
        """
        return self.__default_fontsize

    @default_fontsize.setter
    def default_fontsize(self, font_size: int):
        """set fefault font size

        Args:
            font_size (int): font size
        """
        self.__default_fontsize = font_size

    def set_rootview(self, rootview: PyDuiLayout):
        """set window root view

        Args:
            rootview (PyDuiWidget): widnow root view
        """
        self.__rootview = rootview
        rootview.set_render_manager(self)

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

# -*- coding: utf-8 -*-
import logging
import math
import pathlib
from typing import Tuple

from pydui import utils
from pydui.common.attribute_string import PyDuiAttrStrParser
from pydui.common.base import *
from pydui.common.import_gtk import *
from pydui.core.layout import *
from pydui.core.render_canvas import *
from pydui.core.resource_loader import PyDuiResourceLoader
from pydui.core.widget import *


def __pt2px__(pt: float) -> int:
    return math.ceil(pt * 1.3333343412075)


def __px2pt__(px: int) -> float:
    return math.ceil(px / 1.3333343412075)


__is_initial__: bool = False
__display_max_width__: int = 0
__display_max_height__: int = 0

RENDER_MAX_LINE = 9999


def __get_display_maxsize__() -> Tuple[int, int]:
    global __display_max_width__, __display_max_height__, __is_initial__
    if __is_initial__:
        return (__display_max_width__, __display_max_height__)
    __is_initial__ = True
    monitors = Gdk.Screen.get_default().get_n_monitors()
    for i in range(monitors):
        # resolution = Gdk.Screen.get_default().get_resolution()
        factor = Gdk.Screen.get_default().get_monitor_scale_factor(i)
        rect = Gdk.Screen.get_default().get_monitor_geometry(i)
        __display_max_width__ = max(__display_max_width__, rect.width * factor)
        __display_max_height__ = max(__display_max_height__, rect.height * factor)
    return (__display_max_width__, __display_max_height__)


def __config_text_layout__(
    layout: Pango.Layout,
    *,
    font: str,
    font_size: int,
    wh: Tuple[float, float],
    hvalign: Tuple[PyDuiAlign, PyDuiAlign] = (PyDuiAlign.CENTER, PyDuiAlign.CENTER),
    ellipsis_mode: Pango.EllipsizeMode = Pango.EllipsizeMode.END,
    wrap_mode: Pango.WrapMode = Pango.WrapMode.WORD,
    line_spacing: float = 1.25,
) -> float:
    w, h = wh
    fo = cairo.FontOptions()
    fo.set_antialias(cairo.ANTIALIAS_GRAY)  # ANTIALIAS_SUBPIXEL ANTIALIAS_GRAY
    fo.set_hint_style(cairo.HINT_STYLE_FULL)  # HINT_STYLE_SLIGHT HINT_STYLE_FULL
    fo.set_hint_metrics(cairo.HINT_METRICS_DEFAULT)  # HINT_METRICS_ON
    PangoCairo.context_set_resolution(layout.get_context(), 96)
    PangoCairo.context_set_font_options(layout.get_context(), fo)

    font_desc = Pango.font_description_from_string(f"{font} {__px2pt__(font_size)}")
    layout.set_font_description(font_desc)
    if line_spacing < 1:
        line_spacing = 1
    layout.set_line_spacing(line_spacing)
    line_height = __pt2px__(font_desc.get_size()) * line_spacing

    layout.set_ellipsize(ellipsis_mode)
    if ellipsis_mode != Pango.EllipsizeMode.NONE and h != -1:
        max_line = math.ceil(h * Pango.SCALE / line_height)
        layout.set_height(math.ceil(max_line * line_height))
    else:
        layout.set_height(-RENDER_MAX_LINE)

    if w == -1:
        layout.set_width(-1)
    else:
        layout.set_width(int(w * Pango.SCALE))
    if wrap_mode is None:
        if ellipsis_mode == Pango.EllipsizeMode.NONE:
            layout.set_width(-1)
        else:
            # set layout height to single line text height
            layout.set_height(line_height)
    else:
        layout.set_wrap(wrap_mode)
        # layout.set_spacing(5 * Pango.SCALE)
        # layout.set_attributes(attrs)
    return line_height / Pango.SCALE


class PyDuiRender:
    """Render static function"""

    @staticmethod
    def Rectangle(
        ctx: cairo.Context,
        color: Gdk.RGBA,
        x: float,
        y: float,
        w: float,
        h: float,
    ):
        ctx.save()
        ctx.rectangle(x, y, w, h)
        ctx.set_source_rgba(*color)
        ctx.fill()
        ctx.restore()

    @staticmethod
    def EstimateImageSize(
        loader: PyDuiResourceLoader,
        path: str,
        limit_width: float,
        limit_height: float,
    ) -> Tuple[float, float]:
        img_path = path
        img_attrib = dict[str, Any]()
        if PyDuiAttrStrParser.is_attrstr(img_path):
            img_attrib = PyDuiAttrStrParser.parse(img_path)
            if "file" in img_attrib:
                img_path = img_attrib["file"]

        buf, factor = loader.load_image(img_path)
        if len(buf) == 0:
            logging.error("load image fail. buf is empty. path = {img_path}")
            return (0, 0)
        ext_name = pathlib.Path(img_path).suffix.lstrip(".")
        pixbuf_loader = GdkPixbuf.PixbufLoader.new_with_type(ext_name)
        pixbuf_loader.write(buf)
        pixbuf_loader.close()
        pixbuf = pixbuf_loader.get_pixbuf()
        im_w, im_h = pixbuf.get_width(), pixbuf.get_height()
        return (im_w / factor, im_h / factor)

    @staticmethod
    def DrawImage(
        ctx: cairo.Context,
        loader: PyDuiResourceLoader,
        path: str,
        xy: Tuple[float, float],
        wh: Tuple[float, float],
        corner: PyDuiEdge = PyDuiEdge(),
    ):
        img_path = path
        img_attrib = dict[str, Any]()
        opacity = 100
        if PyDuiAttrStrParser.is_attrstr(img_path):
            img_attrib = PyDuiAttrStrParser.parse(img_path)
            if "file" in img_attrib:
                img_path = img_attrib["file"]
            if "opacity" in img_attrib:
                opacity = int(img_attrib["opacity"])
        # TODO: ResourceLoader, Render, RenderCanvas should have a device-dpi manager
        # that it can easier to get access the dpi scale factor.
        buf, factor = loader.load_image(img_path)
        if len(buf) == 0:
            logging.error(f"buf is empty. path = {img_path} loader = {loader}")
            return

        ctx.save()
        ctx.scale(1.0 / factor, 1.0 / factor)

        ext_name = pathlib.Path(img_path).suffix.lstrip(".")
        pixbuf_loader = GdkPixbuf.PixbufLoader.new_with_type(ext_name)
        pixbuf_loader.write(buf)
        pixbuf_loader.close()
        pixbuf = pixbuf_loader.get_pixbuf()
        im_w, im_h = pixbuf.get_width(), pixbuf.get_height()
        x, y = xy[0] * factor, xy[1] * factor
        w, h = wh[0] * factor, wh[1] * factor
        pixed_corner = corner.copy_with_factor(factor)
        if pixed_corner.left < 0 or pixed_corner.left > im_w or pixed_corner.right < 0 or pixed_corner.right > im_w:
            pixed_corner = PyDuiEdge.from_ltrb(int(im_w / 2), pixed_corner.top, int(im_w / 2), pixed_corner.bottom)
        if pixed_corner.top < 0 or pixed_corner.top > im_w or pixed_corner.bottom < 0 or pixed_corner.bottom > im_w:
            pixed_corner = PyDuiEdge.from_ltrb(pixed_corner.left, int(im_h / 2), pixed_corner.right, int(im_h / 2))

        has_corner = not corner.is_empty()
        if has_corner:
            middle_w = max(0, w - pixed_corner.width)
            middle_h = max(0, h - pixed_corner.height)
            # left top
            pix = pixbuf.new_subpixbuf(0, 0, pixed_corner.left, pixed_corner.top)
            Gdk.cairo_set_source_pixbuf(ctx, pix, x, y)
            ctx.paint()
            # right top
            pix = pixbuf.new_subpixbuf(im_w - pixed_corner.right, 0, pixed_corner.right, pixed_corner.top)
            Gdk.cairo_set_source_pixbuf(ctx, pix, x + w - pixed_corner.right, y)
            ctx.paint()
            if middle_w > 0:
                # middle top
                pix = pixbuf.new_subpixbuf(pixed_corner.left, 0, im_w - pixed_corner.width, pixed_corner.top)
                pix = pix.scale_simple(middle_w, pixed_corner.top, GdkPixbuf.InterpType.NEAREST)
                Gdk.cairo_set_source_pixbuf(ctx, pix, x + pixed_corner.left, y)
                ctx.paint()
            if middle_w > 0 and middle_h > 0:
                # left middle
                pix = pixbuf.new_subpixbuf(0, pixed_corner.top, pixed_corner.left, im_h - pixed_corner.height)
                pix = pix.scale_simple(pixed_corner.left, middle_h, GdkPixbuf.InterpType.NEAREST)
                Gdk.cairo_set_source_pixbuf(ctx, pix, x, y + pixed_corner.top)
                ctx.paint()
                # middle middle
                pix = pixbuf.new_subpixbuf(
                    pixed_corner.left,
                    pixed_corner.top,
                    im_w - pixed_corner.width,
                    im_h - pixed_corner.height,
                )
                pix = pix.scale_simple(middle_w, middle_h, GdkPixbuf.InterpType.NEAREST)
                Gdk.cairo_set_source_pixbuf(ctx, pix, x + pixed_corner.left, y + pixed_corner.top)
                ctx.paint()
                # right middle
                pix = pixbuf.new_subpixbuf(
                    im_w - pixed_corner.right, pixed_corner.top, pixed_corner.right, im_h - pixed_corner.height
                )
                pix = pix.scale_simple(pixed_corner.right, middle_h, GdkPixbuf.InterpType.NEAREST)
                Gdk.cairo_set_source_pixbuf(ctx, pix, x + w - pixed_corner.right, y + pixed_corner.top)
                ctx.paint()
            # left bottom
            pix = pixbuf.new_subpixbuf(0, im_h - pixed_corner.bottom, pixed_corner.left, pixed_corner.bottom)
            Gdk.cairo_set_source_pixbuf(ctx, pix, x, y + h - pixed_corner.bottom)
            ctx.paint()
            if middle_w > 0:
                # middle bottom
                pix = pixbuf.new_subpixbuf(
                    pixed_corner.left, im_h - pixed_corner.bottom, im_w - pixed_corner.width, pixed_corner.bottom
                )
                pix = pix.scale_simple(middle_w, pixed_corner.bottom, GdkPixbuf.InterpType.NEAREST)
                Gdk.cairo_set_source_pixbuf(ctx, pix, x + pixed_corner.left, y + h - pixed_corner.bottom)
                ctx.paint()
            # right bottom
            pix = pixbuf.new_subpixbuf(
                im_w - pixed_corner.right, im_h - pixed_corner.bottom, pixed_corner.right, pixed_corner.bottom
            )
            Gdk.cairo_set_source_pixbuf(ctx, pix, x + w - pixed_corner.right, y + h - pixed_corner.bottom)
            ctx.paint()
        else:
            pixbuf = pixbuf.scale_simple(w, h, GdkPixbuf.InterpType.BILINEAR)
            Gdk.cairo_set_source_pixbuf(ctx, pixbuf, x, y)
            ctx.paint()

        ctx.restore()

    @staticmethod
    def DrawText(
        ctx: cairo.Context,
        *,
        text: str,
        font: str,
        font_size: int,
        color: Gdk.RGBA,
        xy: Tuple[float, float],
        wh: Tuple[float, float],
        hvalign: Tuple[PyDuiAlign, PyDuiAlign] = (PyDuiAlign.CENTER, PyDuiAlign.CENTER),
        ellipsis_mode: Pango.EllipsizeMode = Pango.EllipsizeMode.END,
        wrap_mode: Pango.WrapMode = Pango.WrapMode.WORD,
        line_spacing: float = 1.25,
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

        # config font layout
        line_height = __config_text_layout__(
            layout,
            font=font,
            font_size=font_size,
            wh=(w, h),
            hvalign=hvalign,
            ellipsis_mode=ellipsis_mode,
            wrap_mode=wrap_mode,
            line_spacing=line_spacing,
        )
        PangoCairo.update_layout(ctx, layout)

        # calulate text align
        layout_w, layout_h = layout.get_size()
        layout_w, layout_h = layout_w / Pango.SCALE, layout_h / Pango.SCALE
        if hvalign[0] == PyDuiAlign.CENTER:
            x = x + round((w - layout_w) / 2)
        elif hvalign[0] == PyDuiAlign.END:
            x = x + round(w - layout_w)
        if hvalign[1] == PyDuiAlign.CENTER:
            y = y + round((h - layout_h) / 2)
        elif hvalign[1] == PyDuiAlign.END:
            y = y + round(h - layout_h) - round(line_height * (line_spacing - 1.0))
        else:
            y = y + round(line_height * (line_spacing - 1.0))
        ctx.move_to(x, y)
        PangoCairo.show_layout(ctx, layout)

        # restore ctx
        ctx.restore()

    @staticmethod
    def EstimateTextSize(
        ctx: cairo.Context,
        *,
        text: str,
        font: str,
        fontsize: int,
        limit_wh: Tuple[float, float] = (-1, -1),
        hvalign: Tuple[PyDuiAlign, PyDuiAlign] = (PyDuiAlign.CENTER, PyDuiAlign.CENTER),
        ellipsis_mode: Pango.EllipsizeMode = Pango.EllipsizeMode.END,
        wrap_mode: Pango.WrapMode = Pango.WrapMode.WORD,
        line_spacing: float = 1.25,
    ) -> Tuple[float, float]:
        """Estimate text size"""
        if ctx is None:
            logging.error("cairo.Context not ready for render text.")
            return (0, 0)

        limit_w, limit_h = limit_wh
        layout = PangoCairo.create_layout(ctx)
        layout.set_text(text, -1)

        # config font layout
        line_height = __config_text_layout__(
            layout,
            font=font,
            font_size=fontsize,
            wh=limit_wh,
            hvalign=hvalign,
            ellipsis_mode=ellipsis_mode,
            wrap_mode=wrap_mode,
            line_spacing=line_spacing,
        )

        PangoCairo.update_layout(ctx, layout)
        w, h = layout.get_pixel_size()
        lines = layout.get_line_count()
        return (math.ceil(w), math.ceil(lines * line_height))

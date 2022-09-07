# -*- coding: utf-8 -*-
import logging
from dataclasses import dataclass
from typing import Type

from pydui import utils
from pydui.core.attribute_string import *
from pydui.core.base import *
from pydui.core.import_gtk import *
from pydui.core.layout import *
from pydui.core.render_canvas import *
from pydui.core.resource_loader import PyDuiResourceLoader
from pydui.core.widget import *


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
        canvas_width: float,
        canvas_height: float,
    ):
        ctx.save()
        ctx.rectangle(x / canvas_width, y / canvas_height, w / canvas_width, h / canvas_height)
        ctx.set_source_rgba(*color)
        ctx.fill()
        ctx.restore()

    @staticmethod
    def DrawImage(
        ctx: cairo.Context,
        loader: PyDuiResourceLoader,
        path: str,
        xy: tuple[float, float],
        wh: tuple[float, float],
        corner: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0),
    ):
        # TODO: ResourceLoader, Render, RenderCanvas should have a device-dpi manager
        # that it can easier to get access the dpi scale factor.
        buf, factor = loader.load_image(path)
        if len(buf) == 0:
            logging.error(f"buf is empty. path = {path} loader = {loader}")
            return

        ctx.save()
        ctx.scale(1.0 / factor, 1.0 / factor)

        pixbuf_loader = GdkPixbuf.PixbufLoader.new_with_type("png")
        pixbuf_loader.write(buf)
        pixbuf_loader.close()
        pixbuf = pixbuf_loader.get_pixbuf()
        im_w, im_h = pixbuf.get_width(), pixbuf.get_height()
        x, y = xy[0] * factor, xy[1] * factor
        w, h = wh[0] * factor, wh[1] * factor
        pixed_corner = tuple(n * factor for n in corner)

        has_corner = utils.IsNoneZeroRect(corner)
        if has_corner:
            # left top
            pix = pixbuf.new_subpixbuf(0, 0, pixed_corner[0], pixed_corner[1])
            Gdk.cairo_set_source_pixbuf(ctx, pix, x, y)
            ctx.paint()
            # right top
            pix = pixbuf.new_subpixbuf(im_w - pixed_corner[2], 0, pixed_corner[2], pixed_corner[1])
            Gdk.cairo_set_source_pixbuf(ctx, pix, x + w - pixed_corner[2], y)
            ctx.paint()
            # middle top
            pix = pixbuf.new_subpixbuf(pixed_corner[0], 0, im_w - (pixed_corner[0] + pixed_corner[2]), pixed_corner[1])
            pix = pix.scale_simple(
                (w - (pixed_corner[0] + pixed_corner[2])), pixed_corner[1], GdkPixbuf.InterpType.NEAREST
            )
            Gdk.cairo_set_source_pixbuf(ctx, pix, x + pixed_corner[0], y)
            ctx.paint()
            # left middle
            pix = pixbuf.new_subpixbuf(0, pixed_corner[1], pixed_corner[0], im_h - pixed_corner[1] - pixed_corner[3])
            pix = pix.scale_simple(pixed_corner[0], h - pixed_corner[1] - pixed_corner[3], GdkPixbuf.InterpType.NEAREST)
            Gdk.cairo_set_source_pixbuf(ctx, pix, x, y + pixed_corner[1])
            ctx.paint()
            # middle middle
            pix = pixbuf.new_subpixbuf(
                pixed_corner[0],
                pixed_corner[1],
                im_w - pixed_corner[0] - pixed_corner[2],
                im_h - pixed_corner[1] - pixed_corner[3],
            )
            pix = pix.scale_simple(
                w - pixed_corner[0] - pixed_corner[2],
                h - pixed_corner[1] - pixed_corner[3],
                GdkPixbuf.InterpType.NEAREST,
            )
            Gdk.cairo_set_source_pixbuf(ctx, pix, x + pixed_corner[0], y + pixed_corner[1])
            ctx.paint()
            # right middle
            pix = pixbuf.new_subpixbuf(
                im_w - pixed_corner[2], pixed_corner[1], pixed_corner[2], im_h - pixed_corner[1] - pixed_corner[3]
            )
            pix = pix.scale_simple(pixed_corner[2], h - pixed_corner[1] - pixed_corner[3], GdkPixbuf.InterpType.NEAREST)
            Gdk.cairo_set_source_pixbuf(ctx, pix, x + w - pixed_corner[2], y + pixed_corner[1])
            ctx.paint()
            # left bottom
            pix = pixbuf.new_subpixbuf(0, im_h - pixed_corner[3], pixed_corner[0], pixed_corner[3])
            Gdk.cairo_set_source_pixbuf(ctx, pix, x, y + h - pixed_corner[3])
            ctx.paint()
            # middle bottom
            pix = pixbuf.new_subpixbuf(
                pixed_corner[0], im_h - pixed_corner[3], im_w - pixed_corner[0] - pixed_corner[2], pixed_corner[3]
            )
            pix = pix.scale_simple(w - pixed_corner[0] - pixed_corner[2], pixed_corner[3], GdkPixbuf.InterpType.NEAREST)
            Gdk.cairo_set_source_pixbuf(ctx, pix, x + pixed_corner[0], y + h - pixed_corner[3])
            ctx.paint()
            # right bottom
            pix = pixbuf.new_subpixbuf(im_w - pixed_corner[2], im_h - pixed_corner[3], pixed_corner[2], pixed_corner[3])
            Gdk.cairo_set_source_pixbuf(ctx, pix, x + w - pixed_corner[2], y + h - pixed_corner[3])
            ctx.paint()
        else:
            pixbuf = pixbuf.scale_simple(w, h, GdkPixbuf.InterpType.BILINEAR)
            Gdk.cairo_set_source_pixbuf(ctx, pixbuf, x, y)
            ctx.paint()

        ctx.restore()

    @staticmethod
    def DrawText(
        ctx: cairo.Context,
        text: str,
        font: str,
        font_size: int,
        color: Gdk.RGBA,
        xy: tuple[float, float],
        wh: tuple[float, float],
        hvalign: tuple[PyDuiAlign, PyDuiAlign] = (PyDuiAlign.CENTER, PyDuiAlign.CENTER),
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
        if hvalign[0] == PyDuiAlign.CENTER:
            x = x + round((w - layout_w) / 2)
        elif hvalign[0] == PyDuiAlign.END:
            x = x + round(w - layout_w)
        if hvalign[1] == PyDuiAlign.CENTER:
            y = y + round((h - layout_h) / 2)
        elif hvalign[1] == PyDuiAlign.END:
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

# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Callable, Type

from pydui import utils
from pydui.core.import_gtk import *
from pydui.core.screen import PyDuiScreen


class PyDuiRenderCanvas(Gtk.Frame):

    """Render canvas"""

    __area: Gtk.DrawingArea
    __width: float = 0
    __height: float = 0
    __ondraw: Callable[[cairo.Context, float, float], None] = None

    def __init__(self, ondraw: callable, css=None, border_width=0):
        super().__init__()
        self.set_shadow_type(Gtk.ShadowType.NONE)
        self.set_border_width(0)
        self.vexpand = True
        self.hexpand = True
        self.surface = None
        self.__ondraw = ondraw

        self.__area = Gtk.DrawingArea()
        self.add(self.__area)

        self.__area.connect("draw", self.__on_draw__)
        self.__area.connect("configure-event", self.__on_configure__)

    def __init_surface__(self, area: Gtk.DrawingArea):
        # Destroy previous buffer
        if self.surface is not None:
            self.surface.finish()
            self.surface = None

        # Create a new buffer
        scale_factor = PyDuiScreen.get_system_dpi_scale()
        self.surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            round(area.get_allocated_width() * scale_factor),
            round(area.get_allocated_height() * scale_factor),
        )
        self.surface.set_device_scale(scale_factor, scale_factor)

    def redraw(self):
        self.__init_surface__(self.__area)

        # draw to surface
        context = cairo.Context(self.surface)
        self.__do_drawing__(context)
        self.surface.flush()

    def __on_draw__(self, area: Gtk.DrawingArea, context: cairo.Context):
        if self.surface is not None:
            context.set_source_surface(self.surface, 0.0, 0.0)
            context.paint()
        else:
            logging.error("Invalid surface")
        return True

    def __on_configure__(self, gtk_object, gtk_event):
        width, height = gtk_event.width, gtk_event.height
        if width != self.__width or height != self.__height:
            self.__width, self.__height = width, height
            need_redraw = True
        if need_redraw:
            self.redraw()
        return True

    def __do_drawing__(self, ctx: cairo.Context):
        if self.__ondraw is not None:
            ctx.save()
            self.__ondraw(ctx, self.__width, self.__height)
            ctx.restore()

    def get_width(self) -> float:
        return self.__width

    def get_height(self) -> float:
        return self.__height

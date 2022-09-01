from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Type

import cairo
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")

from gi.repository import Gdk, GdkPixbuf, Gtk, Pango, PangoCairo

from pydui.core import utils


class PyDuiRenderCanvas(Gtk.Frame):

    """Render canvas"""

    __area: Gtk.DrawingArea
    __width: float = 0
    __height: float = 0
    __ondraw: callable

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
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, area.get_allocated_width(), area.get_allocated_height())

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
            print("Invalid surface")
        return False

    def __on_configure__(self, gtk_object, gtk_event):
        width, height = gtk_event.width, gtk_event.height
        if width != self.__width or height != self.__height:
            self.__width, self.__height = width, height
            need_redraw = True
        if need_redraw:
            self.redraw()

    def __do_drawing__(self, ctx: cairo.Context):
        if self.__ondraw is not None:
            ctx.save()
            self.__ondraw(ctx, self.__width, self.__height)
            ctx.restore()

    def get_width(self) -> float:
        return self.__width

    def get_height(self) -> float:
        return self.__height

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
from gi.repository import Gdk, GdkPixbuf, Gtk


class PyDuiRenderManager(object):

    """Render manager"""

    __canvas: PyDuiRenderCanvas
    __rootview: PyDuiLayout

    # manager all widget
    def __init__(self, window: PyDuiWindow):
        self.__window = window
        self.__canvas = PyDuiRenderCanvas(self.__on_draw__)
        self.__rootview = None

        gtk_window = self.__window.get_gtk_window()
        gtk_window.add(self.__canvas)

    def set_rootview(self, rootview: PyDuiLayout):
        """set window root view

        Args:
            rootview (PyDuiWidget): widnow root view
        """
        if self.__rootview is not None:
            # remove from window
            pass
        self.__rootview = rootview
        # add to window
        # self.__window.get_gtk_window().add(rootview.get_gtk_widget())

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

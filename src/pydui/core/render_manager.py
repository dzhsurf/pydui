# -*- coding: utf-8 -*-
from pydui.core.import_gtk import *
from pydui.core.layout import PyDuiLayout
from pydui.core.render_base import PyDuiRenderManagerBase
from pydui.core.render_canvas import PyDuiRenderCanvas
from pydui.core.resource_loader import PyDuiResourceLoader
from pydui.core.widget import PyDuiWidget
from pydui.core.window_base import PyDuiWindowBase


class PyDuiRenderManager(PyDuiRenderManagerBase):

    """Render manager"""

    __loader: PyDuiResourceLoader = None
    __canvas: PyDuiRenderCanvas = None
    __rootview: PyDuiLayout = None
    __default_fontfamily: str = "Arial"
    __default_fontsize: int = 16
    __default_fontcolor: Gdk.RGBA = Gdk.RGBA(0.0, 0.0, 0.0, 1.0)

    # manager all widget
    def __init__(self, window: PyDuiWindowBase, loader: PyDuiResourceLoader):
        self.__window = window
        self.__canvas = PyDuiRenderCanvas(self.__on_draw__)
        self.__loader = loader

        gtk_window = self.__window.get_gtk_window()
        gtk_window.add(self.__canvas)

    def notify_redraw(self):
        # TODO: redraw dirty area
        self.__canvas.redraw()
        self.__canvas.queue_draw_area(0, 0, self.__canvas.get_width(), self.__canvas.get_height())

    def get_resource_loader(self):
        return self.__loader

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

    def get_widget(self, widget_id: str) -> PyDuiWidget:
        """Get widget by widget id

        Args:
            widget_id (str): widget id
        """
        return self.__rootview.get_child(widget_id)

    def get_widget_by_pos(self, x: float, y: float) -> PyDuiWidget:
        if self.__rootview is None:
            return None

        return self.__rootview.get_child_by_pos(x, y)

    def __on_draw__(self, ctx: cairo.Context, width: float, height: float):
        if self.__rootview is None:
            return
        self.__rootview.layout(0, 0, width, height)
        self.__rootview.draw(ctx, 0, 0, width, height)

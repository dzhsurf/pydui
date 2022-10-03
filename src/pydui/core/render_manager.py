# -*- coding: utf-8 -*-
from typing import Any, Callable

from pynoticenter import PyNotiCenter, PyNotiTaskQueue

from pydui.core.base import PyDuiLayoutConstraint
from pydui.core.gtk_widget_interface import PyDuiGtkWidgetInterface
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
    __layer: Gtk.Fixed = None
    __ctx: cairo.Context = None
    __rootview: PyDuiLayout = None
    __default_fontfamily: str = "Arial"
    __default_fontsize: int = 16
    __default_fontcolor: Gdk.RGBA = Gdk.RGBA(0.0, 0.0, 0.0, 1.0)
    __task_queue: PyNotiTaskQueue = None

    # manager all widget
    def __init__(self, window: PyDuiWindowBase, loader: PyDuiResourceLoader):
        self.__window = window
        self.__canvas = PyDuiRenderCanvas(self.__on_draw__)
        self.__loader = loader
        self.__ctx = None
        queue_name = f"pydui-task-queue"
        self.__task_queue = PyNotiCenter.default().create_task_queue(queue_name)
        self.__task_queue.set_preprocessor(self.__post_task_to_gtk_thread__)

        gtk_window = self.__window.get_gtk_window()

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)

        self.__layer = Gtk.Fixed()
        self.__layer.set_has_window(True)
        self.__layer.put(self.__canvas, 0, 0)
        scrolled_window.add(self.__layer)

        gtk_window.add(scrolled_window)

    def release(self):
        self.__task_queue.terminate(False)

    def notify_redraw(self):
        # TODO: redraw dirty area
        self.__canvas.redraw()
        self.__canvas.queue_draw_area(0, 0, self.__canvas.get_width(), self.__canvas.get_height())

    def put_gtk_widget(self, widget: PyDuiGtkWidgetInterface):
        if not isinstance(widget, PyDuiGtkWidgetInterface):
            return
        gtk_widget = widget.get_gtk_widget()
        self.__layer.put(gtk_widget, 0, 0)

    def remove_gtk_widget(self, widget: PyDuiGtkWidgetInterface):
        if not isinstance(widget, PyDuiGtkWidgetInterface):
            return
        gtk_widget = widget.get_gtk_widget()
        self.__layer.remove(gtk_widget)

    def move_gtk_widget(self, widget: PyDuiGtkWidgetInterface, x: float, y: float):
        if not isinstance(widget, PyDuiGtkWidgetInterface):
            return
        gtk_widget = widget.get_gtk_widget()
        self.__layer.move(gtk_widget, x, y)

    def set_window_size(self, w: float, h: float):
        self.__canvas.set_size_request(w, h)

    def get_render_context(self) -> cairo.Context:
        return self.__ctx

    def cancel_task(self, task_id: str):
        self.__task_queue.cancel_task(task_id)

    def post_task(self, fn: callable, *args: Any, **kwargs: Any) -> str:
        return self.post_task_with_delay(0.0, fn, *args, **kwargs)

    def post_task_with_delay(self, delay: float, fn: callable, *args: Any, **kwargs: Any) -> str:
        if self.__task_queue.is_terminated:
            return ""
        if fn is None:
            return ""
        return self.__task_queue.post_task_with_delay(delay, fn, *args, **kwargs)

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
            rootview (PyDuiWidget): window root view
        """
        self.__rootview = rootview
        rootview.set_render_manager(self)

    def get_rootview(self) -> PyDuiLayout:
        """Return root view widget.

        Returns:
            PyDuiLayout: root view.
        """
        return self.__rootview

    def get_widget(self, widget_id: str) -> PyDuiWidget:
        """Get widget by widget id

        Args:
            widget_id (str): widget id
        """
        return self.__rootview.get_child(widget_id)

    def get_widget_by_pos(
        self,
        x: float,
        y: float,
        *,
        filter: Callable[[PyDuiWidget], bool] = PyDuiWidget.find_widget_default_filter,
    ) -> PyDuiWidget:
        if self.__rootview is None:
            return None

        return self.__rootview.find_widget_by_pos(x, y, filter=filter)

    def __on_draw__(self, ctx: cairo.Context, width: float, height: float):
        if self.__rootview is None:
            return
        self.__ctx = ctx
        constraint = PyDuiLayoutConstraint(width, height)
        self.__rootview.layout(0, 0, width, height, constraint)
        self.__rootview.draw(ctx, 0, 0, width, height)

    def __post_task_to_gtk_thread__(self, fn: callable, *args: Any, **kwargs: Any) -> bool:
        if self.__task_queue.is_terminated:
            return True
        GLib.idle_add(fn, *args, **kwargs)
        return True

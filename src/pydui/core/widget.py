# -*- coding: utf-8 -*-
import logging
import sys
import weakref
from dataclasses import dataclass
from typing import Any, List, Tuple
from weakref import ReferenceType

from pydui import utils
from pydui.common.base import *
from pydui.common.import_gtk import *
from pydui.core.render import PyDuiRender
from pydui.core.window_client_interface import PyDuiWindowClientInterface


@dataclass(frozen=True)
class PyDuiConstraint:

    """Constraint dataclass"""

    min_width: float = 0
    max_width: float = sys.maxsize
    min_height: float = 0
    max_height: float = sys.maxsize


class PyDuiObject:
    """PyDuiObject, base object"""

    pass


class PyDuiWidget(PyDuiObject):

    """Widget base class"""

    __window_client: ReferenceType[PyDuiWindowClientInterface] = None

    __id: str = ""
    __parent: PyDuiObject
    __x: float = 0
    __y: float = 0
    __width: float = 0
    __height: float = 0
    __fixed_x: float = 0
    __fixed_y: float = 0
    __fixed_width: float = 0
    __fixed_height: float = 0
    __enabled: bool = True
    __autofit: bool = False
    __can_focus: bool = False
    # attrib
    __bkcolor: Gdk.RGBA = None
    __margin: tuple[float, float, float, float] = (0, 0, 0, 0)
    __corner: tuple[float, float, float, float] = (0, 0, 0, 0)
    __bkimage: str = ""
    # event
    __signals: dict[str, list[callable]] = None
    __enable_mouse_event: bool = False

    @staticmethod
    def build_name() -> str:
        return "__Control"

    @staticmethod
    def find_widget_default_filter(widget: PyDuiObject) -> bool:
        return widget is not None

    @staticmethod
    def find_widget_mouse_event_filter(widget: PyDuiObject) -> bool:
        if widget is None:
            return False
        return widget.enable_mouse_event

    def __init__(self, parent: PyDuiObject):
        super().__init__()
        self.__parent = parent
        self.__signals = dict[str, list[callable]]()

    def set_window_client(self, window_client: PyDuiWindowClientInterface):
        """Set the window client

        Do not call this function yourself if you do not know what it is for!
        """
        self.__window_client = weakref.ref(window_client)

    def get_window_client(self):
        """Get the widget window client

        The widget will setup window client after call do_post_init. before the widget init finish, window client will be empty.
        """
        if self.__window_client is not None:
            return self.__window_client()

        return None

    def get_id(self) -> str:
        """Return widget id

        Returns:
            str: widget id
        """
        return self.__id

    def draw(
        self,
        ctx: cairo.Context,
        x: float,
        y: float,
        width: float,
        height: float,
    ):
        self.draw_bkcolor(ctx, x, y, width, height)
        self.draw_bkimage(ctx, x, y, width, height)

    def draw_bkcolor(
        self,
        ctx: cairo.Context,
        x: float,
        y: float,
        width: float,
        height: float,
    ):
        if self.bkcolor is None:
            return

        PyDuiRender.Rectangle(ctx, self.bkcolor, x, y, width, height)

    def draw_bkimage(
        self,
        ctx: cairo.Context,
        x: float,
        y: float,
        width: float,
        height: float,
    ):
        if self.bkimage == "":
            return

        PyDuiRender.DrawImage(
            ctx,
            loader=self.get_window_client().get_resource_loader(),
            path=self.bkimage,
            xy=(x, y),
            wh=(width, height),
            corner=self.corner,
        )

    def layout(self, x: float, y: float, width: float, height: float, constraint: PyDuiLayoutConstraint):
        self.__x, self.__y = x, y
        self.__width, self.__height = width, height
        logging.debug(f"Layout: {self.build_name()} => ({x}, {y}, {width}, {height})")

    def estimate_size(
        self, parent_width: float, parent_height: float, constraint: PyDuiLayoutConstraint
    ) -> tuple[float, float]:
        return (self.fixed_width, self.fixed_height)

    def parse_attributes(self, attrib: dict[str, str]):
        """Parse all attributes

        Args:
            attrib (dict[str, str]): attributes dict key=value ...
        """
        for k, v in attrib.items():
            self.parse_attrib(k, v)
        pass

    def parse_attrib(self, k: str, v: str):
        """Parse single attribute

        Args:
            attrib (dict[str, str]): attributes dict key=value ...
        """
        # logging.debug(f"{self} parse {k} = {v}")
        if k == "id":
            self.__id = v
        elif k == "width":
            self.fixed_width = float(v)
        elif k == "height":
            self.fixed_height = float(v)
        elif k == "size":
            size_arr = v.split(",")
            self.fixed_size(tuple(float(n) for n in size_arr))
        elif k == "x":
            self.fixed_x = float(v)
        elif k == "y":
            self.fixed_y = float(v)
        elif k == "xy":
            self.fixed_xy = tuple(float(a) for a in v.split(","))
        elif k == "margin":
            self.margin = utils.Str2Rect(v)
        elif k == "bkcolor":
            self.bkcolor = utils.Str2Color(v)
        elif k == "bkimage":
            self.bkimage = v
        elif k == "corner":
            self.corner = utils.Str2Rect(v)
        elif k == "enable":
            self.enabled = v == "true"
        elif k == "autofit":
            self.__autofit = v == "true"

    # event
    @property
    def enable_mouse_event(self) -> bool:
        return self.__enable_mouse_event

    @enable_mouse_event.setter
    def enable_mouse_event(self, enable: bool):
        self.__enable_mouse_event = enable

    def on_post_init(self):
        pass

    def on_mouse_enter(self):
        pass

    def on_mouse_leave(self, next_widget: PyDuiObject):
        pass

    def on_mouse_move(self, x: float, y: float):
        pass

    def on_lbutton_press(self, x: float, y: float):
        return False

    def on_lbutton_release(self, x: float, y: float):
        pass

    def on_rbutton_press(self, x: float, y: float):
        return False

    def on_rbutton_release(self, x: float, y: float):
        pass

    def on_lbutton_click(self, x: float, y: float):
        pass

    def on_rbutton_click(self, x: float, y: float):
        pass

    def on_l2button_click(self, x: float, y: float):
        pass

    def on_r2button_click(self, x: float, y: float):
        pass

    def on_l3button_click(self, x: float, y: float):
        pass

    def on_r3button_click(self, x: float, y: float):
        pass

    # method
    def get_signals(self) -> List[str]:
        return []

    def connect(self, signal_name: str, callback: callable):
        if signal_name in self.__signals:
            self.__signals[signal_name].append(callback)
        else:
            self.__signals[signal_name] = list([callback])

    def disconnect(self, signal_name: str, callback: callable):
        def remove_fn(item: callable):
            if item == callback:
                return True
            return False

        if signal_name in self.__signals:
            self.__signals[signal_name] = list(filter(remove_fn, self.__signals[signal_name]))

    def disconnect_signal(self, signal_name: str):
        if signal_name in self.__signals:
            self.__signals.pop(signal_name)

    def emit(self, signal_name: str, *args: Any, **kwargs: Any):
        if signal_name in self.__signals:
            fn_list = self.__signals[signal_name].copy()

            def run_all_fn(*args: Any, **kwargs: Any):
                for fn in fn_list:
                    if fn(*args, **kwargs):
                        break

            self.get_window_client().post_task(run_all_fn, *args, **kwargs)

    def set_focus(self):
        pass

    def contain_pos(self, x: float, y: float) -> bool:
        if (x >= self.x) and (x <= (self.x + self.width)) and (y >= self.y) and (y <= (self.y + self.height)):
            return True
        return False

    # properties
    # position & size

    @property
    def parent(self) -> PyDuiObject:
        return self.__parent

    @property
    def size(self) -> Tuple[float, float]:
        return (self.width, self.height)

    @property
    def width(self) -> float:
        return self.__width

    @property
    def height(self) -> float:
        return self.__height

    @property
    def layout_rect(self) -> tuple[float, float, float, float]:
        return (
            self.x,
            self.y,
            self.x + self.width + utils.RectW(self.margin),
            self.y + self.height + utils.RectH(self.margin),
        )

    @property
    def fixed_size(self) -> tuple[float, float]:
        return (self.fixed_width, self.fixed_height)

    @fixed_size.setter
    def fixed_size(self, size: tuple[float, float]):
        self.fixed_width = size[0]
        self.fixed_height = size[1]

    @property
    def fixed_width(self) -> float:
        return self.__fixed_width

    @fixed_width.setter
    def fixed_width(self, w: float):
        self.__fixed_width = w

    @property
    def fixed_height(self) -> float:
        return self.__fixed_height

    @fixed_height.setter
    def fixed_height(self, h: float):
        self.__fixed_height = h

    @property
    def xy(self) -> tuple[float, float]:
        return (self.x, self.y)

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def is_float(self) -> bool:
        pass

    @property
    def fixed_x(self) -> float:
        return self.__fixed_x

    @fixed_x.setter
    def fixed_x(self, x: float):
        self.__fixed_x = x

    @property
    def fixed_y(self) -> float:
        return self.__fixed_y

    @fixed_y.setter
    def fixed_y(self, y: float):
        self.__fixed_y = y

    @property
    def fixed_xy(self) -> tuple[float, float]:
        return (self.__fixed_x, self.__fixed_y)

    @fixed_xy.setter
    def fixed_xy(self, xy: tuple[float, float]):
        self.fixed_x = xy[0]
        self.fixed_y = xy[1]

    @is_float.setter
    def is_float(self, is_float: bool):
        pass

    @property
    def margin(self) -> tuple[float, float, float, float]:
        """Return widget margin

        The value in tuple means [left, top, right, bottom]

        Returns:
            tuple[float, float, float, float]: return margin.
        """
        return self.__margin

    @margin.setter
    def margin(self, margin: tuple[float, float, float, float]):
        """Set the widget margin

        Args:
            margin (tuple[float, float, float, float]): widget margin

        """
        self.__margin = margin

    # constraint
    @property
    def constraint(self) -> PyDuiConstraint:
        pass

    @constraint.setter
    def constraint(self, v: PyDuiConstraint):
        pass

    # state
    @property
    def visible(self) -> bool:
        pass

    @visible.setter
    def visible(self, visible: bool):
        pass

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @enabled.setter
    def enabled(self, enabled: bool):
        self.__enabled = enabled

    @property
    def autofit(self) -> bool:
        return self.__autofit

    @autofit.setter
    def autofit(self, autofit: bool):
        self.__autofit = autofit

    @property
    def is_focused(self) -> bool:
        # return self.get_manager().is_focused(self)
        return False

    @property
    def can_focus(self) -> bool:
        return self.__can_focus

    @can_focus.setter
    def can_focus(self, can_focus: bool):
        self.__can_focus = can_focus

    # appearance
    @property
    def bkcolor(self) -> Gdk.RGBA:
        return self.__bkcolor

    @bkcolor.setter
    def bkcolor(self, color: Gdk.RGBA):
        self.__bkcolor = color

    @property
    def bkimage(self) -> str:
        return self.__bkimage

    @bkimage.setter
    def bkimage(self, image: str):
        self.__bkimage = image

    @property
    def corner(self) -> tuple[float, float, float, float]:
        return self.__corner

    @corner.setter
    def corner(self, corner: tuple[float, float, float, float]):
        self.__corner = corner

    # private function
    def __do_post_init__(self, window_client: PyDuiWindowClientInterface):
        self.set_window_client(window_client)
        self.on_post_init()

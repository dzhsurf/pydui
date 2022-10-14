# -*- coding: utf-8 -*-
from dataclasses import dataclass
from enum import Enum
from typing import Type

from pydui.common.import_gtk import *
from pydui.core.layout import *
from pydui.core.widget import *
from pydui.widgets.label import *


class PyDuiButtonState(Enum):
    """Button State"""

    NORMAL = (0,)
    HOVER = (1,)
    PRESS = (2,)


class PyDuiButton(PyDuiLabel):

    """Button widget"""

    __bkimage_hover: str = ""
    __bkimage_press: str = ""
    __bkimage_disable: str = ""
    __bkimage_disable_hover: str = ""
    __bkimage_disable_press: str = ""
    __button_state: PyDuiButtonState = PyDuiButtonState.NORMAL

    @staticmethod
    def build_name() -> str:
        return "Button"

    def __init__(self):
        super().__init__()
        self.can_focus = True
        self.enable_mouse_event = True

    def parse_attrib(self, k: str, v: str):
        if k == "bkimage_hover":
            self.__bkimage_hover = v
        elif k == "bkimage_press":
            self.__bkimage_press = v
        elif k == "bkimage_disable":
            self.__bkimage_disable = v
        elif k == "bkimage_disable_hover":
            self.__bkimage_disable_hover = v
        elif k == "bkimage_disable_press":
            self.__bkimage_disable_press = v

        super().parse_attrib(k, v)

    def draw_bkimage(
        self,
        ctx: cairo.Context,
        x: float,
        y: float,
        width: float,
        height: float,
    ):
        path = self.__get_drawimage_by_state()
        if path == "":
            path = self.bkimage

        if path == "":
            return

        PyDuiRender.DrawImage(
            ctx,
            loader=self.get_window_client().get_resource_loader(),
            path=path,
            xy=(0, 0),
            wh=(self.width, self.height),
            corner=self.corner,
        )

    @property
    def bkimage_hover(self) -> str:
        return self.__bkimage_hover

    @bkimage_hover.setter
    def bkimage_hover(self, image: str):
        self.__bkimage_hover = image

    @property
    def bkimage_press(self) -> str:
        return self.__bkimage_press

    @bkimage_press.setter
    def bkimage_press(self, image: str):
        self.__bkimage_press = image

    @property
    def bkimage_disable(self) -> str:
        return self.__bkimage_disable

    @bkimage_disable.setter
    def bkimage_disable(self, image: str):
        self.__bkimage_disable = image

    def get_bindevents(self) -> List[str]:
        events = super().get_bindevents()
        events.extend(["lbutton-press", "lbutton-release"])
        return events

    def get_signals(self) -> List[str]:
        signals = super().get_signals()
        signals.extend(
            [
                "lbutton-click",
                "rbutton-click",
                "lbutton-dbclick",
                "rbutton-dbclick",
                "lbutton-tripleclick",
                "rbutton-tripleclick",
            ]
        )
        return signals

    def on_mouse_enter(self):
        super().on_mouse_enter()
        self.__button_state = PyDuiButtonState.HOVER
        self.get_window_client().notify_redraw()

    def on_mouse_leave(self, next_widget: PyDuiWidget):
        super().on_mouse_leave(next_widget)
        self.__button_state = PyDuiButtonState.NORMAL
        self.get_window_client().notify_redraw()

    def on_lbutton_press(self, x: float, y: float):
        if self.do_bind_event("lbutton-press", self, x, y):
            return True
        return super().on_lbutton_press(x, y)

    def on_lbutton_release(self, x: float, y: float):
        if self.do_bind_event("lbutton-release", self, x, y):
            return True
        return super().on_lbutton_release(x, y)

    def on_lbutton_click(self, x: float, y: float):
        self.emit("lbutton-click", self, x, y)

    def on_rbutton_click(self, x: float, y: float):
        self.emit("rbutton-click", self, x, y)

    def on_l2button_click(self, x: float, y: float):
        self.emit("lbutton-dblick", self, x, y)

    def on_r2button_click(self, x: float, y: float):
        self.emit("rbutton-dbclick", self, x, y)

    def on_l3button_click(self, x: float, y: float):
        self.emit("lbutton-tripleclick", self, x, y)

    def on_r3button_click(self, x: float, y: float):
        self.emit("rbutton-tripleclick", self, x, y)

    def __get_drawimage_by_state(self):
        if not self.enabled:
            img = {
                PyDuiButtonState.NORMAL: self.__bkimage_disable,
                PyDuiButtonState.HOVER: self.__bkimage_disable_hover,
                PyDuiButtonState.PRESS: self.__bkimage_disable_press,
            }[self.__button_state]
            if img == "":
                img = self.__bkimage_disable
            return img
        return {
            PyDuiButtonState.NORMAL: self.bkimage,
            PyDuiButtonState.HOVER: self.__bkimage_hover,
            PyDuiButtonState.PRESS: self.__bkimage_press,
        }[self.__button_state]

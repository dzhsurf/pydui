# -*- coding: utf-8 -*-
from dataclasses import dataclass
from enum import Enum
from typing import Type

from pydui.core.import_gtk import *
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

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)
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
            loader=self.get_render_manager().get_resource_loader(),
            path=path,
            xy=(x, y),
            wh=(width, height),
            corner=self.corner,
        )

    def on_mouse_enter(self):
        super().on_mouse_enter()
        self.__button_state = PyDuiButtonState.HOVER
        self.get_render_manager().notify_redraw()

    def on_mouse_leave(self, next_widget: PyDuiWidget):
        super().on_mouse_leave(next_widget)
        self.__button_state = PyDuiButtonState.NORMAL
        self.get_render_manager().notify_redraw()

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

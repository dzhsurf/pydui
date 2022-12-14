# -*- coding: utf-8 -*-
from pydui.common.base import PyDuiEdge
from pydui.common.import_gtk import *


class PyDuiAppearanceManager:
    """PyDuiAppearanceManager"""

    def __init__(self) -> None:
        self.__box_size = PyDuiEdge()
        self.__default_fontfamily: str = "Arial"
        self.__default_fontsize: int = 16
        self.__default_fontcolor: Gdk.RGBA = Gdk.RGBA(0.0, 0.0, 0.0, 1.0)
        self.__customize_titlebar: bool = False
        self.__caption_height: int = 0

    @property
    def default_fontcolor(self) -> Gdk.RGBA:
        return self.__default_fontcolor

    @default_fontcolor.setter
    def default_fontcolor(self, fontcolor: Gdk.RGBA):
        self.__default_fontcolor = fontcolor

    @property
    def default_font_desc(self) -> str:
        return f"{self.default_fontfamily} {self.default_fontsize}"

    @property
    def default_fontfamily(self) -> str:
        return self.__default_fontfamily

    @default_fontfamily.setter
    def default_fontfamily(self, font_family: str):
        self.__default_fontfamily = font_family

    @property
    def default_fontsize(self) -> int:
        return self.__default_fontsize

    @default_fontsize.setter
    def default_fontsize(self, font_size: int):
        self.__default_fontsize = font_size

    @property
    def customize_titlebar(self) -> bool:
        return self.__customize_titlebar

    @customize_titlebar.setter
    def customize_titlebar(self, customize_title: bool):
        self.__customize_titlebar = customize_title

    @property
    def box_size(self) -> PyDuiEdge:
        return self.__box_size

    @box_size.setter
    def box_size(self, box_size: PyDuiEdge):
        self.__box_size = box_size

    @property
    def caption_height(self) -> int:
        return self.__caption_height

    @caption_height.setter
    def caption_height(self, caption_height: int):
        self.__caption_height = caption_height

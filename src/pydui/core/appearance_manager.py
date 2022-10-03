# -*- coding: utf-8 -*-
from pydui.common.import_gtk import *


class PyDuiAppearanceManager:
    """"""

    __default_fontfamily: str = "Arial"
    __default_fontsize: int = 16
    __default_fontcolor: Gdk.RGBA = Gdk.RGBA(0.0, 0.0, 0.0, 1.0)

    def __init__(self) -> None:
        pass

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

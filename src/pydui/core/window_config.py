# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Tuple

from pydui.common.import_gtk import *


@dataclass(frozen=True)
class PyDuiWindowConfig:

    """Window config dataclass

    Attributes:
        title (str): window title
        size (tuple[int, int]): window size, default is (400, 300)
        min_size (tuple[int, int]): window min size, default is (0, 0)
        max_size (tuple[int, int]): window max size, default is (0, 0), when set to zero, means no limit.
        positon (Gtk.WindowPosition): window initial position
        default_font (str): window default font
        default_fontsize (int): window default font size
        default_fontbold (bool): window default font is bold or not
    """

    title: str
    size: Tuple[int, int]
    min_size: Tuple[int, int]
    max_size: Tuple[int, int]
    position: Gtk.WindowPosition = Gtk.WindowPosition.CENTER
    default_font: str = "Arial"
    default_fontsize: int = 16
    default_fontbold: bool = False

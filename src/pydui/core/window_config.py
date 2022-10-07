# -*- coding: utf-8 -*-
from dataclasses import dataclass
from distutils.sysconfig import customize_compiler
from typing import Tuple

from pydui.common.import_gtk import *


@dataclass(frozen=True)
class PyDuiWindowConfig:

    """Window config dataclass"""

    title: str
    size: Tuple[int, int]
    min_size: Tuple[int, int]
    max_size: Tuple[int, int]
    position: Gtk.WindowPosition = Gtk.WindowPosition.CENTER
    default_font: str = "Arial"
    default_fontsize: int = 16
    default_fontbold: bool = False
    customize_titlebar: bool = False
    caption_height: int = 0
    box_size: Tuple[int, int, int, int] = (0, 0, 0, 0)

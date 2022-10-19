# -*- coding: utf-8 -*-
"""PyDui-GTK modules.

core: Core module
    - PyDuiApplication
    - PyDuiBuilder
    - PyDuiWindow, PyDuiWindowHandler
    - PyDuiWidget, PyDuiLayout
    - PyDuiUtils

widgets: Widget module
    - Label, Button, Text, Edit, ...

layout: Layout module
    - HLayout
    - VLayout
    - FixedLayout

"""

from typing import TYPE_CHECKING, List

from . import utils
from .core.application import PyDuiApplication
from .core.builder import PyDuiBuilder
from .core.window import PyDuiWindowInterface
from .core.window_handler import PyDuiWindowHandler

__version__ = "0.1.1"

if TYPE_CHECKING:
    __all__: List[str] = [
        "utils",
        "PyDuiApplication",
        "PyDuiWindowInterface",
        "PyDuiWindowHandler",
        "PyDuiBuilder",
    ]

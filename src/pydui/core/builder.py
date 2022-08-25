# builder.py
from dataclasses import dataclass
from typing import Optional, Type

from pydui.core.widget import *
from pydui.core.window import *


@dataclass(frozen=True)
class PyDuiBuilder:

    @staticmethod
    def build_window_from_path(path: str) -> PyDuiWindowConfig:
        # TODO: load from xml
        return PyDuiWindowConfig(
            title='Hello',
            size=(800, 600),
        )

    @staticmethod
    def build_widget(path: str) -> PyDuiWidget:
        return PyDuiWidget()

    @staticmethod
    def build_window(path: str, handler: Type[PyDuiWindowHandler]) -> PyDuiWindow:
        config = PyDuiBuilder.build_window_from_path(path)
        return PyDuiWindow(config=config, handler=handler)

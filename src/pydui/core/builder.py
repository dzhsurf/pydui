""" PyDuiBuilder module

PyDuiBuilder provider construct Widget from xml resource.
The resource xml file read from local path by default.
But you can custom the resource provider to compose the ui resources.

Example::

    PyDuiBuilder.build_window(path='res/main.xml')


"""
from dataclasses import dataclass
from typing import Optional, Type

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from pydui.core.widget import *
from pydui.core.window import *


@dataclass(frozen=True)
class PyDuiBuilder:

    """Build Widget, Window from xml resource"""

    @staticmethod
    def __build_window_from_path__(path: str) -> PyDuiWindowConfig:

        # TODO: load from xml
        return PyDuiWindowConfig(
            title="Hello",
            size=(800, 600),
        )

    @staticmethod
    def build_widget(path: str) -> PyDuiWidget:
        """Build widget from path

        Args:
            path (str): xml resource path

        Returns:
            PyDuiWidget: return the widget
        """
        return PyDuiWidget()

    @staticmethod
    def build_window(path: str) -> PyDuiWindow:
        """Build window from path and handler

        Args:
            path (str): xml resource path

        Returns:
            PyDuiWindow: return window object.
        """
        config = PyDuiBuilder.__build_window_from_path__(path)
        return PyDuiWindow(config=config)

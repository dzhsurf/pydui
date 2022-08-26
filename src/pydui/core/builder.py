""" PyDuiBuilder module

PyDuiBuilder provider construct Widget from xml resource.
The resource xml file read from local path by default.
But you can custom the resource provider to compose the ui resources.

Example::

    PyDuiBuilder.build_window(path='res/main.xml')


"""
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Optional, Type

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from pydui.core import utils
from pydui.core.widget import *
from pydui.core.window import *


def __process_root_node__(node: ET.Element) -> PyDuiWindowConfig:
    return PyDuiWindowConfig(
        title=node.attrib.get("title", ""),
        size=utils.Str2Size(node.attrib.get("size", "")),
        position=utils.Str2Position(node.attrib.get("position", "")),
    )


def __process_tree_node__(node: ET.Element):
    # node.tag, node.attrib
    pass


def __recursive_tree_node__(node: ET.Element, cb: callable):
    cb(node)
    for child in node:
        __recursive_tree_node__(child, cb)


def __build_window_from_path__(path: str) -> PyDuiWindowConfig:
    tree = ET.parse(path)
    root = tree.getroot()
    config = __process_root_node__(root)
    for child in root:
        __recursive_tree_node__(child, __process_tree_node__)

    return config


@dataclass(frozen=True)
class PyDuiBuilder:

    """Build Widget, Window from xml resource"""

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
        config = __build_window_from_path__(path)
        return PyDuiWindow(config=config)

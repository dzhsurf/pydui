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
from pydui.core.layout import *
from pydui.core.widget import *
from pydui.core.window import *
from pydui.layout.fit_layout import *
from pydui.layout.fixed_layout import *
from pydui.layout.hlayout import *
from pydui.layout.vlayout import *


def __process_root_node__(node: ET.Element) -> PyDuiWindowConfig:
    return PyDuiWindowConfig(
        title=node.attrib.get("title", ""),
        size=utils.Str2Size(node.attrib.get("size", "400,300")),
        min_size=utils.Str2Size(node.attrib.get("min_size", "0,0")),
        max_size=utils.Str2Size(node.attrib.get("min_size", "0,0")),
        position=utils.Str2Position(node.attrib.get("position", "CENTER")),
    )


def __process_HLayout__(attrib: dict[str, str]) -> PyDuiHLayout:
    return PyDuiHLayout()


def __process_VLayout__(attrib: dict[str, str]) -> PyDuiVLayout:
    return PyDuiVLayout()


def __process_FixedLayout__(attrib: dict[str, str]) -> PyDuiFixedLayout:
    return PyDuiFixedLayout()


def __process_FitLayout__(attrib: dict[str, str]) -> PyDuiFitLayout:
    return PyDuiFitLayout()


def __process_Label__(attrib: dict[str, str]) -> PyDuiWidget:
    return PyDuiWidget()


def __process_Button__(attrib: dict[str, str]) -> PyDuiWidget:
    return PyDuiWidget()


def __process_tree_node__(node: ET.Element) -> PyDuiWidget:

    logging.debug(f"node {node.tag}: {node.attrib}")
    tag = node.tag
    attrib = node.attrib

    def build_gtk_widget():
        layout_table = {
            "HLayout": __process_HLayout__,
            "VLayout": __process_VLayout__,
            "FixedLayout": __process_FixedLayout__,
            "FitLayout": __process_FitLayout__,
        }
        if tag in layout_table:
            return layout_table[tag](attrib)
        internal_widget_table = {
            "Label": __process_Label__,
            "Button": __process_Button__,
        }
        if tag in internal_widget_table:
            return internal_widget_table[tag](attrib)
        # TODO: handle custom user define widget
        return PyDuiWidget()

    result = build_gtk_widget()
    result.parse_attrib(attrib)
    return result


def __recursive_tree_node__(node: ET.Element, parent_widget: PyDuiLayout, cb: callable):
    child_widget = cb(node)
    if parent_widget is not None:
        parent_widget.add_child(child_widget)
    for child in node:
        __recursive_tree_node__(node=child, parent_widget=child_widget, cb=cb)


def __build_window_from_path__(path: str) -> (PyDuiWindowConfig, PyDuiWidget):
    tree = ET.parse(path)
    root = tree.getroot()
    config = __process_root_node__(root)
    root_widget = PyDuiVLayout()
    for child in root:
        __recursive_tree_node__(
            node=child,
            parent_widget=root_widget,
            cb=__process_tree_node__,
        )
        # Notice: Only handle first node from root.
        break

    return (config, root_widget)


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
        config, root_widget = __build_window_from_path__(path)
        window = PyDuiWindow(config=config, rootview=root_widget)
        return window

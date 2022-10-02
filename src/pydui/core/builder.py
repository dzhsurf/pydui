# -*- coding: utf-8 -*-
""" PyDuiBuilder module

PyDuiBuilder provider construct Widget from xml resource.
The resource xml file read from local path by default.
But you can custom the resource provider to compose the ui resources.

Example::

    PyDuiBuilder.build_window(path='res/main.xml')


"""
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Callable, Tuple, Type, Union

from pydui import utils
from pydui.core.import_gtk import *
from pydui.core.layout import *
from pydui.core.resource_loader import PyDuiResourceLoader
from pydui.core.widget import *
from pydui.core.window import *
from pydui.layout.fixed_layout import PyDuiFixedLayout
from pydui.layout.hlayout import PyDuiHLayout
from pydui.layout.pglayout import PyDuiPGLayout
from pydui.layout.vlayout import PyDuiVLayout
from pydui.widgets.pgview import PyDuiPGView
from pydui.widgets.button import PyDuiButton
from pydui.widgets.edit import PyDuiEdit
from pydui.widgets.icon import PyDuiIcon
from pydui.widgets.label import PyDuiLabel
from pydui.widgets.picture import PyDuiPicture

INTERNAL_WIDGET_LIST = [
    PyDuiPGView,
    PyDuiHLayout,
    PyDuiVLayout,
    PyDuiPGLayout,
    PyDuiFixedLayout,
    PyDuiLabel,
    PyDuiButton,
    PyDuiPicture,
    PyDuiEdit,
]
INTERNAL_WIDGET_TABLE = dict[str, Any]()
INTERNAL_WIDGET_INIT = False


class __PyDuiResourceProvider__(PyDuiResourceLoader):

    __loaders: list[PyDuiResourceLoader] = None

    def __init__(self):
        super().__init__()
        self.__loaders = list()

    def scheme(self) -> str:
        return "__resource_provider__"

    def clear_loaders(self):
        self.__loaders.clear()

    def register_loader(self, loader: PyDuiResourceLoader):
        self.__loaders.append(loader)

    def load_xml(self, path: str) -> str:
        for loader in self.__loaders:
            v = loader.load_xml(path)
            if v is not None:
                return v
        return None

    def load_data(self, path: str) -> bytes:
        for loader in self.__loaders:
            v = loader.load_data(path)
            if v is not None:
                return v
        return None

    def load_image(self, path: str) -> Tuple[bytes, float]:
        for loader in self.__loaders:
            v = loader.load_image(path)
            if v is not None:
                return v
        return None

    def load_string(self, path: str) -> str:
        for loader in self.__loaders:
            v = loader.load_string(path)
            if v is not None:
                return v
        return None


class PyDuiBuilder:

    """Build Widget, Window from xml resource"""

    __resource_provider: __PyDuiResourceProvider__ = None

    def __init__(self):
        self.__resource_provider = __PyDuiResourceProvider__()

    def register_resource_loader(self, loader: PyDuiResourceLoader):
        self.__resource_provider.register_loader(loader)

    def get_loader(self) -> PyDuiResourceLoader:
        return self.__resource_provider

    def build_widget(self, path: str) -> PyDuiWidget:
        """Build widget from path

        Args:
            path (str): xml resource path

        Returns:
            PyDuiWidget: return the widget
        """
        return PyDuiWidget()

    def build_window(self, path: str, handler: Type[PyDuiWindowHandler]) -> PyDuiWindow:
        """Build window from path and handler

        Args:
            path (str): xml resource path
            handler (Type[PyDuiWindowHandler]): handler class

        Returns:
            PyDuiWindow: return window object.
        """
        config, root_widget = self.__build_window_from_path__(path)
        # render_manager = PyDuiRenderManager(window, loader)
        window = PyDuiWindow(
            loader=self.__resource_provider,
            config=config,
            rootview=root_widget,
            handler=handler,
        )
        return window

    def __build_window_from_path__(self, path: str) -> Tuple[Union[PyDuiWindowConfig, None], PyDuiWidget]:
        xml_content = self.__resource_provider.load_xml(path)
        if xml_content is None:
            logging.error(f"load xml fail. path not exist. path = {path}")
            return (None, PyDuiWidget())
        # syslog.syslog(syslog.LOG_ALERT, f"xml len {len(xml_content)}, path = {path}")
        # tree = ET.parse(path)
        # root = tree.getroot()
        root = ET.fromstring(xml_content)
        config = self.__process_root_node__(root)
        root_widget = PyDuiVLayout(None)
        for child in root:
            self.__recursive_tree_node__(
                node=child,
                parent_widget=root_widget,
                cb=self.__process_tree_node__,
            )
            # Notice: Only handle first node from root.
            break

        return (config, root_widget)

    def __process_root_node__(self, node: ET.Element) -> PyDuiWindowConfig:
        return PyDuiWindowConfig(
            title=node.attrib.get("title", ""),
            size=utils.Str2Size(node.attrib.get("size", "400,300")),
            min_size=utils.Str2Size(node.attrib.get("min_size", "0,0")),
            max_size=utils.Str2Size(node.attrib.get("min_size", "0,0")),
            position=utils.Str2Position(node.attrib.get("position", "CENTER")),
            default_font=node.attrib.get("default_font", "Arial"),
            default_fontsize=int(node.attrib.get("default_fontsize", "16")),
            default_fontbold=node.attrib.get("default_fontbold", "false") == "true",
        )

    def __process_tree_node__(self, node: ET.Element, parent_widget: PyDuiLayout) -> PyDuiWidget:
        logging.debug(f"Builder parse node, Key: {node.tag} Value: {node.attrib}")
        tag = node.tag
        attrib = node.attrib

        def build_gtk_widget():
            global INTERNAL_WIDGET_INIT, INTERNAL_WIDGET_TABLE, INTERNAL_WIDGET_LIST
            if not INTERNAL_WIDGET_INIT:
                INTERNAL_WIDGET_INIT = True
                for widget_cls in INTERNAL_WIDGET_LIST:
                    name = widget_cls.build_name()
                    INTERNAL_WIDGET_TABLE[name] = widget_cls
                logging.info(f"Initial internal widget classes. count = {len(INTERNAL_WIDGET_TABLE)}")
                logging.info(f"Internal widget classes: {INTERNAL_WIDGET_TABLE.keys()}")
            if tag in INTERNAL_WIDGET_TABLE:
                return INTERNAL_WIDGET_TABLE[tag](parent_widget)
            # TODO: handle custom user define widget
            return PyDuiWidget(parent_widget)

        result = build_gtk_widget()
        if parent_widget is not None:
            parent_widget.add_child(result)
        result.parse_attributes(attrib)
        return result

    def __recursive_tree_node__(
        self, node: ET.Element, parent_widget: PyDuiLayout, cb: Callable[[ET.Element, PyDuiLayout], PyDuiWidget]
    ):
        child_widget = cb(node, parent_widget)
        for child in node:
            self.__recursive_tree_node__(child, child_widget, cb)

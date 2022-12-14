# -*- coding: utf-8 -*-
""" PyDuiBuilder module

PyDuiBuilder provider construct Widget from xml resource.
The resource xml file read from local path by default.
But you can custom the resource provider to compose the ui resources.

Example::

    PyDuiBuilder.build_window(path='res/main.xml')


"""
import xml.etree.ElementTree as ET
from typing import Callable, Tuple, Type

from pydui import utils
from pydui.common.import_gtk import *
from pydui.core.layout import *
from pydui.core.resource_loader import PyDuiResourceLoader
from pydui.core.widget import *
from pydui.core.window import PyDuiWindow
from pydui.core.window_config import PyDuiWindowConfig
from pydui.core.window_handler import PyDuiWindowHandler
from pydui.layout.hlayout import PyDuiHLayout
from pydui.layout.pglayout import PyDuiPGLayout
from pydui.layout.scrolled_layout import PyDuiFitLayout, PyDuiScrolledLayout
from pydui.layout.vlayout import PyDuiVLayout
from pydui.widgets.button import PyDuiButton
from pydui.widgets.edit import PyDuiEdit
from pydui.widgets.label import PyDuiLabel
from pydui.widgets.listview import PyDuiListView
from pydui.widgets.pgview import PyDuiPGView
from pydui.widgets.picture import PyDuiPicture

INTERNAL_WIDGET_LIST = [
    PyDuiPGView,
    PyDuiHLayout,
    PyDuiVLayout,
    PyDuiPGLayout,
    PyDuiScrolledLayout,
    PyDuiFitLayout,
    PyDuiLabel,
    PyDuiButton,
    PyDuiPicture,
    PyDuiEdit,
    PyDuiListView,
]
INTERNAL_WIDGET_TABLE: Dict[str, Any] = {}
g_internal_widget_init = False


class __PyDuiResourceProvider__(PyDuiResourceLoader):
    def __init__(self):
        super().__init__()
        self.__loaders: List[PyDuiResourceLoader] = []

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
        return ""

    def load_data(self, path: str) -> bytes:
        for loader in self.__loaders:
            v = loader.load_data(path)
            if v is not None:
                return v
        return bytes()

    def load_image(self, path: str) -> Tuple[bytes, float]:
        for loader in self.__loaders:
            v = loader.load_image(path)
            if v is not None:
                return v
        return (bytes(), 0)

    def load_string(self, sid: str) -> str:
        for loader in self.__loaders:
            v = loader.load_string(sid)
            if v is not None:
                return v
        return ""


class PyDuiBuilder:

    """Build Widget, Window from xml resource"""

    def __init__(self):
        self.__resource_provider: __PyDuiResourceProvider__ = __PyDuiResourceProvider__()

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
        # build widget from xml
        config, root_widget = self.__build_window_from_path__(path)
        # create window
        window = PyDuiWindow(
            loader=self.__resource_provider,
            config=config,
            rootview=root_widget,
            handler=handler,
        )
        return window

    def __build_window_from_path__(self, path: str) -> Tuple[PyDuiWindowConfig, PyDuiLayout]:
        xml_content = self.__resource_provider.load_xml(path)
        if xml_content is None or len(xml_content) == 0:
            logging.error(f"load xml fail. path not exist. path = {path}")
            return (
                PyDuiWindowConfig(
                    title="",
                    size=(400, 300),
                    min_size=(0, 0),
                    max_size=(0, 0),
                    position=Gtk.WindowPosition.CENTER,
                ),
                PyDuiVLayout(),
            )
        # syslog.syslog(syslog.LOG_ALERT, f"xml len {len(xml_content)}, path = {path}")
        # tree = ET.parse(path)
        # root = tree.getroot()
        root = ET.fromstring(xml_content)
        config = self.__process_root_node__(root)
        root_widget = PyDuiVLayout()
        # root_widget.bkcolor = utils.Str2Color("#00FFFFFF")
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
            size=utils.Str2SizeInt(node.attrib.get("size", "400,300")),
            min_size=utils.Str2SizeInt(node.attrib.get("min_size", "0,0")),
            max_size=utils.Str2SizeInt(node.attrib.get("min_size", "0,0")),
            position=utils.Str2Position(node.attrib.get("position", "CENTER")),
            default_font=node.attrib.get("default_font", "Arial"),
            default_fontsize=int(node.attrib.get("default_fontsize", "16")),
            default_fontbold=node.attrib.get("default_fontbold", "false") == "true",
            customize_titlebar=node.attrib.get("customize_titlebar", "false") == "true",
            caption_height=int(node.attrib.get("caption_height", "24")),
            box_size=utils.Str2Edge(node.attrib.get("box_size", "4,4,4,4")),
        )

    def __process_tree_node__(self, node: ET.Element, parent_widget: PyDuiLayout) -> PyDuiWidget:
        logging.debug(f"Builder parse node, Key: {node.tag} Value: {node.attrib}")
        tag = node.tag
        attrib = node.attrib

        def build_gtk_widget():
            global g_internal_widget_init, INTERNAL_WIDGET_TABLE, INTERNAL_WIDGET_LIST
            if not g_internal_widget_init:
                g_internal_widget_init = True
                for widget_cls in INTERNAL_WIDGET_LIST:
                    name = widget_cls.build_name()
                    INTERNAL_WIDGET_TABLE[name] = widget_cls
                logging.info(f"Initial internal widget classes. count = {len(INTERNAL_WIDGET_TABLE)}")
                logging.info(f"Internal widget classes: {INTERNAL_WIDGET_TABLE.keys()}")
            if tag in INTERNAL_WIDGET_TABLE:
                return INTERNAL_WIDGET_TABLE[tag]()
            # TODO: handle custom user define widget
            return PyDuiWidget()

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
            if isinstance(child_widget, PyDuiLayout):
                self.__recursive_tree_node__(child, child_widget, cb)
            else:
                raise ValueError("Widget is not a Layout.")

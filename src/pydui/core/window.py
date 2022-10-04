# -*- coding: utf-8 -*-
from typing import Type

from pydui.common.import_gtk import *
from pydui.component.embedded_widget import PyDuiEmbeddedWidgetHost
from pydui.core.layout import *
from pydui.core.resource_loader import PyDuiResourceLoader
from pydui.core.widget import *
from pydui.core.window_client import PyDuiWindowClient
from pydui.core.window_config import PyDuiWindowConfig
from pydui.core.window_handler import PyDuiWindowHandler
from pydui.core.window_interface import PyDuiWindowInterface
from pydui.core.window_provider import PyDuiWindowProvider
from pydui.provider.window_provider_gtk3 import PyDuiWindowProviderGTK3


class PyDuiWindow(PyDuiWindowInterface):
    """PyDuiWindow"""

    __provider: PyDuiWindowProvider = None
    __client: PyDuiWindowClient = None

    def __init__(
        self,
        loader: Type[PyDuiResourceLoader],
        config: PyDuiWindowConfig,
        rootview: PyDuiWidget,
        handler: Type[PyDuiWindowHandler] = None,
    ):
        super().__init__()
        self.__provider = None

        # Init window client
        self.__client = PyDuiWindowClient(
            window=self,
            config=config,
            loader=loader,
            rootview=rootview,
            handler=handler,
        )

    # PyDuiWindowInterface implement
    def get_widget(self, widget_id: str) -> PyDuiWidget:
        return self.__client.get_widget(widget_id=widget_id)

    def execute_platform_code(self, cb: Callable[[Any], None]):
        # TODO: remove it later
        if cb is None:
            return
        cb(self.get_window_provider()._PyDuiWindowProviderGTK3__gtk_window)

    def create_embedded_widget(self, widget_typename: str) -> PyDuiEmbeddedWidgetHost:
        provider = self.get_embedded_widget_provider()
        if provider is None:
            return None
        return provider.create_embedded_widget(widget_typename)

    def get_window_provider(self) -> PyDuiWindowProvider:
        if self.__provider is None:
            self.__provider = PyDuiWindowProviderGTK3()

        return self.__provider

    def show(self):
        self.get_window_provider().show()

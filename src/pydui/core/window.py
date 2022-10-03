# -*- coding: utf-8 -*-
from __future__ import annotations

import imp
import logging
from dataclasses import dataclass
from typing import Type

from pydui.core.import_gtk import *
from pydui.core.layout import *
from pydui.core.resource_loader import PyDuiResourceLoader
from pydui.core.widget import *
from pydui.core.window_base import PyDuiWindowBase
from pydui.core.window_client import PyDuiWindowClient
from pydui.core.window_config import PyDuiWindowConfig
from pydui.core.window_handler import PyDuiWindowHandler


class PyDuiWindow(PyDuiWindowBase):

    """Window object"""

    # window backend
    __gtk_window: Gtk.Window = None

    # client
    __client: PyDuiWindowClient = None

    def __init__(
        self,
        loader: Type[PyDuiResourceLoader],
        config: PyDuiWindowConfig,
        rootview: PyDuiWidget,
        handler: Type[PyDuiWindowHandler] = None,
    ):
        # Init Gtk Window
        self.__gtk_window = Gtk.Window()
        # TODO: custom window style
        # self.__gtk_window.set_decorated(False)

        # Init window client
        self.__client = PyDuiWindowClient(
            window=self,
            config=config,
            loader=loader,
            rootview=rootview,
            handler=handler,
        )

    def get_gtk_window(self):
        return self.__gtk_window

    def show(self):
        self.__gtk_window.show_all()

    def get_widget(self, widget_id: str) -> PyDuiWidget:
        return self.__client.get_widget(widget_id=widget_id)

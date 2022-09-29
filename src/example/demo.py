# -*- coding: utf-8 -*-
import threading

from pynoticenter import PyNotiCenter

import pydui
from pydui import *
from pydui.core.import_gtk import *
from pydui.core.resource_loader import create_default_resource_loader


# config builder here
def get_builder() -> PyDuiBuilder:
    builder = PyDuiBuilder()
    builder.register_resource_loader(create_default_resource_loader())
    return builder


# custom window handler
class DemoHandler(PyDuiWindowHandler):
    def on_window_init(self, window: PyDuiWindowBase):
        print(f"on_window_init")

    def on_window_destroy(self):
        print(f"on_window_destroy")
        PyDuiApplication.main_quit()


def main():
    print(f"start pydui version: {pydui.__version__}")

    window = get_builder().build_window(path="res/main_poga.xml", handler=DemoHandler)
    window.show()

    PyDuiApplication.main_run()
    PyNotiCenter.default().shutdown(True)


if __name__ == "__main__":
    main()

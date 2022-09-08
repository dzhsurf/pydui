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

        def handle_lclick(object: PyDuiWidget, x: float, y: float) -> bool:
            print("lclick")
            return False

        def handle_l2click(object: PyDuiWidget, x: float, y: float) -> bool:
            print("l2click")
            return False

        def handle_rclick(object: PyDuiWidget, x: float, y: float) -> bool:
            print("rclick")
            return False

        def handle_r2click(object: PyDuiWidget, x: float, y: float) -> bool:
            print("r2click")
            return False

        widget = window.get_widget(widget_id="button")
        widget.connect("lclick", handle_lclick)
        widget.connect("l2click", handle_l2click)
        widget.connect("rclick", handle_rclick)
        widget.connect("r2click", handle_r2click)

    def on_window_destroy(self):
        print(f"on_window_destroy")
        PyDuiApplication.main_quit()


def main():
    print(f"start pydui version: {pydui.__version__}")

    window = get_builder().build_window(path="res/main.xml", handler=DemoHandler)
    window.show()

    PyDuiApplication.main_run()
    PyNotiCenter.default().shutdown(True)


if __name__ == "__main__":
    main()

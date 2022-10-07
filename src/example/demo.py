# -*- coding: utf-8 -*-
import os
import pathlib
import threading

from poga.libpoga_capi import poga_version
from pynoticenter import PyNotiCenter

import platform
if platform.system() == "Windows":
    try:
        from pygobject_prebuilt_deps import import_pygobject_dll_module
        import_pygobject_dll_module()
    except ImportError:
        pass

import pydui
from pydui import *
from pydui.common.import_gtk import *
from pydui.core.resource_loader import create_default_resource_loader

# setup logger
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [stdout_handler]
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
    handlers=handlers,
)
logger = logging.getLogger(__name__)


# config builder here
def get_builder() -> PyDuiBuilder:
    builder = PyDuiBuilder()
    builder.register_resource_loader(create_default_resource_loader())
    return builder


# custom window handler
class DemoHandler(PyDuiWindowHandler):
    def on_window_init(self, window: PyDuiWindowInterface):
        print(f"on_window_init")

    def on_window_destroy(self):
        print(f"on_window_destroy")
        PyDuiApplication.main_quit()


def main():
    print(f"start pydui version: {pydui.__version__}")
    print(f"Poga version: {poga_version()}")

    # change current working directory
    os.chdir(pathlib.Path(__file__).parent)

    window = get_builder().build_window(path="res/main_poga.xml", handler=DemoHandler)
    window.show()

    PyDuiApplication.main_run()
    PyNotiCenter.default().shutdown(True)


if __name__ == "__main__":
    main()

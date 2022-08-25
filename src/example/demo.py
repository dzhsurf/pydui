import logging

import pydui
from pydui import *

class DemoWindowHandler(PyDuiWindowHandler):
    def __init__(self, window: PyDuiWindow):
        super().__init__(window=window)

    def on_window_show(self):
        logging.info(f"on_window_show")
        window = self.window()
        widget = window.get_widget(widget_id="button")
        print(window, widget)

    def on_window_destroy(self):
        logging.info(f"on_window_destroy")
        PyDuiApplication.main_quit()


def main():
    logging.info(f"start pydui version: {pydui.__version__}")
    print(type(DemoWindowHandler))
    window = PyDuiBuilder.build_window(
        path="res/main.xml",
        handler=DemoWindowHandler,
    )
    window.show()

    PyDuiApplication.main_run()


if __name__ == "__main__":
    main()

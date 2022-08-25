import pydui
from pydui import *


class DemoWindowHandler(PyDuiWindowHandler):
    def __init__(self, window: PyDuiWindow):
        super().__init__(window=window)

    def on_window_show(self):
        print(f"on_window_show")
        window = self.window()
        widget = window.get_widget(widget_id="button")

        def handle_click(object):
            print("You clicked!", object)

        widget.connect("clicked", handle_click)

    def on_window_destroy(self):
        print(f"on_window_destroy")
        PyDuiApplication.main_quit()


def main():
    print(f"start pydui version: {pydui.__version__}")

    window = PyDuiBuilder.build_window(
        path="res/main.xml",
        handler=DemoWindowHandler,
    )
    window.show()

    PyDuiApplication.main_run()


if __name__ == "__main__":
    main()

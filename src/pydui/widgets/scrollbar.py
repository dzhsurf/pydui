from typing import List
from pydui import utils
from pydui.common.base import PyDuiLayoutConstraint
from pydui.common.import_gtk import *
from pydui.core.layout import PyDuiLayout
from pydui.core.widget import PyDuiWidget
from pydui.widgets.button import PyDuiButton


class PyDuiScrollbar(PyDuiLayout):
    """PyDuiScrollbar"""

    __scroller: PyDuiButton = None
    __press_x: float = 0
    __press_y: float = 0
    __scroller_x: float = 0
    __scroller_y: float = 0

    @staticmethod
    def build_name() -> str:
        return "Scrollbar"

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)
        self.__scroller = PyDuiButton(parent)
        self.__scroller.bkimage = "res/images/vscroller.png"
        self.__scroller.bkimage_hover = "res/images/vscroller_hover.png"
        self.__scroller.bkimage_press = "res/images/vscroller_press.png"
        self.__scroller.corner = (3, 3, 3, 3)
        self.__scroller.fixed_width = 7
        self.add_child(self.__scroller)
        self.fixed_width = self.__scroller.fixed_width + 4
        self.__scroller.bind_event("lbutton-press", self.__on_lbutton_press__)
        self.__scroller.bind_event("lbutton-release", self.__on_lbutton_release__)

    def on_post_init(self):
        super().on_post_init()

    def update_scroller(self, width: float, height: float):
        # vscroller
        self.__scroller.fixed_x = self.__scroller_x + 2
        self.__scroller.fixed_y = self.__scroller_y + 2
        self.__scroller.fixed_height = height

    def draw(self, ctx: cairo.Context, x: float, y: float, width: float, height: float):
        super().draw(ctx, x, y, width, height)
        self.__scroller.draw(ctx, self.__scroller.x, self.__scroller.y, self.__scroller.width, self.__scroller.height)

    def layout(self, x: float, y: float, width: float, height: float, constraint: PyDuiLayoutConstraint):
        super().layout(x, y, width, height, constraint)
        self.__scroller.layout(
            self.x + self.__scroller.fixed_x,
            self.y + self.__scroller.fixed_y,
            self.__scroller.fixed_width,
            self.__scroller.fixed_height,
            constraint=PyDuiLayoutConstraint(),
        )

    # properties
    @property
    def scroll_position(self) -> float:
        return self.__scroller_y

    # events
    def get_signals(self) -> List[str]:
        signals = super().get_signals()
        signals.extend['vscroll-changed', 'hscroll-changed']
        return signals

    # private
    def __on_lbutton_press__(self, widget: PyDuiWidget, x: float, y: float) -> bool:
        self.__press_x = x
        self.__press_y = y
        self.get_window_client().add_event_observer("mouse-move", self.__on_mouse_move__)
        return False

    def __on_lbutton_release__(self, widget: PyDuiWidget, x: float, y: float) -> bool:
        self.__press_x = 0
        self.__press_y = 0
        self.get_window_client().remove_event_observer("mouse-move", self.__on_mouse_move__)
        return False

    def __on_mouse_move__(self, x: float, y: float):
        dx, dy = x - self.__press_x, y - self.__press_y
        self.__scroll_to__(dx, dy)
        self.__press_x = x
        self.__press_y = y

    def __scroll_to__(self, dx: float, dy: float):
        self.__scroller_y += dy
        self.__scroller_y = max(0, self.__scroller_y)
        self.__scroller_y = min(self.height - self.__scroller.height, self.__scroller_y)
        self.__scroller.fixed_y = self.__scroller_y + 2
        self.emit('vscroll-changed', self.scroll_position)
        # TODO, set needupdate, invalidrect
        self.get_window_client().notify_redraw()

import random

import gi

from pydui.core.layout import *
from pydui.core.widget import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk


class PyDuiHLayout(PyDuiLayout):
    """Horizontal layout"""

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent, PyDuiLayoutEnum.HLayout)

    def layout(self, x: int, y: int, width: int, height: int):
        super().layout(x, y, width, height)

        layout_info_list = []
        auto_expand_count = 0

        # estimate children width
        valiable_width, valiable_height = width, height
        for i in range(self.child_count):
            child = self.get_child_at(i)

            estimate_size = child.estimate_size(valiable_width, valiable_height)
            estimate_w = estimate_size[0]
            if estimate_w != 0:
                layout_info_list.append(estimate_w)
                valiable_width = valiable_width - estimate_w
                if valiable_width <= 0:
                    valiable_width = 0
            else:
                # mark auto expand child
                layout_info_list.append(0)
                auto_expand_count += 1

        auto_expand_w = 0
        if auto_expand_count > 0:
            auto_expand_w = valiable_width // auto_expand_count

        # layout children
        for i in range(len(layout_info_list)):
            child = self.get_child_at(i)
            w = layout_info_list[i]
            if w != 0:
                child.layout(x, y, w, height)
                x = x + w
            else:
                child.layout(x, y, auto_expand_w, height)
                x = x + auto_expand_w

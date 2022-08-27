import gi

from pydui.core.layout import *
from pydui.core.widget import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk


class PyDuiVLayout(PyDuiLayout):

    """Vertical layout"""

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent, PyDuiLayoutEnum.VLayout)
        # self.set_gtk_widget(Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0))
        # self.set_gtk_widget(Gtk.VBox(False, 0))

    def layout(self, width: int, height: int):
        super().layout(width, height)

        layout_info_list = []
        auto_expand_count = 0

        # estimate children width
        valiable_width, valiable_height = width, height
        for i in range(self.child_count):
            child = self.get_child_at(i)

            estimate_size = child.estimate_size(valiable_width, valiable_height)
            estimate_h = estimate_size[1]
            if estimate_h != 0:
                layout_info_list.append(estimate_h)
                valiable_height = valiable_height - estimate_h
                if valiable_height <= 0:
                    valiable_height = 0
            else:
                # mark auto expand child
                layout_info_list.append(0)
                auto_expand_count += 1

        auto_expand_h = 0
        if auto_expand_count > 0:
            auto_expand_h = valiable_height // auto_expand_count

        # layout children
        for i in range(len(layout_info_list)):
            child = self.get_child_at(i)
            h = layout_info_list[i]
            if h != 0:
                child.layout(width, h)
            else:
                child.layout(width, auto_expand_h)

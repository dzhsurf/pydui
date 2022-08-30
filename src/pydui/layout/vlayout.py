import math

import gi

from pydui.core.layout import *
from pydui.core.widget import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk


class PyDuiVLayout(PyDuiLayout):

    """Vertical layout"""

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent, PyDuiLayoutEnum.VLayout)

    def draw(
        self,
        ctx: cairo.Context,
        x: float,
        y: float,
        width: float,
        height: float,
        canvas_width: float,
        canvas_height: float,
    ):
        super().draw(ctx, x, y, width, height, canvas_width, canvas_height)
        auto_expand_count = self.__auto_expand_count__()
        auto_expand_idx = 0
        last_draw_y = None
        for i in range(self.child_count):
            child = self.get_child_at(i)
            draw_x, draw_w, draw_h = child.x, child.width, child.height
            draw_y = child.y
            if last_draw_y is not None:
                draw_y = last_draw_y + child.margin[1]
            # if is last expand child
            if int(child.fixed_height) == 0:
                auto_expand_idx += 1
                if auto_expand_idx == auto_expand_count:
                    if i < self.child_count - 1:
                        next_child = self.get_child_at(i + 1)
                        draw_h = next_child.y - next_child.margin[1] - child.margin[3] - draw_y
                    else:
                        draw_h = y + height - child.margin[3] - draw_y
            child.draw(ctx, draw_x, draw_y, draw_w, draw_h, canvas_width, canvas_height)
            last_draw_y = draw_y + draw_h + child.margin[3]

    def layout(self, x: float, y: float, width: float, height: float):
        super().layout(x, y, width, height)

        # estimate children height
        estimate_layout_result = self.__estimate_children_height__(width, height)

        # layout children
        auto_layout_idx = 0
        layout_x, layout_y = x, y
        for i in range(self.child_count):
            child = self.get_child_at(i)
            margin = child.margin
            margin_w, margin_h = utils.RectW(margin), utils.RectH(margin)
            child_w = width - margin_w
            child_h = estimate_layout_result.estimate_items[i]

            # is auto layout
            if int(child_h) == 0:
                auto_layout_idx += 1
                child_h = estimate_layout_result.auto_layout_value
                if auto_layout_idx == estimate_layout_result.auto_layout_count:
                    child_h = (
                        y + height - self.get_children_range_fixed_height(i + 1, self.child_count) - layout_y - margin_h
                    )

            child.layout(layout_x + margin[0], layout_y + margin[1], child_w, child_h)
            layout_y = layout_y + child_h + margin_h

    def __auto_expand_count__(self):
        count = 0
        for i in range(self.child_count):
            child = self.get_child_at(i)
            if int(child.fixed_height) == 0:
                count += 1
        return count

    def __estimate_children_height__(self, width: int, height: int) -> PyDuiLayoutEstimateResult:
        # estimate children height
        estimate_items_height = []
        auto_layout_count = 0
        valiable_width, valiable_height = width, height
        for i in range(self.child_count):
            child = self.get_child_at(i)
            margin = child.margin
            estimate_size = child.estimate_size(valiable_width, valiable_height)
            estimate_h = round(estimate_size[1])
            if estimate_h != 0:
                estimate_items_height.append(estimate_h)
            else:
                # mark auto layout child
                estimate_items_height.append(0)
                auto_layout_count += 1

            valiable_height = valiable_height - estimate_h - utils.RectH(margin)
            if valiable_height <= 0:
                valiable_height = 0

        return PyDuiLayoutEstimateResult(
            auto_layout_count=auto_layout_count,
            auto_layout_value=round(valiable_height / auto_layout_count) if auto_layout_count > 0 else 0,
            estimate_items=estimate_items_height,
        )

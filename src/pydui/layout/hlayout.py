import math
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
        last_draw_x = None
        for i in range(self.child_count):
            child = self.get_child_at(i)
            draw_y, draw_w, draw_h = child.y, child.width, child.height
            draw_x = child.x
            if last_draw_x is not None:
                draw_x = last_draw_x + child.margin[0]
            # if is last expand child
            if int(child.fixed_width) == 0:
                auto_expand_idx += 1
                if auto_expand_idx == auto_expand_count:
                    if i < self.child_count - 1:
                        next_child = self.get_child_at(i + 1)
                        draw_w = next_child.x - next_child.margin[0] - draw_x - child.margin[2]
                    else:
                        draw_w = x + width - draw_x - child.margin[2]
            child.draw(ctx, draw_x, draw_y, draw_w, draw_h, canvas_width, canvas_height)
            last_draw_x = draw_x + draw_w + child.margin[2]

    def layout(self, x: float, y: float, width: float, height: float):
        super().layout(x, y, width, height)

        # estimate children height
        estimate_layout_result = self.__estimate_children_width__(width, height)

        # layout children
        auto_layout_idx = 0
        layout_x, layout_y = x, y
        for i in range(self.child_count):
            child = self.get_child_at(i)
            margin = child.margin
            margin_w, margin_h = utils.RectW(margin), utils.RectH(margin)
            child_w = estimate_layout_result.estimate_items[i]
            child_h = height - margin_h

            # is auto layout
            if int(child_w) == 0:
                auto_layout_idx += 1
                child_w = estimate_layout_result.auto_layout_value
                if auto_layout_idx == estimate_layout_result.auto_layout_count:
                    child_w = (
                        x + width - self.get_children_range_fixed_width(i + 1, self.child_count) - layout_x - margin_w
                    )

            child.layout(layout_x + margin[0], layout_y + margin[1], child_w, child_h)
            layout_x = layout_x + child_w + margin_h

    def __auto_expand_count__(self):
        count = 0
        for i in range(self.child_count):
            child = self.get_child_at(i)
            if int(child.fixed_width) == 0:
                count += 1
        return count

    def __estimate_children_width__(self, width: int, height: int) -> PyDuiLayoutEstimateResult:
        # estimate children width
        estimate_items_width = []
        auto_layout_count = 0
        valiable_width, valiable_height = width, height
        for i in range(self.child_count):
            child = self.get_child_at(i)
            margin = child.margin
            estimate_size = child.estimate_size(valiable_width, valiable_height)
            estimate_w = estimate_size[0]
            if estimate_w != 0:
                estimate_items_width.append(estimate_w)
            else:
                # mark auto layout child
                estimate_items_width.append(0)
                auto_layout_count += 1

            valiable_width = valiable_width - estimate_w - utils.RectW(margin)
            if valiable_width <= 0:
                valiable_width = 0

        return PyDuiLayoutEstimateResult(
            auto_layout_count=auto_layout_count,
            auto_layout_value=round(valiable_width / auto_layout_count) if auto_layout_count > 0 else 0,
            estimate_items=estimate_items_width,
        )

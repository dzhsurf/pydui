# -*- coding: utf-8 -*-
import math
from typing import Tuple

from pydui import utils
from pydui.core.import_gtk import *
from pydui.core.layout import *
from pydui.core.widget import *


class PyDuiVLayout(PyDuiLayout):

    """Vertical layout"""

    @staticmethod
    def build_name() -> str:
        return "VLayout"

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)

    def draw(
        self,
        ctx: cairo.Context,
        x: float,
        y: float,
        width: float,
        height: float,
    ):
        super().draw(ctx, x, y, width, height)
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
            ctx.save()
            child.draw(ctx, draw_x, draw_y, draw_w, draw_h)
            ctx.restore()
            last_draw_y = draw_y + draw_h + child.margin[3]

    def __get_fitrule__(self) -> Tuple[bool, bool]:
        fit_v, fit_h = False, False
        if self.autofit:
            if not "v" in self.fitrule and not "h" in self.fitrule:
                fit_h = True
        return (fit_v, fit_h)

    def estimate_size(
        self, parent_width: float, parent_height: float, constaint: PyDuiLayoutConstraint
    ) -> Tuple[float, float]:
        if not self.autofit:
            return super().estimate_size(parent_width, parent_height, constaint)

        # autofit
        fit_w, fit_h = self.__get_fitrule__()

        layout_max_w, layout_max_h = parent_width, parent_height
        layout_max_w = max(0, layout_max_w - utils.RectW(self.padding))
        layout_max_h = max(0, layout_max_h - utils.RectH(self.padding))

        layout_current_max_w = 0
        layout_current_max_h = 0

        for i in range(self.child_count):
            child = self.get_child_at(i)
            margin_w = utils.RectW(child.margin)
            margin_h = utils.RectH(child.margin)
            child_w, child_h = child.fixed_width, child.fixed_height
            if child.autofit:
                # update the constaint depends on the fit rule
                layout_constaint = PyDuiLayoutConstraint(layout_max_w - margin_w, layout_max_h - margin_h)
                if fit_w:
                    layout_constaint = PyDuiLayoutConstraint(-1, layout_constaint.height)
                if fit_h:
                    layout_constaint = PyDuiLayoutConstraint(layout_constaint.width, -1)
                # estimate child size
                child_w, child_h = child.estimate_size(
                    layout_max_w - margin_w, layout_max_h - margin_h, layout_constaint
                )
            # record the maximum area
            if fit_w:
                layout_current_max_w = max(layout_current_max_w, child_w + margin_w)
            if fit_h:
                layout_current_max_h = layout_current_max_h + child_h + margin_h

        # add padding
        if fit_w:
            layout_current_max_w += utils.RectW(self.padding)
        if fit_h:
            layout_current_max_h += utils.RectH(self.padding)
        return (layout_current_max_w, layout_current_max_h)

    def layout(self, x: float, y: float, width: float, height: float, constaint: PyDuiLayoutConstraint):
        fit_w, fit_h = self.__get_fitrule__()
        layout_max_w = width - utils.RectW(self.padding)
        layout_max_h = height - utils.RectH(self.padding)

        layout_current_max_w = 0
        layout_current_max_h = 0
        layout_info_dict = dict[int, Tuple[float, float, PyDuiLayoutConstraint]]()

        pending_layout_h_indexes = set[int]()

        for i in range(self.child_count):
            child = self.get_child_at(i)
            margin_w = utils.RectW(child.margin)
            margin_h = utils.RectH(child.margin)
            child_w, child_h = child.fixed_width, child.fixed_height
            layout_constaint = PyDuiLayoutConstraint(layout_max_w - margin_w, layout_max_h - margin_h)

            if child.autofit:
                # update layout constaint depends on the fit rule
                if fit_h:
                    layout_constaint = PyDuiLayoutConstraint(layout_constaint.width, -1)
                if fit_w:
                    layout_constaint = PyDuiLayoutConstraint(-1, layout_constaint.height)
                # estimate the child size
                child_w, child_h = child.estimate_size(
                    layout_max_w - margin_w, layout_max_h - margin_h, layout_constaint
                )

            # child height may be 0, should be handle later.
            if not fit_h and child_h == 0:
                pending_layout_h_indexes.add(i)

            # mark the estimate width, height, constaint, cache it use later.
            layout_info_dict[i] = (child_w, child_h, layout_constaint)

            # calculate widget used area (layout_current_max_w, layout_current_max_h)
            if self.autofit:
                if fit_w:
                    layout_current_max_w = max(layout_current_max_w, child_w + margin_w)
                if fit_h:
                    layout_current_max_h = layout_current_max_h + child_h + margin_h
            else:
                if child_h != 0:
                    layout_current_max_h += child_h + margin_h

        if not self.autofit:
            # expand to parent
            super().layout(x, y, width, height, constaint)
        else:
            # fit with children
            layout_current_max_w += utils.RectW(self.padding)
            layout_current_max_h += utils.RectH(self.padding)
            layout_constaint = PyDuiLayoutConstraint(layout_current_max_w, layout_current_max_h)
            super().layout(x, y, layout_current_max_w, layout_current_max_h, layout_constaint)

        layout_space_h = max(0, layout_max_h - layout_current_max_h)
        child_avg_h = round(layout_space_h / len(pending_layout_h_indexes)) if len(pending_layout_h_indexes) > 0 else 0

        # before layout children, update the layout max area.
        if fit_w:
            layout_max_w = layout_current_max_w - utils.RectW(self.padding)
        if fit_h:
            layout_max_h = layout_current_max_h - utils.RectH(self.padding)
        layout_x, layout_y = x, y
        for i in range(self.child_count):
            child = self.get_child_at(i)
            margin_w = utils.RectW(child.margin)
            margin_h = utils.RectH(child.margin)
            child_x = layout_x + child.margin[0]
            child_y = layout_y + child.margin[1]
            layout_constaint = PyDuiLayoutConstraint()
            child_w, child_h = child.fixed_width, child.fixed_height
            if i in layout_info_dict:
                # get the child estimate size
                child_w, child_h, layout_constaint = layout_info_dict[i]

            # if there are no size info, fit to parent
            child_w = max(0, layout_max_w - margin_w) if child_w == 0 else child_w
            child_h = max(0, child_avg_h - margin_h) if child_h == 0 else child_h
            layout_constaint = PyDuiLayoutConstraint(child_w, child_h)
            #  start layout
            child.layout(child_x, child_y, child_w, child_h, layout_constaint)
            # next position
            layout_y = layout_y + child_h + margin_h

    def __auto_expand_count__(self):
        count = 0
        for i in range(self.child_count):
            child = self.get_child_at(i)
            if int(child.fixed_height) == 0:
                count += 1
        return count

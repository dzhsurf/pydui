# -*- coding: utf-8 -*-
import math
import random
from typing import Tuple

from pydui import utils
from pydui.core.import_gtk import *
from pydui.core.layout import *
from pydui.core.widget import *


class PyDuiHLayout(PyDuiLayout):
    """Horizontal layout"""

    @staticmethod
    def build_name() -> str:
        return "HLayout"

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
        last_draw_x = None
        for i in range(self.child_count):
            child = self.get_child_at(i)
            draw_y, draw_w, draw_h = child.y, child.width, child.height
            draw_x = child.x
            if last_draw_x is not None:
                draw_x = last_draw_x + child.margin[0]
            # if is last expand child
            # if int(child.fixed_width) == 0:
            #     auto_expand_idx += 1
            #     if auto_expand_idx == auto_expand_count:
            #         if i < self.child_count - 1:
            #             next_child = self.get_child_at(i + 1)
            #             draw_w = next_child.x - next_child.margin[0] - draw_x - child.margin[2]
            #         else:
            #             draw_w = x + width - draw_x - child.margin[2]
            ctx.save()
            child.draw(ctx, draw_x, draw_y, draw_w, draw_h)
            ctx.restore()
            last_draw_x = draw_x + draw_w + child.margin[2]

    def __get_fitrule__(self) -> Tuple[bool, bool]:
        fit_w, fit_h = False, False
        if self.autofit:
            fit_w = "w" in self.fitrule
            fit_h = "h" in self.fitrule
            if not "w" in self.fitrule and not "h" in self.fitrule:
                fit_h = True
        return (fit_w, fit_h)

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
                layout_current_max_w = layout_current_max_w + child_w + margin_w
            if fit_h:
                layout_current_max_h = max(layout_current_max_h, child_h + margin_h)

        # add padding
        if layout_current_max_w != 0:
            layout_current_max_w += utils.RectW(self.padding)
        if layout_current_max_h != 0:
            layout_current_max_h += utils.RectH(self.padding)
        return (layout_current_max_w, layout_current_max_h)

    def layout(self, x: float, y: float, width: float, height: float, constaint: PyDuiLayoutConstraint):

        fit_w, fit_h = self.__get_fitrule__()
        layout_max_w = width - utils.RectW(self.padding)
        layout_max_h = height - utils.RectH(self.padding)

        layout_current_max_w = 0
        layout_current_max_h = 0
        layout_info_dict = dict[int, Tuple[float, float, PyDuiLayoutConstraint]]()

        pending_layout_w_indexes = set[int]()

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

            # child width may be 0, should be handle later.
            if not fit_w and child_w == 0:
                pending_layout_w_indexes.add(i)

            # mark the estimate width, height, constaint, cache it use later.
            layout_info_dict[i] = (child_w, child_h, layout_constaint)

            # calculate widget used area (layout_current_max_w, layout_current_max_h)
            if self.autofit:
                if child_w > 0 or fit_w:
                    layout_current_max_w = layout_current_max_w + child_w + margin_w
                if child_h > 0 or fit_h:
                    layout_current_max_h = max(layout_current_max_h, child_h + margin_h)
            else:
                if child_w != 0:
                    layout_current_max_w += child_w + margin_w

        if not self.autofit:
            # expand to parent
            super().layout(x, y, width, height, constaint)
        else:
            # fit with children
            layout_current_max_w += utils.RectW(self.padding)
            layout_current_max_h += utils.RectH(self.padding)
            layout_constaint = PyDuiLayoutConstraint(layout_current_max_w, layout_current_max_h)
            super().layout(x, y, layout_current_max_w, layout_current_max_h, layout_constaint)

        layout_space_w = max(0, layout_max_w - layout_current_max_w)
        child_avg_w = round(layout_space_w / len(pending_layout_w_indexes)) if len(pending_layout_w_indexes) > 0 else 0

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
            child_w = max(0, child_avg_w - margin_w) if child_w == 0 else child_w
            child_h = max(0, layout_max_h - margin_h) if child_h == 0 else child_h
            layout_constaint = PyDuiLayoutConstraint(child_w, child_h)
            # start layout
            child.layout(child_x, child_y, child_w, child_h, layout_constaint)
            # next position
            layout_x = layout_x + child_w + margin_w

    def __auto_expand_count__(self):
        count = 0
        for i in range(self.child_count):
            child = self.get_child_at(i)
            if int(child.fixed_width) == 0:
                count += 1
        return count

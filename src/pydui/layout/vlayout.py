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
        super().draw(
            ctx,
            x + self.padding[0],
            y + self.padding[1],
            max(0, width - utils.RectW(self.padding)),
            max(0, height - utils.RectH(self.padding)),
        )
        for i in range(self.child_count):
            child = self.get_child_at(i)
            draw_x, draw_w, draw_h = child.x, child.width, child.height
            draw_y = child.y
            ctx.save()
            child.draw(ctx, draw_x, draw_y, draw_w, draw_h)
            ctx.restore()

    def __get_fitrule__(self) -> Tuple[bool, bool]:
        fit_v, fit_h = False, False
        if self.autofit:
            fit_w = "w" in self.fitrule
            fit_h = "h" in self.fitrule
            if not "w" in self.fitrule and not "h" in self.fitrule:
                fit_h = True
        return (fit_v, fit_h)

    def estimate_size(
        self, parent_width: float, parent_height: float, constraint: PyDuiLayoutConstraint
    ) -> Tuple[float, float]:
        if not self.autofit:
            return super().estimate_size(parent_width, parent_height, constraint)

        # autofit
        fit_w, fit_h = self.__get_fitrule__()

        layout_max_w, layout_max_h = parent_width, parent_height
        layout_max_w = max(0, layout_max_w - utils.RectW(self.padding))
        layout_max_h = max(0, layout_max_h - utils.RectH(self.padding))

        # step 1, preprocess all the fixed widget
        layout_fixed_height_usage_dict = dict[int, int]()
        for i in range(self.child_count - 1, -1, -1):
            child = self.get_child_at(i)
            usage = child.fixed_height + utils.RectH(child.margin)
            if child.autofit or child.fixed_height == 0:
                usage = 0
            layout_fixed_height_usage_dict[i] = usage
            if i < self.child_count - 1:
                layout_fixed_height_usage_dict[i] += layout_fixed_height_usage_dict[i + 1]

        def get_ends_height(index: int) -> int:
            if index + 1 in layout_fixed_height_usage_dict:
                return layout_fixed_height_usage_dict[index + 1]
            return 0

        layout_current_max_w = 0
        layout_current_max_h = 0
        pre_fixed_widget_total_height = 0
        for i in range(self.child_count):
            child = self.get_child_at(i)
            margin_w = utils.RectW(child.margin)
            margin_h = utils.RectH(child.margin)
            child_w, child_h = child.fixed_width, child.fixed_height
            child_max_w = max(0, layout_max_w - margin_w)
            child_max_h = max(0, layout_max_h - margin_h - pre_fixed_widget_total_height - get_ends_height(i))
            if child.autofit:
                # update the constraint depends on the fit rule
                layout_constraint = PyDuiLayoutConstraint(child_max_w, child_max_h)
                if fit_w:
                    layout_constraint = PyDuiLayoutConstraint(-1, layout_constraint.height)
                if fit_h:
                    layout_constraint = PyDuiLayoutConstraint(layout_constraint.width, -1)
                # estimate child size
                child_w, child_h = child.estimate_size(child_max_w, child_max_h, layout_constraint)
            elif child_h > 0:
                pre_fixed_widget_total_height += child_h + margin_h
            # record the maximum area
            if fit_w:
                layout_current_max_w = max(layout_current_max_w, child_w + margin_w)
            if fit_h:
                layout_current_max_h = layout_current_max_h + child_h + margin_h

        # add padding
        if layout_current_max_w != 0:
            layout_current_max_w += utils.RectW(self.padding) + utils.RectW(self.margin)
        if layout_current_max_h != 0:
            layout_current_max_h += utils.RectH(self.padding) + utils.RectH(self.margin)
        return (layout_current_max_w, layout_current_max_h)

    def layout(self, x: float, y: float, width: float, height: float, constraint: PyDuiLayoutConstraint):
        fit_w, fit_h = self.__get_fitrule__()

        layout_max_w = max(0, width - utils.RectW(self.padding))
        layout_max_h = max(0, height - utils.RectH(self.padding))

        # step 1, preprocess all the fixed widget
        layout_fixed_height_usage_dict = dict[int, int]()
        for i in range(self.child_count - 1, -1, -1):
            child = self.get_child_at(i)
            usage = child.fixed_height + utils.RectH(child.margin)
            if child.autofit or child.fixed_height == 0:
                usage = 0
            layout_fixed_height_usage_dict[i] = usage
            if i < self.child_count - 1:
                layout_fixed_height_usage_dict[i] += layout_fixed_height_usage_dict[i + 1]

        def get_ends_height(index: int) -> int:
            if index + 1 in layout_fixed_height_usage_dict:
                return layout_fixed_height_usage_dict[index + 1]
            return 0

        layout_current_max_w = 0
        layout_current_max_h = 0
        layout_info_dict = dict[int, Tuple[float, float, PyDuiLayoutConstraint]]()
        pending_layout_h_indexes = set[int]()

        for i in range(self.child_count):
            child = self.get_child_at(i)
            margin_w = utils.RectW(child.margin)
            margin_h = utils.RectH(child.margin)
            child_w, child_h = child.fixed_width, child.fixed_height
            child_max_w = max(0, layout_max_w - margin_w)
            child_max_h = max(0, layout_max_h - margin_h - get_ends_height(i))
            layout_constraint = PyDuiLayoutConstraint(child_max_w, child_max_h)

            if child.autofit:
                # update layout constraint depends on the fit rule
                if fit_h:
                    layout_constraint = PyDuiLayoutConstraint(layout_constraint.width, -1)
                if fit_w:
                    layout_constraint = PyDuiLayoutConstraint(-1, layout_constraint.height)
                # estimate the child size
                child_w, child_h = child.estimate_size(child_max_w, child_max_h, layout_constraint)

            # child height may be 0, should be handle later.
            if not fit_h and child_h == 0:
                pending_layout_h_indexes.add(i)

            # mark the estimate width, height, constraint, cache it use later.
            layout_info_dict[i] = (child_w, child_h, layout_constraint)

            # calculate widget used area (layout_current_max_w, layout_current_max_h)
            if self.autofit:
                if child_w > 0 and fit_w:
                    layout_current_max_w = max(layout_current_max_w, child_w + margin_w)
                if child_h > 0 or fit_h:
                    layout_current_max_h = layout_current_max_h + child_h + margin_h
            else:
                if child_h != 0:
                    layout_current_max_h += child_h + margin_h

        if not self.autofit:
            # expand to parent
            super().layout(
                x, y, layout_max_w + utils.RectW(self.padding), layout_max_h + utils.RectH(self.padding), constraint
            )
        else:
            # fit with children
            layout_constraint = PyDuiLayoutConstraint(
                layout_max_w + utils.RectW(self.padding), layout_max_h + layout_max_h + utils.RectH(self.padding)
            )
            lh = layout_max_h
            if fit_h:
                lh = layout_current_max_h
            super().layout(
                x,
                y,
                layout_max_w + utils.RectW(self.padding),
                lh + utils.RectH(self.padding),
                layout_constraint,
            )

        layout_space_h = max(0, layout_max_h - layout_current_max_h)
        child_avg_h = round(layout_space_h / len(pending_layout_h_indexes)) if len(pending_layout_h_indexes) > 0 else 0

        # before layout children, update the layout max area.
        layout_x, layout_y = x + self.padding[0], y + self.padding[1]
        for i in range(self.child_count):
            child = self.get_child_at(i)
            margin_w = utils.RectW(child.margin)
            margin_h = utils.RectH(child.margin)
            child_x = layout_x + child.margin[0]
            child_y = layout_y + child.margin[1]
            layout_constraint = PyDuiLayoutConstraint()
            child_w, child_h = child.fixed_width, child.fixed_height
            if i in layout_info_dict:
                # get the child estimate size
                child_w, child_h, layout_constraint = layout_info_dict[i]

            # if there are no size info, fit to parent
            child_w = max(0, layout_max_w - margin_w) if child_w == 0 else child_w
            child_h = max(0, child_avg_h - margin_h) if child_h == 0 else child_h
            layout_constraint = PyDuiLayoutConstraint(child_w, child_h)
            #  start layout
            if self.halign == PyDuiAlign.CENTER:
                child_x = child_x + round(max(0, (layout_max_w - margin_w - child_w)) / 2)
            if self.halign == PyDuiAlign.END:
                child_x = child_x + max(0, (layout_max_w - margin_w - child_w))
            child.layout(child_x, child_y, child_w, child_h, layout_constraint)
            # next position
            layout_y = layout_y + child_h + margin_h

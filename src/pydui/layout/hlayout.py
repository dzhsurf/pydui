# -*- coding: utf-8 -*-
from typing import Tuple

from pydui.common.import_gtk import *
from pydui.core.layout import *
from pydui.core.widget import *
from pydui.layout.pglayout import PyDuiLayoutWithPogaSupport


class PyDuiHLayout(PyDuiLayoutWithPogaSupport):
    """Horizontal layout"""

    @staticmethod
    def build_name() -> str:
        return "HLayout"

    def __init__(self):
        super().__init__()

    def draw(self, ctx: cairo.Context, dirty_rect: PyDuiRect, clip_rect: PyDuiRect):
        super().draw(ctx, dirty_rect, clip_rect)

    def __get_fitrule__(self) -> Tuple[bool, bool]:
        fit_w, fit_h = False, False
        if self.autofit:
            fit_w = "w" in self.fitrule
            fit_h = "h" in self.fitrule
            if not "w" in self.fitrule and not "h" in self.fitrule:
                fit_h = True
        return (fit_w, fit_h)

    def estimate_size(
        self, parent_width: float, parent_height: float, constraint: PyDuiLayoutConstraint
    ) -> Tuple[float, float]:
        if not self.autofit:
            return super().estimate_size(parent_width, parent_height, constraint)

        # autofit
        fit_w, fit_h = self.__get_fitrule__()

        layout_max_w, layout_max_h = parent_width, parent_height
        layout_max_w = max(0, layout_max_w - self.padding.width)
        layout_max_h = max(0, layout_max_h - self.padding.height)

        # step 1, preprocess all the fixed widget
        layout_fixed_width_usage_dict: Dict[int, float] = {}
        for i in range(self.child_count - 1, -1, -1):
            child = self.get_child_at(i)
            if child is None:
                continue
            if child.is_float:
                continue
            usage = child.fixed_width + child.margin.width
            if child.autofit or child.fixed_width == 0:
                usage = 0
            layout_fixed_width_usage_dict[i] = usage
            if i < self.child_count - 1:
                layout_fixed_width_usage_dict[i] += layout_fixed_width_usage_dict[i + 1]

        def get_ends_width(index: int) -> float:
            if index + 1 in layout_fixed_width_usage_dict:
                return layout_fixed_width_usage_dict[index + 1]
            return 0

        layout_current_max_w = 0
        layout_current_max_h = 0

        # step 2, preprocess autofit widget
        pre_fixed_widget_total_width = 0
        for i in range(self.child_count):
            child = self.get_child_at(i)
            if child is None:
                continue
            if child.is_float:
                continue
            margin_w = child.margin.width
            margin_h = child.margin.height
            child_w, child_h = child.fixed_width, child.fixed_height
            child_max_w = max(0, layout_max_w - margin_w - pre_fixed_widget_total_width - get_ends_width(i))
            child_max_h = max(0, layout_max_h - margin_h)
            if child.autofit:
                # update the constraint depends on the fit rule
                layout_constraint = PyDuiLayoutConstraint(child_max_w, child_max_h)
                if fit_w:
                    layout_constraint = PyDuiLayoutConstraint(-1, layout_constraint.height)
                if fit_h:
                    layout_constraint = PyDuiLayoutConstraint(layout_constraint.width, -1)
                # estimate child size
                child_w, child_h = child.estimate_size(child_max_w, child_max_h, layout_constraint)
            elif child_w > 0:
                pre_fixed_widget_total_width += child_w + margin_w
            # record the maximum area
            if fit_w:
                layout_current_max_w = layout_current_max_w + child_w + margin_w
            if fit_h:
                layout_current_max_h = max(layout_current_max_h, child_h + margin_h)

        # add padding
        if layout_current_max_w != 0:
            layout_current_max_w += self.padding.width
        if layout_current_max_h != 0:
            layout_current_max_h += self.padding.height
        return (layout_current_max_w, layout_current_max_h)

    def layout(self, x: float, y: float, width: float, height: float, constraint: PyDuiLayoutConstraint):

        fit_w, fit_h = self.__get_fitrule__()
        layout_max_w = max(0, width - self.padding.width)
        layout_max_h = max(0, height - self.padding.height)

        # step 1, preprocess all the fixed widget
        layout_fixed_width_usage_dict: Dict[int, float] = {}
        for i in range(self.child_count - 1, -1, -1):
            child = self.get_child_at(i)
            if child is None or child.is_float:
                layout_fixed_width_usage_dict[i] = 0
                if i < self.child_count - 1:
                    layout_fixed_width_usage_dict[i] = layout_fixed_width_usage_dict[i + 1]
                continue
            usage = child.fixed_width + child.margin.width
            if child.autofit or child.fixed_width == 0:
                usage = 0
            layout_fixed_width_usage_dict[i] = usage
            if i < self.child_count - 1:
                layout_fixed_width_usage_dict[i] += layout_fixed_width_usage_dict[i + 1]

        def get_ends_width(index: int) -> float:
            if index + 1 in layout_fixed_width_usage_dict:
                return layout_fixed_width_usage_dict[index + 1]
            return 0

        # step 2, preprocess the autofit widget
        pending_layout_w_indexes = set[int]()
        layout_info_dict = dict[int, Tuple[float, float, PyDuiLayoutConstraint]]()
        layout_current_max_w = 0
        layout_current_max_h = 0

        for i in range(self.child_count):
            child = self.get_child_at(i)
            if child is None:
                continue
            if child.is_float:
                continue
            margin_w = child.margin.width
            margin_h = child.margin.height
            child_w, child_h = child.fixed_width, child.fixed_height
            child_max_w = max(0, layout_max_w - margin_w - get_ends_width(i))
            child_max_h = max(0, layout_max_h - margin_h)
            layout_constraint = PyDuiLayoutConstraint(child_max_w, child_max_h)

            if child.autofit:
                # update layout constraint depends on the fit rule
                if fit_h:
                    layout_constraint = PyDuiLayoutConstraint(layout_constraint.width, -1)
                if fit_w:
                    layout_constraint = PyDuiLayoutConstraint(-1, layout_constraint.height)
                # estimate the child size
                child_w, child_h = child.estimate_size(child_max_w, child_max_h, layout_constraint)

            # child width may be 0, should be handle later.
            if not fit_w and child_w == 0:
                pending_layout_w_indexes.add(i)

            # mark the estimate width, height, constraint, cache it use later.
            layout_info_dict[i] = (child_w, child_h, layout_constraint)

            # calculate widget used area
            if self.autofit:
                if child_w > 0 or fit_w:
                    layout_current_max_w += child_w + margin_w
                if child_h > 0 and fit_h:
                    # when set to fit_h, and the child_h is zero, it means child is fit to parent
                    # so it does not need to count the usage height.
                    layout_current_max_h = max(layout_current_max_h, child_h + margin_h)
            else:
                if child_w != 0:
                    layout_current_max_w += child_w + margin_w

        if not self.autofit:
            # expand to parent
            super().layout(x, y, layout_max_w + self.padding.width, layout_max_h + self.padding.height, constraint)
        else:
            # fit with children
            layout_constraint = PyDuiLayoutConstraint(
                layout_max_w + self.padding.width, layout_max_h + layout_max_h + self.padding.height
            )
            lw = layout_max_w
            if fit_w:
                lw = layout_current_max_w
            super().layout(
                x,
                y,
                lw + self.padding.width,
                layout_max_h + self.padding.height,
                layout_constraint,
            )

        # step3 calculate fit with children, then start layout.
        layout_space_w = max(0, layout_max_w - layout_current_max_w)
        child_avg_w = round(layout_space_w / len(pending_layout_w_indexes)) if len(pending_layout_w_indexes) > 0 else 0

        # before layout children, update the layout max area.
        layout_x, layout_y = self.padding.left, self.padding.top
        for i in range(self.child_count):
            child = self.get_child_at(i)
            if child is None:
                continue

            if child.is_float:
                child_size = child.estimate_size(width, height, constraint=constraint)
                child_max_width = width - self.padding.width
                child_max_height = height - self.padding.height
                if child_size[0] == 0:
                    child_size = (child_max_width, child_size[1])
                if child_size[1] == 0:
                    child_size = (child_size[0], child_max_height)
                child.layout(child.fixed_x, child.fixed_y, child_size[0], child_size[1], constraint=constraint)
                continue

            margin_w = child.margin.width
            margin_h = child.margin.height
            child_x = layout_x + child.margin.left
            child_y = layout_y + child.margin.top
            layout_constraint = PyDuiLayoutConstraint()
            child_w, child_h = child.fixed_width, child.fixed_height
            if i in layout_info_dict:
                # get the child estimate size
                child_w, child_h, layout_constraint = layout_info_dict[i]

            # if there are no size info, fit to parent
            child_w = max(0, child_avg_w - margin_w) if child_w == 0 else child_w
            child_h = max(0, layout_max_h - margin_h) if child_h == 0 else child_h
            layout_constraint = PyDuiLayoutConstraint(child_w, child_h)
            # start layout
            if self.valign == PyDuiAlign.CENTER:
                child_y = child_y + round(max(0, (layout_max_h - margin_h - child_h)) / 2)
            if self.valign == PyDuiAlign.END:
                child_y = child_y + max(0, layout_max_h - margin_h - child_h)
            child.layout(child_x, child_y, child_w, child_h, layout_constraint)
            # next position
            layout_x = layout_x + child_w + margin_w

# -*- coding: utf-8 -*-
import math

from poga import *
from poga.libpoga_capi import *


def Str2YGPostionType(text: str) -> YGPositionType:
    text = text.lower()
    pos_types = {
        "relative": YGPositionType.Relative,
        "absolute": YGPositionType.Absolute,
    }
    if text in pos_types:
        return pos_types[text]
    # default is relative
    return YGPositionType.Relative


def Str2YGAlign(text: str) -> YGAlign:
    text = text.lower()
    align_types = {
        "flex_start": YGAlign.FlexStart,
        "flex_end": YGAlign.FlexEnd,
        "stretch": YGAlign.Stretch,
        "center": YGAlign.Center,
        "space_between": YGAlign.SpaceBetween,
        "space_around": YGAlign.SpaceAround,
        "baseline": YGAlign.Baseline,
        "auto": YGAlign.Auto,
    }
    if text in align_types:
        return align_types[text]
    return YGAlign.FlexStart


def Str2YGWrap(text: str) -> YGWrap:
    text = text.lower()
    wrap_types = {
        "nowrap": YGWrap.NoWrap,
        "wrap": YGWrap.Wrap,
        "wrap_reverse": YGWrap.WrapReverse,
    }
    if text in wrap_types:
        return wrap_types[text]
    return YGWrap.NoWrap


def Str2Justify(text: str) -> YGJustify:
    text = text.lower()
    justify_types = {
        "flex_start": YGJustify.FlexStart,
        "flex_end": YGJustify.FlexEnd,
        "center": YGJustify.Center,
        "space_between": YGJustify.SpaceBetween,
        "space_around": YGJustify.SpaceAround,
        "space_evenly": YGJustify.SpaceEvenly,
    }
    if text in justify_types:
        return justify_types[text]
    return YGJustify.FlexStart


def Str2YGDirection(text: str) -> YGDirection:
    text = text.lower()
    direction_types = {
        "ltr": YGDirection.LTR,
        "rtl": YGDirection.RTL,
    }
    if text in direction_types:
        return direction_types[text]
    return YGDirection.LTR


def Str2YGFlexDirection(text: str) -> YGFlexDirection:
    text = text.lower()
    flex_direction_types = {
        "row": YGFlexDirection.Row,
        "column": YGFlexDirection.Column,
        "row_reverse": YGFlexDirection.RowReverse,
        "column_reverse": YGFlexDirection.ColumnReverse,
    }
    if text in flex_direction_types:
        return flex_direction_types[text]
    return YGFlexDirection.Row


def apply_poga_attributes(layout: PogaLayout, k: str, v: str) -> bool:
    """Apply poga attributes to PogaLayout.

    Args:
        layout (PogaLayout): PogaLayout instance
        k (str): attribute key
        v (str): attribute value

    Returns:
        bool: Return True means it is handled.
    """

    if k == "poga_layout":
        layout.is_enabled = v.lower() == "true"
    elif k == "position_type":
        layout.position = Str2YGPostionType(v)
    elif k == "align_content":
        layout.align_content = Str2YGAlign(v)
    elif k == "align_items":
        layout.align_items = Str2YGAlign(v)
    elif k == "align_self":
        layout.align_self = Str2YGAlign(v)
    elif k == "aspect_ratio":
        layout.aspect_ratio = YGUndefined if v.lower() == "nan" else float(v)
    elif k == "flex_wrap":
        layout.flex_wrap = Str2YGWrap(v)
    elif k == "flex_grow":
        layout.flex_grow = float(v)
    elif k == "flex_shrink":
        layout.flex_shrink = float(v)
    elif k == "flex_basis":
        if v.lower() == "auto":
            layout.flex_basis = YGValue(YGUndefined, YGUnit.Auto)
        else:
            layout.flex_basis = YGValue(float(v), YGUnit.Point)
    elif k == "flex_basis_percent":
        layout.flex_basis = YGValue(float(v), YGUnit.Percent)
    elif k == "justify_content":
        layout.justify_content = Str2Justify(v)
    elif k == "layout_direction":
        layout.direction = Str2YGDirection(v)
    elif k == "margin":
        margin_arr = v.split(",")
        if len(margin_arr) < 2:
            layout.margin = YGValue(float(margin_arr[0]), YGUnit.Point)
        elif len(margin_arr) < 4:
            layout.margin_horizontal = YGValue(float(margin_arr[0]), YGUnit.Point)
            layout.margin_vertical = YGValue(float(margin_arr[1]), YGUnit.Point)
        else:
            layout.margin_left = YGValue(float(margin_arr[0]), YGUnit.Point)
            layout.margin_top = YGValue(float(margin_arr[1]), YGUnit.Point)
            layout.margin_right = YGValue(float(margin_arr[2]), YGUnit.Point)
            layout.margin_bottom = YGValue(float(margin_arr[3]), YGUnit.Point)
    elif k == "padding":
        padding_arr = v.split(",")
        if len(padding_arr) < 2:
            layout.padding = YGValue(float(padding_arr[0]), YGUnit.Point)
        elif len(padding_arr) < 4:
            layout.padding_horizontal = YGValue(float(padding_arr[0]), YGUnit.Point)
            layout.padding_vertical = YGValue(float(padding_arr[1]), YGUnit.Point)
        else:
            layout.padding_left = YGValue(float(padding_arr[0]), YGUnit.Point)
            layout.padding_top = YGValue(float(padding_arr[1]), YGUnit.Point)
            layout.padding_right = YGValue(float(padding_arr[2]), YGUnit.Point)
            layout.padding_bottom = YGValue(float(padding_arr[3]), YGUnit.Point)
    elif k == "border":
        border_arr = v.split(",")
        if len(border_arr) < 2:
            layout.border_width = YGValue(float(border_arr[0]), YGUnit.Point)
        elif len(border_arr) < 4:
            layout.border_start_width = YGValue(float(border_arr[0]), YGUnit.Point)
            layout.border_end_width = YGValue(float(border_arr[1]), YGUnit.Point)
        else:
            layout.border_left_width = YGValue(float(border_arr[0]), YGUnit.Point)
            layout.border_top_width = YGValue(float(border_arr[1]), YGUnit.Point)
            layout.border_right_width = YGValue(float(border_arr[2]), YGUnit.Point)
            layout.border_bottom_width = YGValue(float(border_arr[3]), YGUnit.Point)
    elif k == "min_width":
        layout.min_width = YGValue(float(v), YGUnit.Point)
    elif k == "min_height":
        layout.min_height = YGValue(float(v), YGUnit.Point)
    elif k == "min_width_percent":
        layout.min_width = YGValue(float(v), YGUnit.Percent)
    elif k == "min_height_percent":
        layout.min_height = YGValue(float(v), YGUnit.Percent)
    elif k == "max_width":
        layout.max_width = YGValue(float(v), YGUnit.Point)
    elif k == "max_height":
        layout.max_height = YGValue(float(v), YGUnit.Point)
    elif k == "max_width_percent":
        layout.max_width = YGValue(float(v), YGUnit.Percent)
    elif k == "max_height_percent":
        layout.max_height = YGValue(float(v), YGUnit.Percent)
    elif k == "flex_direction":
        layout.flex_direction = Str2YGFlexDirection(v)
    elif k == "width":
        if v.lower() == "auto":
            layout.width = YGValue(YGUndefined, YGUnit.Auto)
        else:
            layout.width = YGValue(float(v), YGUnit.Point)
    elif k == "width_percent":
        layout.width = YGValue(float(v), YGUnit.Percent)
    elif k == "height":
        if v.lower() == "auto":
            layout.height = YGValue(YGUndefined, YGUnit.Auto)
        else:
            layout.height = YGValue(float(v), YGUnit.Point)
    elif k == "height_percent":
        layout.height = YGValue(float(v), YGUnit.Percent)
    else:
        return False

    return True

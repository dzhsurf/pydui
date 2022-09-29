# -*- coding: utf-8 -*-
from poga import *

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

    .. list-table:: Attributes Table
        :header-rows: 1

        * - Key
          - Type
          - Value
          - Description
        * - poga_layout
          - bool
          - true, false
          - Enable poga layout
        * - position_type
          - YGPositionType
          - relative, absolute
          -
        * - align_content
          - YGAlign
          - flex_start, flex_end, stretch, center, space_between, space_around, baseline, auto
          -
        * - align_items
          - YGAlign
          -
          -
        * - align_self
          - YGAlign
          -
          -
        * - flex_wrap
          - YGWrap
          - nowrap, wrap, wrap_reverse
          -
        * - flex_grow
          -
          -
          -
        * - flex_shrink
          -
          -
          -
        * - flex_basis
          -
          -
          -
        * - justify_content
          - YGJustify
          - flex_start, flex_end, center, space_between, space_around, space_evenly
          -
        * - layout_direction
          - YGDirection
          - ltr, rtl
          - default is ltr
        * - margin
          -
          -
          -
        * - padding
          -
          -
          -
        * - border
          -
          -
          -
        * - min_width
          -
          -
          -
        * - min_height
          -
          -
          -
        * - max_width
          -
          -
          -
        * - max_height
          -
          -
          -
        * - flex_direction
          - YGFlexDirection
          - row, column, row_reverse, column_reverse
          - default is row
        * - width
          -
          -
          -
        * - width_percent
          -
          -
          -
        * - height
          -
          -
          -
        * - height_percent
          -
          -
          -

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
        layout.aspect_ratio = float(v)
    elif k == "flex_wrap":
        layout.flex_wrap = Str2YGWrap(v)
    elif k == "flex_grow":
        layout.flex_grow = float(v)
    elif k == "flex_shrink":
        layout.flex_shrink = float(v)
    elif k == "flex_basis":
        # TODO:
        pass
    elif k == "justify_content":
        layout.justify_content = Str2Justify(v)
    elif k == "layout_direction":
        layout.direction = Str2YGDirection(v)
    elif k == "margin":
        # TODO:
        pass
    elif k == "padding":
        # TODO:
        pass
    elif k == "border":
        # TODO:
        pass
    elif k == "min_width":
        pass
    elif k == "min_height":
        pass
    elif k == "max_width":
        pass
    elif k == "max_height":
        pass
    elif k == "flex_direction":
        layout.flex_direction = Str2YGFlexDirection(v)
    elif k == "width":
        if v.lower() == "auto":
            layout.width = YGValue(0.0, YGUnit.Auto)
        else:
            layout.width = YGValue(float(v), YGUnit.Point)
    elif k == "width_percent":
        layout.width = YGValue(float(v), YGUnit.Percent)
    elif k == "height":
        if v.lower() == "auto":
            layout.height = YGValue(0.0, YGUnit.Auto)
        else:
            layout.height = YGValue(float(v), YGUnit.Point)
    elif k == "height_percent":
        layout.height = YGValue(float(v), YGUnit.Percent)
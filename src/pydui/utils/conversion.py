# -*- coding: utf-8 -*-
"""Conversion function"""
from typing import Tuple

from pydui.common.base import PyDuiEdge, PyDuiRect
from pydui.common.import_gtk import *


def Str2Bool(text: str) -> bool:
    return text.lower() == "true"


def Str2Size(text: str) -> Tuple[float, float]:
    """Convert text to Tuple[float, float]

    if the text in wrong format, it will return (0, 0)

    Args:
        text (str): input text

    Retruns:
        Tuple[float, float]: return size in tuple
    """
    arr = text.split(",")
    if len(arr) != 2:
        return (0, 0)

    return (float(arr[0]), float(arr[1]))


def Str2Position(text: str) -> Gtk.WindowPosition:
    """Convert text to Gtk.WindowPosition flag

    if the input not match, it will return Gtk.WindowPosition.CENTER by default.

    Args:
        text (str): input text

    Retruns:
        Gtk.WindowPosition: return gtk position flag
    """
    flags_table = {
        "CENTER": Gtk.WindowPosition.CENTER,
    }
    if text in flags_table:
        return flags_table[text]

    return Gtk.WindowPosition.CENTER


def Str2Color(text: str) -> Gdk.RGBA:
    text = text.lstrip("#")
    text = text.upper()
    text = text.rjust(8, "F")
    color = [255, 255, 255, 255]
    for i in range(4):
        color[i] = int(text[0:2], 16)
        text = text[2:]

    return Gdk.RGBA(color[1] / 255, color[2] / 255, color[3] / 255, color[0] / 255)


def Str2Edge(text: str) -> PyDuiEdge:
    arr = text.split(",")
    if len(arr) != 4:
        return PyDuiEdge()

    return PyDuiEdge.from_ltrb(float(arr[0]), float(arr[1]), float(arr[2]), float(arr[3]))


def Str2Rect(text: str) -> PyDuiRect:
    arr = text.split(",")
    if len(arr) != 4:
        return PyDuiRect()

    return PyDuiRect.from_ltrb(float(arr[0]), float(arr[1]), float(arr[2]), float(arr[3]))


def intersect_rect(rect1: PyDuiRect, rect2: PyDuiRect) -> PyDuiRect:
    rect = PyDuiRect()
    rect.left = max(rect1.left, rect2.left)
    rect.top = max(rect1.top, rect2.top)
    rect.right = min(rect1.right, rect2.right)
    rect.bottom = min(rect1.bottom, rect2.bottom)
    if rect.left > rect.right:
        rect.left, rect.right = 0, 0
    if rect.top > rect.bottom:
        rect.top, rect.bottom = 0, 0
    return rect


def merge_rect(rect1: PyDuiRect, rect2: PyDuiRect) -> PyDuiRect:
    return rect1

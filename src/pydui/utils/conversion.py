# -*- coding: utf-8 -*-
"""Conversion function
"""
from typing import Tuple

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


def Str2IntRect(text: str) -> Tuple[int, int, int, int]:
    arr = text.split(",")
    if len(arr) != 4:
        return (0, 0, 0, 0)

    return tuple(int(n) for n in arr)


def Str2Rect(text: str) -> Tuple[float, float, float, float]:
    arr = text.split(",")
    if len(arr) != 4:
        return (0, 0, 0, 0)

    return tuple(float(n) for n in arr)


def IsNoneZeroRect(rect: Tuple[float, float, float, float]) -> bool:
    for r in rect:
        if int(r) == 0:
            return False
    return True


def IsPointInRect(x: float, y: float, rect: Tuple[float, float, float, float]) -> bool:
    if x >= rect[0] and x <= rect[2] and y >= rect[1] and y <= rect[3]:
        return True
    return False


def IsPointInIntRect(x: float, y: float, rect: Tuple[int, int, int, int]) -> bool:
    float_rect = tuple(float(n) for n in rect)
    return IsPointInRect(x, y, float_rect)


def RectH(rect: Tuple[float, float, float, float]) -> float:
    return rect[1] + rect[3]


def RectW(rect: Tuple[float, float, float, float]) -> float:
    return rect[0] + rect[2]

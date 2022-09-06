# -*- coding: utf-8 -*-
"""Conversion function
"""

from pydui.core.import_gtk import *


def Str2Size(text: str) -> tuple[float, float]:
    """Convert text to tuple[float, float]

    if the text in wrong format, it will return (0, 0)

    Args:
        text (str): input text

    Retruns:
        tuple[float, float]: return size in tuple
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


def Str2Rect(text: str) -> tuple[float, float, float, float]:
    arr = text.split(",")
    if len(arr) != 4:
        return (0, 0, 0, 0)

    return tuple(float(n) for n in arr)


def IsNoneZeroRect(rect: tuple[float, float, float, float]) -> bool:
    for r in rect:
        if int(r) == 0:
            return False
    return True


def RectH(rect: tuple[float, float, float, float]) -> float:
    return rect[1] + rect[3]


def RectW(rect: tuple[float, float, float, float]) -> float:
    return rect[0] + rect[2]

# -*- coding: utf-8 -*-
from dataclasses import dataclass
from enum import Enum

from pydui.common.import_gtk import *


class PyDuiAlign(Enum):
    """Align type"""

    CENTER = 0
    START = 1
    END = 2


class PyDuiClickType(Enum):
    """Click Type"""

    NONE = 0
    CLICK = 1
    DBCLICK = 2


class PyDuiLayoutConstraint:
    """Layout constraint
    if the value set to -1, it means no limit
    """

    def __init__(self, w: float = -1, h: float = -1) -> None:
        super().__init__()
        self.width = w
        self.height = h

    width: float = -1
    height: float = -1

    # def merge(self, constraint: PyDuiLayoutConstraint):
    #     if constraint.width != -1:
    #         self.width = min(self.width, constraint.width)
    #     if constraint.height != -1:
    #         self.height = min(self.height, constraint.height)


def Text2PyDuiAlign(text: str) -> PyDuiAlign:
    return {
        "CENTER": PyDuiAlign.CENTER,
        "START": PyDuiAlign.START,
        "END": PyDuiAlign.END,
    }[text.upper()]


def Text2WrapMode(text: str) -> Pango.WrapMode:
    return {
        "NONE": None,
        "WORD": Pango.WrapMode.WORD,
        "CHAR": Pango.WrapMode.CHAR,
        "WORD_CHAR": Pango.WrapMode.WORD_CHAR,
    }[text.upper()]


def Text2EllipsizeMode(text: str) -> Pango.EllipsizeMode:
    return {
        "NONE": Pango.EllipsizeMode.NONE,
        "START": Pango.EllipsizeMode.START,
        "MIDDLE": Pango.EllipsizeMode.MIDDLE,
        "END": Pango.EllipsizeMode.END,
    }[text.upper()]

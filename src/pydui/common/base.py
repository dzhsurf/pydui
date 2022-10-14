# -*- coding: utf-8 -*-
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

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


class PyDuiEdge:
    left: float = 0
    top: float = 0
    right: float = 0
    bottom: float = 0

    def __init__(self) -> None:
        pass

    def copy(self):
        return PyDuiEdge.from_ltrb(self.left, self.top, self.right, self.bottom)

    def copy_with_factor(self, factor: float):
        return PyDuiEdge.from_ltrb(self.left * factor, self.top * factor, self.right * factor, self.bottom * factor)

    @staticmethod
    def from_value(v: float):
        edge = PyDuiEdge()
        edge.left = v
        edge.top = v
        edge.right = v
        edge.bottom = v
        return edge

    @staticmethod
    def from_hv(h: float, v: float):
        edge = PyDuiEdge()
        edge.left = h
        edge.top = v
        edge.right = h
        edge.bottom = v
        return edge

    @staticmethod
    def from_ltrb(left: float, top: float, right: float, bottom: float):
        edge = PyDuiEdge()
        edge.left = left
        edge.top = top
        edge.right = right
        edge.bottom = bottom
        return edge

    @property
    def width(self) -> float:
        return self.left + self.right

    @property
    def height(self) -> float:
        return self.top + self.bottom

    def is_empty(self):
        if self.left == 0 and self.right == 0 and self.top == 0 and self.bottom == 0:
            return True
        return False


class PyDuiRect:
    left: float = 0
    top: float = 0
    right: float = 0
    bottom: float = 0

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.bottom - self.top

    def copy(self):
        return PyDuiRect.from_ltrb(self.left, self.top, self.right, self.bottom)

    @staticmethod
    def from_size(pos: Tuple[float, float], size: Tuple[float, float]):
        rect = PyDuiRect()
        rect.left = pos[0]
        rect.top = pos[1]
        rect.right = pos[0] + size[0]
        rect.bottom = pos[1] + size[1]
        return rect

    @staticmethod
    def from_ltrb(left: float, top: float, right: float, bottom: float):
        edge = PyDuiRect()
        edge.left = left
        edge.top = top
        edge.right = right
        edge.bottom = bottom
        return edge

    def is_empty(self):
        if self.left == 0 and self.right == 0 and self.top == 0 and self.bottom == 0:
            return True
        return False

    def contain_point(self, point: Tuple[float, float]) -> bool:
        if point[0] >= self.left and point[0] <= self.right and point[1] >= self.top and point[1] <= self.bottom:
            return True
        return False

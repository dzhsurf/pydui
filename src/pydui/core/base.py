from enum import Enum

import gi
from gi.repository import Pango


class PyDuiLayoutEnum(Enum):
    """Layout type enum

    Attributes:
        Undefine: default
        HLayout: horizontal layout
        VLayout: vertical layout

    """

    NotLayout = 0
    HLayout = 1
    VLayout = 2
    FitLayout = 3
    FixedLayout = 4
    CustomLayout = 10


class PyDuiTextAlign(Enum):
    """Text align"""

    CENTER = (0,)
    START = 1
    END = 2


def Text2TextAlign(text: str) -> PyDuiTextAlign:
    return {
        "CENTER": PyDuiTextAlign.CENTER,
        "START": PyDuiTextAlign.START,
        "END": PyDuiTextAlign.END,
    }[text]


def Text2WrapMode(text: str) -> Pango.WrapMode:
    return {
        "NONE": None,
        "WORD": Pango.WrapMode.WORD,
        "CHAR": Pango.WrapMode.CHAR,
        "WORD_CHAR": Pango.WrapMode.WORD_CHAR,
    }[text]


def Text2EllipsizeMode(text: str) -> Pango.EllipsizeMode:
    return {
        "NONE": Pango.EllipsizeMode.NONE,
        "START": Pango.EllipsizeMode.START,
        "MIDDLE": Pango.EllipsizeMode.MIDDLE,
        "END": Pango.EllipsizeMode.END,
    }[text]

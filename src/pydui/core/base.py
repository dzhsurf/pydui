from enum import Enum

from pydui.core.import_gtk import *


class PyDuiAlign(Enum):
    """Align type"""

    CENTER = (0,)
    START = 1
    END = 2


def Text2PyDuiAlign(text: str) -> PyDuiAlign:
    return {
        "CENTER": PyDuiAlign.CENTER,
        "START": PyDuiAlign.START,
        "END": PyDuiAlign.END,
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

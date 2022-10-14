# -*- coding: utf-8 -*-
from dataclasses import dataclass
from enum import Enum
from tkinter import UNDERLINE


class NCAreaType(Enum):
    UNDEFINED = 0
    CAPTION = 1
    LEFT = 2
    TOP = 3
    RIGHT = 4
    BOTTOM = 5
    LEFT_TOP = 6
    RIGHT_TOP = 7
    LEFT_BOTTOM = 8
    RIGHT_BOTTOM = 9
    CLIENT = 10


class ButtonType(Enum):
    UNDEFINED = 0
    BUTTON_LEFT = 1
    BUTTON_RIGHT = 2


class ButtonEventType(Enum):
    UNDEFINED = 0
    PRESS = 1
    DBPRESS = 2
    TRIPRESS = 3
    RELEASE = 4


@dataclass(frozen=True)
class EventObject:
    pass


@dataclass(frozen=True)
class ButtonEvent(EventObject):
    x: int
    y: int
    button: ButtonType
    event: ButtonEventType
    time: int


class ScrollDirection(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    SMOOTH = 4


# class ModifierType(Enum):
#     SHIFT_MASK = 1
#     CONTROL_MASK = 4


@dataclass(frozen=True)
class ScrollEvent(EventObject):
    x: int
    y: int
    delta_x: float
    delta_y: float
    direction: ScrollDirection
    # state: ModifierType
    time: int

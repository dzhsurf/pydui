# -*- coding: utf-8 -*-
from dataclasses import dataclass
from enum import Enum


class PyDuiButtonType(Enum):
    UNDEFINED = 0
    BUTTON_LEFT = 1
    BUTTON_RIGHT = 2


class PyDuiButtonEventType(Enum):
    UNDEFINED = 0
    PRESS = 1
    DBPRESS = 2
    TRIPRESS = 3
    RELEASE = 4


@dataclass(frozen=True)
class PyDuiWindowEvent:
    pass


@dataclass(frozen=True)
class PyDuiWindowButtonEvent(PyDuiWindowEvent):
    x: int
    y: int
    button_type: PyDuiButtonType
    event_type: PyDuiButtonEventType
    time: int
